"""PRESETS — the registry of model configurations.

To add a new model:
  1. Add a new ModelPreset() entry to PRESETS below
  2. That's it. Training scripts, extraction scripts, plugin, and deploy
     apps all read from here via --preset / HEXIS_MODEL_PRESET.

Fields like layer_class_path must be verified against the target model in
vLLM. Phase 2a of the portability plan does this introspection.
"""
from __future__ import annotations

from .model_preset import ModelPreset


PRESETS: dict[str, ModelPreset] = {
    # ---------------- Qwen3.5-4B — the control ---------------------------
    "qwen3.5-4b": ModelPreset(
        name="qwen3.5-4b",
        hf_id="Qwen/Qwen3.5-4B",
        family="qwen3",
        mode="standard",
        d_model=2560,
        n_layers=32,
        n_attn_heads=32,
        n_kv_heads=8,
        stride=3,
        # Hybrid DeltaNet:FullAttn at 3:1 — full-attn at layers 3,7,11,...,31.
        full_attention_interval=4,
        rank=16,
        margin_base=0.3,
        v_scale_init=1.0,
        lr_phase_a=1e-4,
        lr_phase_b=3e-4,
        lr_phase_d=3e-5,
        belief_window=512,
        chat_format="chatml",
        tool_format="qwen_xml",
        layer_class_path="vllm.model_executor.models.qwen3_5.Qwen3_5DecoderLayer",
        vllm_max_model_len=131072,
        vllm_gpu="H100",
        vllm_tp=1,
        vllm_enforce_eager=True,
    ),

    # ---------------- Ministral-8B — medium portability test -------------
    "ministral-8b": ModelPreset(
        name="ministral-8b",
        hf_id="mistralai/Ministral-8B-Instruct-2410",
        family="mistral",
        mode="standard",
        d_model=4096,
        n_layers=36,
        n_attn_heads=32,
        n_kv_heads=8,
        stride=3,
        rank=32,
        margin_base=0.5,
        v_scale_init=1.0,
        lr_phase_a=1e-4,
        lr_phase_b=3e-4,
        lr_phase_d=3e-5,
        belief_window=512,
        chat_format="mistral_inst",
        tool_format="mistral_tool_calls",
        # TBD — verify in Phase 2a. Mistral models register as their own
        # arch in vLLM (MistralForCausalLM / MistralDecoderLayer).
        layer_class_path="vllm.model_executor.models.llama.LlamaDecoderLayer",
        vllm_max_model_len=32768,
        vllm_gpu="H100",
        vllm_tp=1,
        vllm_enforce_eager=True,
    ),

    # ---------------- Qwen3-30B-A3B-Thinking — large + thinking ----------
    "qwen3-30b-a3b-thinking": ModelPreset(
        name="qwen3-30b-a3b-thinking",
        hf_id="Qwen/Qwen3-30B-A3B-Thinking-2507",
        family="qwen3_moe",
        mode="thinking",
        d_model=2048,  # per-attention d_model (MoE experts separate)
        n_layers=48,
        n_attn_heads=32,
        n_kv_heads=4,
        stride=3,
        rank=32,
        margin_base=1.0,
        v_scale_init=1.0,
        lr_phase_a=1e-4,
        lr_phase_b=3e-4,
        lr_phase_d=3e-5,
        belief_window=512,
        chat_format="chatml",
        tool_format="qwen_xml",
        # TBD — verify in Phase 3a. Likely Qwen3MoeDecoderLayer.
        layer_class_path="vllm.model_executor.models.qwen3_moe.Qwen3MoeDecoderLayer",
        vllm_max_model_len=32768,
        vllm_gpu="H100:2",
        vllm_tp=2,
        vllm_enforce_eager=True,
    ),

    # ---------------- Qwen3.6-35B-A3B — 2026-04-23 release ---------------
    # Hybrid DeltaNet/full-attention (10 of 40 layers are full attention,
    # indices 3,7,11,...,39). MoE 256 experts / 8 active + 1 shared.
    # Unified thinking+standard: default=thinking, toggle via
    # enable_thinking=False on the tokenizer.
    "qwen3.6-35b-a3b": ModelPreset(
        name="qwen3.6-35b-a3b",
        hf_id="Qwen/Qwen3.6-35B-A3B",
        family="qwen3_moe",
        mode="thinking",  # default; toggle via adapter.apply_chat_template enable_thinking=False
        d_model=2048,
        n_layers=40,
        n_attn_heads=16,   # full-attention layers only
        n_kv_heads=2,      # full-attention layers only
        # Hybrid model (DeltaNet:FullAttn at 3:1). hexis/model_hybrid.py
        # patches both layer types uniformly. stride=3 matches the recipe's
        # pattern for the sibling Qwen3.5-4B and gives 14 patched layers
        # (of 40 total), a balanced mix of full-attn and DeltaNet.
        stride=3,
        full_attention_interval=4,
        rank=32,
        margin_base=1.0,
        v_scale_init=1.0,
        lr_phase_a=1e-4,
        lr_phase_b=3e-4,
        lr_phase_d=3e-5,
        belief_window=512,
        chat_format="chatml",
        tool_format="qwen_xml",
        # TBD — verify in Phase 3a. Class is likely shared with Qwen3.5 MoE
        # per HF config reuse (model_type=qwen3_5_moe on this model).
        layer_class_path="vllm.model_executor.models.qwen3_5_moe.Qwen3_5MoeDecoderLayer",
        # 262K native context, but bumping the plugin workload there would
        # be gratuitous for tau-bench. Start at 32K, raise if trajectories
        # overrun.
        vllm_max_model_len=32768,
        # 35B MoE with 3B active still needs a big host. H100:4 is the
        # safe default; tighten to H100:2 + aggressive quant if tight.
        vllm_gpu="H100:4",
        vllm_tp=4,
        vllm_enforce_eager=True,
    ),
}


def list_presets() -> list[str]:
    return sorted(PRESETS.keys())


def register_preset(preset: ModelPreset) -> None:
    """Register a new preset at runtime. Used for experimentation.
    For production entries, prefer editing this file directly.
    """
    if preset.name in PRESETS:
        raise ValueError(f"preset {preset.name!r} already registered")
    PRESETS[preset.name] = preset
