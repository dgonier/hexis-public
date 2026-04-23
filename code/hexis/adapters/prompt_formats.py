"""Chat template wrappers — delegate to tokenizer.apply_chat_template().

We don't hand-roll templates per format. The tokenizer shipped with each
model knows the right tokens/markers for that model; overriding that is a
recipe for silent corruption. The `chat_format` field on ModelPreset
remains because downstream code sometimes needs to know what it's dealing
with (e.g., whether to expect a BOS, whether to strip `[INST]` markers in
render output).
"""
from __future__ import annotations

from typing import Iterable


def render_chat(
    tokenizer,
    messages: Iterable[dict],
    add_generation_prompt: bool = True,
    enable_thinking: bool | None = None,
) -> str:
    """Render a messages list to a string via the tokenizer's template.

    enable_thinking is forwarded to Qwen3-Thinking tokenizers that support it.
    None means "let the template default."
    """
    kwargs = dict(tokenize=False, add_generation_prompt=add_generation_prompt)
    if enable_thinking is not None:
        kwargs["enable_thinking"] = enable_thinking
    try:
        return tokenizer.apply_chat_template(list(messages), **kwargs)
    except TypeError:
        # enable_thinking not supported by this tokenizer; drop it.
        kwargs.pop("enable_thinking", None)
        return tokenizer.apply_chat_template(list(messages), **kwargs)


def strip_bos(text: str, bos_token: str | None) -> str:
    """Drop a leading BOS token if present."""
    if bos_token and text.startswith(bos_token):
        return text[len(bos_token):]
    return text
