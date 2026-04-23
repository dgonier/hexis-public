"""
Extract d*_repeat: direction vector separating "novel tool call" hidden states
from "repeated/duplicate tool call" hidden states.

Approach:
1. Run tau-bench tasks locally with Qwen3.5-4B, using a forward hook to capture
   hidden states at the last token of the prefill phase (the generation decision point).
   Single forward pass — no output_hidden_states=True overhead.
2. Label each tool call as "novel" (first time this signature) or "repeat" (duplicate).
3. Compute d*_repeat = normalize(mean(novel) - mean(repeat)) per layer.
4. Inject +d*_repeat to bias model toward novel/decisive tool use.

Usage:
    python scripts/extract_d_star_repeat.py \
        --tasks 10 26 10 26 10 0 5 11 19 \
        --output checkpoints/d_star_repeat.pt
"""

import argparse
import gc
import json
import os
import re
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "tau-bench"))

import torch
import torch.nn.functional as F
from transformers import AutoModelForCausalLM, AutoTokenizer

from tau_bench.envs.airline.env import MockAirlineDomainEnv
from tau_bench.envs.airline.wiki import WIKI
from tau_bench.types import Action, RESPOND_ACTION_NAME

from scripts.eval_hybrid import (
    GoldAwareUserSim, USER_MODEL,
    parse_tool_calls, coerce_param_types,
)


def capture_prefill_hidden_states(model, input_ids, layers):
    """Capture hidden states at the last token during the prefill phase of generate().

    Uses forward hooks on each layer that fire once (on the full prefill sequence)
    and then disable themselves. Returns (gen_out, {layer_idx: tensor(d_model,)}).
    """
    captured = {}
    handles = []
    prefill_len = input_ids.shape[1]

    for layer_idx in layers:
        def make_hook(li, plen):
            fired = [False]
            def hook(module, input, output):
                if fired[0]:
                    return
                # input[0] is the residual stream entering this layer: (batch, seq, d_model)
                if isinstance(input, tuple) and len(input) > 0:
                    h = input[0]
                else:
                    return
                if h.shape[1] == plen:  # only fire on the full prefill pass
                    captured[li] = h[0, -1, :].detach().to(torch.float16).cpu()
                    fired[0] = True
            return hook
        handle = model.model.layers[layer_idx].register_forward_hook(
            make_hook(layer_idx, prefill_len)
        )
        handles.append(handle)

    with torch.no_grad():
        gen_out = model.generate(
            input_ids,
            max_new_tokens=512,
            do_sample=True,
            temperature=0.1,
            top_p=0.95,
            pad_token_id=model.config.eos_token_id,
            use_cache=True,
        )

    for h in handles:
        h.remove()

    return gen_out, captured


def build_prompt(tokenizer, messages, tools_info):
    """Build the full prompt string including the pre-seeded think block."""
    kwargs = dict(tokenize=False, add_generation_prompt=False)
    if tools_info:
        kwargs["tools"] = tools_info
    try:
        kwargs["enable_thinking"] = False
        prompt = tokenizer.apply_chat_template(messages, **kwargs)
    except Exception:
        del kwargs["enable_thinking"]
        prompt = tokenizer.apply_chat_template(messages, **kwargs)
    return prompt + "<|im_start|>assistant\n<think>\n\n</think>\n\n"


