"""Thinking-mode handling for models that emit <think>...</think> prefixes.

Used by sycophancy eval, persona-drift scorers, tool-call extractors, and
any other code that needs the model's "answer" separate from its
"reasoning."
"""
from __future__ import annotations

import re


_THINK_OPEN = re.compile(r"<think>", re.IGNORECASE)
_THINK_CLOSE = re.compile(r"</think>", re.IGNORECASE)


def has_think_tag(text: str) -> bool:
    return bool(_THINK_OPEN.search(text) or _THINK_CLOSE.search(text))


def strip_thinking(text: str) -> str:
    """Return the portion of text AFTER </think>.

    If </think> is absent, return the original text unchanged. Leading
    whitespace after </think> is trimmed.

    Canonical per CLAUDE.md project notes: split on </think> is the only
    reliable answer extractor for GRPO/thinking models.
    """
    m = _THINK_CLOSE.search(text)
    if not m:
        return text
    return text[m.end():].lstrip()


def extract_thinking(text: str) -> str | None:
    """Return just the <think>...</think> content, or None if absent."""
    open_m = _THINK_OPEN.search(text)
    close_m = _THINK_CLOSE.search(text)
    if not (open_m and close_m) or close_m.start() <= open_m.end():
        return None
    return text[open_m.end():close_m.start()].strip()
