"""
Extract a generic behavioral d* direction from prompt-variation contrast.

Same math as extract_d_star_repeat.py (normalize(mean_pos - mean_neg) per
layer), but without tau-bench trajectory replay: we just feed ~20 positive
and ~20 negative prompts through the model, capture the last-prefill hidden
state at strided layers, and compute the mean difference.

This is the primitive for adding *behavioral* directions — "don't stop early",
"check parameters before committing", "reflect before terminating". The
positive prompts frame the target behavior; the negative prompts frame its
opposite. As long as the base model has some representational encoding of
the distinction (even latent), the mean difference captures it.

Outputs wrapped-format checkpoints compatible with
deploy/agentic_eval/directions.py::load_from_checkpoint:

    {
        "d_star": {layer_idx: unit_vector(d_model,)},
        "n_novel": int,   # reused field name — = n_positive
        "n_repeat": int,  # reused field name — = n_negative
        "separable_layers": int,
        "tasks": [],
        "model": str,
        "stride": int,
        "layers": list[int],
        "direction_name": str,
    }

Usage:
    python scripts/extract_d_star_prompted.py \
        --direction d_star_no_early_termination \
        --positive prompts/no_early_term_positive.txt \
        --negative prompts/no_early_term_negative.txt \
        --output checkpoints/d_star_no_early_termination.pt

Input prompt files are one prompt per line, # comments allowed.
"""
import argparse
import gc
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import torch
import torch.nn.functional as F
from transformers import AutoModelForCausalLM, AutoTokenizer


def read_prompts(path: str) -> list[str]:
    prompts = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            prompts.append(line)
    return prompts


def capture_prompt_hidden_states(model, tokenizer, prompt, layers, device):
    """Capture last-token hidden state at each target layer on a single
    forward pass through `prompt`. Returns {layer_idx: tensor(d_model,)}.
    Uses register_forward_hook on each layer, fires once on the prefill.
    """
    input_ids = tokenizer(
        prompt, return_tensors="pt", truncation=True, max_length=2048,
    ).input_ids.to(device)
    prefill_len = input_ids.shape[1]

    captured = {}
    handles = []
    for layer_idx in layers:
        def make_hook(li, plen):
            fired = [False]
            def hook(module, inputs, output):
                if fired[0]:
                    return
                if isinstance(inputs, tuple) and len(inputs) > 0:
                    h = inputs[0]
                else:
                    return
                if h.shape[1] == plen:
                    captured[li] = h[0, -1, :].detach().to(torch.float16).cpu()
                    fired[0] = True
            return hook
        handle = model.model.layers[layer_idx].register_forward_hook(
            make_hook(layer_idx, prefill_len)
        )
        handles.append(handle)

    with torch.no_grad():
        _ = model(input_ids)

    for h in handles:
        h.remove()

    return captured


def compute_direction(pos_samples, neg_samples, layers):
    """d*[L] = normalize(mean(pos[L]) - mean(neg[L])). Returns dict and
    per-layer cos(mean_pos, mean_neg) for separability reporting.
    """
    d_star = {}
    sep = {}
    for l in layers:
        pos_l = [s[l] for s in pos_samples if l in s]
        neg_l = [s[l] for s in neg_samples if l in s]
        if not pos_l or not neg_l:
            continue
        pos_mean = torch.stack(pos_l).float().mean(0)
        neg_mean = torch.stack(neg_l).float().mean(0)
        direction = pos_mean - neg_mean
        norm = direction.norm().item()
        if norm < 1e-6:
            continue
        d_star[l] = direction / direction.norm()
        cos = F.cosine_similarity(
            pos_mean.unsqueeze(0), neg_mean.unsqueeze(0)
        ).item()
        sep[l] = cos
    return d_star, sep


