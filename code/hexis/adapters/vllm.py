"""vLLM plugin + Modal deploy helpers keyed by preset name.

The plugin (vllm_hexis) is architecture-generic — it just needs the
layer_class_path. This module wires the preset lookup into the plugin
entry point so every consumer (training smoke, deploy app, CI) can opt
into the right arch with a single `HEXIS_MODEL_PRESET` env var.
"""
from __future__ import annotations

import os


def install_vllm_plugin_for_preset(preset_name: str | None = None) -> None:
    """Install the vllm_hexis plugin with the preset's layer_class_path.

    If preset_name is None, reads HEXIS_MODEL_PRESET env var. If that's
    also unset, falls through to the plugin's default (Qwen3.5 layer).
    """
    name = preset_name or os.environ.get("HEXIS_MODEL_PRESET")
    try:
        from vllm_hexis import patch  # type: ignore
    except ImportError:
        raise RuntimeError(
            "vllm_hexis package not installed. "
            "pip install deploy/agentic_eval_h200/vllm_hexis_pkg/"
        )
    if not name:
        patch.install()
        return
    from . import get_preset
    preset = get_preset(name)
    patch.install(layer_class_path=preset.layer_class_path or None)


def modal_gpu_spec(preset_name: str) -> str:
    """Return the Modal GPU spec string for a preset's deploy."""
    from . import get_preset
    return get_preset(preset_name).vllm_gpu


def vllm_serve_kwargs(preset_name: str) -> dict:
    """Canonical kwargs for `vllm.LLM(...)` or `AsyncLLM.from_engine_args(...)`.

    Enforces enforce_eager=True when the plugin is active (Dynamo can't
    trace os.stat on the IPC read).
    """
    from . import get_preset
    p = get_preset(preset_name)
    return dict(
        model=p.hf_id,
        max_model_len=p.vllm_max_model_len,
        tensor_parallel_size=p.vllm_tp,
        enforce_eager=p.vllm_enforce_eager,
        trust_remote_code=True,
    )
