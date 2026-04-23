"""
d*_tool v2 extraction — varied parameter edition.

Fixes the parameter-contamination bug in extract_d_star_tools_v2.py: the
original used one hardcoded parameter set per tool, ran 20 identical forward
passes, and called that "averaging". This version produces 20 *genuinely
different* parameter sets per tool by drawing from realistic pools, so the
mean across samples actually averages out argument-specific features and
leaves tool-identity signal.

Variant 2 only: prompt is "Call TOOL with arguments: k=v, k=v", capture at
the last user-message token. Variant 1 (full prefill) could be added the
same way if we wanted, but V2 is the one that matters for routing-driven
injection — and V2 was proven cleanest in the earlier separability analysis.

Output:
    checkpoints/d_star_tools_v2_varied/v2_user_end_samples.pt
        — per-sample hidden states, labeled by tool
    Plus the same compute_d_star_tools_v2.py analysis script can read it.

Usage:
    python scripts/extract_d_star_tools_v2_varied.py \\
        --output-dir checkpoints/d_star_tools_v2_varied \\
        --n-variants 20
"""
import argparse
import os
import random
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "tau-bench"))

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

from tau_bench.envs.airline.tools import ALL_TOOLS
from tau_bench.envs.airline.wiki import WIKI


# ---------------------------------------------------------------------------
# Realistic pools for varied parameter generation
# ---------------------------------------------------------------------------


USER_IDS = [
    "sophia_torres_8432", "michael_chen_1024", "aisha_patel_5573",
    "james_wong_9921", "olivia_nguyen_2201", "ethan_brown_7348",
    "mia_rodriguez_3067", "noah_kim_6189", "ava_jackson_4502",
    "liam_davis_9813", "emma_garcia_1456", "lucas_martinez_8970",
    "isabella_lopez_6423", "mason_anderson_2857", "charlotte_lee_7134",
    "benjamin_hall_3609", "amelia_young_5728", "william_walker_8346",
    "harper_allen_1985", "elijah_wright_6072",
]

RESERVATION_CODES = [
    "H3N9QK", "BZ7R2M", "PL4X8K", "N9Q1WC", "M5F8JT",
    "V2K7RD", "C4L1SN", "X8B3WY", "G6T2FH", "R1Z9DP",
    "K7M4VB", "J2N8LQ", "F5X1CT", "Q9W6HR", "T3P7NK",
    "D8Y2BM", "W4G6JS", "L1R5FX", "B9C3MZ", "S7H2QP",
]

AIRPORTS = [
    "JFK", "LAX", "SFO", "ORD", "BOS", "DEN", "SEA", "MIA",
    "ATL", "DFW", "EWR", "LGA", "PHX", "IAH", "MCO",
]

DATES = [
    "2024-03-15", "2024-04-02", "2024-04-22", "2024-05-01",
    "2024-05-14", "2024-06-05", "2024-06-18", "2024-06-30",
    "2024-07-09", "2024-07-23", "2024-08-04", "2024-08-17",
    "2024-09-01", "2024-09-15", "2024-09-28", "2024-10-11",
    "2024-10-24", "2024-11-06", "2024-11-19", "2024-12-02",
]

CABINS = ["basic_economy", "economy", "business"]

PASSENGER_COUNTS = [1, 2, 3, 4]
BAGGAGE_COUNTS = [0, 1, 2, 3, 4]

CERTIFICATE_AMOUNTS = [50, 100, 150, 200, 250, 300, 500]

THINK_THOUGHTS = [
    "I should verify the reservation before making changes.",
    "Let me check whether this modification is allowed under the user's fare class.",
    "I need to confirm the user's identity before proceeding with any mutation.",
    "The customer's request is complex — let me plan the next step carefully.",
    "I should calculate the refund amount before confirming the cancellation.",
    "Let me review the cancellation policy for this ticket type.",
    "I need to gather more information before I can help with this request.",
    "The user has multiple reservations — I should clarify which one to modify.",
    "Let me check whether this user has travel insurance.",
    "I should verify the flight availability before suggesting alternatives.",
    "Let me consider whether a partial refund is appropriate here.",
    "I need to check the baggage allowance for the current fare class.",
    "The user's request spans multiple flights — I should handle them one at a time.",
    "Let me confirm the destination airport before searching.",
    "I should check if the user qualifies for an upgrade.",
    "Let me verify the requested date is within the allowed change window.",
    "I need to think about whether this cancellation requires manager approval.",
    "Let me check if the new flight has seats in the requested cabin class.",
    "I should confirm the passenger names before adding them to the reservation.",
    "Let me review the airline's rebooking policy for this situation.",
]