def run_task_collect_states(task_id, model, tokenizer, device, layers,
                             max_turns=30, log_fn=print):
    """Run one task trajectory, returning labeled hidden-state samples."""

    env = MockAirlineDomainEnv(
        user_strategy="llm", user_model=USER_MODEL,
        user_provider="bedrock", task_split="test", task_index=task_id,
    )
    reset = env.reset(task_index=task_id)
    task_def = reset.info.task

    gold_actions_list = [
        {"name": a.name, "arguments": a.kwargs} if hasattr(a, "name") else a
        for a in (task_def.actions or [])
    ]
    env.user = GoldAwareUserSim(
        model=USER_MODEL, provider="bedrock", gold_actions=gold_actions_list,
    )
    task_observation = env.user.reset(instruction=task_def.instruction)

    tools_info = env.tools_info
    tool_by_name = {t["function"]["name"]: t for t in tools_info}

    messages = [
        {"role": "system", "content": WIKI},
        {"role": "user", "content": task_observation},
    ]

    call_signatures = {}  # sig -> first_seen_turn
    turn_data = []
    done = False

    for turn in range(max_turns):
        if done:
            break

        prompt = build_prompt(tokenizer, messages, tools_info)
        input_ids = tokenizer(
            prompt, return_tensors="pt", truncation=True, max_length=8192,
        ).input_ids.to(device)

        gen_out, hidden = capture_prefill_hidden_states(model, input_ids, layers)
        prefill_len = input_ids.shape[1]
        new_tokens = gen_out[0, prefill_len:].cpu()
        raw_output = tokenizer.decode(new_tokens, skip_special_tokens=False)
        del input_ids, gen_out, new_tokens
        torch.cuda.empty_cache()
        action_text = re.sub(r'<\|im_end\|>.*', '', raw_output, flags=re.DOTALL).strip()
        action_text = re.sub(r'<\|endoftext\|>.*', '', action_text, flags=re.DOTALL).strip()
        action_text_clean = re.sub(r'<think>.*?</think>', '', action_text, flags=re.DOTALL)

        tool_calls = parse_tool_calls(action_text_clean)

        if tool_calls:
            messages.append({"role": "assistant", "content": action_text})
            for fname, kwargs_tool in tool_calls:
                schema = tool_by_name.get(fname)
                if schema is not None:
                    try:
                        kwargs_tool = coerce_param_types(schema, kwargs_tool)
                    except Exception:
                        pass

                try:
                    sig = f"{fname}({json.dumps(kwargs_tool, sort_keys=True, default=str)})"
                except Exception:
                    sig = f"{fname}({kwargs_tool})"

                if sig in call_signatures:
                    label = "repeat"
                    log_fn(f"    turn {turn:2d}: REPEAT  {fname}")
                else:
                    label = "novel"
                    log_fn(f"    turn {turn:2d}: NOVEL   {fname}")
                    call_signatures[sig] = turn

                if hidden:
                    turn_data.append({
                        "turn": turn,
                        "label": label,
                        "hidden": hidden,
                        "tool_name": fname,
                        "sig": sig,
                    })

                action = Action(name=fname, kwargs=kwargs_tool)
                resp = env.step(action)
                messages.append({"role": "tool", "name": fname, "content": str(resp.observation)})

                if resp.done:
                    done = True
                    break
        else:
            content = action_text_clean[:500] or "Could you clarify?"
            action = Action(name=RESPOND_ACTION_NAME, kwargs={"content": content})
            resp = env.step(action)
            messages.append({"role": "assistant", "content": content})
            log_fn(f"    turn {turn:2d}: respond")

            if hidden:
                turn_data.append({
                    "turn": turn,
                    "label": "respond",
                    "hidden": hidden,
                    "tool_name": "respond",
                    "sig": None,
                })

            if resp.done:
                done = True
            else:
                messages.append({"role": "user", "content": resp.observation})

    return turn_data


def compute_d_star(all_turn_data, layers):
    """Compute d* = normalize(mean(novel) - mean(repeat)) per layer."""
    novel_by_layer = {l: [] for l in layers}
    repeat_by_layer = {l: [] for l in layers}

    for td in all_turn_data:
        if td["label"] == "novel":
            for l in layers:
                if l in td["hidden"]:
                    novel_by_layer[l].append(td["hidden"][l])
        elif td["label"] == "repeat":
            for l in layers:
                if l in td["hidden"]:
                    repeat_by_layer[l].append(td["hidden"][l])

    n_novel = len(novel_by_layer[layers[0]])
    n_repeat = len(repeat_by_layer[layers[0]])
    print(f"\n  Novel samples:  {n_novel}")
    print(f"  Repeat samples: {n_repeat}")

    if n_repeat == 0:
        print("  WARNING: no repeat samples — cannot compute d*")
        return None

    d_star = {}
    for l in layers:
        if not novel_by_layer[l] or not repeat_by_layer[l]:
            continue
        novel_mean = torch.stack(novel_by_layer[l]).float().mean(0)
        repeat_mean = torch.stack(repeat_by_layer[l]).float().mean(0)
        direction = novel_mean - repeat_mean
        magnitude = direction.norm().item()
        d_star[l] = direction / direction.norm()

        cos = F.cosine_similarity(novel_mean.unsqueeze(0), repeat_mean.unsqueeze(0)).item()
        print(f"  Layer {l:2d}: ||Δmean||={magnitude:.4f}  cos(novel,repeat)={cos:.4f}  "
              f"{'SEPARABLE' if cos < 0.95 else 'NOT SEPARABLE'}")

    return d_star


