"""
d*_tool extraction v2: two prefill variants + per-sample dump + category analysis.

Two extraction variants, run from the same script in one pass so they share the
model load. Both produce a per-sample hidden-state dump; compute_d_star_tools_v2.py
consumes those dumps to compute per-tool directions (one-vs-rest) and
category+within-category hierarchical directions.

Variant 1 — prefill_full:
  The assistant turn contains the entire tool call text as prefilled tokens:
    <|im_start|>assistant\\n<think>\\n\\n</think>\\n\\n<function=TOOL>\\n
    <parameter=k>v</parameter>\\n</function>

  Forward pass, capture hidden states at every layer. Two capture points per sample:
    (a) "name_end"   — hidden state at the last token of the tool name
                       (right before the '>' that closes the function tag)
    (b) "call_mean"  — mean-pool of hidden states over the span from the
                       token after "<function=" through the final "</function>"

Variant 2 — user_instruction:
  The last user message explicitly names a tool to call:
    role=user content="Call TOOL now with arguments: k=v, k2=v2."
  The prompt ends right after that user message, with the assistant opener +
  empty think block but NO <function= prefill. Capture at the **last token of
  the user message** — which is the same position across all tools (just
  before <|im_end|>).

  This gives a tool-agnostic capture position where the only thing that varies
  across samples is what the user literally said.

Both variants save per-sample dumps:
  checkpoints/d_star_tools_v2/v1_samples.pt
  checkpoints/d_star_tools_v2/v2_samples.pt

Format of a samples file:
  {
    "model": "Qwen/Qwen3.5-4B",
    "layers": [0, 6, 12, 18, 24, 30],
    "variant": "prefill_full" | "user_instruction",
    "capture_name": "name_end" | "call_mean" | "user_end",
    "samples": [
      {
        "tool": "book_reservation",
        "context_id": "book_1",
        "hidden": {layer_idx: fp16_tensor(d_model,)},
      },
      ...
    ],
  }

Usage:
    python scripts/extract_d_star_tools_v2.py \\
        --model Qwen/Qwen3.5-4B \\
        --output-dir checkpoints/d_star_tools_v2 \\
        --variants prefill_full user_instruction
"""
import argparse
import os
import sys
import time
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "tau-bench"))

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

from tau_bench.envs.airline.tools import ALL_TOOLS
from tau_bench.envs.airline.wiki import WIKI


# ---------------------------------------------------------------------------
# Per-tool parameter examples — realistic values, same across contexts
# ---------------------------------------------------------------------------

TOOL_EXAMPLE_PARAMS = {
    "book_reservation": [
        ("user_id", "sophia_torres_8432"),
        ("origin", "JFK"),
        ("destination", "LAX"),
    ],
    "calculate": [
        ("expression", "2 * 450 + 100"),
    ],
    "cancel_reservation": [
        ("reservation_id", "H3N9QK"),
    ],
    "get_reservation_details": [
        ("reservation_id", "H3N9QK"),
    ],
    "get_user_details": [
        ("user_id", "sophia_torres_8432"),
    ],
    "list_all_airports": [],
    "search_direct_flight": [
        ("origin", "SFO"),
        ("destination", "ORD"),
        ("date", "2024-05-01"),
    ],
    "search_onestop_flight": [
        ("origin", "BOS"),
        ("destination", "SEA"),
        ("date", "2024-05-01"),
    ],
    "send_certificate": [
        ("user_id", "sophia_torres_8432"),
        ("amount", "150"),
    ],
    "think": [
        ("thought", "I should verify the reservation before making changes."),
    ],
    "transfer_to_human_agents": [
        ("summary", "Complex multi-leg reservation modification required."),
    ],
    "update_reservation_baggages": [
        ("reservation_id", "H3N9QK"),
        ("total_baggages", "3"),
    ],
    "update_reservation_flights": [
        ("reservation_id", "H3N9QK"),
        ("cabin", "business"),
    ],
    "update_reservation_passengers": [
        ("reservation_id", "H3N9QK"),
        ("passengers", "[{\"first_name\":\"Sophia\",\"last_name\":\"Torres\",\"dob\":\"1990-03-14\"}]"),
    ],
}


