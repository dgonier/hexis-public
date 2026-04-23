"""
Extract d*_repeat_v2 via 3-class contrast.

The original d*_repeat.pt collapsed two distinctions into one: "calling a tool
that was called before with DIFFERENT args" (legitimate — task 26 needs 3
parallel get_reservation_details calls) got lumped in with "calling a tool
that was called before with the SAME args" (loop, the thing we actually want
to suppress). The resulting direction over-suppressed legitimate parallel
lookups.

Fix: three separate classes of prompts, then compute a direction that
isolates class 3 from class 1 while being orthogonal to the class 1 ↔ class 2
distinction.

    class 1  no_repeat      : fresh planning state, next tool is new
    class 2  diff_args       : tool T called before with args A, about to call
                               T with args B (legitimate multi-lookup)
    class 3  same_args       : tool T called before with args A, about to call
                               T with args A again (real loop — SUPPRESS)

Math:
    axis_novel_vs_parallel = normalize(mean_1 - mean_2)
    v_loop = mean_3 - mean_1
    d_star = normalize(v_loop - (v_loop · axis_novel_vs_parallel)
                                 * axis_novel_vs_parallel)

The direction encodes what's distinctive about class 3 (true loop) after
accounting for the class 1 ↔ class 2 variation, so injecting it pushes
away from true loops without steering away from legitimate parallel lookups.

Output wrapped-format checkpoint compatible with
deploy/agentic_eval/directions.py::load_from_checkpoint.

Usage:
    python scripts/extract_d_star_repeat_v2.py \
        --output checkpoints/d_star_repeat.pt
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


# Prompts use Qwen3.5 ChatML format with <tool_call> tags + tool results.
# Each prompt ends at the EXACT position where the model's next token would
# be the opening of a new <tool_call>, so the captured hidden state is at
# the actual decision point the base model uses for tool-call emission.
#
# Class 1 (no_repeat): fresh turn, no prior tool call of the same kind.
# Class 2 (diff_args): prior tool call of tool T with args A, now T with B.
# Class 3 (same_args): prior tool call of tool T with args A, now T with A.

IM_START = "<|im_start|>"
IM_END = "<|im_end|>"


def _chat(turns, ending):
    """Build a ChatML prompt, ending at the assistant's next-token position."""
    parts = []
    for role, content in turns:
        parts.append(f"{IM_START}{role}\n{content}{IM_END}\n")
    parts.append(f"{IM_START}assistant\n{ending}")
    return "".join(parts)


def _prior_call(name, args):
    """A prior assistant turn that made a tool call, plus a tool-result turn."""
    import json as _j
    call = f'<tool_call>\n{{"name": "{name}", "arguments": {_j.dumps(args)}}}\n</tool_call>'
    return [
        ("assistant", call),
        ("tool", '{"ok": true}'),
    ]


