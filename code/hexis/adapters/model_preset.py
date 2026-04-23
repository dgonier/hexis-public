"""ModelPreset — single config object carrying per-model settings for
every HEXIS consumer (training, extraction, serving, deploy).

A preset is frozen at import time. CLI scripts take `--preset <name>` and
load the preset via `hexis.adapters.get_preset(name)`. Individual fields
can be overridden via explicit CLI flags that default to None and fall
through to the preset when unset.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal, Optional

Family = Literal["qwen3", "qwen3_moe", "mistral"]
Mode = Literal["standard", "thinking"]
ChatFormat = Literal["chatml", "mistral_inst"]
ToolFormat = Literal["qwen_xml", "mistral_tool_calls"]


@dataclass(frozen=True)
class ModelPreset:
    """Per-model configuration for HEXIS training, extraction, and serving.

    Every field has a sensible default where possible. Required fields are
    identity (hf_id, family), architecture (d_model, n_layers), and the
    plugin knob (layer_class_path).
    """

    # Identity
    name: str
    hf_id: str
    family: Family
    mode: Mode = "standard"

    # Architecture — read from HF config, baked here for offline reference
    # and for consumers that need them before model load.
    d_model: int = 0
    n_layers: int = 0
    n_attn_heads: int = 0
    n_kv_heads: int = 0

    # Training hyperparams (from M_canonical_recipe.md)
    stride: int = 3
    rank: int = 16
    margin_base: float = 0.3
    v_scale_init: float = 1.0
    lr_phase_a: float = 1e-4
    lr_phase_b: float = 3e-4
    lr_phase_d: float = 3e-5
    belief_window: int = 512

    # Prompt + tool format
    chat_format: ChatFormat = "chatml"
    tool_format: ToolFormat = "qwen_xml"

    # Hybrid attention metadata — documentary only. For hybrid models
    # (Qwen3.5, Qwen3.6-35B-A3B with DeltaNet:FullAttn mix), HEXIS's
    # hexis/model_hybrid.py handles both layer types uniformly in phi
    # hooks. This field is NOT consumed by patched_layer_indices — it's
    # here so callers can verify the loaded model matches expectations.
    # None = non-hybrid (all layers full attention).
    full_attention_interval: int | None = None

    # vLLM plugin + deploy
    layer_class_path: str = ""
    vllm_max_model_len: int = 32768
    vllm_gpu: str = "H100"
    vllm_tp: int = 1
    vllm_enforce_eager: bool = True

    # Storage — per-preset isolation so multi-model checkpoints don't collide
    checkpoint_base: str = ""
    seeds_base: str = ""

    def __post_init__(self):
        # Fill empty checkpoint_base/seeds_base with sensible defaults
        if not self.checkpoint_base:
            object.__setattr__(self, "checkpoint_base", f"checkpoints/{self.name}")
        if not self.seeds_base:
            object.__setattr__(self, "seeds_base", f"seeds/{self.name}")

    # ------ helpers consumers call ----------------------------------------

    def patched_layer_indices(self, n_layers_override: Optional[int] = None) -> list[int]:
        """Simple stride-sampled layer indices.

        HEXIS's hexis/model_hybrid.py handles both full-attention and
        linear-attention (DeltaNet) layers uniformly when patching phi
        hooks, so stride sampling is correct regardless of model family.
        """
        n = n_layers_override if n_layers_override is not None else self.n_layers
        if n == 0:
            raise ValueError(
                f"n_layers not set on preset {self.name}; pass n_layers_override"
            )
        return list(range(0, n, self.stride))

    def full_attention_layer_indices(self, n_layers_override: Optional[int] = None) -> list[int]:
        """All full-attention layers in the model (before stride sampling)."""
        n = n_layers_override if n_layers_override is not None else self.n_layers
        if self.full_attention_interval is None:
            return list(range(n))
        k = self.full_attention_interval
        return list(range(k - 1, n, k))

    def apply_chat_template(self, tokenizer, messages, add_generation_prompt: bool = True):
        """Delegate to tokenizer's native chat template.

        We deliberately don't hand-roll templates per format id — the
        tokenizer always knows the right thing for its model. The
        chat_format field is kept for downstream rendering where we need
        to know what we're dealing with (e.g., should we strip a BOS?).
        """
        return tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=add_generation_prompt,
        )

    def strip_thinking(self, text: str) -> str:
        """Remove <think>...</think> prefix for thinking-mode models.

        For standard-mode models this is a no-op. For thinking-mode models,
        the split-on-</think> pattern is the canonical extractor (see
        CLAUDE.md project notes)."""
        if self.mode != "thinking":
            return text
        if "</think>" in text:
            return text.split("</think>", 1)[1].lstrip()
        return text

    def has_think_tag(self, text: str) -> bool:
        return "<think>" in text or "</think>" in text

    def parse_tool_calls(self, text: str):
        """Parse tool calls out of generated text using the preset's tool format.

        Returns a list of {"name": str, "arguments": dict}.
        """
        from . import tool_formats
        if self.tool_format == "qwen_xml":
            return tool_formats.parse_qwen_xml(text)
        elif self.tool_format == "mistral_tool_calls":
            return tool_formats.parse_mistral_tool_calls(text)
        raise ValueError(f"unknown tool_format: {self.tool_format}")

    def render_tool_instruction(self) -> str:
        """The tool-format instruction block for system prompts."""
        from . import tool_formats
        if self.tool_format == "qwen_xml":
            return tool_formats.qwen_xml_instruction()
        elif self.tool_format == "mistral_tool_calls":
            return tool_formats.mistral_tool_calls_instruction()
        raise ValueError(f"unknown tool_format: {self.tool_format}")

    def install_vllm_plugin(self) -> None:
        """Install the vLLM plugin with this preset's layer_class_path.

        Called from vllm_hexis.register() when HEXIS_MODEL_PRESET env var
        is set. Callers outside the plugin context typically don't need
        this — the plugin wires itself up.
        """
        from vllm_hexis import patch
        patch.install(layer_class_path=self.layer_class_path or None)

    def checkpoint_path(self, phase: str, filename: str = "BEST.pt") -> str:
        """Canonical checkpoint path for a training phase under this preset.

        phase is one of: "v21", "v21_1", "v21_2", "v21_4",
                          "v23_compiled_v2", "v23_sycophancy", "d_star",
                          "agentic/d_star_repeat", etc.
        """
        return f"{self.checkpoint_base}/{phase}/{filename}"