# ---------------------------------------------------------------------------
# 20 prior contexts for Variant 1 — generic airline scenarios that could lead
# to any tool call. Since Variant 1 prefills the tool call explicitly, the
# prior context just needs to be plausible for the resulting call to fit.
# ---------------------------------------------------------------------------

GENERIC_PRIORS = [
    [{"role": "user", "content": "Hi, I need help with my reservation."}],
    [{"role": "user", "content": "I'd like to check on a booking I made last week."}],
    [{"role": "user", "content": "Can you help me with a flight change?"}],
    [{"role": "user", "content": "I need to modify my reservation to add baggage."}],
    [{"role": "user", "content": "What flights are available from my home airport next week?"}],
    [{"role": "user", "content": "I want to update the passengers on my reservation."}],
    [{"role": "user", "content": "Can you pull up my account please?"}],
    [{"role": "user", "content": "I have a reservation and want to make changes."}],
    [
        {"role": "user", "content": "My user id is sophia_torres_8432. I want to update my reservation."},
        {"role": "assistant", "content": "<function=get_user_details>\n<parameter=user_id>sophia_torres_8432</parameter>\n</function>"},
        {"role": "tool", "name": "get_user_details", "content": '{"user_id": "sophia_torres_8432", "membership": "gold", "reservations": ["H3N9QK"]}'},
    ],
    [
        {"role": "user", "content": "Please help with reservation H3N9QK for user sophia_torres_8432."},
        {"role": "assistant", "content": "<function=get_reservation_details>\n<parameter=reservation_id>H3N9QK</parameter>\n</function>"},
        {"role": "tool", "name": "get_reservation_details", "content": '{"reservation_id": "H3N9QK", "user_id": "sophia_torres_8432", "flights": [{"origin": "JFK", "destination": "LAX"}], "status": "active"}'},
    ],
    [
        {"role": "user", "content": "I want to book a direct flight from SFO to ORD on 2024-05-01."},
        {"role": "assistant", "content": "<function=search_direct_flight>\n<parameter=origin>SFO</parameter>\n<parameter=destination>ORD</parameter>\n<parameter=date>2024-05-01</parameter>\n</function>"},
        {"role": "tool", "name": "search_direct_flight", "content": '{"flights": [{"flight_number": "UA123", "price": 350}, {"flight_number": "AA456", "price": 410}]}'},
    ],
    [
        {"role": "user", "content": "I want to change my flight on reservation H3N9QK."},
        {"role": "assistant", "content": "<function=get_reservation_details>\n<parameter=reservation_id>H3N9QK</parameter>\n</function>"},
        {"role": "tool", "name": "get_reservation_details", "content": '{"reservation_id": "H3N9QK", "flights": [{"origin": "BOS", "destination": "DEN"}]}'},
        {"role": "assistant", "content": "<function=search_direct_flight>\n<parameter=origin>BOS</parameter>\n<parameter=destination>DEN</parameter>\n<parameter=date>2024-06-15</parameter>\n</function>"},
        {"role": "tool", "name": "search_direct_flight", "content": '{"flights": [{"flight_number": "DL789", "price": 275}]}'},
    ],
    [{"role": "user", "content": "I need to add 2 bags to my reservation H3N9QK."}],
    [{"role": "user", "content": "The flight I booked got canceled, can you help me rebook?"}],
    [{"role": "user", "content": "I want to know how much my reservation would cost with more baggage."}],
    [{"role": "user", "content": "I have a complicated situation with multiple reservations. Where should we start?"}],
    [{"role": "user", "content": "What airports does your airline serve?"}],
    [{"role": "user", "content": "I want to escalate this to a human agent."}],
    [{"role": "user", "content": "Can you calculate the total cost for 3 passengers with 2 bags each?"}],
    [{"role": "user", "content": "Send me a $150 travel certificate for the inconvenience."}],
]


