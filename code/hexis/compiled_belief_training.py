"""
HEXIS v23: Compiled Belief Training.

Trains V-modulation projections to carry belief content through
the rank bottleneck. The model sees [system + question] only.
Compiled Q+V modulation from beliefs provides the content signal.

Fixed belief context window (BELIEF_WINDOW tokens) with padding.
Beliefs are processed in a separate forward pass, hidden states
pooled per layer, projected to V-modulation matrices.

Training loss: NTP(stance | system + question, compiled Q+V)
  must beat NTP(stance | system + question, no modulation)

The V-modulation must carry enough belief content for the model
to generate belief-grounded text without seeing the beliefs.

Usage:
    PYTHONUNBUFFERED=1 python qkvm/compiled_belief_training.py \\
        --epochs 100 --run_name v23_compiled
"""

import argparse
import json
import os
import random
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import torch
import torch.nn as nn
import torch.nn.functional as F

random.seed(42)
torch.manual_seed(42)

# Fixed belief context window
BELIEF_WINDOW = 512  # max tokens for beliefs (covers P95 + expansion room)
BELIEF_PAD_TOKEN_ID = 0  # will be set from tokenizer


def pad_or_truncate_beliefs(belief_ids, max_len=BELIEF_WINDOW, pad_id=0):
    """Pad beliefs to fixed length or truncate if too long.

    Returns:
        padded_ids: (1, max_len) tensor
        belief_mask: (1, max_len) boolean mask (True for real tokens)
    """
    seq_len = belief_ids.shape[1]

    if seq_len >= max_len:
        # Truncate from the end (keep most important beliefs at start)
        padded = belief_ids[:, :max_len]
        mask = torch.ones(1, max_len, dtype=torch.bool, device=belief_ids.device)
    else:
        # Pad with pad_id
        padding = torch.full((1, max_len - seq_len), pad_id,
                              dtype=belief_ids.dtype, device=belief_ids.device)
        padded = torch.cat([belief_ids, padding], dim=1)
        mask = torch.zeros(1, max_len, dtype=torch.bool, device=belief_ids.device)
        mask[0, :seq_len] = True

    return padded, mask


class VModulationProjector(nn.Module):
    """Projects pooled hidden states to V-modulation matrices.

    Per-layer projections: h_pooled → (E_A, E_B) of shape (d_model, rank).
    Uses conviction-weighted pooling over belief positions.
    """

    def __init__(self, d_model, rank, n_layers, max_norm=1.5):
        super().__init__()
        self.d_model = d_model
        self.rank = rank
        self.max_norm = max_norm

        # Bottleneck: d_model → 256 → d_model*rank
        # Much smaller than d_model → d_model → d_model*rank
        bottleneck = 256
        self.v_proj_A = nn.ModuleList([
            nn.Sequential(
                nn.Linear(d_model, bottleneck),
                nn.SiLU(),
                nn.Linear(bottleneck, d_model * rank),
            ) for _ in range(n_layers)
        ])
        self.v_proj_B = nn.ModuleList([
            nn.Sequential(
                nn.Linear(d_model, bottleneck),
                nn.SiLU(),
                nn.Linear(bottleneck, d_model * rank),
            ) for _ in range(n_layers)
        ])
        self.v_scales = nn.ParameterList([
            nn.Parameter(torch.tensor(1.0)) for _ in range(n_layers)
        ])

        # Init small
        for proj in list(self.v_proj_A) + list(self.v_proj_B):
            for p in proj.parameters():
                if p.dim() >= 2:
                    nn.init.normal_(p, std=0.02)

    def _norm_clamp(self, t):
        n = t.norm().clamp(min=1e-8)
        if n > self.max_norm:
            t = t * (self.max_norm / n)
        return t

    def forward(self, hidden_states_per_layer, belief_mask):
        """
        Args:
            hidden_states_per_layer: dict {layer_idx: (1, BELIEF_WINDOW, d_model)}
            belief_mask: (1, BELIEF_WINDOW) boolean

        Returns:
            list of (E_A, E_B, v_scale) per layer
        """
        outputs = []

        # Masked mean pooling
        mask_expanded = belief_mask.unsqueeze(-1).float()  # (1, BELIEF_WINDOW, 1)
        n_real = mask_expanded.sum(dim=1, keepdim=True).clamp(min=1)  # (1, 1, 1)

        for l in range(len(self.v_proj_A)):
            h = list(hidden_states_per_layer.values())[l]  # (1, BELIEF_WINDOW, d_model)
            h_pooled = (h.float() * mask_expanded).sum(dim=1) / n_real.squeeze(-1)  # (1, d_model)
            h_pooled = h_pooled.squeeze(0)  # (d_model,)

            E_A = torch.tanh(self.v_proj_A[l](h_pooled)).reshape(self.d_model, self.rank)
            E_B = torch.tanh(self.v_proj_B[l](h_pooled)).reshape(self.d_model, self.rank)
            E_A = self._norm_clamp(E_A)
            E_B = self._norm_clamp(E_B)

            outputs.append((E_A, E_B, self.v_scales[l]))

        return outputs


