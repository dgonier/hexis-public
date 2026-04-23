"""Unit tests for hexis/adapters.

These tests have no torch/transformers dependency — they validate pure
Python config and format logic. They should pass in any Python 3.10+
environment with just pytest installed.

Run: python -m pytest hexis/adapters/tests/ -v
"""
from __future__ import annotations

import pytest

from hexis.adapters import get_preset, list_presets, PRESETS
from hexis.adapters.model_preset import ModelPreset
from hexis.adapters import tool_formats, thinking_modes


# ---------- Registry ---------------------------------------------------------


def test_presets_registered():
    names = list_presets()
    assert "qwen3.5-4b" in names
    assert "ministral-8b" in names
    assert "qwen3-30b-a3b-thinking" in names
    assert "qwen3.6-35b-a3b" in names


def test_get_preset_unknown_raises():
    with pytest.raises(KeyError):
        get_preset("not-a-real-model")


@pytest.mark.parametrize("name", list(PRESETS.keys()))
def test_preset_has_required_fields(name):
    p = get_preset(name)
    assert p.hf_id
    assert p.family in ("qwen3", "qwen3_moe", "mistral")
    assert p.mode in ("standard", "thinking")
    assert p.d_model > 0
    assert p.n_layers > 0
    assert p.stride >= 1
    assert p.rank >= 1
    assert p.margin_base > 0
    assert p.chat_format in ("chatml", "mistral_inst")
    assert p.tool_format in ("qwen_xml", "mistral_tool_calls")
    assert p.layer_class_path
    assert p.checkpoint_base
    assert p.seeds_base


def test_checkpoint_paths_isolated():
    """Multi-model checkpoints must not collide."""
    bases = {p.checkpoint_base for p in PRESETS.values()}
    assert len(bases) == len(PRESETS), "checkpoint_base collision"


# ---------- patched_layer_indices -------------------------------------------


def test_qwen35_4b_patched_layers():
    p = get_preset("qwen3.5-4b")
    # stride=3, n_layers=32 → [0, 3, 6, 9, 12, 15, 18, 21, 24, 27, 30]
    assert p.patched_layer_indices() == [0, 3, 6, 9, 12, 15, 18, 21, 24, 27, 30]


def test_ministral_patched_layers():
    p = get_preset("ministral-8b")
    assert p.patched_layer_indices() == [0, 3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33]


def test_qwen3_30b_patched_layers():
    p = get_preset("qwen3-30b-a3b-thinking")
    # stride=3, n_layers=48 → 16 layers
    indices = p.patched_layer_indices()
    assert len(indices) == 16
    assert indices[0] == 0
    assert indices[-1] == 45


def test_qwen36_35b_patched_layers():
    p = get_preset("qwen3.6-35b-a3b")
    # stride=3, n_layers=40 → 14 layers
    indices = p.patched_layer_indices()
    assert len(indices) == 14
    assert indices == [0, 3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36, 39]


def test_patched_layer_indices_with_override():
    p = get_preset("qwen3.5-4b")
    assert p.patched_layer_indices(n_layers_override=16) == [0, 3, 6, 9, 12, 15]


# ---------- thinking mode ---------------------------------------------------


def test_strip_thinking_standard_mode_noop():
    p = get_preset("ministral-8b")
    assert p.mode == "standard"
    text = "The answer is <think>reasoning</think> final response."
    # Preset's strip_thinking delegates to helper; standard mode should no-op.
    assert p.strip_thinking(text) == text


def test_strip_thinking_thinking_mode_strips():
    p = get_preset("qwen3.6-35b-a3b")
    assert p.mode == "thinking"
    text = "<think>reasoning</think> final response."
    result = p.strip_thinking(text)
    assert result == "final response."
    assert "<think>" not in result


def test_strip_thinking_no_close_tag_returns_original():
    p = get_preset("qwen3-30b-a3b-thinking")
    text = "no think tags here"
    assert p.strip_thinking(text) == text


def test_has_think_tag():
    p = get_preset("qwen3.6-35b-a3b")
    assert p.has_think_tag("<think>x</think>") is True
    assert p.has_think_tag("no tags") is False


# ---------- tool formats ----------------------------------------------------


def test_qwen_xml_round_trip():
    text = (
        "<function=get_weather>"
        "<parameter=city>Tokyo</parameter>"
        "<parameter=unit>celsius</parameter>"
        "</function>"
    )
    calls = tool_formats.parse_qwen_xml(text)
    assert len(calls) == 1
    assert calls[0]["name"] == "get_weather"
    assert calls[0]["arguments"] == {"city": "Tokyo", "unit": "celsius"}


def test_qwen_xml_multiple():
    text = (
        "<function=a><parameter=x>1</parameter></function>"
        "<function=b><parameter=y>hello</parameter></function>"
    )
    calls = tool_formats.parse_qwen_xml(text)
    assert len(calls) == 2
    assert calls[0]["name"] == "a" and calls[0]["arguments"] == {"x": 1}
    assert calls[1]["name"] == "b" and calls[1]["arguments"] == {"y": "hello"}


def test_qwen_xml_coerces_types():
    text = (
        "<function=f>"
        "<parameter=i>42</parameter>"
        "<parameter=f>3.14</parameter>"
        "<parameter=b>true</parameter>"
        "<parameter=n>null</parameter>"
        "<parameter=s>hello</parameter>"
        "</function>"
    )
    calls = tool_formats.parse_qwen_xml(text)
    args = calls[0]["arguments"]
    assert args["i"] == 42
    assert args["f"] == 3.14
    assert args["b"] is True
    assert args["n"] is None
    assert args["s"] == "hello"


def test_mistral_tool_calls_basic():
    text = '[TOOL_CALLS][{"name": "get_weather", "arguments": {"city": "Paris"}}]'
    calls = tool_formats.parse_mistral_tool_calls(text)
    assert len(calls) == 1
    assert calls[0]["name"] == "get_weather"
    assert calls[0]["arguments"] == {"city": "Paris"}


def test_mistral_tool_calls_stringified_args():
    """Mistral sometimes encodes arguments as a JSON string."""
    text = '[TOOL_CALLS][{"name": "f", "arguments": "{\\"x\\": 1}"}]'
    calls = tool_formats.parse_mistral_tool_calls(text)
    assert len(calls) == 1
    assert calls[0]["arguments"] == {"x": 1}


def test_tool_format_dispatch_via_preset():
    p = get_preset("qwen3.5-4b")
    text = "<function=f><parameter=x>1</parameter></function>"
    calls = p.parse_tool_calls(text)
    assert len(calls) == 1

    m = get_preset("ministral-8b")
    text = '[TOOL_CALLS][{"name": "f", "arguments": {"x": 1}}]'
    calls = m.parse_tool_calls(text)
    assert len(calls) == 1


def test_render_tool_instruction_non_empty():
    for name in PRESETS:
        p = get_preset(name)
        inst = p.render_tool_instruction()
        assert isinstance(inst, str)
        assert len(inst) > 20