HUMAN_TRANSFER_SUMMARIES = [
    "Complex multi-leg reservation modification required.",
    "User disputing charge not covered by standard policy.",
    "Account access issue preventing agent from verifying user.",
    "Refund amount exceeds agent authorization limit.",
    "Request involves non-standard route changes.",
    "User has accessibility accommodation needs beyond standard tools.",
    "Medical emergency rebooking requiring special handling.",
    "Possible identity fraud on the account.",
    "Complex partial refund calculation outside agent scope.",
    "User requesting corporate contract adjustment.",
    "Multiple concurrent reservation issues requiring supervisor.",
    "Legal hold on account prevents standard operations.",
    "Bereavement fare change requiring documentation review.",
    "User has conflicting information on file needing verification.",
    "Pet travel logistics beyond agent authority.",
    "Bulk group booking modification not supported by self-service.",
    "User requesting exception to no-refund policy.",
    "Visa documentation issue affecting rebooking.",
    "Unusual compensation request requiring manager review.",
    "Escalation for unresolved issue from multiple prior calls.",
]

CALCULATE_EXPRESSIONS = [
    "2 * 450 + 100",
    "3 * 275 - 75",
    "125 + 89 + 45",
    "450 * 0.85",
    "(120 + 35) * 2",
    "890 - 150 - 75",
    "4 * 200 + 50",
    "600 * 0.9 + 40",
    "350 + 125 * 2",
    "1200 * 0.75",
    "2 * (180 + 55)",
    "789 - 234",
    "550 * 0.95 + 30",
    "3 * 250 - 100",
    "420 + 175 + 60",
    "1000 * 0.88",
    "(95 + 40) * 3",
    "675 - 125 + 50",
    "2 * 380 + 85",
    "825 * 0.92",
]


def build_variants(tool_name: str, n: int, rng: random.Random) -> list[list[tuple[str, str]]]:
    """Produce n distinct parameter sets for the given tool.

    Each parameter set is a list of (param_name, value) tuples, same shape
    as the old TOOL_EXAMPLE_PARAMS but with 20 variants per tool instead
    of 1. Drawn from realistic pools defined above.
    """
    out = []

    if tool_name == "book_reservation":
        for i in range(n):
            uid = rng.choice(USER_IDS)
            origin, dest = rng.sample(AIRPORTS, 2)
            out.append([("user_id", uid), ("origin", origin), ("destination", dest)])

    elif tool_name == "calculate":
        exprs = rng.sample(CALCULATE_EXPRESSIONS, min(n, len(CALCULATE_EXPRESSIONS)))
        while len(exprs) < n:
            exprs.append(rng.choice(CALCULATE_EXPRESSIONS))
        for e in exprs[:n]:
            out.append([("expression", e)])

    elif tool_name == "cancel_reservation":
        codes = rng.sample(RESERVATION_CODES, min(n, len(RESERVATION_CODES)))
        while len(codes) < n:
            codes.append(rng.choice(RESERVATION_CODES))
        for c in codes[:n]:
            out.append([("reservation_id", c)])

    elif tool_name == "get_reservation_details":
        codes = rng.sample(RESERVATION_CODES, min(n, len(RESERVATION_CODES)))
        while len(codes) < n:
            codes.append(rng.choice(RESERVATION_CODES))
        for c in codes[:n]:
            out.append([("reservation_id", c)])

    elif tool_name == "get_user_details":
        uids = rng.sample(USER_IDS, min(n, len(USER_IDS)))
        while len(uids) < n:
            uids.append(rng.choice(USER_IDS))
        for u in uids[:n]:
            out.append([("user_id", u)])

    elif tool_name == "list_all_airports":
        for _ in range(n):
            out.append([])  # no parameters

    elif tool_name == "search_direct_flight":
        for i in range(n):
            origin, dest = rng.sample(AIRPORTS, 2)
            date = rng.choice(DATES)
            out.append([("origin", origin), ("destination", dest), ("date", date)])

    elif tool_name == "search_onestop_flight":
        for i in range(n):
            origin, dest = rng.sample(AIRPORTS, 2)
            date = rng.choice(DATES)
            out.append([("origin", origin), ("destination", dest), ("date", date)])

    elif tool_name == "send_certificate":
        for i in range(n):
            uid = rng.choice(USER_IDS)
            amount = rng.choice(CERTIFICATE_AMOUNTS)
            out.append([("user_id", uid), ("amount", str(amount))])

    elif tool_name == "think":
        thoughts = rng.sample(THINK_THOUGHTS, min(n, len(THINK_THOUGHTS)))
        while len(thoughts) < n:
            thoughts.append(rng.choice(THINK_THOUGHTS))
        for t in thoughts[:n]:
            out.append([("thought", t)])

    elif tool_name == "transfer_to_human_agents":
        sums = rng.sample(HUMAN_TRANSFER_SUMMARIES, min(n, len(HUMAN_TRANSFER_SUMMARIES)))
        while len(sums) < n:
            sums.append(rng.choice(HUMAN_TRANSFER_SUMMARIES))
        for s in sums[:n]:
            out.append([("summary", s)])

    elif tool_name == "update_reservation_baggages":
        for i in range(n):
            rid = rng.choice(RESERVATION_CODES)
            bags = rng.choice(BAGGAGE_COUNTS)
            out.append([("reservation_id", rid), ("total_baggages", str(bags))])

    elif tool_name == "update_reservation_flights":
        for i in range(n):
            rid = rng.choice(RESERVATION_CODES)
            cabin = rng.choice(CABINS)
            out.append([("reservation_id", rid), ("cabin", cabin)])

    elif tool_name == "update_reservation_passengers":
        for i in range(n):
            rid = rng.choice(RESERVATION_CODES)
            first = rng.choice([u.split("_")[0].title() for u in USER_IDS])
            last = rng.choice([u.split("_")[1].title() for u in USER_IDS])
            dob_year = rng.randint(1960, 2005)
            dob = f"{dob_year}-{rng.randint(1,12):02d}-{rng.randint(1,28):02d}"
            passengers = (
                '[{"first_name":"' + first + '",'
                '"last_name":"' + last + '",'
                '"dob":"' + dob + '"}]'
            )
            out.append([("reservation_id", rid), ("passengers", passengers)])

    else:
        # Unknown tool — produce n empty param sets so extraction still runs
        for _ in range(n):
            out.append([])

    return out