def build_class_1():
    """No prior call of this tool — fresh decision."""
    specs = [
        ("lookup_user", {"user_id": "U1"}),
        ("fetch_order", {"order_id": "A1"}),
        ("get_balance", {"account": "checking"}),
        ("check_inventory", {"sku": "S100"}),
        ("cancel_reservation", {"id": "R1"}),
        ("search_flights", {"origin": "JFK", "destination": "LAX"}),
        ("get_weather", {"city": "NYC"}),
        ("translate", {"text": "hello", "target": "es"}),
        ("get_user", {"id": 42}),
        ("list_files", {"path": "/home"}),
        ("fetch_doc", {"id": "doc-1"}),
        ("get_reservation_details", {"id": "X1"}),
        ("read_file", {"path": "a.txt"}),
        ("send_email", {"to": "alice@x.com"}),
        ("get_metric", {"name": "cpu"}),
        ("get_stock", {"symbol": "AAPL"}),
        ("lookup_address", {"zip": "10001"}),
        ("add_tag", {"resource": "r1", "tag": "prod"}),
        ("run_query", {"sql": "SELECT * FROM users"}),
        ("verify_id", {"id": "abc"}),
        ("create_invoice", {"customer": "c1", "amount": 100}),
        ("delete_item", {"item_id": "i1"}),
        ("update_profile", {"user_id": "u1", "name": "Alice"}),
        ("schedule_event", {"date": "2025-10-01", "title": "meeting"}),
        ("set_alarm", {"time": "08:00"}),
        ("book_ticket", {"event": "concert", "qty": 2}),
        ("get_exchange_rate", {"from": "USD", "to": "EUR"}),
        ("post_comment", {"thread": "t1", "body": "nice"}),
        ("rename_file", {"src": "a", "dst": "b"}),
        ("list_sessions", {"user": "alice"}),
        ("get_log", {"level": "error"}),
        ("flush_cache", {"key": "users"}),
        ("create_token", {"scope": "read"}),
        ("revoke_key", {"key_id": "k1"}),
        ("set_rate_limit", {"user": "u1", "per_min": 60}),
        ("generate_report", {"type": "daily"}),
        ("archive_thread", {"thread_id": "t1"}),
        ("pin_message", {"message_id": "m1"}),
        ("upgrade_plan", {"plan": "pro"}),
        ("track_shipment", {"tracking_id": "TRK1"}),
        ("get_membership", {"member_id": "mem1"}),
        ("transfer_funds", {"from": "a", "to": "b", "amount": 100}),
        ("mark_read", {"message_id": "m1"}),
        ("follow_user", {"target": "bob"}),
        ("vote", {"poll_id": "p1", "option": "a"}),
        ("submit_form", {"form_id": "f1"}),
        ("reset_device", {"device_id": "d1"}),
        ("pair_device", {"code": "1234"}),
        ("get_temperature", {"location": "kitchen"}),
        ("start_timer", {"name": "brew", "duration": 300}),
        ("log_event", {"event": "login"}),
        ("fetch_image", {"url": "http://img/1"}),
        ("compress_file", {"path": "a.txt"}),
        ("encrypt_blob", {"algo": "aes"}),
        ("sign_document", {"doc_id": "d1"}),
        ("parse_json", {"text": "{}"}),
        ("get_calendar_events", {"date": "today"}),
        ("count_members", {"group_id": "g1"}),
        ("join_channel", {"channel": "general"}),
        ("leave_channel", {"channel": "general"}),
    ]
    prompts = []
    for name, args in specs:
        turns = [
            ("system", "You are a helpful agent with tool access."),
            ("user", f"Please call {name} for me."),
        ]
        # Prompt ends PARTWAY through this first tool_call — no prior call
        # in history, so this is a fresh decision with no repeat context.
        prompts.append(_chat(turns, _next_call_prefix(name, args)))
    return prompts


def _next_call_prefix(name, args):
    """A half-emitted tool_call that ends partway through the arguments field.
    Capturing the hidden state here tells us what the model is 'committing' to
    — namely, the tool name and the first few characters of args, which is
    where same-args vs different-args becomes representable.
    """
    import json as _j
    args_json = _j.dumps(args)
    # Truncate args_json partway through — leave just enough to pin the values
    return f'<tool_call>\n{{"name": "{name}", "arguments": {args_json}'


