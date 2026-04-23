"""Tool-call format parsers for Qwen XML and Mistral [TOOL_CALLS] JSON.

The Qwen XML parser is lifted from scripts/eval_remember.py (the pre-adapter
home). The Mistral parser is new.

Both return a uniform list[{"name": str, "arguments": dict}] so downstream
code doesn't care which format the model emitted.
"""
from __future__ import annotations

import json
import re
from typing import Any


# -------- Qwen XML: <function=name><parameter=k>v</parameter></function> ----

_QWEN_FN_RE = re.compile(r"<function=([^>]+)>(.*?)</function>", re.DOTALL)
_QWEN_PARAM_RE = re.compile(r"<parameter=([^>]+)>(.*?)</parameter>", re.DOTALL)


def parse_qwen_xml(text: str) -> list[dict[str, Any]]:
    """Parse <function=name><parameter=k>v</parameter></function> blocks.

    Handles the common cases: string, int, float, bool, null, JSON-arrayish.
    Falls back to raw string if no type hint matches.
    """
    calls: list[dict[str, Any]] = []
    for m in _QWEN_FN_RE.finditer(text):
        name = m.group(1).strip()
        body = m.group(2)
        args: dict[str, Any] = {}
        for p in _QWEN_PARAM_RE.finditer(body):
            k = p.group(1).strip()
            v_raw = p.group(2).strip()
            args[k] = _coerce_value(v_raw)
        calls.append({"name": name, "arguments": args})
    return calls


def _coerce_value(v: str) -> Any:
    """Best-effort string → typed coercion for tool-call args."""
    if v == "" or v.lower() in ("null", "none"):
        return None
    if v.lower() == "true":
        return True
    if v.lower() == "false":
        return False
    # Try JSON first (handles lists, objects, quoted strings, numbers)
    try:
        return json.loads(v)
    except json.JSONDecodeError:
        pass
    # Numeric fallback
    try:
        if "." in v or "e" in v.lower():
            return float(v)
        return int(v)
    except ValueError:
        return v


def qwen_xml_instruction() -> str:
    """System-prompt block telling the model to emit Qwen XML tool calls."""
    return (
        "When calling a tool, emit exactly this format:\n"
        "<function=tool_name><parameter=arg_name>value</parameter>"
        "<parameter=other_arg>value</parameter></function>\n"
        "Do not wrap in ```json``` or any other fence."
    )


# -------- Mistral [TOOL_CALLS] JSON ------------------------------------------

# Mistral instruct template emits either:
#   [TOOL_CALLS][{"name": "...", "arguments": {...}}]
# or, in some variants, uses explicit tool_calls field in API-style responses.
# We parse the former (raw-text) form; structured API responses go through a
# different path.

_MISTRAL_TOOL_CALLS_RE = re.compile(r"\[TOOL_CALLS\]\s*(\[.*?\])", re.DOTALL)


def parse_mistral_tool_calls(text: str) -> list[dict[str, Any]]:
    """Parse [TOOL_CALLS][{"name": ..., "arguments": {...}}, ...] blocks.

    Multiple [TOOL_CALLS] segments are concatenated. Arguments may arrive
    as a JSON-encoded string — we decode it into a dict for uniformity.
    """
    out: list[dict[str, Any]] = []
    for m in _MISTRAL_TOOL_CALLS_RE.finditer(text):
        try:
            calls = json.loads(m.group(1))
        except json.JSONDecodeError:
            continue
        for c in calls:
            name = c.get("name")
            args = c.get("arguments", {})
            # Mistral sometimes stringifies arguments
            if isinstance(args, str):
                try:
                    args = json.loads(args)
                except json.JSONDecodeError:
                    args = {"_raw": args}
            if name:
                out.append({"name": name, "arguments": args or {}})
    return out


def mistral_tool_calls_instruction() -> str:
    """System-prompt block for Mistral [TOOL_CALLS] format."""
    return (
        'When calling a tool, emit exactly this format:\n'
        '[TOOL_CALLS][{"name": "tool_name", "arguments": {"arg_name": "value"}}]\n'
        "You may emit multiple calls in a single [TOOL_CALLS] block."
    )


# -------- Dispatch table -----------------------------------------------------

_PARSERS = {
    "qwen_xml": parse_qwen_xml,
    "mistral_tool_calls": parse_mistral_tool_calls,
}

_INSTRUCTIONS = {
    "qwen_xml": qwen_xml_instruction,
    "mistral_tool_calls": mistral_tool_calls_instruction,
}


def parse(format_id: str, text: str) -> list[dict[str, Any]]:
    p = _PARSERS.get(format_id)
    if not p:
        raise ValueError(f"unknown tool format: {format_id!r}")
    return p(text)


def instruction(format_id: str) -> str:
    g = _INSTRUCTIONS.get(format_id)
    if not g:
        raise ValueError(f"unknown tool format: {format_id!r}")
    return g()