# ---------------------------------------------------------------------------
# Variant 2 prompt + capture (same as extract_d_star_tools_v2.py but uses
# varied parameters)
# ---------------------------------------------------------------------------


def format_params_inline(params: list[tuple[str, str]]) -> str:
    if not params:
        return ""
    return ", ".join(f"{k}={v}" for k, v in params)


def build_variant2_prompt(tokenizer, tools_info, tool_name: str, params: list[tuple[str, str]]):
    param_str = format_params_inline(params)
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
    return base


def capture_last_token_hiddens(model, input_ids, layers):
    """Run one forward pass, capture hidden state at the last token of each layer."""
    captured = {}
    handles = []

    def make_hook(li):
        def hook(module, input, output):
            if isinstance(input, tuple) and len(input) > 0:
                h = input[0]
                captured[li] = h[0, -1, :].detach().to(torch.float16).cpu()
        return hook

    for li in layers:
        handles.append(model.model.layers[li].register_forward_hook(make_hook(li)))

    try:
        with torch.no_grad():
            model(input_ids, use_cache=False)
    finally:
        for h in handles:
            h.remove()

    return captured


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main():
    from hexis.adapters.cli import add_preset_args, resolve_preset_args

    ap = argparse.ArgumentParser()
    add_preset_args(ap, agentic=True, output_subpath=None)
    ap.add_argument("--n-variants", type=int, default=20)
    ap.add_argument("--output-dir", default=None,
                    help="Default: <preset.checkpoint_base>/agentic/d_star_tools_v2_varied")
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()
    preset = resolve_preset_args(args)
    if args.output_dir is None:
        args.output_dir = f"{preset.checkpoint_base}/agentic/d_star_tools_v2_varied"

    print("=" * 60)
    print("d*_tool v2 — VARIED parameters re-extraction")
    print(f"  Preset:    {preset.name}")
    print(f"  Model:     {args.model}")
    print(f"  Variants:  {args.n_variants} per tool")
    print(f"  Output:    {args.output_dir}")
    print(f"  Seed:      {args.seed}")
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

    # --- Build varied parameter sets per tool
    rng = random.Random(args.seed)
    tool_variants = {}
    for name in tool_names:
        tool_variants[name] = build_variants(name, args.n_variants, rng)
    log(f"  Varied param sets: {args.n_variants} per tool")
    # Spot-check one
    sample_tool = "search_direct_flight"
    log(f"  Example variants for {sample_tool}:")
    for i, v in enumerate(tool_variants[sample_tool][:3]):
        log(f"    v{i}: {v}")

    # --- Extract
    log("\nExtracting...")
    samples = []
    total = sum(len(tool_variants[t]) for t in tool_names)
    done = 0
    t0 = time.time()

    for tool_name in tool_names:
        for vi, params in enumerate(tool_variants[tool_name]):
            prompt = build_variant2_prompt(tokenizer, tools_info, tool_name, params)
            ids = tokenizer(
                prompt, return_tensors="pt", truncation=True, max_length=8192,
            ).input_ids.to(device)
            hidden = capture_last_token_hiddens(model, ids, layers)
            samples.append({
                "tool": tool_name,
                "context_id": f"varied_{vi:02d}",
                "hidden": hidden,
                "params": params,
            })
            done += 1
            if done % 20 == 0 or done == total:
                elapsed = time.time() - t0
                rate = done / elapsed if elapsed > 0 else 0
                eta = (total - done) / rate if rate > 0 else 0
                log(f"  [{done}/{total}] elapsed={elapsed:.0f}s rate={rate:.1f}/s eta={eta:.0f}s")

    wall = time.time() - t0

    # --- Save
    out_path = os.path.join(args.output_dir, "v2_user_end_samples.pt")
    torch.save({
        "model": args.model,
        "layers": layers,
        "variant": "user_instruction_varied",
        "capture_name": "user_end",
        "samples": samples,
        "n_variants_per_tool": args.n_variants,
        "seed": args.seed,
        "extraction_wall_s": wall,
    }, out_path)
    log(f"\nSaved → {out_path}")
    log(f"Extraction wall: {wall:.0f}s ({total/wall:.1f} samples/s)")

    # Print a quick per-tool sample count
    from collections import Counter
    c = Counter(s["tool"] for s in samples)
    log(f"Per-tool sample counts: {dict(c)}")


if __name__ == "__main__":
    main()