def build_tool_call_text(tool_name: str) -> str:
    """Render a <function=TOOL>...</function> block with example parameters."""
    params = TOOL_EXAMPLE_PARAMS.get(tool_name, [])
    param_lines = [f"<parameter={k}>{v}</parameter>" for k, v in params]
    body = "\n".join(param_lines)
    if body:
        return f"<function={tool_name}>\n{body}\n</function>"
    return f"<function={tool_name}>\n</function>"


def format_params_inline(tool_name: str) -> str:
    """For Variant 2: format the tool's parameters as "k=v, k=v"."""
    params = TOOL_EXAMPLE_PARAMS.get(tool_name, [])
    if not params:
        return ""
    return ", ".join(f"{k}={v}" for k, v in params)


def build_variant1_prompt(tokenizer, prior_context, tools_info, tool_name):
    """Variant 1: full tool call is prefilled in the assistant turn."""
    messages = [{"role": "system", "content": WIKI}] + prior_context
    kwargs = dict(tokenize=False, add_generation_prompt=False)
    if tools_info:
        kwargs["tools"] = tools_info
    try:
        kwargs["enable_thinking"] = False
        base = tokenizer.apply_chat_template(messages, **kwargs)
    except Exception:
        del kwargs["enable_thinking"]
        base = tokenizer.apply_chat_template(messages, **kwargs)

    tool_call = build_tool_call_text(tool_name)
    # Full prefill: assistant turn opens, empty think block, then the full tool call,
    # then close the assistant turn. No generation.
    return (
        base
        + "<|im_start|>assistant\n<think>\n\n</think>\n\n"
        + tool_call
        + "<|im_end|>\n"
    )


def build_variant2_prompt(tokenizer, tools_info, tool_name):
    """Variant 2: user explicitly names the tool + params, nothing from assistant yet."""
    param_str = format_params_inline(tool_name)
    if param_str:
        user_msg = f"Call {tool_name} now with arguments: {param_str}."
    else:
        user_msg = f"Call {tool_name} now."

    messages = [
        {"role": "system", "content": WIKI},
        {"role": "user", "content": user_msg},
    ]
    kwargs = dict(tokenize=False, add_generation_prompt=False)
    if tools_info:
        kwargs["tools"] = tools_info
    try:
        kwargs["enable_thinking"] = False
        base = tokenizer.apply_chat_template(messages, **kwargs)
    except Exception:
        del kwargs["enable_thinking"]
        base = tokenizer.apply_chat_template(messages, **kwargs)
    # Capture at the last token of the rendered user message, before the
    # assistant opener. The chat template already terminates the user turn
    # with "<|im_end|>\n" so the last token of base is that im_end.
    return base


def find_tool_call_span(tokenizer, prompt_ids, tool_name):
    """Given a tokenized Variant 1 prompt, find (start, end) indices (exclusive end)
    of the tool call span. Start = first token after `<function=`, end = last token
    of `</function>`.

    Returns (start_idx, end_idx, name_end_idx) or None if span can't be located.
    name_end_idx is the last token of the tool name (right before '>').
    """
    # Decode one-token-at-a-time to find the span markers robustly.
    # We look for the subsequence matching "<function=TOOL>" and "</function>".
    text = tokenizer.decode(prompt_ids, skip_special_tokens=False)
    marker_open = f"<function={tool_name}>"
    marker_close = "</function>"

    open_char = text.rfind(marker_open)
    close_char = text.rfind(marker_close)
    if open_char == -1 or close_char == -1 or close_char < open_char:
        return None

    # Convert character positions to token positions by decoding incrementally.
    # We need token indices such that decoding prompt_ids[:i] ends near our markers.
    char_count = 0
    token_at_char = [0] * (len(text) + 1)
    cursor = 0
    for ti, tok_id in enumerate(prompt_ids):
        dec = tokenizer.decode([tok_id], skip_special_tokens=False)
        for ch_offset in range(len(dec)):
            if cursor + ch_offset < len(token_at_char):
                token_at_char[cursor + ch_offset] = ti
        cursor += len(dec)
    # cursor now ~= len(text); fill any trailing
    for i in range(cursor, len(token_at_char)):
        token_at_char[i] = len(prompt_ids) - 1

    # Start of the tool call span: first token whose character start is after
    # the "=" in "<function=TOOL>"
    equals_pos = open_char + len("<function=")
    name_last_char = open_char + len(marker_open) - 2  # position of last char of TOOL
    close_last_char = close_char + len(marker_close) - 1

    start_tok = token_at_char[equals_pos]
    name_end_tok = token_at_char[name_last_char]
    end_tok = token_at_char[close_last_char] + 1  # exclusive

    return start_tok, end_tok, name_end_tok


