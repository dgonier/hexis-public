"""
Teacher-forced per-tool d* extraction.

Instead of running full trajectories and hoping the model naturally picks each
tool enough times, this script *teacher-forces* the tool-call prefix and
captures the hidden state at the exact position where the next token would be
the tool name. No sampling, no generation, deterministic.

Procedure:
  1. Take a tool catalog (list of OpenAI-style tool schemas).
  2. Take a small set of realistic prior contexts (system prompt + user message
     + optional prior assistant turns).
  3. For each (context, tool) pair:
       a. Build a prompt ending in the assistant opener + think block +
          "<function=" prefix.
       b. Run a single forward pass up to that position (no generate).
       c. Capture the hidden state at the last token across stride-6 layers.
  4. For each tool: d*_t = normalize(mean(states emitting t) - mean(pooled others)).
  5. Save {tool_name: {layer: unit_vector}} to checkpoints/d_star_tools_tf.pt.

This is the production-ready primitive that the FastAPI `/v1/register_tools`
endpoint (see docs/hexis_vllm_capabilities.md) calls under the hood.

Usage:
    python scripts/extract_d_star_tools_teacher_forced.py \\
        --model Qwen/Qwen3.5-4B \\
        --n-contexts 20 \\
        --output checkpoints/d_star_tools_tf.pt
"""

import argparse
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "tau-bench"))

import torch
import torch.nn.functional as F
from transformers import AutoModelForCausalLM, AutoTokenizer

from tau_bench.envs.airline.tools import ALL_TOOLS
from tau_bench.envs.airline.wiki import WIKI


# ── Prior contexts: small set of realistic tau-bench-shaped openers ─────
# Each context is a list of messages. The final assistant emission is what
# we're probing — we'll append the opener and the "<function=" prefix, then
# capture the hidden state at the last position.

PRIOR_CONTEXTS = [
    # Fresh start — just a user opener
    [{"role": "user", "content": "Hi, I need help managing my reservation."}],
    [{"role": "user", "content": "I'd like to check the details of my booking."}],
    [{"role": "user", "content": "Can you help me cancel a flight?"}],
    [{"role": "user", "content": "I need to update my reservation to add baggage."}],
    [{"role": "user", "content": "What flights are available from JFK to LAX next week?"}],
    [{"role": "user", "content": "I want to change the passengers on my reservation."}],
    [{"role": "user", "content": "Can you look up my account?"}],
    [{"role": "user", "content": "I have a reservation with confirmation code ABC123 and want to modify it."}],
    # With prior user-details lookup already done
    [
        {"role": "user", "content": "My user id is user_123. I want to update my reservation."},
        {"role": "assistant", "content": "<function=get_user_details>\n<parameter=user_id>user_123</parameter>\n</function>"},
        {"role": "tool", "name": "get_user_details", "content": '{"user_id": "user_123", "email": "a@b.com", "membership": "gold", "reservations": ["res_1"]}'},
    ],
    # With prior reservation-details lookup
    [
        {"role": "user", "content": "Please cancel reservation res_1 for user user_123."},
        {"role": "assistant", "content": "<function=get_reservation_details>\n<parameter=reservation_id>res_1</parameter>\n</function>"},
        {"role": "tool", "name": "get_reservation_details", "content": '{"reservation_id": "res_1", "user_id": "user_123", "flights": [{"origin": "JFK", "destination": "LAX"}], "status": "active"}'},
    ],
    # With prior search
    [
        {"role": "user", "content": "I want to book a direct flight from SFO to ORD on 2024-05-01."},
        {"role": "assistant", "content": "<function=search_direct_flight>\n<parameter=origin>SFO</parameter>\n<parameter=destination>ORD</parameter>\n<parameter=date>2024-05-01</parameter>\n</function>"},
        {"role": "tool", "name": "search_direct_flight", "content": '{"flights": [{"flight_number": "UA123", "price": 350}, {"flight_number": "AA456", "price": 410}]}'},
    ],
    # Mid-trajectory with multiple observations
    [
        {"role": "user", "content": "I want to change my flight on reservation res_2."},
        {"role": "assistant", "content": "<function=get_reservation_details>\n<parameter=reservation_id>res_2</parameter>\n</function>"},
        {"role": "tool", "name": "get_reservation_details", "content": '{"reservation_id": "res_2", "flights": [{"origin": "BOS", "destination": "DEN"}]}'},
        {"role": "assistant", "content": "<function=search_direct_flight>\n<parameter=origin>BOS</parameter>\n<parameter=destination>DEN</parameter>\n<parameter=date>2024-06-15</parameter>\n</function>"},
        {"role": "tool", "name": "search_direct_flight", "content": '{"flights": [{"flight_number": "DL789", "price": 275}]}'},
    ],
    # Complaint / baggage context
    [{"role": "user", "content": "I need to add 2 bags to my reservation res_3."}],
    [{"role": "user", "content": "The flight I booked got canceled, can you help me rebook?"}],
    [{"role": "user", "content": "I want to know how much my reservation would cost if I added more baggage."}],
    # Think-friendly
    [{"role": "user", "content": "I have a complicated situation with multiple reservations. Where should we start?"}],
    [{"role": "user", "content": "What are all the airports you service?"}],
    [{"role": "user", "content": "I want to escalate to a human agent."}],
    [{"role": "user", "content": "Can you calculate the total cost for 3 passengers with 2 bags each?"}],
    [{"role": "user", "content": "Send me a $150 travel certificate."}],
]


