from .config import QKVMConfig
from .model import (
    QModulator, VModulator, WriteFunction, StochasticWriteFunction,
    CoupledWriteFunction, patch_model, patch_model_coupled,
)
from .model_multi_gpu import (
    patch_model_coupled_multi_gpu,
    init_memory_multi_gpu, init_e_memory_multi_gpu,
    set_memory_multi_gpu, set_e_memory_multi_gpu,
    clear_memory_multi_gpu, clear_e_memory_multi_gpu,
    detach_memory_multi_gpu, detach_e_memory_multi_gpu,
    forward_with_coupled_update_multi_gpu,
)
from .memory import (
    init_memory, set_memory, clear_memory, detach_memory,
    memory_norm, forward_with_memory_update, flatten_memory,
    compute_e_from_delta, set_e_memory, clear_e_memory,
    init_e_memory, detach_e_memory, forward_with_coupled_update,
    clamp_memory_norm, clamp_memory_norm_differentiable,
    scale_memory,
)
from .data import MINDSETS, TEST_PROMPTS, HELD_OUT_PROMPTS, tokenize, build_training_pairs
from .data_diagnostic_mindsets import DIAGNOSTIC_MINDSETS, DIAGNOSTIC_PROMPTS
from .losses import ntp_loss, contrastive_memory_loss, combined_loss, norm_regularization_loss
from .eval import evaluate_carryover, evaluate_no_memory, compute_ppl_matrix
from .generation import (
    generate_with_mindset, generate_without_memory,
    generate_with_seed, build_seed, interpolate_seeds,
    build_custom_seed, build_custom_seed_coupled,
    accumulate_sessions_coupled,
    record_belief, compose_perspective,
    generate_with_coupled_seed, generate_base,
)

__version__ = "0.9.0"