def analyze_per_tool(all_turn_data, layers):
    from collections import defaultdict
    tool_data = defaultdict(lambda: {"novel": [], "repeat": []})
    for td in all_turn_data:
        if td["label"] in ("novel", "repeat"):
            tool_data[td["tool_name"]][td["label"]].append(td)

    print("\n  Per-tool breakdown:")
    for tool_name, data in sorted(tool_data.items()):
        n_n = len(data["novel"])
        n_r = len(data["repeat"])
        extra = ""
        if n_r > 0 and n_n > 0:
            mid_l = layers[len(layers) // 2]
            novs = [td["hidden"][mid_l] for td in data["novel"] if mid_l in td["hidden"]]
            reps = [td["hidden"][mid_l] for td in data["repeat"] if mid_l in td["hidden"]]
            if novs and reps:
                cos = F.cosine_similarity(
                    torch.stack(novs).float().mean(0, keepdim=True),
                    torch.stack(reps).float().mean(0, keepdim=True)
                ).item()
                extra = f"  cos(layer {mid_l})={cos:.4f}"
        print(f"    {tool_name:35s}: {n_n:2d} novel, {n_r:2d} repeat{extra}")


def main():
    from hexis.adapters.cli import add_preset_args, resolve_preset_args

    ap = argparse.ArgumentParser()
    add_preset_args(ap, agentic=True, output_subpath="agentic/d_star_repeat.pt")
    # Pass tasks as a list — repeating a task = multiple trajectories
    ap.add_argument("--tasks", type=int, nargs="+",
                    default=[10, 26, 10, 26, 10, 0, 5, 11, 19])
    ap.add_argument("--max-turns", type=int, default=20)
    ap.add_argument("--save-per-sample",
                    help="Also save raw per-sample hidden states (labeled by tool) "
                         "to this path, for per-tool d* extraction")
    args = ap.parse_args()
    preset = resolve_preset_args(args)

    print("=" * 60)
    print("Extract d*_repeat: novel vs duplicate tool call direction")
    print(f"  Preset: {preset.name}")
    print(f"  Model:  {args.model}")
    print(f"  Tasks:  {args.tasks}")
    print(f"  Stride: {args.stride}")
    print(f"  Output: {args.output}")
    print("=" * 60)

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
    print(f"\n  Model: {n_layers} layers  |  Capture layers ({args.stride}-stride): {layers}")

    all_turn_data = []
    for traj_idx, task_id in enumerate(args.tasks):
        print(f"\n--- Trajectory {traj_idx+1}/{len(args.tasks)}: task {task_id} ---")
        t0 = time.time()
        turn_data = run_task_collect_states(
            task_id, model, tokenizer, device, layers,
            max_turns=args.max_turns,
        )
        elapsed = time.time() - t0
        n_n = sum(1 for td in turn_data if td["label"] == "novel")
        n_r = sum(1 for td in turn_data if td["label"] == "repeat")
        print(f"  {len(turn_data)} turns: {n_n} novel, {n_r} repeat  ({elapsed:.0f}s)")
        all_turn_data.extend(turn_data)
        gc.collect()
        torch.cuda.empty_cache()
        if torch.cuda.is_available():
            print(f"  GPU mem: {torch.cuda.memory_allocated()/1e9:.1f}GB alloc, "
                  f"{torch.cuda.memory_reserved()/1e9:.1f}GB reserved")

    print(f"\n{'='*60}")
    print("ANALYSIS")
    print(f"{'='*60}")
    analyze_per_tool(all_turn_data, layers)
    d_star = compute_d_star(all_turn_data, layers)

    if d_star is None:
        print("\nExtraction failed — no repeat samples.")
        sys.exit(1)

    n_novel_total = sum(1 for td in all_turn_data if td["label"] == "novel")
    n_repeat_total = sum(1 for td in all_turn_data if td["label"] == "repeat")
    separable = sum(
        1 for l, dv in d_star.items()
        if F.cosine_similarity(
            torch.stack([td["hidden"][l] for td in all_turn_data if td["label"] == "novel" and l in td["hidden"]]).float().mean(0, keepdim=True),
            torch.stack([td["hidden"][l] for td in all_turn_data if td["label"] == "repeat" and l in td["hidden"]]).float().mean(0, keepdim=True),
        ).item() < 0.95
    )

    print(f"\n  Separable layers: {separable}/{len(d_star)}")
    print(f"  Total novel:      {n_novel_total}")
    print(f"  Total repeat:     {n_repeat_total}")
    passed = n_repeat_total >= 15 and separable >= 3
    print(f"\n  {'PASSED' if passed else 'WARNING — low signal'}: "
          f"{'Proceed to Phase 2 validation.' if passed else 'Consider running more tasks.'}")

    out_dir = os.path.dirname(os.path.abspath(args.output))
    os.makedirs(out_dir, exist_ok=True)
    torch.save({
        "d_star": d_star,
        "n_novel": n_novel_total,
        "n_repeat": n_repeat_total,
        "separable_layers": separable,
        "tasks": args.tasks,
        "model": args.model,
        "stride": args.stride,
        "layers": layers,
    }, args.output)
    print(f"  Saved → {args.output}")

    if args.save_per_sample:
        per_sample = [
            {
                "tool_name": td["tool_name"],
                "label": td["label"],
                "turn": td["turn"],
                "sig": td["sig"],
                "hidden": td["hidden"],
            }
            for td in all_turn_data
        ]
        out_dir = os.path.dirname(os.path.abspath(args.save_per_sample))
        os.makedirs(out_dir, exist_ok=True)
        torch.save({
            "per_sample": per_sample,
            "layers": layers,
            "model": args.model,
            "tasks": args.tasks,
        }, args.save_per_sample)
        print(f"  Per-sample hiddens → {args.save_per_sample}")


if __name__ == "__main__":
    main()
