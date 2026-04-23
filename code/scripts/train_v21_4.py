"""
QKVM v21.4: M retrained WITH beliefs+d* in prompt.

The critical fix: M was trained on bare prompts (v19-v21.2) and learned
to substitute for belief content. Now M trains in the environment it
deploys in: beliefs in prompt + d* active.

Baseline for content loss = beliefs + d* (no M).
M must improve NTP ABOVE what beliefs+d* already provide.
M can only earn gradient by making the model attend to beliefs
more effectively — not by overriding them.

Warm-start: GNN + phi from v21.2 (content encoding useful).
Fresh-init: M-state read head projections (old mapping overrides beliefs).

Usage:
    PYTHONUNBUFFERED=1 nohup python scripts/train_v21_4.py \
        --epochs 100 --run_name v21_4 \
        > logs/v21_4_train.log 2>&1 &
"""

import argparse
import json
import math
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

DSTAR_GEN_SCALE = 0.10


def build_belief_prompt_for_topic(topic, side, credences=None):
    """Build hierarchical belief prompt for a topic."""
    from hexis.belief_prompt import (
        build_hierarchical_belief_xml, build_full_prompt, load_classifications,
    )
    classifications = load_classifications()
    xml = build_hierarchical_belief_xml(topic, side, credences, classifications)
    return build_full_prompt(topic["probe"], xml)


def statement_ntp(model, tokenizer, prompt, statement, device):
    full_text = prompt + statement
    full_ids = tokenizer(full_text, return_tensors="pt",
                         max_length=1024, truncation=True).input_ids.to(device)
    prompt_ids = tokenizer(prompt, return_tensors="pt",
                           max_length=1024, truncation=True).input_ids
    target_start = prompt_ids.shape[1]
    target_ids = full_ids.clone()
    target_ids[0, :target_start] = -100
    logits = model(input_ids=full_ids).logits
    shift_logits = logits[:, :-1, :].contiguous()
    shift_labels = target_ids[:, 1:].contiguous()
    return F.cross_entropy(
        shift_logits.view(-1, shift_logits.size(-1)),
        shift_labels.view(-1), ignore_index=-100)


