# M Canonical Recipe — Building HEXIS on a New Model

**Last updated: 2026-03-26**

This document is the single source of truth for reproducing the HEXIS M-state system on any new base model. A developer with access to this repo and a GPU should be able to follow these instructions and get a working system.

---

## Prerequisites

- Base model: any causal LM from HuggingFace (tested on Qwen3.5-4B-Base, Qwen3.5-27B)
- GPU: 24GB+ for ≤9B models, 80GB+ (or 2×80GB) for 27B+
- Python 3.11+, PyTorch 2.4+, transformers 4.50+
- This repo: `git clone https://github.com/dgonier/unconscious-memory && pip install -e .`

### Datasets (HuggingFace)

- **Training topics**: Built into `qkvm/data_200_topics.py` (162 train + 20 held-out) and `scripts/train_amplifier_v6_ppl.py` (12 train + 6 held-out)
- **Sycophancy golds**: `dgonier/hexis-training-data/sycophancy_golds.json` (44 challenge-response pairs from Claude Sonnet 4.6)
- **Credence golds**: `dgonier/hexis-training-data/gold_credence_responses.json` (1044 responses from GPT-4o)
- **Checkpoints (4B)**: Local at `checkpoints/v21_4/`, `checkpoints/v23_compiled_v2/`, etc.
- **Checkpoints (27B)**: HuggingFace `dgonier/qkvm-v22-27b`

---

## Step 0: Know Your Model

Before anything else, extract these from your target model:

```python
from transformers import AutoConfig
config = AutoConfig.from_pretrained("YOUR_MODEL", trust_remote_code=True)
tc = config.text_config if hasattr(config, "text_config") else config

D_MODEL = tc.hidden_size          # e.g., 2560 (4B), 4096 (9B), 5120 (27B)
N_LAYERS = tc.num_hidden_layers   # e.g., 32 (4B/9B), 64 (27B)

# For hybrid models (Qwen3.5), check layer types:
if hasattr(tc, "layer_types"):
    FA_LAYERS = [i for i, t in enumerate(tc.layer_types) if t == "full_attention"]
    # e.g., [3,7,11,15,19,23,27,31] for 4B
```

### Scaling Rules

| Parameter | Formula | 4B | 9B | 27B |
|-----------|---------|-----|-----|------|
| d_model | from config | 2560 | 4096 | 5120 |
| n_layers | from config | 32 | 32 | 64 |
| stride | 3 (must include full attn layers) | 3 | 3 | 3 |
| patched_layers | range(0, n_layers, stride) | 11 | 11 | 22 |
| **rank** | 16 for ≤4B, 32 for >4B | 16 | 32 | 32 |
| d_node | 128 (fixed) | 128 | 128 | 128 |
| V-mod bottleneck | 256 (fixed) | 256 | 256 | 256 |
| max_norm | 1.5 (fixed) | 1.5 | 1.5 | 1.5 |
| belief_window | 512 tokens (fixed) | 512 | 512 | 512 |

**Rank scaling**: rank/d_model ratio should stay ~0.006. At d_model=2560, rank=16 (ratio=0.00625). At d_model=5120, rank=32 (ratio=0.00625). Going higher (rank=64) is safe but increases params.

**Stride**: MUST be chosen so patched layers include some full-attention layers. For Qwen3.5 with 3:1 DeltaNet:Attention ratio, stride=3 works at all sizes. stride=4 on 64-layer models misses ALL full attention layers — don't do this.

**Margin scaling**: Larger models need larger margins. 4B: margin=0.3-0.5. 27B: margin=1.0. The model is more capable → M beats baseline more easily → need harder target.

---

## Step 1: Extract d* Direction Vectors (~5 min)

d* encodes the pro/con direction from base model activations. No training needed.

```bash
python scripts/extract_d_star.py --model YOUR_MODEL --stride 3
```

**What it does**: For 20+ topics, runs pro and con stances through the model, extracts hidden states at patched layers, computes `d* = normalize(mean(pro) - mean(con))`.

**Output**: `checkpoints/d_star.pt` — dict of `{layer_idx: unit_vector(d_model,)}`

**Validate**: Run `scripts/probe_rep_engineering.py` — should get 77-81% held-out ranking accuracy.

---

## Step 2: Train Phase A — Content Encoding (~6 hours on 4B)

This is a 4-step curriculum that teaches phi to encode experiences and M to produce useful Q-modulation.

### Step 2a: Base Content (v21)
```bash
python scripts/train_v21.py \
    --model YOUR_MODEL --epochs 100 --margin 0.3 \
    --run_name v21_YOUR_MODEL
```
- **Loss**: L_margin = ReLU(NTP_M - NTP_baseline + margin)
- **Trainable**: ALL (phi + btm + m_read_head + conviction_reader)
- **From scratch**: No warm-start
- **Watch for**: M wins should reach 90%+ by epoch 50. If not, increase epochs or check d_model compatibility.

### Step 2b: Conviction Calibration (v21.1)
```bash
python scripts/train_v21_1.py \
    --model YOUR_MODEL --checkpoint checkpoints/v21/BEST.pt \
    --epochs 125 --margin 0.3
```
- **Loss**: L_margin + L_align(MSE, λ=1.0) + L_content(margin=0.1, λ=0.5)
- **Warm-start**: ALL modules from Step 2a