def build_class_2():
    """Prior call of T with args A, about to call T with args B (legit parallel).
    Capture hidden state at the position right after the args B has been
    committed — this is where 'different args' is representationally distinct
    from 'same args'."""
    specs = [
        ("lookup_user", {"user_id": "U1"}, {"user_id": "U2"}),
        ("fetch_order", {"order_id": "A1"}, {"order_id": "B2"}),
        ("get_balance", {"account": "checking"}, {"account": "savings"}),
        ("check_inventory", {"sku": "S100"}, {"sku": "S200"}),
        ("cancel_reservation", {"id": "R1"}, {"id": "R2"}),
        ("search_flights", {"origin": "JFK", "destination": "LAX"}, {"origin": "LAX", "destination": "SFO"}),
        ("get_weather", {"city": "NYC"}, {"city": "Boston"}),
        ("translate", {"text": "hello", "target": "es"}, {"text": "goodbye", "target": "es"}),
        ("get_user", {"id": 42}, {"id": 43}),
        ("list_files", {"path": "/home"}, {"path": "/tmp"}),
        ("fetch_doc", {"id": "doc-1"}, {"id": "doc-2"}),
        ("get_reservation_details", {"id": "X1"}, {"id": "X2"}),
        ("read_file", {"path": "a.txt"}, {"path": "b.txt"}),
        ("send_email", {"to": "alice@x.com"}, {"to": "bob@x.com"}),
        ("get_metric", {"name": "cpu"}, {"name": "memory"}),
        ("get_stock", {"symbol": "AAPL"}, {"symbol": "GOOG"}),
        ("lookup_address", {"zip": "10001"}, {"zip": "90210"}),
        ("add_tag", {"resource": "r1", "tag": "prod"}, {"resource": "r2", "tag": "prod"}),
        ("run_query", {"sql": "SELECT * FROM users"}, {"sql": "SELECT * FROM orders"}),
        ("verify_id", {"id": "abc"}, {"id": "xyz"}),
        ("create_invoice", {"customer": "c1", "amount": 100}, {"customer": "c2", "amount": 200}),
        ("delete_item", {"item_id": "i1"}, {"item_id": "i2"}),
        ("update_profile", {"user_id": "u1", "name": "Alice"}, {"user_id": "u2", "name": "Bob"}),
        ("schedule_event", {"date": "2025-10-01", "title": "meeting"}, {"date": "2025-10-02", "title": "review"}),
        ("set_alarm", {"time": "08:00"}, {"time": "09:00"}),
        ("book_ticket", {"event": "concert", "qty": 2}, {"event": "theater", "qty": 1}),
        ("get_exchange_rate", {"from": "USD", "to": "EUR"}, {"from": "USD", "to": "JPY"}),
        ("post_comment", {"thread": "t1", "body": "nice"}, {"thread": "t2", "body": "ok"}),
        ("rename_file", {"src": "a", "dst": "b"}, {"src": "c", "dst": "d"}),
        ("list_sessions", {"user": "alice"}, {"user": "bob"}),
        ("get_log", {"level": "error"}, {"level": "warn"}),
        ("flush_cache", {"key": "users"}, {"key": "orders"}),
        ("create_token", {"scope": "read"}, {"scope": "write"}),
        ("revoke_key", {"key_id": "k1"}, {"key_id": "k2"}),
        ("set_rate_limit", {"user": "u1", "per_min": 60}, {"user": "u2", "per_min": 120}),
        ("generate_report", {"type": "daily"}, {"type": "weekly"}),
        ("archive_thread", {"thread_id": "t1"}, {"thread_id": "t2"}),
        ("pin_message", {"message_id": "m1"}, {"message_id": "m2"}),
        ("upgrade_plan", {"plan": "pro"}, {"plan": "enterprise"}),
        ("track_shipment", {"tracking_id": "TRK1"}, {"tracking_id": "TRK2"}),
        ("get_membership", {"member_id": "mem1"}, {"member_id": "mem2"}),
        ("transfer_funds", {"from": "a", "to": "b", "amount": 100}, {"from": "c", "to": "d", "amount": 50}),
        ("mark_read", {"message_id": "m1"}, {"message_id": "m2"}),
        ("follow_user", {"target": "bob"}, {"target": "carol"}),
        ("vote", {"poll_id": "p1", "option": "a"}, {"poll_id": "p2", "option": "b"}),
        ("submit_form", {"form_id": "f1"}, {"form_id": "f2"}),
        ("reset_device", {"device_id": "d1"}, {"device_id": "d2"}),
        ("pair_device", {"code": "1234"}, {"code": "5678"}),
        ("get_temperature", {"location": "kitchen"}, {"location": "bedroom"}),
        ("start_timer", {"name": "brew", "duration": 300}, {"name": "bake", "duration": 600}),
        ("log_event", {"event": "login"}, {"event": "logout"}),
        ("fetch_image", {"url": "http://img/1"}, {"url": "http://img/2"}),
        ("compress_file", {"path": "a.txt"}, {"path": "b.txt"}),
        ("encrypt_blob", {"algo": "aes"}, {"algo": "rsa"}),
        ("sign_document", {"doc_id": "d1"}, {"doc_id": "d2"}),
        ("parse_json", {"text": "{}"}, {"text": "[]"}),
        ("get_calendar_events", {"date": "today"}, {"date": "tomorrow"}),
        ("count_members", {"group_id": "g1"}, {"group_id": "g2"}),
        ("join_channel", {"channel": "general"}, {"channel": "random"}),
        ("leave_channel", {"channel": "general"}, {"channel": "random"}),
    ]
    prompts = []
    for name, prior_args, next_args in specs:
        turns = [
            ("system", "You are a helpful agent with tool access."),
            ("user", f"Please fetch data for both items."),
        ]
        turns.extend(_prior_call(name, prior_args))
        # Prompt ends PARTWAY through the next tool_call with next_args.
        # Capture point is right after the new args have been emitted, so
        # the hidden state differs from class 3 (where args == prior_args).
        prompts.append(_chat(turns, _next_call_prefix(name, next_args)))
    return prompts