def build_teacher_forced_prompt(tokenizer, messages, tools_info, tool_name):
    """Build a prompt ending exactly where the model would emit the tool name.

    The Qwen3.5 + tau-bench tool-call format is `<function=NAME>...</function>`.
    We want the hidden state at the position where NAME is about to be emitted,
    so we append the assistant opener (with pre-seeded think block) plus the
    literal `<function=` prefix plus the tool name itself — capturing the
    hidden state at the last token of the tool name gives us the "about to
    finish emitting this tool name, about to generate args" state.
    """
    # Render the chat template with add_generation_prompt=True to get the
    # assistant-turn opener + think block.
    kwargs = dict(tokenize=False, add_generation_prompt=True)
    if tools_info:
        kwargs["tools"] = tools_info
    try:
        kwargs["enable_thinking"] = False
        prompt = tokenizer.apply_chat_template(messages, **kwargs)
    except Exception:
        del kwargs["enable_thinking"]
        prompt = tokenizer.apply_chat_template(messages, **kwargs)

    # The template typically ends with the think block already.
    # Append the tool-call prefix and the tool name.
    prompt += f"<function={tool_name}"
    return prompt


def capture_last_hidden_state(model, tokenizer, prompt, layers, device):
    """Run one forward pass, capture hidden state at the last token for each
    requested layer. Returns {layer_idx: tensor(d_model,)} as float16 CPU tensors.
    """
    captured = {}
    handles = []

    for layer_idx in layers:
        def make_hook(li):
            def hook(module, input, output):
                if isinstance(input, tuple) and len(input) > 0:
                    h = input[0]
                    captured[li] = h[0, -1, :].detach().to(torch.float16).cpu()
            return hook
        h = model.model.layers[layer_idx].register_forward_hook(make_hook(layer_idx))
        handles.append(h)

    try:
        input_ids = tokenizer(
            prompt, return_tensors="pt", truncation=True, max_length=8192,
        ).input_ids.to(device)
        with torch.no_grad():
            model(input_ids, use_cache=False)
    finally:
        for h in handles:
            h.remove()

    return captured


def compute_per_tool_directions(samples_by_tool, layers):
    """d*_t = normalize(mean(samples[t]) - mean(pooled samples from all other tools)), per layer."""
    d_star = {}
    separability = {}

    for tool_name, per_layer in samples_by_tool.items():
        d_star[tool_name] = {}
        separability[tool_name] = {}
        for l in layers:
            if l not in per_layer or not per_layer[l]:
                continue
            tool_stack = torch.stack(per_layer[l]).float()
            tool_mean = tool_stack.mean(0)

            rest = []
            for other_name, other_per_layer in samples_by_tool.items():
                if other_name == tool_name:
                    continue
                if l in other_per_layer and other_per_layer[l]:
                    rest.append(torch.stack(other_per_layer[l]).float())
            if not rest:
                continue
            rest_mean = torch.cat(rest, dim=0).mean(0)

            direction = tool_mean - rest_mean
            if direction.norm().item() < 1e-6:
                continue
            d_star[tool_name][l] = direction / direction.norm()

            cos = F.cosine_similarity(
                tool_mean.unsqueeze(0), rest_mean.unsqueeze(0)
            ).item()
            separability[tool_name][l] = cos

    return d_star, separability