def build_conviction_xml(topic, side, max_tokens=None, tokenizer=None):
    """Build belief XML, optionally checking token budget."""
    side_key = "A" if side == "pro" else "B"
    stance = topic.get(f"stance_{side_key}", topic["probe"])
    reasonings = topic.get(f"reasoning_{side_key}", [])
    experiences = topic.get(f"experiences_{side_key}", [])

    xml = '<beliefs>\n  <claim conviction="strong">\n'
    xml += f"    {stance}\n"
    for i, r in enumerate(reasonings[:3]):
        conv = "strong" if i == 0 else "moderate"
        xml += f'    <argument conviction="{conv}" supports="claim">\n      {r}\n'
        if i < len(experiences):
            xml += f'      <evidence conviction="{conv}" supports="argument">\n        {experiences[i]}\n      </evidence>\n'
        xml += "    </argument>\n"
    xml += "  </claim>\n</beliefs>"

    if max_tokens and tokenizer:
        toks = tokenizer.encode(xml)
        if len(toks) > max_tokens:
            # Truncate by removing evidence first, then arguments
            xml_short = '<beliefs>\n  <claim conviction="strong">\n'
            xml_short += f"    {stance}\n"
            xml_short += "  </claim>\n</beliefs>"
            return xml_short

    return xml


