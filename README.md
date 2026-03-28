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

```bash
# 1. Extract d* direction vectors (~5 min)
python code/scripts/extract_d_star.py --model Qwen/Qwen3.5-4B-Base

# 2. Train base M (~2 hours)
python code/scripts/train_v21.py --model Qwen/Qwen3.5-4B-Base --epochs 50

# 3. Train M with beliefs (~30 min)
python code/scripts/train_v21_4.py --checkpoint checkpoints/v21/BEST.pt --epochs 25

# 4. Evaluate
python code/scripts/v23_paper_eval.py
```

See `code/M_canonical_recipe.md` for the full reproducibility guide.

## Base Model

All experiments use **Qwen3.5-4B-Base** (hybrid DeltaNet + full attention, 32 layers, d=2560).
The host model is completely frozen — only the enmeshed modules (~367M params) are trained.

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