def main():
    from hexis.adapters.cli import add_preset_args, resolve_preset_args

    ap = argparse.ArgumentParser()
    add_preset_args(ap, agentic=True, output_subpath="agentic/d_star_tools_tf.pt")
    ap.add_argument("--n-contexts", type=int, default=len(PRIOR_CONTEXTS),
                    help="Number of prior contexts to cycle through per tool")
    ap.add_argument("--tools", nargs="+", default=None,
                    help="Subset of tool names to extract (default: all in catalog)")
    ap.add_argument("--max-length", type=int, default=8192)
    args = ap.parse_args()
    preset = resolve_preset_args(args)

    print("=" * 60)
    print("Teacher-forced d*_tool extraction")
    print(f"  Preset:    {preset.name}")
    print(f"  Model:     {args.model}")
    print(f"  Contexts:  {args.n_contexts}")
    print(f"  Output:    {args.output}")
    print("=" * 60)

    # Tool catalog
    tools_info = [t.get_info() for t in ALL_TOOLS]
    all_tool_names = [t["function"]["name"] for t in tools_info]
    if args.tools:
        target_tools = [t for t in args.tools if t in all_tool_names]
        missing = set(args.tools) - set(all_tool_names)
        if missing:
            print(f"  WARNING: unknown tools ignored: {sorted(missing)}")
    else:
        target_tools = all_tool_names
    print(f"  Target tools ({len(target_tools)}): {target_tools}")

    # Load model
    print(f"\nLoading {args.model}...")
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
    device = next(model.parameters()).device

    n_layers = model.config.num_hidden_layers
    layers = list(range(0, n_layers, args.stride))
    print(f"  Model: {n_layers} layers | capture layers: {layers}")
    print(f"  Ready.")

    # System prompt: tau-bench WIKI + tool catalog
    system_msg = {"role": "system", "content": WIKI}

    # Contexts to cycle
    contexts = PRIOR_CONTEXTS[: args.n_contexts]
    total_samples = len(target_tools) * len(contexts)
    print(f"\nExtracting {len(target_tools)} tools x {len(contexts)} contexts = "
          f"{total_samples} samples...")

    samples_by_tool = {t: {l: [] for l in layers} for t in target_tools}

    t0 = time.time()
    sample_idx = 0

    for tool_name in target_tools:
        for ctx in contexts:
            messages = [system_msg] + ctx
            prompt = build_teacher_forced_prompt(tokenizer, messages, tools_info, tool_name)

            hidden = capture_last_hidden_state(model, tokenizer, prompt, layers, device)
            for l, h in hidden.items():
                samples_by_tool[tool_name][l].append(h)

            sample_idx += 1
            if sample_idx % 20 == 0 or sample_idx == total_samples:
                elapsed = time.time() - t0
                rate = sample_idx / elapsed if elapsed > 0 else 0
                eta = (total_samples - sample_idx) / rate if rate > 0 else 0
                print(f"  [{sample_idx}/{total_samples}] elapsed={elapsed:.0f}s "
                      f"rate={rate:.1f}/s eta={eta:.0f}s")

    wall = time.time() - t0
    print(f"\n  Extraction wall: {wall:.1f}s ({total_samples/wall:.1f} samples/s)")

    # Compute per-tool directions
    print("\nComputing per-tool directions...")
    d_star, separability = compute_per_tool_directions(samples_by_tool, layers)

    # Print separability table
    print(f"\n  {'tool':<35s} " + "  ".join(f"L{l:02d}" for l in layers))
    for tn in target_tools:
        if tn not in separability:
            print(f"  {tn:<35s}  (no samples)")
            continue
        cos_strs = []
        for l in layers:
            if l in separability[tn]:
                cos_strs.append(f"{separability[tn][l]:+.2f}")
            else:
                cos_strs.append("  - ")
        flag = " *" if any(
            separability[tn].get(l, 1.0) < 0.95 for l in layers
        ) else ""
        print(f"  {tn:<35s}  " + "  ".join(f"{s:>5s}" for s in cos_strs) + flag)
    print("  (* = separable at ≥1 layer with cos < 0.95)")

    n_separable = sum(
        1 for tn in d_star
        if any(separability.get(tn, {}).get(l, 1.0) < 0.95 for l in layers)
    )
    print(f"\n  Tools with ≥1 separable layer: {n_separable}/{len(target_tools)}")

    # Save
    out_dir = os.path.dirname(os.path.abspath(args.output))
    os.makedirs(out_dir, exist_ok=True)
    torch.save({
        "d_star_tools": d_star,
        "layers": layers,
        "model": args.model,
        "n_contexts": len(contexts),
        "target_tools": target_tools,
        "separability": separability,
        "extraction_method": "teacher_forced",
        "extraction_wall_s": wall,
    }, args.output)
    print(f"\n  Saved → {args.output}")
    print(f"  Total tools: {len(d_star)}")
    print(f"  Wall: {wall:.1f}s")


if __name__ == "__main__":
    main()