def train(args):
    from transformers import AutoModelForCausalLM, AutoTokenizer
    from hexis.model_hybrid import get_text_config
    from hexis.belief_tree_memory import BeliefTreeMemory, build_topic_tree, get_pro_con_node_ids
    from hexis.phi_node_writer import PhiNodeWriter
    from hexis.mstate_read_head import MStateReadHead
    from hexis.jeffrey_update import initialize_credences_from_zero_points
    from hexis.data_200_topics import TRAIN_200, HELD_OUT_200
    from scripts.train_amplifier_v6_ppl import TRAIN_TOPICS, HELD_OUT_TOPICS

    print("=" * 60)
    print("v23 COMPILED BELIEF TRAINING")
    print(f"  Belief window: {BELIEF_WINDOW} tokens")
    print(f"  Margin: {args.margin}")
    print("=" * 60)

    tokenizer = AutoTokenizer.from_pretrained(args.model, trust_remote_code=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    global BELIEF_PAD_TOKEN_ID
    BELIEF_PAD_TOKEN_ID = tokenizer.pad_token_id

    base_model = AutoModelForCausalLM.from_pretrained(
        args.model, dtype=torch.bfloat16, device_map="auto", trust_remote_code=True)
    base_model.eval()
    for p in base_model.parameters():
        p.requires_grad = False

    config = get_text_config(base_model.config)
    d_model = config.hidden_size
    n_layers = config.num_hidden_layers
    device = next(base_model.parameters()).device
    patched_layers = list(range(0, n_layers, 3))

    # Load v21.4 for Q-modulation (frozen)
    ck = torch.load(args.checkpoint, map_location="cpu", weights_only=False)
    cfg = ck["config"]
    d_node = cfg["d_node"]

    pw = PhiNodeWriter(d_model=d_model, d_node=d_node).to(device)
    pw.load_state_dict(ck["phi_writer"]); pw.eval()
    for p in pw.parameters(): p.requires_grad = False

    mr = MStateReadHead(d_node=d_node, d_model=d_model, rank=cfg["rank"],
                         n_layers=len(patched_layers)).to(device)
    mr.load_state_dict(ck["m_read_head"]); mr.eval()
    for p in mr.parameters(): p.requires_grad = False

    btm_t = BeliefTreeMemory(d_node=d_node, d_edge=64, n_message_passes=2)
    btm_t.init_from_tree(build_topic_tree({"probe": "init",
        "experiences_A": ["a"], "experiences_B": ["b"]}), d_model=d_model, device=device)
    btm_t = btm_t.to(device)
    btm_t.load_state_dict(ck["btm_template"]); btm_t.eval()
    for p in btm_t.parameters(): p.requires_grad = False

    print(f"  Loaded v21.4 (frozen Q-mod)")
    print(f"  d_model={d_model}, patched={len(patched_layers)}, rank={cfg['rank']}")

    # NEW: V-modulation projector (trainable)
    v_proj = VModulationProjector(d_model=d_model, rank=cfg["rank"],
                                   n_layers=len(patched_layers)).to(device)

    # Warm-start from previous checkpoint if available
    if args.v_checkpoint and os.path.exists(args.v_checkpoint):
        v_ck = torch.load(args.v_checkpoint, map_location="cpu", weights_only=False)
        v_proj.load_state_dict(v_ck["v_proj"])
        print(f"  Warm-started V-mod from {args.v_checkpoint} (epoch {v_ck.get('epoch', '?')})")

    trainable = sum(p.numel() for p in v_proj.parameters())
    print(f"  V-modulation projector: {trainable/1e6:.1f}M trainable params")

    optimizer = torch.optim.AdamW(v_proj.parameters(), lr=args.lr, weight_decay=0.01)

    # Topics
    all_topics = {}
    for t in list(TRAIN_TOPICS) + list(TRAIN_200):
        all_topics[t["id"]] = t
    held_out = list(HELD_OUT_TOPICS) + list(HELD_OUT_200)
    train_ids = list(all_topics.keys())
    print(f"  Train: {len(train_ids)}, Held-out: {len(held_out)}")

    os.makedirs(f"checkpoints/{args.run_name}", exist_ok=True)

    # === Helpers ===
    def encode_text(text):
        enc = tokenizer(text[:300], return_tensors="pt", truncation=True, max_length=128)
        with torch.no_grad():
            out = base_model(input_ids=enc["input_ids"].to(device), output_hidden_states=True)
        return out.hidden_states[-1].mean(1).float().squeeze(0)

    def get_q_mod(topic, side):
        """Get Q-modulation from trained M (frozen)."""
        tree = build_topic_tree(topic)
        pro_ids, con_ids = get_pro_con_node_ids(tree, n_pro=len(topic["experiences_A"]))
        btm = BeliefTreeMemory(d_node=d_node, d_edge=64, n_message_passes=2)
        btm.edge_embedding = btm_t.edge_embedding; btm.message_fn = btm_t.message_fn
        btm.update_fn = btm_t.update_fn; btm.node_init_proj = btm_t.node_init_proj
        for nid, node in tree.nodes.items():
            h = encode_text(node.statement)
            btm._embeddings[nid] = btm.node_init_proj(h.unsqueeze(0)).squeeze(0).detach()
        btm.propagate(tree)
        exp_list = topic["experiences_A"] if side == "pro" else topic["experiences_B"]
        ev_ids = (pro_ids if side == "pro" else con_ids)[1:]
        persp_ids = pro_ids if side == "pro" else con_ids
        for exp, nid in zip(exp_list, ev_ids):
            h = encode_text(exp)
            with torch.no_grad(): delta = pw(h, btm.get_embedding(nid))
            btm.set_embedding(nid, (0.95 * btm.get_embedding(nid) + 0.1 * delta).detach())
        btm.propagate(tree)
        for pid in persp_ids[1:]: tree.nodes[pid].credence = 0.80
        embed_s, cred_s = btm.get_perspective_embeddings(persp_ids, tree)
        with torch.no_grad(): m_layers = mr(embed_s, cred_s)
        return m_layers

    def compile_beliefs(belief_xml):
        """Forward beliefs through base model, extract hidden states at patched layers."""
        enc = tokenizer(belief_xml, return_tensors="pt", truncation=True,
                       max_length=BELIEF_WINDOW).to(device)
        belief_ids = enc["input_ids"]
        padded_ids, belief_mask = pad_or_truncate_beliefs(belief_ids,
                                                           max_len=BELIEF_WINDOW,
                                                           pad_id=BELIEF_PAD_TOKEN_ID)

        with torch.no_grad():
            outputs = base_model(input_ids=padded_ids, output_hidden_states=True)

        hidden_per_layer = {}
        for l_idx, layer_num in enumerate(patched_layers):
            hidden_per_layer[l_idx] = outputs.hidden_states[layer_num + 1].float()

        return hidden_per_layer, belief_mask

    def install_qv_hooks(q_layers, v_layers):
        """Install combined Q (from trained M) + V (from compiler) hooks."""
        handles = []
        for l_idx, layer_num in enumerate(patched_layers):
            M_A, M_B, q_scale = q_layers[l_idx]
            E_A, E_B, v_scale = v_layers[l_idx]

            def make_hook(ma, mb, qs, ea, eb, vs):
                def hook(module, args, kwargs=None):
                    x = args[0] if args else kwargs.get("hidden_states")
                    if x is None: return args, kwargs
                    dev, dt = x.device, x.dtype

                    # Q-modulation (frozen)
                    q_mod = torch.matmul(torch.matmul(x, ma.to(dev, dt)), mb.to(dev, dt).T)

                    # V-modulation (trainable)
                    v_mod = torch.matmul(torch.matmul(x, ea.to(dev, dt)), eb.to(dev, dt).T)

                    x_mod = x + qs * q_mod + vs * v_mod

                    if args: return (x_mod,) + args[1:], kwargs
                    kw = dict(kwargs) if kwargs else {}; kw["hidden_states"] = x_mod
                    return args, kw
                return hook

            handles.append(base_model.model.layers[layer_num].register_forward_pre_hook(
                make_hook(M_A, M_B, q_scale, E_A, E_B, v_scale), with_kwargs=True))
        return handles

    def statement_ntp(prompt, statement):
        full = prompt + statement
        ids = tokenizer(full, return_tensors="pt", max_length=1024, truncation=True).input_ids.to(device)
        p_len = tokenizer(prompt, return_tensors="pt", max_length=1024, truncation=True).input_ids.shape[1]
        tgt = ids.clone(); tgt[0, :p_len] = -100
        logits = base_model(input_ids=ids).logits
        sl = logits[:, :-1, :].contiguous()
        tl = tgt[:, 1:].contiguous()
        return F.cross_entropy(sl.view(-1, sl.size(-1)), tl.view(-1), ignore_index=-100)

    # === Training loop ===
    sys_msg = "You hold strong convictions on this topic based on your experience. Argue your position directly."
    print(f"\n{'='*60}")
    print("TRAINING V-MODULATION")
    print(f"{'='*60}\n")

    history = []

    for epoch in range(args.epochs):
        t0 = time.time()
        batch = random.sample(train_ids, k=min(args.topics_per_epoch, len(train_ids)))

        epoch_loss = 0.0
        wins, total = 0, 0

        for tid in batch:
            optimizer.zero_grad()
            topic = all_topics[tid]

            for side in ["pro", "con"]:
                stance = topic.get(f"stance_{'A' if side == 'pro' else 'B'}", topic["probe"])

                # 1. Get frozen Q-modulation from existing M
                q_layers = get_q_mod(topic, side)

                # 2. Compile beliefs → hidden states → V-modulation (trainable)
                xml = build_conviction_xml(topic, side, max_tokens=BELIEF_WINDOW, tokenizer=tokenizer)
                hidden_per_layer, belief_mask = compile_beliefs(xml)
                v_layers = v_proj(hidden_per_layer, belief_mask)

                # 3. Prompts
                prompt_no_beliefs = (
                    f"<|im_start|>system\n{sys_msg}<|im_end|>\n"
                    f"<|im_start|>user\n{topic['probe']}<|im_end|>\n"
                    f"<|im_start|>assistant\n"
                )
                prompt_with_beliefs = (
                    f"{xml}\n\n<|im_start|>system\n{sys_msg}<|im_end|>\n"
                    f"<|im_start|>user\n{topic['probe']}<|im_end|>\n"
                    f"<|im_start|>assistant\n"
                )

                # 4. Baseline: beliefs in prompt (no M)
                # Compiled Q+V must beat having beliefs explicitly in context
                with torch.no_grad():
                    ntp_beliefs = statement_ntp(prompt_with_beliefs, stance)

                # 5. Test: compiled Q+V modulation (no beliefs in prompt)
                hooks = install_qv_hooks(q_layers, v_layers)
                ntp_compiled = statement_ntp(prompt_no_beliefs, stance)
                for h in hooks: h.remove()

                # 6. Loss: compiled (no beliefs) must beat beliefs-in-prompt
                L = F.relu(ntp_compiled - ntp_beliefs.detach() + args.margin)
                L.backward()

                epoch_loss += L.item()
                if ntp_compiled.item() < ntp_beliefs.item():
                    wins += 1
                total += 1

            torch.nn.utils.clip_grad_norm_(v_proj.parameters(), 1.0)
            optimizer.step()

        elapsed = time.time() - t0
        row = {"epoch": epoch, "time": elapsed,
               "loss": epoch_loss / max(total, 1),
               "wins": f"{wins}/{total}"}
        history.append(row)

        if epoch % args.print_every == 0:
            print(f"E{epoch:03d} [{elapsed:.1f}s] loss={row['loss']:.4f} wins={row['wins']}")
            sys.stdout.flush()

        if (epoch + 1) % args.checkpoint_every == 0 or epoch == args.epochs - 1:
            path = f"checkpoints/{args.run_name}/{args.run_name}_epoch{epoch}.pt"
            torch.save({
                "epoch": epoch,
                "v_proj": v_proj.state_dict(),
                "config": {
                    "d_model": d_model, "rank": cfg["rank"],
                    "n_layers": len(patched_layers),
                    "patched_layers": patched_layers,
                    "belief_window": BELIEF_WINDOW,
                    "parent_checkpoint": args.checkpoint,
                },
                "history": history,
            }, path)
            print(f"  Saved: {path}")

        # Early stop
        if epoch >= 15 and all(h["loss"] < 0.001 for h in history[-10:]):
            print(f"  Early stop at epoch {epoch}")
            break

    print(f"\nDone. Final: {history[-1]}")


if __name__ == "__main__":
    from hexis.adapters.cli import add_preset_args, resolve_preset_args

    p = argparse.ArgumentParser()
    # Phase B = V-mod compiled training. Recipe lr=3e-4 is preset.lr_phase_b.
    add_preset_args(p, agentic=False, add_training_args=True, training_phase="b")
    p.add_argument("--checkpoint", default=None,
                   help="Default: <preset.checkpoint_base>/v21_4/BEST.pt")
    p.add_argument("--epochs", type=int, default=100)
    p.add_argument("--topics_per_epoch", type=int, default=12)
    p.add_argument("--print_every", type=int, default=1)
    p.add_argument("--checkpoint_every", type=int, default=25)
    p.add_argument("--v_checkpoint", default=None,
                   help="Warm-start V-mod from previous checkpoint")
    p.add_argument("--run_name", default="v23_compiled")
    args = p.parse_args()
    preset = resolve_preset_args(args)
    if args.checkpoint is None:
        args.checkpoint = f"{preset.checkpoint_base}/v21_4/BEST.pt"
    # Phase B recipe: margin=1.0 (was hardcoded 0.5 in this script; recipe
    # says 1.0 for v_scale=1.0 default). Preset.margin_base may differ —
    # leave Phase B at its recipe value unless user overrides.
    if args.margin == preset.margin_base:
        args.margin = 1.0
    train(args)