# ---------------------------------------------------------------------------
# Hidden state capture
# ---------------------------------------------------------------------------


def capture_positions(model, input_ids, layers, positions):
    """Run one forward pass, capture hidden states at each requested
    (position_name -> token_index) at each requested layer.

    Returns {position_name: {layer_idx: tensor(d_model,)}}.
    """
    out = {name: {} for name in positions}
    handles = []

    def make_hook(li):
        def hook(module, input, output):
            if isinstance(input, tuple) and len(input) > 0:
                h = input[0]
                # h is (batch, seq, d_model)
                for name, idx_or_range in positions.items():
                    if isinstance(idx_or_range, int):
                        # single token
                        vec = h[0, idx_or_range, :].detach().to(torch.float16).cpu()
                    else:
                        start, end = idx_or_range
                        # mean-pool over [start, end)
                        vec = h[0, start:end, :].detach().float().mean(0).to(torch.float16).cpu()
                    out[name][li] = vec
        return hook

    for li in layers:
        handles.append(model.model.layers[li].register_forward_hook(make_hook(li)))

    try:
        with torch.no_grad():
            model(input_ids, use_cache=False)
    finally:
        for h in handles:
            h.remove()

    return out


# ---------------------------------------------------------------------------
# Variant runners
# ---------------------------------------------------------------------------


def run_variant1(model, tokenizer, device, layers, tools_info, tool_names, priors, log):
    """Variant 1: prefill full tool call, capture at name-end and call-mean."""
    name_end_samples = []
    call_mean_samples = []
    total = len(tool_names) * len(priors)
    done = 0
    t0 = time.time()

    for tool_name in tool_names:
        for ci, prior in enumerate(priors):
            prompt = build_variant1_prompt(tokenizer, prior, tools_info, tool_name)
            ids = tokenizer(
                prompt, return_tensors="pt", truncation=True, max_length=8192,
            ).input_ids

            span = find_tool_call_span(tokenizer, ids[0].tolist(), tool_name)
            if span is None:
                log(f"  WARN could not locate span for {tool_name} ctx={ci}; skip")
                continue
            start_tok, end_tok, name_end_tok = span

            ids = ids.to(device)
            positions = {
                "name_end": name_end_tok,
                "call_mean": (start_tok, end_tok),
            }
            captured = capture_positions(model, ids, layers, positions)

            name_end_samples.append({
                "tool": tool_name,
                "context_id": f"ctx{ci}",
                "hidden": captured["name_end"],
            })
            call_mean_samples.append({
                "tool": tool_name,
                "context_id": f"ctx{ci}",
                "hidden": captured["call_mean"],
            })
            done += 1
            if done % 20 == 0 or done == total:
                elapsed = time.time() - t0
                rate = done / elapsed if elapsed > 0 else 0
                eta = (total - done) / rate if rate > 0 else 0
                log(f"  [v1 {done}/{total}] elapsed={elapsed:.0f}s rate={rate:.1f}/s eta={eta:.0f}s")
    return name_end_samples, call_mean_samples