def build_class_3():
    """Prior call of T with args A, about to call T with THE SAME args A."""
    specs = [
        ("lookup_user", {"user_id": "U1"}),
        ("fetch_order", {"order_id": "A1"}),
        ("get_balance", {"account": "checking"}),
        ("check_inventory", {"sku": "S100"}),
        ("cancel_reservation", {"id": "R1"}),
        ("search_flights", {"origin": "JFK", "destination": "LAX"}),
        ("get_weather", {"city": "NYC"}),
        ("translate", {"text": "hello", "target": "es"}),
        ("get_user", {"id": 42}),
        ("list_files", {"path": "/home"}),
        ("fetch_doc", {"id": "doc-1"}),
        ("get_reservation_details", {"id": "X1"}),
        ("read_file", {"path": "a.txt"}),
        ("send_email", {"to": "alice@x.com"}),
        ("get_metric", {"name": "cpu"}),
        ("get_stock", {"symbol": "AAPL"}),
        ("lookup_address", {"zip": "10001"}),
        ("add_tag", {"resource": "r1", "tag": "prod"}),
        ("run_query", {"sql": "SELECT * FROM users"}),
        ("verify_id", {"id": "abc"}),
        ("create_invoice", {"customer": "c1", "amount": 100}),
        ("delete_item", {"item_id": "i1"}),
        ("update_profile", {"user_id": "u1", "name": "Alice"}),
        ("schedule_event", {"date": "2025-10-01", "title": "meeting"}),
        ("set_alarm", {"time": "08:00"}),
        ("book_ticket", {"event": "concert", "qty": 2}),
        ("get_exchange_rate", {"from": "USD", "to": "EUR"}),
        ("post_comment", {"thread": "t1", "body": "nice"}),
        ("rename_file", {"src": "a", "dst": "b"}),
        ("list_sessions", {"user": "alice"}),
        ("get_log", {"level": "error"}),
        ("flush_cache", {"key": "users"}),
        ("create_token", {"scope": "read"}),
        ("revoke_key", {"key_id": "k1"}),
        ("set_rate_limit", {"user": "u1", "per_min": 60}),
        ("generate_report", {"type": "daily"}),
        ("archive_thread", {"thread_id": "t1"}),
        ("pin_message", {"message_id": "m1"}),
        ("upgrade_plan", {"plan": "pro"}),
        ("track_shipment", {"tracking_id": "TRK1"}),
        ("get_membership", {"member_id": "mem1"}),
        ("transfer_funds", {"from": "a", "to": "b", "amount": 100}),
        ("mark_read", {"message_id": "m1"}),
        ("follow_user", {"target": "bob"}),
        ("vote", {"poll_id": "p1", "option": "a"}),
        ("submit_form", {"form_id": "f1"}),
        ("reset_device", {"device_id": "d1"}),
        ("pair_device", {"code": "1234"}),
        ("get_temperature", {"location": "kitchen"}),
        ("start_timer", {"name": "brew", "duration": 300}),
        ("log_event", {"event": "login"}),
        ("fetch_image", {"url": "http://img/1"}),
        ("compress_file", {"path": "a.txt"}),
        ("encrypt_blob", {"algo": "aes"}),
        ("sign_document", {"doc_id": "d1"}),
        ("parse_json", {"text": "{}"}),
        ("get_calendar_events", {"date": "today"}),
        ("count_members", {"group_id": "g1"}),
        ("join_channel", {"channel": "general"}),
        ("leave_channel", {"channel": "general"}),
    ]
    prompts = []
    for name, args in specs:
        turns = [
            ("system", "You are a helpful agent with tool access."),
            ("user", "Please check this for me."),
        ]
        turns.extend(_prior_call(name, args))
        # Prompt ends PARTWAY through a second tool_call with the SAME args
        # as the prior call. This is the loop we want to suppress.
        prompts.append(_chat(turns, _next_call_prefix(name, args)))
    return prompts


CLASS_1_NO_REPEAT = build_class_1()
CLASS_2_DIFFERENT_ARGS = build_class_2()
CLASS_3_SAME_ARGS = build_class_3()


