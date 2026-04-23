"""
Stage 1: Extract d* — the base model's native pro/con direction vector.

Validated by rep engineering probe: 81% held-out at scale 10-20.

d* is FIXED forever after extraction. Registered as buffer, never trained.

Usage:
    python scripts/extract_d_star.py
"""

import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import torch
import torch.nn.functional as F

from scripts.train_v19_structured import statement_ntp

PROBE_TEMPLATE = (
    "You have strong opinions formed from years of direct experience. "
    "Share your honest view based on what you've personally witnessed.\n\n"
    "Question: {probe}\nAnswer: "
)


def extract_d_star(base_model, tokenizer, topics, patched_layers, device):
    """Extract per-layer unit direction vector d* = normalize(mean(pro_act - con_act))."""
    pro_acts = {l: [] for l in patched_layers}
    con_acts = {l: [] for l in patched_layers}

    base_model.eval()
    with torch.no_grad():
        for i, topic in enumerate(topics):
            for side, stance_text, act_dict in [
                ("pro", topic["stance_A"], pro_acts),
                ("con", topic["stance_B"], con_acts),
            ]:
                prompt = PROBE_TEMPLATE.format(probe=topic["probe"])
                full_text = prompt + stance_text
                enc = tokenizer(full_text, return_tensors="pt",
                               truncation=True, max_length=512)
                out = base_model(input_ids=enc["input_ids"].to(device),
                                 output_hidden_states=True)
                for l in patched_layers:
                    h = out.hidden_states[l + 1].mean(dim=1).squeeze(0).float().cpu()
                    act_dict[l].append(h)

            if (i + 1) % 20 == 0:
                print(f"  {i+1}/{len(topics)} topics encoded")

    d_star = {}
    for l in patched_layers:
        pro_mean = torch.stack(pro_acts[l]).mean(dim=0)
        con_mean = torch.stack(con_acts[l]).mean(dim=0)
        direction = pro_mean - con_mean
        d_star[l] = direction / direction.norm()  # unit vector

    return d_star


def verify_d_star(base_model, tokenizer, d_star, held_out_topics,
                   patched_layers, device, scale=10.0):
    """Verify d* reproduces ~81% held-out accuracy."""
    from hexis.model_hybrid import get_text_config

    layers = base_model.model.layers

    class DStarHook:
        def __init__(self):
            self.d = None
            self.scale = 0.0
            self.active = False
        def hook_fn(self, module, input, output):
            if not self.active:
                return output
            if isinstance(output, tuple):
                h = output[0]
                h = h + self.scale * self.d.to(h.device, h.dtype)
                return (h,) + output[1:]
            return output + self.scale * self.d.to(output.device, output.dtype)

    hooks_objs = {}
    handles = []
    for li in patched_layers:
        dh = DStarHook()
        dh.d = d_star[li].to(device)
        hooks_objs[li] = dh
        attn = getattr(layers[li], 'self_attn', None) or getattr(layers[li], 'linear_attn', None)
        if attn:
            handles.append(attn.register_forward_hook(dh.hook_fn))

    pro_wins, con_wins, total = 0, 0, 0

    # +d* for pro
    for dh in hooks_objs.values():
        dh.scale = scale
        dh.active = True

    for topic in held_out_topics:
        prompt = PROBE_TEMPLATE.format(probe=topic["probe"])
        with torch.no_grad():
            l_pro = statement_ntp(base_model, tokenizer, prompt, topic["stance_A"], device)
            l_con = statement_ntp(base_model, tokenizer, prompt, topic["stance_B"], device)
        if l_pro.item() < l_con.item():
            pro_wins += 1
        total += 1

    # -d* for con
    for dh in hooks_objs.values():
        dh.scale = -scale

    for topic in held_out_topics:
        prompt = PROBE_TEMPLATE.format(probe=topic["probe"])
        with torch.no_grad():
            l_pro = statement_ntp(base_model, tokenizer, prompt, topic["stance_A"], device)
            l_con = statement_ntp(base_model, tokenizer, prompt, topic["stance_B"], device)
        if l_con.item() < l_pro.item():
            con_wins += 1
        total += 1

    for h in handles:
        h.remove()
    for dh in hooks_objs.values():
        dh.active = False

    accuracy = 100 * (pro_wins + con_wins) / total
    print(f"  Verification: +d*={pro_wins}, -d*={con_wins}, total={pro_wins+con_wins}/{total} ({accuracy:.0f}%)")
    return accuracy


def main():
    from transformers import AutoModelForCausalLM, AutoTokenizer
    from hexis.model_hybrid import get_text_config
    from hexis.data_200_topics import TRAIN_200, HELD_OUT_200
    from scripts.train_amplifier_v6_ppl import (
        TRAIN_TOPICS as TRAIN_ORIGINAL,
        HELD_OUT_TOPICS as HELD_OUT_ORIGINAL,
    )

    t0 = time.time()
    print("=" * 60)
    print("Stage 1: Extract d* direction vector")
    print("=" * 60)

    import argparse
    from hexis.adapters.cli import add_preset_args, resolve_preset_args

    ap = argparse.ArgumentParser()
    add_preset_args(ap, agentic=False, output_subpath="d_star.pt")
    args = ap.parse_args()
    preset = resolve_preset_args(args)
    model_name = args.model
    stride = args.stride
    output_path = args.output
    print(f"  Preset: {preset.name} (hf_id={model_name}, stride={stride})")

    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    base_model = AutoModelForCausalLM.from_pretrained(
        model_name, dtype=torch.bfloat16, device_map="auto", trust_remote_code=True)
    base_model.eval()
    for param in base_model.parameters():
        param.requires_grad = False

    model_config = get_text_config(base_model.config)
    d_model = model_config.hidden_size
    n_layers = model_config.num_hidden_layers
    device = next(base_model.parameters()).device
    patched_layers = preset.patched_layer_indices(n_layers_override=n_layers) \
        if args.stride is None \
        else list(range(0, n_layers, stride))

    # Training topics for extraction (NOT held-out)
    train_topics = list(TRAIN_ORIGINAL) + list(TRAIN_200)
    held_out = list(HELD_OUT_ORIGINAL) + list(HELD_OUT_200)
    print(f"  Extraction topics: {len(train_topics)}")
    print(f"  Held-out topics: {len(held_out)}")
    print(f"  Patched layers: {patched_layers}")

    # Extract d*
    print(f"\nExtracting d*...")
    d_star = extract_d_star(base_model, tokenizer, train_topics, patched_layers, device)

    # Print norms
    print(f"\nd* norms per layer:")
    for l in patched_layers:
        print(f"  Layer {l:2d}: norm={d_star[l].norm():.4f}, shape={d_star[l].shape}")

    # Save
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    torch.save(d_star, output_path)
    print(f"\nSaved d* to {output_path}")

    # Verify: reproduce ~81% held-out
    print(f"\nVerifying on held-out...")
    accuracy = verify_d_star(base_model, tokenizer, d_star, held_out,
                              patched_layers, device, scale=10.0)

    if accuracy >= 75:
        print(f"\n✓ Stage 1 PASSED — d* verified at {accuracy:.0f}% held-out")
    else:
        print(f"\n✗ Stage 1 FAILED — expected ~81%, got {accuracy:.0f}%")
        print(f"  Check extraction. Do not proceed.")

    print(f"\n  Total time: {(time.time()-t0)/60:.1f} min")


if __name__ == "__main__":
    main()