def run_variant2(model, tokenizer, device, layers, tools_info, tool_names, priors, log):
    """Variant 2: user instruction with explicit tool name, capture at last user token."""
    samples = []
    total = len(tool_names) * len(priors)
    done = 0
    t0 = time.time()

    # For Variant 2 the prior context is irrelevant — the user message IS the context.
    # We still iterate `priors` times to get `len(priors)` samples per tool, but each
    # sample uses the same Variant 2 prompt per tool (no variation). This gives
    # exactly one sample per (tool, context_id) slot; they will collapse to one point
    # in hidden-state space. That's expected: Variant 2 checks whether a single
    # well-defined decision-point state is separable between tools, not whether
    # it varies within a tool.
    for tool_name in tool_names:
        for ci in range(len(priors)):
            prompt = build_variant2_prompt(tokenizer, tools_info, tool_name)
            ids = tokenizer(
                prompt, return_tensors="pt", truncation=True, max_length=8192,
            ).input_ids.to(device)

            last_idx = ids.shape[1] - 1
            captured = capture_positions(
                model, ids, layers, {"user_end": last_idx}
            )
            samples.append({
                "tool": tool_name,
                "context_id": f"ctx{ci}",
                "hidden": captured["user_end"],
            })
            done += 1
            if done % 20 == 0 or done == total:
                elapsed = time.time() - t0
                rate = done / elapsed if elapsed > 0 else 0
                eta = (total - done) / rate if rate > 0 else 0
                log(f"  [v2 {done}/{total}] elapsed={elapsed:.0f}s rate={rate:.1f}/s eta={eta:.0f}s")
    return samples


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main():
    from hexis.adapters.cli import add_preset_args, resolve_preset_args

    ap = argparse.ArgumentParser()
    # Uses --output-dir (plural); doesn't match add_preset_args' --output
    # suffix pattern. Add preset args without output handling, then use
    # preset.checkpoint_base as default for --output-dir.
    add_preset_args(ap, agentic=True, output_subpath=None)
    ap.add_argument("--output-dir", default=None,
                    help="Default: <preset.checkpoint_base>/agentic/d_star_tools_v2")
    ap.add_argument("--variants", nargs="+",
                    default=["prefill_full", "user_instruction"],
                    choices=["prefill_full", "user_instruction"])
    args = ap.parse_args()
    preset = resolve_preset_args(args)
    if args.output_dir is None:
        args.output_dir = f"{preset.checkpoint_base}/agentic/d_star_tools_v2"

    print("=" * 60)
    print("d*_tool v2 extraction")
    print(f"  Preset:   {preset.name}")
    print(f"  Model:    {args.model}")
    print(f"  Variants: {args.variants}")
    print(f"  Output:   {args.output_dir}")
    print("=" * 60)

    os.makedirs(args.output_dir, exist_ok=True)
    def log(msg): print(msg)

    # --- Load model
    log(f"\nLoading {args.model}...")
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
    log(f"  Model: {n_layers} layers | capture layers: {layers}")

    # --- Tool catalog
    tools_info = [t.get_info() for t in ALL_TOOLS]
    tool_names = [t["function"]["name"] for t in tools_info]
    log(f"  Catalog: {len(tool_names)} tools")
    priors = GENERIC_PRIORS
    log(f"  Priors:  {len(priors)} contexts")

    # --- Variant 1
    if "prefill_full" in args.variants:
        log("\n[Variant 1] prefill_full — capture at name_end and call_mean")
        name_end_samples, call_mean_samples = run_variant1(
            model, tokenizer, device, layers, tools_info, tool_names, priors, log,
        )
        torch.save({
            "model": args.model, "layers": layers,
            "variant": "prefill_full", "capture_name": "name_end",
            "samples": name_end_samples,
        }, os.path.join(args.output_dir, "v1_name_end_samples.pt"))
        torch.save({
            "model": args.model, "layers": layers,
            "variant": "prefill_full", "capture_name": "call_mean",
            "samples": call_mean_samples,
        }, os.path.join(args.output_dir, "v1_call_mean_samples.pt"))
        log(f"  saved {len(name_end_samples)} name_end + {len(call_mean_samples)} call_mean samples")

    # --- Variant 2
    if "user_instruction" in args.variants:
        log("\n[Variant 2] user_instruction — capture at last user-msg token")
        v2_samples = run_variant2(
            model, tokenizer, device, layers, tools_info, tool_names, priors, log,
        )
        torch.save({
            "model": args.model, "layers": layers,
            "variant": "user_instruction", "capture_name": "user_end",
            "samples": v2_samples,
        }, os.path.join(args.output_dir, "v2_user_end_samples.pt"))
        log(f"  saved {len(v2_samples)} user_end samples")

    log("\nDone.")


if __name__ == "__main__":
    main()