def train(args):
    from transformers import AutoModelForCausalLM, AutoTokenizer
    from hexis.model_hybrid import get_text_config
    from hexis.direction_injector import (
        DirectionInjector, install_direction_hooks, remove_direction_hooks,
    )
    from hexis.belief_tree_memory import BeliefTreeMemory, build_topic_tree, get_pro_con_node_ids
    from hexis.phi_node_writer import PhiNodeWriter
    from hexis.conviction_reader import ConvictionReader
    from hexis.mstate_read_head import MStateReadHead
    from hexis.jeffrey_update import (
        jeffrey_update_node, propagate_credences,
        initialize_credences_from_zero_points,
        credence_to_conviction,
    )

    from hexis.data_200_topics import TRAIN_200, HELD_OUT_200
    from scripts.train_amplifier_v6_ppl import (
        TRAIN_TOPICS as TRAIN_ORIGINAL,
        HELD_OUT_TOPICS as HELD_OUT_ORIGINAL,
    )

    print("=" * 60)
    print("QKVM v21.4: M retrained WITH beliefs+d* in prompt")
    print("=" * 60)
    print(f"  d* gen scale: {DSTAR_GEN_SCALE}")
    print(f"  M-state read head: FRESH INIT")
    print(f"  GNN + phi: warm-start from v21.2")

    # === Load model ===
    tokenizer = AutoTokenizer.from_pretrained(args.model, trust_remote_code=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    base_model = AutoModelForCausalLM.from_pretrained(
        args.model, dtype=torch.bfloat16, device_map="auto", trust_remote_code=True)
    base_model.eval()
    for p in base_model.parameters():
        p.requires_grad = False

    model_config = get_text_config(base_model.config)
    d_model = model_config.hidden_size
    n_layers = model_config.num_hidden_layers
    device = next(base_model.parameters()).device
    stride = 3
    patched_layers = list(range(0, n_layers, stride))

    # d* at low generation scale
    d_star = torch.load("checkpoints/d_star.pt", map_location="cpu", weights_only=True)
    direction_injector = DirectionInjector(d_star, base_scale=DSTAR_GEN_SCALE).to(device)
    direction_injector.eval()

    topic_zero_points = torch.load("checkpoints/topic_zero_points.pt",
                                    map_location="cpu", weights_only=True)

    # === Topics ===
    all_topics = {}
    for t in list(TRAIN_ORIGINAL) + list(TRAIN_200):
        all_topics[t["id"]] = t
    held_out = list(HELD_OUT_ORIGINAL) + list(HELD_OUT_200)
    train_ids = list(all_topics.keys())
    print(f"  Train: {len(train_ids)}, Held-out: {len(held_out)}")

    # === Modules ===
    phi_writer = PhiNodeWriter(d_model=d_model, d_node=args.d_node).to(device)
    conviction_reader = ConvictionReader(d_node=args.d_node).to(device)

    # FRESH M-state read head (old one overrides beliefs)
    m_read_head = MStateReadHead(
        d_node=args.d_node, d_model=d_model, rank=args.rank,
        n_layers=len(patched_layers),
    ).to(device)

    btm_template = BeliefTreeMemory(d_node=args.d_node, d_edge=64, n_message_passes=2)
    btm_template.init_from_tree(build_topic_tree({
        "probe": "init", "experiences_A": ["a"], "experiences_B": ["b"],
    }), d_model=d_model, device=device)
    btm_template = btm_template.to(device)

    # Warm-start GNN + phi + conviction from v21.2
    if args.checkpoint:
        ckpt = torch.load(args.checkpoint, map_location="cpu", weights_only=False)
        phi_writer.load_state_dict(ckpt["phi_writer"])
        conviction_reader.load_state_dict(ckpt["conviction_reader"])
        btm_template.load_state_dict(ckpt["btm_template"])
        # DO NOT load m_read_head — fresh init
        print(f"  Warm-started GNN+phi+conviction from epoch {ckpt['epoch']}")
        print(f"  M-state read head: FRESH (old mapping overrides beliefs)")

    trainable_params = (
        sum(p.numel() for p in phi_writer.parameters()) +
        sum(p.numel() for p in conviction_reader.parameters()) +
        sum(p.numel() for p in m_read_head.parameters()) +
        sum(p.numel() for p in btm_template.parameters())
    )
    print(f"  Trainable: {trainable_params/1e6:.1f}M")

    optimizer = torch.optim.AdamW([
        {"params": phi_writer.parameters(), "lr": args.lr},
        {"params": conviction_reader.parameters(), "lr": args.lr},
        {"params": m_read_head.parameters(), "lr": args.lr},
        {"params": btm_template.parameters(), "lr": args.lr},
    ], weight_decay=0.01)

    os.makedirs("checkpoints/v21_4", exist_ok=True)

    # === Helpers ===
    def build_btm(topic):
        tree = build_topic_tree(topic)
        pro_ids, con_ids = get_pro_con_node_ids(tree, n_pro=len(topic["experiences_A"]))
        initialize_credences_from_zero_points(tree, topic["id"], topic_zero_points)

        btm = BeliefTreeMemory(d_node=args.d_node, d_edge=64, n_message_passes=2)
        btm.edge_embedding = btm_template.edge_embedding
        btm.message_fn = btm_template.message_fn
        btm.update_fn = btm_template.update_fn
        btm.node_init_proj = btm_template.node_init_proj

        for nid, node in tree.nodes.items():
            enc = tokenizer(node.statement[:200], return_tensors="pt",
                           truncation=True, max_length=128)
            with torch.no_grad():
                out = base_model(input_ids=enc["input_ids"].to(device),
                                 output_hidden_states=True)
            h_pooled = out.hidden_states[-1].mean(dim=1).float()
            btm._embeddings[nid] = btm.node_init_proj(h_pooled).squeeze(0)

        btm.propagate(tree)
        return btm, tree, pro_ids, con_ids

    def write_and_update(btm, tree, exp_texts, ev_ids, direction):
        for exp_text, nid in zip(exp_texts, ev_ids):
            enc = tokenizer(exp_text[:200], return_tensors="pt",
                           truncation=True, max_length=128)
            with torch.no_grad():
                out = base_model(input_ids=enc["input_ids"].to(device),
                                 output_hidden_states=True)
            h_exp = out.hidden_states[-1].mean(dim=1).float().squeeze(0)
            delta = phi_writer(h_exp, btm.get_embedding(nid))
            new_embed = 0.95 * btm.get_embedding(nid) + 0.1 * delta
            btm.set_embedding(nid, new_embed)

            gate_val = torch.sigmoid(phi_writer.gate_proj(
                torch.cat([phi_writer.experience_encoder(h_exp.unsqueeze(0)).squeeze(0),
                           btm.get_embedding(nid)])
            )).item()
            jeffrey_update_node(tree, nid, gate_val, direction)

        btm.propagate(tree)
        propagate_credences(tree)

    def install_m_hooks(m_layers):
        handles = []
        layers = base_model.model.layers
        for l_idx, layer_num in enumerate(patched_layers):
            M_A, M_B, mod_scale = m_layers[l_idx]
            def make_q_hook(ma, mb, s):
                def hook(module, args, kwargs=None):
                    x = args[0] if args else kwargs.get("hidden_states")
                    if x is None:
                        return args, kwargs
                    mod = torch.matmul(x, ma.to(x.device, x.dtype))
                    x_mod = x + s * torch.matmul(mod, mb.to(x.device, x.dtype).T)
                    if args:
                        return (x_mod,) + args[1:], kwargs
                    kwargs = dict(kwargs) if kwargs else {}
                    kwargs["hidden_states"] = x_mod
                    return args, kwargs
                return hook
            h = layers[layer_num].register_forward_pre_hook(
                make_q_hook(M_A, M_B, mod_scale), with_kwargs=True)
            handles.append(h)
        return handles

    # === Training loop ===
    print(f"\n{'='*60}")
    print("TRAINING (M learns to amplify beliefs, not override them)")
    print(f"{'='*60}\n")

    history = []

    for epoch in range(args.epochs):
        epoch_start = time.time()
        batch_ids = random.sample(train_ids, k=min(args.topics_per_epoch, len(train_ids)))

        epoch_loss = 0.0
        m_wins, total = 0, 0

        for topic_id in batch_ids:
            optimizer.zero_grad()
            topic = all_topics[topic_id]

            btm, tree, pro_ids, con_ids = build_btm(topic)
            saved = btm.clone_embeddings()

            for side, exp_list, ev_ids, persp_ids, match_st, direction in [
                ("pro", topic["experiences_A"], pro_ids[1:], pro_ids,
                 topic["stance_A"], +1.0),
                ("con", topic["experiences_B"], con_ids[1:], con_ids,
                 topic["stance_B"], -1.0),
            ]:
                btm.restore_embeddings(saved)
                initialize_credences_from_zero_points(tree, topic_id, topic_zero_points)

                write_and_update(btm, tree, exp_list, ev_ids, direction)

                posterior_credence = tree.nodes[tree.root_id].credence
                formal_conviction = credence_to_conviction(posterior_credence)

                for pid in pro_ids[1:]:
                    tree.nodes[pid].credence = 0.8 if side == "pro" else 0.3
                for cid in con_ids[1:]:
                    tree.nodes[cid].credence = 0.8 if side == "con" else 0.3

                embed_s, cred_s = btm.get_perspective_embeddings(persp_ids, tree)
                m_layers = m_read_head(embed_s, cred_s)

                # Build belief nodes for prompt
                # Build hierarchical belief prompt
                node_credences = {nid: tree.nodes[nid].credence for nid in tree.nodes}
                prompt = build_belief_prompt_for_topic(topic, side, node_credences)

                # d* conviction for this side
                dstar_conv = torch.tensor(
                    abs(formal_conviction) if side == "pro" else -abs(formal_conviction),
                    device=device, dtype=torch.float32
                )

                # === BASELINE: beliefs + d* (no M) ===
                d_h = install_direction_hooks(base_model, direction_injector,
                                              dstar_conv, patched_layers)
                with torch.no_grad():
                    ntp_baseline = statement_ntp(base_model, tokenizer,
                                                 prompt, match_st, device)
                remove_direction_hooks(d_h)

                # === TEST: beliefs + d* + M ===
                d_h = install_direction_hooks(base_model, direction_injector,
                                              dstar_conv, patched_layers)
                m_h = install_m_hooks(m_layers)
                ntp_full = statement_ntp(base_model, tokenizer,
                                        prompt, match_st, device)
                for h in m_h: h.remove()
                remove_direction_hooks(d_h)

                # M must beat beliefs+d* baseline
                L = F.relu(ntp_full - ntp_baseline.detach() + args.margin)
                L.backward()

                epoch_loss += L.item()
                if ntp_full.item() < ntp_baseline.item():
                    m_wins += 1
                total += 1

            torch.nn.utils.clip_grad_norm_(
                list(phi_writer.parameters()) + list(conviction_reader.parameters()) +
                list(m_read_head.parameters()) + list(btm_template.parameters()),
                args.grad_clip)
            optimizer.step()

        elapsed = time.time() - epoch_start
        row = {
            "epoch": epoch, "time": elapsed,
            "loss": epoch_loss / max(total, 1),
            "m_wins": f"{m_wins}/{total}",
        }
        history.append(row)

        if epoch % args.print_every == 0:
            print(f"E{epoch:03d} [{elapsed:.1f}s] "
                  f"loss={row['loss']:.4f} m_wins={row['m_wins']}")

        if (epoch + 1) % args.checkpoint_every == 0 or epoch == args.epochs - 1:
            ckpt_path = f"checkpoints/v21_4/v21_4_epoch{epoch}_{args.run_name}.pt"
            torch.save({
                "epoch": epoch,
                "phi_writer": phi_writer.state_dict(),
                "conviction_reader": conviction_reader.state_dict(),
                "m_read_head": m_read_head.state_dict(),
                "btm_template": btm_template.state_dict(),
                "config": {
                    "d_node": args.d_node, "rank": args.rank,
                    "dstar_gen_scale": DSTAR_GEN_SCALE,
                    "patched_layers": patched_layers,
                    "d_model": d_model,
                },
                "history": history,
            }, ckpt_path)
            print(f"  Saved: {ckpt_path}")

        # Held-out eval
        if (epoch + 1) % args.eval_every == 0:
            print(f"\n  --- Held-out eval (epoch {epoch}) ---")
            eval_topics = random.sample(held_out, k=min(20, len(held_out)))

            ho_m_wins, ho_total = 0, 0
            ntp_base_sum, ntp_full_sum = 0.0, 0.0

            for topic in eval_topics:
                btm_e, tree_e, pro_e, con_e = build_btm(topic)
                write_and_update(btm_e, tree_e, topic["experiences_A"], pro_e[1:], +1.0)

                for pid in pro_e[1:]:
                    tree_e.nodes[pid].credence = 0.8
                for cid in con_e[1:]:
                    tree_e.nodes[cid].credence = 0.3

                embed_s, cred_s = btm_e.get_perspective_embeddings(pro_e, tree_e)
                with torch.no_grad():
                    m_layers = m_read_head(embed_s, cred_s)

                node_credences_e = {nid: tree_e.nodes[nid].credence for nid in tree_e.nodes}
                prompt = build_belief_prompt_for_topic(topic, "pro", node_credences_e)

                post_cr = tree_e.nodes[tree_e.root_id].credence
                dstar_conv = torch.tensor(
                    credence_to_conviction(post_cr),
                    device=device, dtype=torch.float32
                )

                with torch.no_grad():
                    # Baseline: beliefs + d*
                    d_h = install_direction_hooks(base_model, direction_injector,
                                                  dstar_conv, patched_layers)
                    nb = statement_ntp(base_model, tokenizer, prompt,
                                      topic["stance_A"], device).item()
                    remove_direction_hooks(d_h)

                    # Full: beliefs + d* + M
                    d_h = install_direction_hooks(base_model, direction_injector,
                                                  dstar_conv, patched_layers)
                    m_h = install_m_hooks(m_layers)
                    nf = statement_ntp(base_model, tokenizer, prompt,
                                      topic["stance_A"], device).item()
                    for h in m_h: h.remove()
                    remove_direction_hooks(d_h)

                if nf < nb:
                    ho_m_wins += 1
                ho_total += 1
                ntp_base_sum += nb
                ntp_full_sum += nf

            print(f"  M wins: {ho_m_wins}/{ho_total} ({100*ho_m_wins/ho_total:.0f}%)")
            print(f"  NTP base={ntp_base_sum/ho_total:.4f} full={ntp_full_sum/ho_total:.4f} "
                  f"Δ={ntp_full_sum/ho_total - ntp_base_sum/ho_total:+.4f}")

    print(f"\n{'='*60}")
    print(f"TRAINING COMPLETE — v21.4")
    print(f"{'='*60}")
    print(f"  Final: {history[-1]}")

    with open(f"logs/v21_4_{args.run_name}_history.json", "w") as f:
        json.dump(history, f, indent=2)


if __name__ == "__main__":
    from hexis.adapters.cli import add_preset_args, resolve_preset_args

    p = argparse.ArgumentParser()
    add_preset_args(p, agentic=False, add_training_args=True, training_phase="a")
    p.add_argument("--checkpoint", default=None,
                   help="Default: <preset.checkpoint_base>/v21_2/BEST.pt")
    p.add_argument("--epochs", type=int, default=100)
    p.add_argument("--d_node", type=int, default=128)
    p.add_argument("--topics_per_epoch", type=int, default=16)
    p.add_argument("--grad_clip", type=float, default=1.0)
    p.add_argument("--print_every", type=int, default=1)
    p.add_argument("--checkpoint_every", type=int, default=25)
    p.add_argument("--eval_every", type=int, default=10)
    p.add_argument("--run_name", default="v21_4")
    args = p.parse_args()
    preset = resolve_preset_args(args)
    if args.checkpoint is None:
        args.checkpoint = f"{preset.checkpoint_base}/v21_2/BEST.pt"
    # Phase A step 2d recipe: margin=0.1 (smaller than earlier phases).
    # Preset's margin_base is the Phase A.1 default; override for 2d.
    if args.margin == preset.margin_base:  # user didn't override
        args.margin = 0.1

    train(args)
