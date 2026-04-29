"""Minimal vLLM endpoint serving Qwen3.5-4B + a LoRA adapter loaded at startup.

Used as a CONTROL endpoint to compare against the full HEXIS agentic stack on
the same tau3-bench panel. This endpoint exposes the standard OpenAI-compatible
/v1/chat/completions API. The LoRA adapter is loaded as the default; the API
applies it on every request.

Volumes:
- hexis-lora-checkpoints: holds /lora_tau2_r16/{adapter_model.safetensors, adapter_config.json}

Usage:
    modal deploy deploy/lora_only/app.py
    # then hit URL via curl as you would the HEXIS endpoint
"""
import os
import modal

MODEL_ID = "Qwen/Qwen3.5-4B"
MODEL_DIR = "/models"
LORA_NAME = "lora_tau2_r16"
LORA_PATH = f"/lora/{LORA_NAME}"

app = modal.App("hexis-lora-only-h100")
LORA_VOLUME = modal.Volume.from_name("hexis-lora-checkpoints", create_if_missing=False)
MODELS_VOLUME = modal.Volume.from_name("hexis-lora-base-models", create_if_missing=True)


def download_model():
    import os as _os_dl
    _os_dl.environ.pop("HF_HUB_OFFLINE", None)
    from huggingface_hub import snapshot_download
    snapshot_download(MODEL_ID, local_dir=MODEL_DIR)
    print(f"downloaded {MODEL_ID} -> {MODEL_DIR}")


vllm_image = (
    modal.Image.from_registry("nvidia/cuda:12.8.1-devel-ubuntu22.04", add_python="3.12")
    .pip_install(
        "vllm>=0.8.0",
        "huggingface-hub[hf_transfer]>=0.19.0",
        "fastapi[standard]>=0.100.0",
        "httpx>=0.24.0",
        "transformers>=4.52.0",
        "peft>=0.13.0",
        "boto3>=1.34.0",
        "pydantic>=2.5.0",
    )
    .env({
        "HF_HUB_ENABLE_HF_TRANSFER": "1",
    })
    .run_function(
        download_model,
        secrets=[modal.Secret.from_name("huggingface-secret")],
        volumes={MODEL_DIR: MODELS_VOLUME},
    )
)


@app.function(
    image=vllm_image,
    gpu="H100",
    timeout=60 * 60 * 4,
    volumes={
        MODEL_DIR: MODELS_VOLUME,
        "/lora": LORA_VOLUME,
    },
    min_containers=0,
    scaledown_window=60 * 5,
    secrets=[modal.Secret.from_name("huggingface-secret")],
)
@modal.concurrent(max_inputs=8)
@modal.web_server(8000, startup_timeout=60 * 10)
def serve():
    """Boot vLLM OpenAI-compatible server with LoRA pre-loaded."""
    import subprocess
    import os as _os
    _os.environ["HF_HUB_OFFLINE"] = "1"
    cmd = [
        "vllm", "serve", MODEL_DIR,
        "--host", "0.0.0.0",
        "--port", "8000",
        "--enable-lora",
        "--max-loras", "1",
        "--max-lora-rank", "16",
        "--lora-modules", f"{LORA_NAME}={LORA_PATH}",
        "--max-model-len", "16384",
        "--gpu-memory-utilization", "0.85",
        "--enforce-eager",  # avoid Dynamo/CUDA-graph compile delays on cold start
        "--served-model-name", "qwen-lora",
        "--trust-remote-code",
        # Required for tool-calling (tau-bench sends tools=[...] with auto choice)
        "--enable-auto-tool-choice",
        "--tool-call-parser", "hermes",  # qwen3.5 uses hermes-style <tool_call> format
        # Disable image inputs so vLLM skips the multimodal-encoder JIT compile
        # step that hangs at startup (Qwen3.5-4B is registered as multimodal
        # but we only do text). Costs nothing because we never send images.
        "--limit-mm-per-prompt", '{"image":0,"video":0}',
        # Use Triton GDN prefill backend (the FlashInfer one JIT-compiles for
        # 5+ min on cold start, frequently SIGINT'd by container churn before
        # it finishes).
        "--gdn-prefill-backend", "triton",
    ]
    print(f"[lora-only] launching: {' '.join(cmd)}")
    subprocess.Popen(cmd)
