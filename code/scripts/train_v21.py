"""
QKVM v21: Direction × Conviction Architecture

d* (fixed, extracted) provides WHICH WAY to lean.
Conviction (learned from GNN) provides HOW MUCH to lean.
M-state (learned) provides WHAT TO ATTEND TO.

Training signal: d* at learned conviction + M must beat d* at zero-point
(ambivalent baseline). This measures phi's contribution above what d* gives for free.

Usage:
    PYTHONUNBUFFERED=1 nohup python scripts/train_v21.py \
        --epochs 200 --run_name v21 \
        > logs/v21_train.log 2>&1 &
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

PROBE_TEMPLATE = (
    "You have strong opinions formed from years of direct experience. "
    "Share your honest view based on what you've personally witnessed.\n\n"
    "Question: {probe}\nAnswer: "
)


def statement_ntp(model, tokenizer, prompt, statement, device):
    full_text = prompt + statement
    full_ids = tokenizer(full_text, return_tensors="pt",
                         max_length=512, truncation=True).input_ids.to(device)
    prompt_ids = tokenizer(prompt, return_tensors="pt",
                           max_length=512, truncation=True).input_ids
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

    from hexis.data_200_topics import TRAIN_200, HELD_OUT_200
    from scripts.train_amplifier_v6_ppl import (
        TRAIN_TOPICS as TRAIN_ORIGINAL,
        HELD_OUT_TOPICS as HELD_OUT_ORIGINAL,
    )

    print("=" * 60)
    print("QKVM v21: Direction × Conviction")
    print("=" * 60)

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
    print(f"  d_model={d_model}, layers={n_layers}, patched={len(patched_layers)}")

    # === Load d* (fixed, never trained) ===
    d_star = torch.load("checkpoints/d_star.pt", map_location="cpu", weights_only=True)
    direction_injector = DirectionInjector(d_star, base_scale=args.base_scale).to(device)
    direction_injector.eval()

    # === Load zero points ===
    topic_zero_points = torch.load("checkpoints/topic_zero_points.pt",
                                    map_location="cpu", weights_only=True)
    print(f"  Zero points loaded for {len(topic_zero_points)} topics")

    # === Prepare topics ===
    all_topics = {}
    for t in list(TRAIN_ORIGINAL) + list(TRAIN_200):
        all_topics[t["id"]] = t
    held_out = list(HELD_OUT_ORIGINAL) + list(HELD_OUT_200)
    train_ids = list(all_topics.keys())
    print(f"  Train: {len(train_ids)}, Held-out: {len(held_out)}")

    # === Build trainable modules ===
    phi_writer = PhiNodeWriter(d_model=d_model, d_node=args.d_node).to(device)
    conviction_reader = ConvictionReader(d_node=args.d_node).to(device)
    m_read_head = MStateReadHead(
        d_node=args.d_node, d_model=d_model, rank=args.rank,
        n_layers=len(patched_layers),
    ).to(device)

    # Shared BTM template (GNN params)
    btm_template = BeliefTreeMemory(d_node=args.d_node, d_edge=64, n_message_passes=2)
    btm_template.init_from_tree(build_topic_tree({
        "probe": "init", "experiences_A": ["a"], "experiences_B": ["b"],
    }), d_model=d_model, device=device)
    btm_template = btm_template.to(device)

    trainable_params = (
        sum(p.numel() for p in phi_writer.parameters()) +
        sum(p.numel() for p in conviction_reader.parameters()) +
        sum(p.numel() for p in m_read_head.parameters()) +
        sum(p.numel() for p in btm_template.parameters())
    )
    print(f"  Trainable: {trainable_params/1e6:.1f}M")

    # === Optimizer ===
    optimizer = torch.optim.AdamW([
        {"params": phi_writer.parameters(), "lr": args.lr},
        {"params": conviction_reader.parameters(), "lr": args.lr},
        {"params": m_read_head.parameters(), "lr": args.lr},
        {"params": btm_template.parameters(), "lr": args.lr},
    ], weight_decay=0.01)

    os.makedirs("checkpoints/v21", exist_ok=True)

    # === Helpers ===
    def build_btm_for_topic(topic):
        tree = build_topic_tree(topic)
        pro_ids, con_ids = get_pro_con_node_ids(tree, n_pro=len(topic["experiences_A"]))

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

    def write_experiences(btm, tree, exp_texts, node_ids):
        for exp_text, nid in zip(exp_texts, node_ids):
            enc = tokenizer(exp_text[:200], return_tensors="pt",
                           truncation=True, max_length=128)
            with torch.no_grad():
                out = base_model(input_ids=enc["input_ids"].to(device),
                                 output_hidden_states=True)
            h_exp = out.hidden_states[-1].mean(dim=1).float().squeeze(0)
            delta = phi_writer(h_exp, btm.get_embedding(nid))
            new_embed = 0.95 * btm.get_embedding(nid) + 0.1 * delta
            btm.set_embedding(nid, new_embed)
        btm.propagate(tree)

    def install_v21_hooks(m_layers, conviction):
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

        # d* injection
        d_handles = install_direction_hooks(
            base_model, direction_injector, conviction, patched_layers)
        handles.extend(d_handles)
        return handles

    # === Training loop ===
    print(f"\n{'='*60}")
    print("TRAINING")
    print(f"{'='*60}\n")

    history = []

    for epoch in range(args.epochs):
        epoch_start = time.time()
        batch_ids = random.sample(train_ids, k=min(args.topics_per_epoch, len(train_ids)))

        epoch_loss = 0.0
        v21_wins, total = 0, 0
        conv_vals = []

        optimizer.zero_grad()

        for topic_id in batch_ids:
            topic = all_topics[topic_id]
            prompt = PROBE_TEMPLATE.format(probe=topic["probe"])
            zero_point = topic_zero_points.get(topic_id, 0.0)

            btm, tree, pro_ids, con_ids = build_btm_for_topic(topic)
            saved = btm.clone_embeddings()

            for side, exp_list, ev_ids, perspective_ids, match_st, creds_high, creds_low in [
                ("pro", topic["experiences_A"], pro_ids[1:], pro_ids,
                 topic["stance_A"], 0.8, 0.3),
                ("con", topic["experiences_B"], con_ids[1:], con_ids,
                 topic["stance_B"], 0.8, 0.3),
            ]:
                btm.restore_embeddings(saved)

                # Write experiences
                write_experiences(btm, tree, exp_list, ev_ids)

                # Set credences for this perspective
                for pid in pro_ids[1:]:
                    tree.nodes[pid].credence = creds_high if side == "pro" else creds_low
                for cid in con_ids[1:]:
                    tree.nodes[cid].credence = creds_high if side == "con" else creds_low

                # Read conviction and M-state
                embed_s, cred_s = btm.get_perspective_embeddings(perspective_ids, tree)
                conviction = conviction_reader(embed_s, cred_s)
                m_layers = m_read_head(embed_s, cred_s)
                conv_vals.append(conviction.item())

                # v21 NTP: M + d*×conviction
                hooks = install_v21_hooks(m_layers, conviction)
                ntp_v21 = statement_ntp(base_model, tokenizer, prompt, match_st, device)
                for h in hooks:
                    h.remove()

                # Baseline NTP: d* at zero point (ambivalent)
                zp_tensor = torch.tensor(zero_point, device=device, dtype=torch.float32)
                d_handles = install_direction_hooks(
                    base_model, direction_injector, zp_tensor, patched_layers)
                with torch.no_grad():
                    ntp_baseline = statement_ntp(base_model, tokenizer, prompt, match_st, device)
                remove_direction_hooks(d_handles)

                # Loss: v21 must beat ambivalent baseline
                margin_loss = F.relu(ntp_v21 - ntp_baseline.detach() + args.margin)
                topic_loss = margin_loss / (args.topics_per_epoch * 2)
                topic_loss.backward()

                epoch_loss += margin_loss.item()
                if ntp_v21.item() < ntp_baseline.item():
                    v21_wins += 1
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
            "v21_wins": f"{v21_wins}/{total}",
            "conv_min": min(conv_vals) if conv_vals else 0,
            "conv_max": max(conv_vals) if conv_vals else 0,
        }
        history.append(row)

        if epoch % args.print_every == 0:
            print(f"E{epoch:03d} [{elapsed:.1f}s] "
                  f"loss={row['loss']:.4f} wins={row['v21_wins']} "
                  f"conv=[{row['conv_min']:.3f}, {row['conv_max']:.3f}]")

        # Checkpoint
        if (epoch + 1) % args.checkpoint_every == 0 or epoch == args.epochs - 1:
            ckpt_path = f"checkpoints/v21/v21_epoch{epoch}_{args.run_name}.pt"
            torch.save({
                "epoch": epoch,
                "phi_writer": phi_writer.state_dict(),
                "conviction_reader": conviction_reader.state_dict(),
                "m_read_head": m_read_head.state_dict(),
                "btm_template": btm_template.state_dict(),
                "config": {
                    "d_node": args.d_node, "rank": args.rank,
                    "base_scale": args.base_scale,
                    "patched_layers": patched_layers,
                    "d_model": d_model,
                },
                "history": history,
            }, ckpt_path)
            print(f"  Saved: {ckpt_path}")

        # Held-out eval
        if (epoch + 1) % args.eval_every == 0:
            print(f"\n  --- Held-out eval (epoch {epoch}) ---")
            ntp_A, ntp_B, ntp_C = [], [], []

            eval_topics = random.sample(held_out, k=min(args.eval_topics, len(held_out)))

            for topic in eval_topics:
                prompt = PROBE_TEMPLATE.format(probe=topic["probe"])
                zp = topic_zero_points.get(topic["id"], 0.0)

                btm_e, tree_e, pro_e, con_e = build_btm_for_topic(topic)
                write_experiences(btm_e, tree_e, topic["experiences_A"], pro_e[1:])

                for pid in pro_e[1:]:
                    tree_e.nodes[pid].credence = 0.8
                for cid in con_e[1:]:
                    tree_e.nodes[cid].credence = 0.3

                embed_s, cred_s = btm_e.get_perspective_embeddings(pro_e, tree_e)
                with torch.no_grad():
                    conv = conviction_reader(embed_s, cred_s)
                    m_layers = m_read_head(embed_s, cred_s)

                # A: no intervention
                with torch.no_grad():
                    na = statement_ntp(base_model, tokenizer, prompt,
                                      topic["stance_A"], device).item()

                # B: d* at zero point
                d_handles = install_direction_hooks(
                    base_model, direction_injector,
                    torch.tensor(zp, device=device, dtype=torch.float32),
                    patched_layers)
                with torch.no_grad():
                    nb = statement_ntp(base_model, tokenizer, prompt,
                                      topic["stance_A"], device).item()
                remove_direction_hooks(d_handles)

                # C: full v21
                hooks = install_v21_hooks(m_layers, conv)
                with torch.no_grad():
                    nc = statement_ntp(base_model, tokenizer, prompt,
                                      topic["stance_A"], device).item()
                for h in hooks:
                    h.remove()

                ntp_A.append(na)
                ntp_B.append(nb)
                ntp_C.append(nc)

            c_beats_b = sum(1 for c, b in zip(ntp_C, ntp_B) if c < b)
            print(f"  A(none)={sum(ntp_A)/len(ntp_A):.4f} "
                  f"B(d*@zp)={sum(ntp_B)/len(ntp_B):.4f} "
                  f"C(v21)={sum(ntp_C)/len(ntp_C):.4f} "
                  f"C<B: {c_beats_b}/{len(ntp_C)}")

    print(f"\n{'='*60}")
    print(f"TRAINING COMPLETE — v21")
    print(f"{'='*60}")
    print(f"  Final: {history[-1]}")

    with open(f"logs/v21_{args.run_name}_history.json", "w") as f:
        json.dump(history, f, indent=2)


if __name__ == "__main__":
    from hexis.adapters.cli import add_preset_args, resolve_preset_args

    p = argparse.ArgumentParser()
    add_preset_args(p, agentic=False, add_training_args=True, training_phase="a")
    p.add_argument("--epochs", type=int, default=200)
    p.add_argument("--d_node", type=int, default=128)
    p.add_argument("--base_scale", type=float, default=10.0)
    p.add_argument("--topics_per_epoch", type=int, default=16)
    p.add_argument("--eval_topics", type=int, default=20)
    p.add_argument("--grad_clip", type=float, default=1.0)
    p.add_argument("--print_every", type=int, default=1)
    p.add_argument("--checkpoint_every", type=int, default=25)
    p.add_argument("--eval_every", type=int, default=10)
    p.add_argument("--run_name", default="v21")
    args = p.parse_args()
    resolve_preset_args(args)
    print(f"  Preset: {args.preset} (model={args.model}, rank={args.rank}, "
          f"margin={args.margin}, lr={args.lr})")

    train(args)
