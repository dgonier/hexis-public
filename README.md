# HEXIS: Compiled Dispositional Memory Through Enmeshed Networks

**Paper**: [NeurIPS 2026 submission](paper/main_v2.pdf)

## Overview

HEXIS introduces **enmeshed networks** — a new architectural primitive where a lightweight parametric module shares the forward pass of a frozen host model, reading and writing intermediate representations at each layer. Unlike adapters (gradient descent per adaptation), side-tuning (output-only fusion), or activation steering (fixed directions), enmeshed networks create a *parallel context channel* that compiles experience into modulation tensors at inference cost.

Key results on Qwen3.5-4B:
- **100% stance maintenance** through 4K tokens of adversarial dilution (structurally immune)
- **89% sycophancy resistance** across 5 escalating pressure levels (vs 58% baseline)
- **82% token savings** via three-layer architecture (compiled M + curated slot + expansion)
- **3% → 53%** ALFWorld task success with Mind Tree strategies

## Repository Structure

```
paper/              # NeurIPS 2026 paper
  sections/         # LaTeX source files
  figures/          # JSX source + rendered PNGs
  references.bib    # Bibliography
  main_v2.pdf       # Compiled PDF

code/
  qkvm/             # Core library (modulation, write functions, belief trees)
  scripts/          # Training scripts (Phases A-D)
  M_canonical_recipe.md    # How to reproduce HEXIS on any model
  training_curriculum.md   # Full training pipeline

results/            # Benchmark data referenced in paper
checkpoints/        # Released after acceptance
```

## Quick Start

### One-command training (new — recommended)

```bash
# Install
cd code && pip install -e .

# Train the full dispositional pipeline on any supported model
python -m hexis.train --preset qwen3.5-4b
python -m hexis.train --preset ministral-8b
python -m hexis.train --preset qwen3.6-35b-a3b

# Or just a subset
python -m hexis.train --preset ministral-8b --phases a,b,d
python -m hexis.train --preset ministral-8b --phases agentic
python -m hexis.train --preset ministral-8b --smoke    # 5-epoch smoke run

# Dry-run to preview without executing
python -m hexis.train --preset ministral-8b --dry-run
```

### Running individual scripts

```bash
# Dispositional d* extraction (~5 min)
python code/scripts/extract_d_star.py --preset qwen3.5-4b

# Phase A training (~6 hours on 4B, longer for bigger models)
python code/scripts/train_v21.py --preset qwen3.5-4b

# Phase B compiled V-mod (~3 hours)
python code/hexis/compiled_belief_training.py --preset qwen3.5-4b

# Phase D sycophancy (~1 hour)
python code/scripts/train_v23_sycophancy.py --preset qwen3.5-4b
```

### Supported models (via adapter preset)

Each preset encodes the architecture, recipe hyperparameters (rank, stride,
margin, lr), chat/tool format, and vLLM deploy config for one model:

- `qwen3.5-4b` — the paper's base model (dense, 4B, non-thinking)
- `ministral-8b` — Mistral 8B medium-scale portability
- `qwen3-30b-a3b-thinking` — Qwen3 MoE 30B thinking-mode
- `qwen3.6-35b-a3b` — Qwen3.6 MoE 35B hybrid-attention, thinking-mode default

Add a new model by registering a `ModelPreset` in `code/hexis/adapters/presets.py` — see
`code/M_canonical_recipe.md` for the hyperparameter scaling rules.

See `code/M_canonical_recipe.md` for the full reproducibility guide.

## Base Models

The paper's main results are on **Qwen3.5-4B-Base** (hybrid DeltaNet + full
attention, 32 layers, d=2560). The host model is always frozen — only the
enmeshed modules (~367M params on 4B; scales with model size) are trained.

Portability results on Ministral-8B and Qwen3.6-35B-A3B validate that HEXIS
transfers across model families and scales.

## Citation

```bibtex
@inproceedings{gonier2026hexis,
  title={HEXIS: Compiled Dispositional Memory Through Enmeshed Networks},
  author={Gonier, Devin},
  booktitle={Advances in Neural Information Processing Systems},
  year={2026}
}
```

## License

MIT
