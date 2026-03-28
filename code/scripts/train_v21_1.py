"""
QKVM v21.1: Bayesian Direction × Conviction

Properly implements Bayesian epistemology:
  - Credences initialized from measured priors (zero points)
  - Jeffrey conditionalization updates credences after evidence
  - Conviction IS the posterior credence (not an opaque neural output)
  - d* at calibrated scale=0.30 (Pareto knee: 58% ranking, +0.28 nat degradation)

Three loss components:
  L_margin:  posterior-conditioned must beat prior-conditioned (confirmation)
  L_align:   neural conviction must match Jeffrey posterior (calibration)
  L_content: M-state must add value above d* alone (content disposition)

Usage:
    PYTHONUNBUFFERED=1 nohup python scripts/train_v21_1.py \
        --epochs 200 --run_name v21_1 \
        > logs/v21_1_train.log 2>&1 &
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
    from qkvm.model_hybrid import get_text_config
    from qkvm.direction_injector import (
        DirectionInjector, install_direction_hooks, remove_direction_hooks,
    )
    from qkvm.belief_tree_memory import BeliefTreeMemory, build_topic_tree, get_pro_con_node_ids
    from qkvm.phi_node_writer import PhiNodeWriter
    from qkvm.conviction_reader import ConvictionReader
    from qkvm.mstate_read_head import MStateReadHead
    from qkvm.jeffrey_update import (
        jeffrey_update_node, propagate_credences,
        initialize_credences_from_zero_points,
        credence_to_conviction,
    )

    from qkvm.data_200_topics import TRAIN_200, HELD_OUT_200
    from scripts.train_amplifier_v6_ppl import (
        TRAIN_TOPICS as TRAIN_ORIGINAL,
        HELD_OUT_TOPICS as HELD_OUT_ORIGINAL,
    )

    print("=" * 60)
    print("QKVM v21.1: Bayesian Direction × Conviction")
    print("=" * 60)
    print(f"  base_scale: {args.base_scale}")
    print(f"  Losses: margin + align + content")

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

    # === Load d* and zero points ===
    d_star = torch.load("checkpoints/d_star.pt", map_location="cpu", weights_only=True)
    direction_injector = DirectionInjector(d_star, base_scale=args.base_scale).to(device)
    direction_injector.eval()

    topic_zero_points = torch.load("checkpoints/topic_zero_points.pt",
                                    map_location="cpu", weights_only=True)
    print(f"  d* loaded, base_scale={args.base_scale}")
    print(f"  Zero points: {len(topic_zero_points)} topics")

    # === Prepare topics ===
    all_topics = {}
    for t in list(TRAIN_ORIGINAL) + list(TRAIN_200):
        all_topics[t["id"]] = t
    held_out = list(HELD_OUT_ORIGINAL) + list(HELD_OUT_200)
    train_ids = list(all_topics.keys())
    print(f"  Train: {len(train_ids)}, Held-out: {len(held_out)}")

    # === Trainable modules ===
    phi_writer = PhiNodeWriter(d_model=d_model, d_node=args.d_node).to(device)
    conviction_reader = ConvictionReader(d_node=args.d_node).to(device)
    m_read_head = MStateReadHead(
        d_node=args.d_node, d_model=d_model, rank=args.rank,
        n_layers=len(patched_layers),
    ).to(device)

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

    optimizer = torch.optim.AdamW([
        {"params": phi_writer.parameters(), "lr": args.lr},
        {"params": conviction_reader.parameters(), "lr": args.lr},
        {"params": m_read_head.parameters(), "lr": args.lr},
        {"params": btm_template.parameters(), "lr": args.lr},
    ], weight_decay=0.01)

    os.makedirs("checkpoints/v21_1", exist_ok=True)

    # === Helpers ===
    def build_btm(topic):
        tree = build_topic_tree(topic)
        pro_ids, con_ids = get_pro_con_node_ids(tree, n_pro=len(topic["experiences_A"]))

        # Initialize credences from priors (zero points)
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
        """Write experiences: update embeddings AND credences."""
        for exp_text, nid in zip(exp_texts, ev_ids):
            enc = tokenizer(exp_text[:200], return_tensors="pt",
                           truncation=True, max_length=128)
            with torch.no_grad():
                out = base_model(input_ids=enc["input_ids"].to(device),
                                 output_hidden_states=True)
            h_exp = out.hidden_states[-1].mean(dim=1).float().squeeze(0)

            # Neural: update embedding
            delta = phi_writer(h_exp, btm.get_embedding(nid))
            new_embed = 0.95 * btm.get_embedding(nid) + 0.1 * delta
            btm.set_embedding(nid, new_embed)

            # Formal: Jeffrey conditionalization on credence
            # gate_val approximates evidence strength
            gate_val = torch.sigmoid(phi_writer.gate_proj(
                torch.cat([phi_writer.experience_encoder(h_exp.unsqueeze(0)).squeeze(0),
                           btm.get_embedding(nid)])
            )).item()
            jeffrey_update_node(tree, nid, gate_val, direction)

        btm.propagate(tree)
        propagate_credences(tree)

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

        epoch_margin = 0.0
        epoch_align = 0.0
        epoch_content = 0.0
        margin_wins, total = 0, 0
        conv_vals = []

        for topic_id in batch_ids:
            optimizer.zero_grad()
            topic = all_topics[topic_id]
            prompt = PROBE_TEMPLATE.format(probe=topic["probe"])

            btm, tree, pro_ids, con_ids = build_btm(topic)
            saved_embeddings = btm.clone_embeddings()

            # Get prior conviction from zero point
            prior_credence = tree.nodes[tree.root_id].credence
            prior_conviction = credence_to_conviction(prior_credence)

            for side, exp_list, ev_ids, perspective_ids, match_st, direction in [
                ("pro", topic["experiences_A"], pro_ids[1:], pro_ids, topic["stance_A"], +1.0),
                ("con", topic["experiences_B"], con_ids[1:], con_ids, topic["stance_B"], -1.0),
            ]:
                btm.restore_embeddings(saved_embeddings)
                # Reset credences to prior
                initialize_credences_from_zero_points(tree, topic_id, topic_zero_points)

                # Write experiences: update embeddings + Jeffrey conditionalization
                write_and_update(btm, tree, exp_list, ev_ids, direction)

                # Get posterior credence from Jeffrey update
                posterior_credence = tree.nodes[tree.root_id].credence
                formal_conviction = credence_to_conviction(posterior_credence)

                # Set perspective credences
                for pid in pro_ids[1:]:
                    tree.nodes[pid].credence = 0.8 if side == "pro" else 0.3
                for cid in con_ids[1:]:
                    tree.nodes[cid].credence = 0.8 if side == "con" else 0.3

                embed_s, cred_s = btm.get_perspective_embeddings(perspective_ids, tree)
                formal_conv_val, predicted_conv = conviction_reader(
                    embed_s, cred_s, posterior_credence)
                m_layers = m_read_head(embed_s, cred_s)

                conv_vals.append(formal_conv_val)

                # === LOSS 1: posterior must beat prior (confirmation) ===
                prior_conv_t = torch.tensor(prior_conviction, device=device, dtype=torch.float32)
                d_handles = install_direction_hooks(
                    base_model, direction_injector, prior_conv_t, patched_layers)
                with torch.no_grad():
                    ntp_prior = statement_ntp(base_model, tokenizer, prompt, match_st, device)
                remove_direction_hooks(d_handles)

                formal_conv_t = torch.tensor(formal_conv_val, device=device, dtype=torch.float32)
                d_handles = install_direction_hooks(
                    base_model, direction_injector, formal_conv_t, patched_layers)
                with torch.no_grad():
                    ntp_posterior = statement_ntp(base_model, tokenizer, prompt, match_st, device)
                remove_direction_hooks(d_handles)

                L_margin = F.relu(ntp_posterior - ntp_prior + args.margin)

                # === LOSS 2: neural prediction aligns with Jeffrey result ===
                formal_conv_target = torch.tensor(formal_conv_val, device=device, dtype=torch.float32)
                L_align = F.mse_loss(predicted_conv, formal_conv_target.detach())

                # === LOSS 3: M-state adds value above d* alone ===
                hooks = install_v21_hooks(m_layers, formal_conv_t)
                ntp_full = statement_ntp(base_model, tokenizer, prompt, match_st, device)
                for h in hooks:
                    h.remove()

                with torch.no_grad():
                    ntp_posterior_ref = statement_ntp(base_model, tokenizer, prompt, match_st, device)
                    d_handles2 = install_direction_hooks(
                        base_model, direction_injector, formal_conv_t, patched_layers)
                    ntp_posterior_ref = statement_ntp(base_model, tokenizer, prompt, match_st, device)
                    remove_direction_hooks(d_handles2)

                L_content = F.relu(ntp_full - ntp_posterior_ref + args.content_margin)

                # Combined loss
                topic_loss = (L_margin + args.lambda_align * L_align + args.lambda_content * L_content) / (args.topics_per_epoch * 2)
                topic_loss.backward()

                epoch_margin += L_margin.item()
                epoch_align += L_align.item()
                epoch_content += L_content.item()

                if ntp_posterior.item() < ntp_prior.item():
                    margin_wins += 1
                total += 1

            # Step per topic (not per epoch) to prevent graph accumulation
            torch.nn.utils.clip_grad_norm_(
                list(phi_writer.parameters()) + list(conviction_reader.parameters()) +
                list(m_read_head.parameters()) + list(btm_template.parameters()),
                args.grad_clip)
            optimizer.step()

        elapsed = time.time() - epoch_start
        row = {
            "epoch": epoch, "time": elapsed,
            "L_margin": epoch_margin / max(total, 1),
            "L_align": epoch_align / max(total, 1),
            "L_content": epoch_content / max(total, 1),
            "margin_wins": f"{margin_wins}/{total}",
            "conv_min": min(conv_vals) if conv_vals else 0,
            "conv_max": max(conv_vals) if conv_vals else 0,
        }
        history.append(row)

        if epoch % args.print_every == 0:
            print(f"E{epoch:03d} [{elapsed:.1f}s] "
                  f"mar={row['L_margin']:.4f} ali={row['L_align']:.4f} "
                  f"con={row['L_content']:.4f} wins={row['margin_wins']} "
                  f"cv=[{row['conv_min']:.3f},{row['conv_max']:.3f}]")

        # Checkpoint
        if (epoch + 1) % args.checkpoint_every == 0 or epoch == args.epochs - 1:
            ckpt_path = f"checkpoints/v21_1/v21_1_epoch{epoch}_{args.run_name}.pt"
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
                btm_e, tree_e, pro_e, con_e = build_btm(topic)

                # Write pro experiences
                write_and_update(btm_e, tree_e, topic["experiences_A"], pro_e[1:], +1.0)

                posterior_cr = tree_e.nodes[tree_e.root_id].credence
                formal_cv = credence_to_conviction(posterior_cr)
                prior_cr = (topic_zero_points.get(topic["id"], 0.0) + 1) / 2
                prior_cv = credence_to_conviction(max(0.05, min(0.95, prior_cr)))

                for pid in pro_e[1:]:
                    tree_e.nodes[pid].credence = 0.8
                for cid in con_e[1:]:
                    tree_e.nodes[cid].credence = 0.3

                embed_s, cred_s = btm_e.get_perspective_embeddings(pro_e, tree_e)
                with torch.no_grad():
                    _, pred_cv = conviction_reader(embed_s, cred_s, posterior_cr)
                    m_layers = m_read_head(embed_s, cred_s)

                # A: no intervention
                with torch.no_grad():
                    na = statement_ntp(base_model, tokenizer, prompt,
                                      topic["stance_A"], device).item()

                # B: d* at prior (zero point)
                prior_t = torch.tensor(prior_cv, device=device, dtype=torch.float32)
                d_handles = install_direction_hooks(
                    base_model, direction_injector, prior_t, patched_layers)
                with torch.no_grad():
                    nb = statement_ntp(base_model, tokenizer, prompt,
                                      topic["stance_A"], device).item()
                remove_direction_hooks(d_handles)

                # C: full v21.1 (d* at formal posterior + M)
                formal_t = torch.tensor(formal_cv, device=device, dtype=torch.float32)
                hooks = install_v21_hooks(m_layers, formal_t)
                with torch.no_grad():
                    nc = statement_ntp(base_model, tokenizer, prompt,
                                      topic["stance_A"], device).item()
                for h in hooks:
                    h.remove()

                ntp_A.append(na)
                ntp_B.append(nb)
                ntp_C.append(nc)

            c_beats_a = sum(1 for c, a in zip(ntp_C, ntp_A) if c < a)
            c_beats_b = sum(1 for c, b in zip(ntp_C, ntp_B) if c < b)
            print(f"  A={sum(ntp_A)/len(ntp_A):.4f} "
                  f"B(d*@prior)={sum(ntp_B)/len(ntp_B):.4f} "
                  f"C(v21.1)={sum(ntp_C)/len(ntp_C):.4f} "
                  f"C<A:{c_beats_a}/{len(ntp_C)} C<B:{c_beats_b}/{len(ntp_C)}")

    print(f"\n{'='*60}")
    print(f"TRAINING COMPLETE — v21.1")
    print(f"{'='*60}")
    print(f"  Final: {history[-1]}")

    with open(f"logs/v21_1_{args.run_name}_history.json", "w") as f:
        json.dump(history, f, indent=2)


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--model", default="Qwen/Qwen3.5-4B-Base")
    p.add_argument("--epochs", type=int, default=200)
    p.add_argument("--d_node", type=int, default=128)
    p.add_argument("--rank", type=int, default=16)
    p.add_argument("--base_scale", type=float, default=0.50)
    p.add_argument("--topics_per_epoch", type=int, default=16)
    p.add_argument("--eval_topics", type=int, default=20)
    p.add_argument("--lr", type=float, default=1e-4)
    p.add_argument("--grad_clip", type=float, default=1.0)
    p.add_argument("--margin", type=float, default=0.3)
    p.add_argument("--content_margin", type=float, default=0.1)
    p.add_argument("--lambda_align", type=float, default=1.0)
    p.add_argument("--lambda_content", type=float, default=0.5)
    p.add_argument("--print_every", type=int, default=1)
    p.add_argument("--checkpoint_every", type=int, default=25)
    p.add_argument("--eval_every", type=int, default=10)
    p.add_argument("--run_name", default="v21_1")

    train(p.parse_args())