### Step 2c: Ranking (v21.2)
```bash
python scripts/train_v21_2.py \
    --model YOUR_MODEL --checkpoint checkpoints/v21_1/BEST.pt \
    --epochs 100
```
- **Loss**: L_rank(margin=0.1) + L_content(margin=0.1, λ=0.5) + L_align(λ=1.0)
- **Warm-start**: ALL modules from Step 2b

### Step 2d: M with Beliefs (v21.4)
```bash
python scripts/train_v21_4.py \
    --model YOUR_MODEL --checkpoint checkpoints/v21_2/BEST.pt \
    --epochs 25 --margin 0.1
```
- **Loss**: L_margin with beliefs+d* as baseline (not bare)
- **CRITICAL**: m_read_head is **FRESH INIT**. phi + btm + conviction are **FROZEN** from Step 2c.
- **This teaches M to amplify beliefs, not substitute for them.**

**Output**: `checkpoints/v21_4/BEST.pt` — this is your **primary Q-mod checkpoint**.

---

## Step 3: Train Phase B — Compiled V-Modulation (~3 hours)

Teaches V-mod to carry belief content through the rank bottleneck so beliefs don't need to be in the prompt.

```bash
python qkvm/compiled_belief_training.py \
    --model YOUR_MODEL \
    --checkpoint checkpoints/v21_4/BEST.pt \
    --epochs 100 --margin 1.0 --lr 3e-4 \
    --run_name v23_compiled_v2
```

- **Loss**: L = ReLU(NTP_compiled_QV - NTP_bare + margin)
- **New module**: VModulationProjector (d_model → 256 → d_model×rank)
- **v_scale init**: 1.0 (NOT 0.3 — too conservative)
- **Trainable**: VModulationProjector ONLY (everything else frozen)
- **Belief window**: 512 tokens, padded

**Output**: `checkpoints/v23_compiled_v2/BEST.pt` — your **V-mod checkpoint**.

**Validate**: Run compiled-only (no beliefs in prompt) on held-out topics. Should get 3-4/5 correct pro stance.

---

## Step 4: Train Phase D — Sycophancy Training (~4 hours)

Fixes the verbatim repetition problem — teaches M to engage with challenges using evidence.

### Step 4a: Generate Gold Responses
```bash
python scripts/generate_sycophancy_golds.py
```
- Uses Claude Sonnet 4.6 via OpenRouter (~$1-2)
- Or download from `dgonier/hexis-training-data/sycophancy_golds.json`
- 44 (belief, challenge, gold_response) triples across 5 pressure levels

### Step 4b: Train
```bash
python scripts/train_v23_sycophancy.py
```
- **Loss**: L_gold(margin=0.3) + L_no_repeat(margin=0.1, λ=1.0)
- **Warm-start**: m_read_head from v21.4
- **Trainable**: m_read_head only
- **Epochs**: 50 (effective at epoch 9)

**Output**: `checkpoints/v23_sycophancy/BEST.pt` — **sycophancy Q-mod checkpoint**.

---

## Step 5 (Optional): Domain-Specific Adaptation

For specific use cases (ALFWorld, user preferences, etc.), additional fine-tuning:

### Neural Ranker (for noisy belief curation)
```bash
python scripts/v23_ranker_comparison.py
```
- Trains a tiny classifier (2.6M params) for within-domain belief ranking
- Used as second stage after M's domain filtering

### Strategy V-mod (for task execution)
```bash
python scripts/train_v23_strategy.py
```
- Fine-tunes V-mod on task strategy XML
- 10 hand-crafted scenarios, 30 epochs

---

## Mind Tree Schema

The Mind Tree (`qkvm/mind_schema.py`) is a typed cognitive schema. Node types map to cognitive functions:

| Section | Cognitive Function | M Compiles To | Slot Provides |
|---------|-------------------|---------------|---------------|
| identity | self-model | voice, register, framing | rarely needed |
| beliefs | epistemic | stance direction, emphasis | evidence, citations |
| strategies | procedural | approach tendency | specific tactics |
| memories | episodic | experiential tone | specific details, names |
| models | theory of mind | awareness of opposition | predicted arguments |
| values | axiological | deep dispositional bias | rarely needed |

### Curation Pipeline (`qkvm/mind_processor.py`)

M and the XML parser are two halves of one curation system:

```
Mind Tree (500-2000 tokens)
    │
    │  M reads abstract layer only (~300 tokens)
    │  (beliefs, strategies, memories, models — NOT evidence/tactics/details)
    │
    ├──→ Compiled Q/V tensors (disposition channel)
    ├──→ Per-node activation scores (selection signal)
    │
    │  Deterministic graph walk from M's activated parents
    │  (filters by node properties + query intent)
    │
    ├──→ Curated slot (evidence, tactics, details — novel content)
    └──→ Expansion reserve (available via tool call)
```

M provides the soft signal: which nodes resonated, which domains are active.
Parser provides the hard signal: which nodes structurally match the query type.

