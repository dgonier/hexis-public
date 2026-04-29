"""Modal wrapper to fine-tune Qwen3.5-4B with LoRA on AReaL tau2 data subset.

Usage:
    modal run scripts/train_lora_tau2_modal.py
"""
import os
import modal

app = modal.App("hexis-lora-tau2")
LORA_VOLUME = modal.Volume.from_name("hexis-lora-checkpoints", create_if_missing=True)

train_image = (
    modal.Image.debian_slim(python_version="3.12")
    .pip_install(
        "torch==2.6.0",
        "transformers>=4.50.0",
        "accelerate>=0.30.0",
        "safetensors>=0.4.0",
        "peft>=0.13.0",
        "huggingface-hub[hf_transfer]>=0.19.0",
    )
    .env({"HF_HUB_ENABLE_HF_TRANSFER": "1"})
    .add_local_file(
        "/home/dgonier/experiments/scripts/train_lora_tau2.py",
        remote_path="/root/train_lora_tau2.py", copy=True,
    )
    .add_local_file(
        "/home/dgonier/experiments/data/areal_tau2/tau2_sft_1k_balanced.jsonl",
        remote_path="/root/tau2_sft_1k_balanced.jsonl", copy=True,
    )
)


@app.function(
    image=train_image,
    gpu="H200",
    timeout=60 * 60 * 3,
    volumes={"/lora": LORA_VOLUME},
    secrets=[modal.Secret.from_name("huggingface-secret")],
)
def train_lora(
    model_id: str = "Qwen/Qwen3.5-4B",
    rank: int = 16,
    epochs: int = 2,
    lr: float = 5e-5,
    batch_size: int = 1,
    out_subdir: str = "lora_tau2_r16",
):
    import sys
    sys.path.insert(0, "/root")
    import argparse
    from train_lora_tau2 import train as train_fn

    output = f"/lora/{out_subdir}"
    args = argparse.Namespace(
        model=model_id,
        data="/root/tau2_sft_1k_balanced.jsonl",
        output=output,
        rank=rank,
        epochs=epochs,
        lr=lr,
        batch_size=batch_size,
        max_length=4096,  # H200 has 140GB; 4096 covers ~58% of samples in full
    )
    train_fn(args)
    LORA_VOLUME.commit()
    print(f"[modal] adapter saved to volume hexis-lora-checkpoints:{out_subdir}")


@app.local_entrypoint()
def main(
    model: str = "Qwen/Qwen3.5-4B",
    rank: int = 16,
    epochs: int = 2,
    lr: float = 5e-5,
    out_subdir: str = "lora_tau2_r16",
):
    print(f"[local] launching tau2 LoRA: rank={rank} epochs={epochs} lr={lr}")
    train_lora.remote(
        model_id=model,
        rank=rank,
        epochs=epochs,
        lr=lr,
        out_subdir=out_subdir,
    )
    print("[local] adapter on hexis-lora-checkpoints volume.")
