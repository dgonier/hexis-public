"""HEXIS per-model adapters.

Usage:
    from hexis.adapters import get_preset
    preset = get_preset("ministral-8b")
    # preset.hf_id, preset.rank, preset.stride, preset.layer_class_path, ...

Adding a new model: see hexis/adapters/presets.py.
"""
from __future__ import annotations

from .model_preset import ModelPreset
from .presets import PRESETS, list_presets, register_preset


def get_preset(name: str) -> ModelPreset:
    """Look up a preset by name.

    Raises KeyError with the list of available presets on miss.
    """
    try:
        return PRESETS[name]
    except KeyError:
        raise KeyError(
            f"unknown preset: {name!r}. "
            f"Available: {', '.join(list_presets())}"
        )


__all__ = [
    "ModelPreset",
    "PRESETS",
    "get_preset",
    "list_presets",
    "register_preset",
]