Each node has `addresses` (query types it answers), `novel` (won't survive compilation),
`domain` (topic domains), `conviction` (argument strength), `salience` (compilation priority).

### Key Design Principle

M only sees abstract nodes. Evidence, tactics, details are NEVER sent to M — they're
selected deterministically based on which PARENT M activated + query intent matching on
`addresses` properties.

---

## Deployment Architecture

### For open-ended generation (debate, preferences, persuasion):
```
Compiled M (Q+V hooks) + curated slot + question
→ Confident, belief-grounded generation with specific evidence
```
Use: v21.4 Q-mod + v23 V-mod + MindTreeProcessor

### For constrained action selection (ALFWorld, tool use):
```
M-curated slot (no Q/V hooks during generation) + question
→ Strategy-grounded action selection
```
Use: M for curation only (domain filter + graph walk), tactics in prompt.
M's Q/V modulation HURTS constrained tasks. M's curation is valuable.

### For sycophancy resistance:
```
Sycophancy Q-mod + beliefs in prompt + challenge
→ Engaged defense referencing evidence
```
Use: v23 sycophancy Q-mod

### The local server (`scripts/serve_local.py`):
```bash
python scripts/serve_local.py  # port 8234
# Supports persona activation, tree creation, reflection, compiled M
```

---

## Things to Consider for New Models

### Architecture Compatibility
- **Standard transformers** (Llama, Mistral): Works directly. All layers are full attention.
- **Hybrid models** (Qwen3.5): Works. Stride must include full attention layers.
- **MoE models** (Qwen3-30B-A3B): Works but needs `device_map="auto"` for multi-GPU. All hook tensors must `.to(x.device)`.
- **Very large models** (70B+): Needs tensor parallelism. vLLM hooks don't work with TP>1 on vLLM v0.18+.

### Hyperparameter Adjustments
- **Margin**: Scale with model capability. If loss hits 0 in epoch 1, double the margin.
- **Learning rate**: 1e-4 for Phase A, 3e-4 for V-mod, 3e-5 for sycophancy. Reduce if training unstable.
- **Rank**: 16 for d_model≤2560, 32 for d_model≤5120, 64 for larger. More rank = more capacity but more params.
- **v_scale**: Always train at 1.0. If generation is too aggressive, reduce at inference.

### Multi-GPU Gotchas
- `device_map="auto"` shards model across GPUs
- M hooks must `.to(x.device, x.dtype)` for BOTH M_A/M_B AND mod_scale
- DirectionInjector conviction must `.to(attn_output.device)`
- `total_memory` not `total_mem` for CUDA device properties

### Common Failures
- **Loss = 0 from epoch 1**: Margin too easy. Increase margin.
- **M-state norms all at 1.5**: max_norm clamp saturated. Normal — direction is learned, magnitude is clamped.
- **Verbatim repetition under pressure**: Need sycophancy training (Phase D).
- **F-sim collapse (0.99)**: Normal for MStateReadHead. M is a style modulator, not topic-specific.
- **Action matcher failures on ALFWorld**: "put" → "move" normalization needed.

### What NOT to Do
- Don't use stride=4 on 64-layer Qwen3.5 (misses all full attention layers)
- Don't use v_scale=0.3 for V-mod training (too conservative, needs 3.3x at inference)
- Don't use compiled M hooks for constrained action selection (hurts performance)
- Don't skip Phase A step 2d (fresh m_read_head) — without it, M substitutes for beliefs instead of amplifying them

---

## Verification Targets

After completing the full pipeline, verify:

| Test | Target | Script |
|------|--------|--------|
| d* held-out ranking | >77% | `scripts/probe_rep_engineering.py` |
| D vs B token ratio | <0.6 | `scripts/v23_paper_eval.py` |
| D think-mode rate | 0% | `scripts/v23_paper_eval.py` |
| F compiled stance accuracy | ≥3/5 | `scripts/v23_compiled_m.py` |
| F dilution at 4000 tokens | 100% | `scripts/v23_paper_eval.py` |
| Sycophancy engagement (not repetition) | 4/5 levels | Manual inspection |
| M domain filter precision | 100% on 100-node test | `scripts/v23_noisy_curation_test.py` |
| Neural ranker P@5 | >0.7 | `scripts/v23_ranker_comparison.py` |

---

## Quick Start (minimum viable HEXIS)

If you just want the core M-state system without all the bells and whistles:

```bash
# 1. Extract d* (~5 min)
python scripts/extract_d_star.py --model Qwen/Qwen3.5-4B-Base

# 2. Train base M (~2 hours, can stop early)
python scripts/train_v21.py --model Qwen/Qwen3.5-4B-Base --epochs 50

# 3. Train M with beliefs (~30 min)
python scripts/train_v21_4.py --checkpoint checkpoints/v21/BEST.pt --epochs 25

# 4. Test
python scripts/v23_paper_eval.py  # Should see D beating B on token count + confidence
```

This gives you the core Q-modulation. Add V-mod (Step 3) for compiled beliefs, sycophancy training (Step 4) for engaged defense, and the neural ranker (Step 5) for noisy curation.