def capture_prompt_hidden_states(model, tokenizer, prompt, layers, device):
    """Capture last-token hidden state at each target layer on a single
    forward pass. Returns {layer_idx: tensor(d_model,)}.
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


def collect(model, tokenizer, prompts, layers, device, label):
    print(f"\n  Capturing {label} samples ({len(prompts)})...")
    t0 = time.time()
    samples = []
    for i, prompt in enumerate(prompts):
        states = capture_prompt_hidden_states(model, tokenizer, prompt, layers, device)
        if states:
            samples.append(states)
        if (i + 1) % 5 == 0:
            print(f"    {i+1}/{len(prompts)}")
    print(f"  Captured {len(samples)} {label} in {time.time()-t0:.0f}s")
    return samples


def compute_direction_3class(class_1, class_2, class_3, layers):
    """d* = normalize(v - (v · ax) * ax) where
        v  = mean_3 - mean_1
        ax = normalize(mean_1 - mean_2)

    Also return diagnostic cosines per layer for separability reporting.
    """
    d_star = {}
    diag = {}
    for l in layers:
        c1 = [s[l] for s in class_1 if l in s]
        c2 = [s[l] for s in class_2 if l in s]
        c3 = [s[l] for s in class_3 if l in s]
        if not (c1 and c2 and c3):
            continue
        m1 = torch.stack(c1).float().mean(0)
        m2 = torch.stack(c2).float().mean(0)
        m3 = torch.stack(c3).float().mean(0)

        ax_raw = m1 - m2
        ax_norm = ax_raw.norm().item()
        if ax_norm < 1e-6:
            # classes 1 and 2 are indistinguishable — fall back to simple
            # (m3 - m1) direction and log a warning
            v = m3 - m1
            d = v / (v.norm() + 1e-9)
        else:
            ax = ax_raw / ax_raw.norm()
            v = m3 - m1
            v_parallel = (v @ ax) * ax
            v_ortho = v - v_parallel
            d = v_ortho / (v_ortho.norm() + 1e-9)

        d_star[l] = d

        # Diagnostics: how close is class 3 to class 1? to class 2?
        cos_31 = F.cosine_similarity(m3.unsqueeze(0), m1.unsqueeze(0)).item()
        cos_32 = F.cosine_similarity(m3.unsqueeze(0), m2.unsqueeze(0)).item()
        cos_12 = F.cosine_similarity(m1.unsqueeze(0), m2.unsqueeze(0)).item()
        diag[l] = {
            "cos(3,1)": cos_31,
            "cos(3,2)": cos_32,
            "cos(1,2)": cos_12,
            "||m3-m1||": (m3 - m1).norm().item(),
            "||ax||": ax_norm,
            "||d_raw||": (v_ortho if ax_norm > 1e-6 else v).norm().item(),
        }
    return d_star, diag


def main():
    from hexis.adapters.cli import add_preset_args, resolve_preset_args

    ap = argparse.ArgumentParser()
    add_preset_args(ap, agentic=True, output_subpath="agentic/d_star_repeat_v2.pt")
    args = ap.parse_args()
    preset = resolve_preset_args(args)

    print("=" * 60)
    print("Extract d*_repeat_v2 (3-class contrast)")
    print(f"  Preset: {preset.name}")
    print(f"  Model:  {args.model}")
    print(f"  Stride: {args.stride}")
    print(f"  Output: {args.output}")
    print("=" * 60)
    print(f"  Class 1 (no repeat):      {len(CLASS_1_NO_REPEAT)}")
    print(f"  Class 2 (different args): {len(CLASS_2_DIFFERENT_ARGS)}")
    print(f"  Class 3 (same args):      {len(CLASS_3_SAME_ARGS)}")

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

    c1 = collect(model, tokenizer, CLASS_1_NO_REPEAT, layers, device, "class 1 no_repeat")
    gc.collect(); torch.cuda.empty_cache()
    c2 = collect(model, tokenizer, CLASS_2_DIFFERENT_ARGS, layers, device, "class 2 diff_args")
    gc.collect(); torch.cuda.empty_cache()
    c3 = collect(model, tokenizer, CLASS_3_SAME_ARGS, layers, device, "class 3 same_args")

    print("\n" + "=" * 60)
    print("DIAGNOSTICS per layer")
    print("=" * 60)
    d_star, diag = compute_direction_3class(c1, c2, c3, layers)
    for l in sorted(d_star.keys()):
        info = diag[l]
        print(
            f"  L{l:02d}: "
            f"cos(3,1)={info['cos(3,1)']:+.3f}  "
            f"cos(3,2)={info['cos(3,2)']:+.3f}  "
            f"cos(1,2)={info['cos(1,2)']:+.3f}  "
            f"||m3-m1||={info['||m3-m1||']:.2f}  "
            f"||d_raw||={info['||d_raw||']:.2f}"
        )

    if not d_star:
        print("  FAILED — no direction computed")
        sys.exit(1)

    out_dir = os.path.dirname(os.path.abspath(args.output))
    os.makedirs(out_dir, exist_ok=True)
    torch.save({
        "d_star": d_star,
        "n_novel": len(c1) + len(c2),  # reuse field for loader compat
        "n_repeat": len(c3),
        "separable_layers": len(d_star),
        "tasks": [],
        "model": args.model,
        "stride": args.stride,
        "layers": layers,
        "direction_name": "d_star_repeat_v2",
        "extraction_method": "3class_orthogonal",
        "diagnostics": diag,
    }, args.output)
    print(f"\n  Saved → {args.output}")


if __name__ == "__main__":
    main()