def main():
    from hexis.adapters.cli import add_preset_args, resolve_preset_args

    ap = argparse.ArgumentParser()
    # --output is required here (direction-specific filename), so we don't
    # pass output_subpath — user must provide --output explicitly.
    add_preset_args(ap, agentic=True, output_subpath=None)
    ap.add_argument("--direction", required=True,
                    help="Direction name, e.g. d_star_no_early_termination")
    ap.add_argument("--positive", required=True,
                    help="Path to file with positive prompts, one per line")
    ap.add_argument("--negative", required=True,
                    help="Path to file with negative prompts, one per line")
    ap.add_argument("--output", required=True)
    args = ap.parse_args()
    preset = resolve_preset_args(args)

    print("=" * 60)
    print(f"Extract {args.direction}")
    print(f"  Preset:   {preset.name}")
    print(f"  Model:    {args.model}")
    print(f"  Positive: {args.positive}")
    print(f"  Negative: {args.negative}")
    print(f"  Stride:   {args.stride}")
    print(f"  Output:   {args.output}")
    print("=" * 60)

    pos_prompts = read_prompts(args.positive)
    neg_prompts = read_prompts(args.negative)
    print(f"\n  {len(pos_prompts)} positive prompts, {len(neg_prompts)} negative prompts")
    if len(pos_prompts) < 10 or len(neg_prompts) < 10:
        print("  WARNING: fewer than 10 prompts per class — direction will be noisy")

    tokenizer = AutoTokenizer.from_pretrained(args.model, trust_remote_code=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    model = AutoModelForCausalLM.from_pretrained(
        args.model, torch_dtype=torch.bfloat16, device_map="auto",
        trust_remote_code=True,
    )
    model.eval()
    for p in model.parameters():
        p.requires_grad = False

    n_layers = model.config.num_hidden_layers
    device = next(model.parameters()).device
    layers = list(range(0, n_layers, args.stride))
    print(f"\n  Model: {n_layers} layers  |  Capture layers: {layers}")

    pos_samples = []
    print("\n  Capturing positive samples...")
    t0 = time.time()
    for i, prompt in enumerate(pos_prompts):
        states = capture_prompt_hidden_states(model, tokenizer, prompt, layers, device)
        if states:
            pos_samples.append(states)
        if (i + 1) % 5 == 0:
            print(f"    {i+1}/{len(pos_prompts)}")
    print(f"  Captured {len(pos_samples)} positive in {time.time()-t0:.0f}s")

    gc.collect()
    torch.cuda.empty_cache()

    neg_samples = []
    print("\n  Capturing negative samples...")
    t0 = time.time()
    for i, prompt in enumerate(neg_prompts):
        states = capture_prompt_hidden_states(model, tokenizer, prompt, layers, device)
        if states:
            neg_samples.append(states)
        if (i + 1) % 5 == 0:
            print(f"    {i+1}/{len(neg_prompts)}")
    print(f"  Captured {len(neg_samples)} negative in {time.time()-t0:.0f}s")

    print("\n" + "=" * 60)
    print("SEPARABILITY (cos(pos_mean, neg_mean) per layer)")
    print("=" * 60)
    d_star, sep = compute_direction(pos_samples, neg_samples, layers)
    separable = 0
    for l in sorted(d_star.keys()):
        cos = sep[l]
        tag = "SEPARABLE" if cos < 0.95 else "not separable"
        mag = (torch.stack([s[l] for s in pos_samples]).float().mean(0)
               - torch.stack([s[l] for s in neg_samples]).float().mean(0)).norm().item()
        print(f"  Layer {l:2d}: ||Δmean||={mag:.4f}  cos(pos,neg)={cos:.4f}  {tag}")
        if cos < 0.95:
            separable += 1
    print(f"\n  Separable layers: {separable}/{len(d_star)}")

    if not d_star:
        print("  FAILED — no direction computed")
        sys.exit(1)

    out_dir = os.path.dirname(os.path.abspath(args.output))
    os.makedirs(out_dir, exist_ok=True)
    torch.save({
        "d_star": d_star,
        "n_novel": len(pos_samples),
        "n_repeat": len(neg_samples),
        "separable_layers": separable,
        "tasks": [],
        "model": args.model,
        "stride": args.stride,
        "layers": layers,
        "direction_name": args.direction,
    }, args.output)
    print(f"\n  Saved → {args.output}")


if __name__ == "__main__":
    main()
