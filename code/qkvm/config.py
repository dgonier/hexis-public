from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class QKVMConfig:
    # Model identity
    model_name: str = "Qwen/Qwen2.5-1.5B-Instruct"

    # Which layers get QKVM memory (every 2nd layer by default)
    qkvm_layer_stride: int = 2
    qkvm_layers: Optional[List[int]] = None  # computed from model if None

    # Memory dimensions
    memory_rank: int = 16
    write_bottleneck: int = 512

    # Memory dynamics
    memory_decay: float = 0.95
    memory_lr: float = 0.05
    max_norm: float = 1.5

    # Training
    lr: float = 2e-4
    weight_decay: float = 0.01
    epochs: int = 200
    grad_accum_steps: int = 4
    n_exposure: int = 5  # reflections per exposure

    # Contrastive (v6)
    lambda_contrast: float = 0.3
    temperature: float = 0.1
    contrastive_warmup: int = 50  # epochs before contrastive loss kicks in

    # v7.1: Norm regulation
    global_max_norm: float = 6.5        # hard ceiling on total memory_norm (M)
    lambda_norm_reg: float = 0.1        # weight for norm regularization loss
    norm_reg_target: float = 6.0        # soft target (penalty starts here)
    e_global_max_norm: float = 6.5      # hard ceiling for E state
    e_attenuation_alpha: float = 2.0    # sigmoid steepness for E suppression
    e_attenuation_threshold: float = 6.0  # M-norm level where E starts suppressing

    # Multi-GPU / deployment (v9+)
    device_map: Optional[str] = None          # None = single GPU, "auto" = multi-GPU sharding
    quantization: Optional[str] = None        # None, "4bit", "8bit" (for BnB quantization)

    # Episodic memory (v13)
    episodic_key_dim: int = 256               # dimension of content-addressable keys
    episodic_n_attn_heads: int = 4            # attention pooling heads in key encoder
    episodic_max_slots: int = 32              # max experiences per user in memory bank
    episodic_relevance_threshold: float = 0.1 # below this, no modulation applied
    lambda_retrieval: float = 2.0             # weight for retrieval accuracy loss
    lambda_irrelevance: float = 1.0           # weight for irrelevance gate loss

    # Logging
    print_every: int = 25
    checkpoint_every: int = 50

    # Derived (set after model loads)
    d_model: int = 0
    n_layers: int = 0
    n_q_heads: int = 0
    n_kv_heads: int = 0

    def init_from_model_config(self, model_config):
        """Populate derived fields from a HuggingFace model config."""
        self.d_model = model_config.hidden_size
        self.n_layers = model_config.num_hidden_layers
        self.n_q_heads = model_config.num_attention_heads
        self.n_kv_heads = model_config.num_key_value_heads

        if self.qkvm_layers is None:
            self.qkvm_layers = list(range(0, self.n_layers, self.qkvm_layer_stride))

        return self
