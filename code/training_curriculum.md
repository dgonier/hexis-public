# HEXIS Training Curriculum — Complete Reproducible Recipe

Last updated: 2026-03-26

## Base Model

All versions v15+ use **Qwen3.5-4B-Base** (hybrid DeltaNet + full attention).
- d_model: 2560, n_layers: 32 (24 DeltaNet + 8 full attention)
- Full attention at layers: [3, 7, 11, 15, 19, 23, 27, 31]
- Patching stride: 3 → 11 patched layers [0, 3, 6, 9, 12, 15, 18, 21, 24, 27, 30]

v22 scaled to **Qwen3.5-27B** (d_model: 5120, n_layers: 64, stride: 3 → 22 patched layers).

## Module Architecture

| Module | Purpose | Params (4B) | Params (27B) |
|--------|---------|-------------|--------------|
| PhiNodeWriter | experience → node embedding delta | ~1.4M | ~1.4M (d_model-dependent) |
| ConvictionReader | tree state → predicted credence | ~9K | ~9K |
| MStateReadHead | embeddings → per-layer M_A, M_B | ~116M | ~930M |
| BeliefTreeMemory | GNN message passing on tree | ~0.8M | ~0.8M |
| VModulationProjector | hidden states → per-layer E_A, E_B | ~246M | (not yet on 27B) |
| NeuralRanker | belief + query → relevance | ~2.6M | ~2.6M |
| DirectionInjector | d* injection (FROZEN buffers) | 0 | 0 |

## Data

- **Training topics**: 174 (12 TRAIN_TOPICS + 162 TRAIN_200)
- **Held-out topics**: 24 (6 HELD_OUT_TOPICS + 18 HELD_OUT_200)
- **Sycophancy golds**: 44 (from Claude Sonnet 4.6 via OpenRouter)
- **Strategy tasks**: 14 ALFWorld scenarios (hand-crafted)
- Source files: `qkvm/data_200_topics.py`, `scripts/train_amplifier_v6_ppl.py`

---

## PHASE A: Content Encoding (v15 → v21.4)

### Step 0: d* Extraction (no training)
```
Script:   scripts/extract_d_star.py
Input:    20+ topics with pro/con stances
Output:   checkpoints/d_star.pt (per-layer unit vectors, d_model dim)
Method:   d*_L = normalize(mean(pro_activations_L) - mean(con_activations_L))
Time:     ~5 min on GPU
Validate: 77-81% held-out ranking accuracy at scale=0.50
```

### Step 1: v21 — Base Content Training
```
Script:   scripts/train_v21.py
Losses:   L_margin = ReLU(NTP_M - NTP_baseline + 0.3)
Epochs:   100
LR:       1e-4
Trainable: phi + btm + m_read_head + conviction_reader (ALL from scratch)
Data:     174 topics × 2 sides, 16 topics/epoch
Output:   checkpoints/v21/v21_epoch99_v21.pt
```

### Step 2: v21.1 — Conviction Calibration
```
Script:   scripts/train_v21_1.py
Losses:   L_margin(0.3) + L_align(MSE) + L_content(0.1)
          λ_align=1.0, λ_content=0.5
Epochs:   125
Warm-start: v21 epoch 99 (ALL modules)
Output:   checkpoints/v21_1/v21_1_epoch124_v21_1.pt
```

### Step 3: v21.2 — Ranking Loss
```
Script:   scripts/train_v21_2.py
Losses:   L_rank(0.1) + L_content(0.1) + L_align
          λ_content=0.5, λ_align=1.0
Epochs:   100
Warm-start: v21.1 epoch 124
Output:   checkpoints/v21_2/v21_2_epoch99_v21_2.pt
```

### Step 4: v21.4 — M Retrained WITH Beliefs
```
Script:   scripts/train_v21_4.py
Losses:   L_margin = ReLU(NTP_M+beliefs+d* - NTP_beliefs+d* + 0.1)
          Baseline includes belief XML — M must add value ABOVE beliefs
Epochs:   25
Warm-start: v21.2 (phi + btm + conviction FROZEN, m_read_head FRESH)
Prompt:   Conviction-word XML
Output:   checkpoints/v21_4/v21_4_epoch24_v21_4.pt  ← PRIMARY 4B CHECKPOINT
```

**Total Phase A: ~350 epochs across 4 steps.**
This checkpoint contains: phi_writer, conviction_reader, m_read_head, btm_template.
All subsequent v23 work builds on this.

---

## PHASE B: Compiled V-Modulation (v23)

### Step 5: v23 V-mod v2 — Debate Content Compilation
```
Script:   qkvm/compiled_belief_training.py
          --epochs 100 --margin 1.0 --lr 3e-4 --v_checkpoint None
          --run_name v23_compiled_v2
Losses:   L = ReLU(NTP_compiled - NTP_bare + 1.0)
          compiled Q+V (no beliefs in prompt) must beat bare baseline
New module: VModulationProjector (d_model→256→d_model*rank bottleneck)
Epochs:   100 (converges ~epoch 24)
v_scale init: 1.0
Belief window: 512 tokens (fixed, padded)
Trainable: VModulationProjector ONLY (phi/btm/mr frozen from v21.4)
Warm-start: None (fresh VModulationProjector)
Output:   checkpoints/v23_compiled_v2/v23_compiled_v2_epoch24.pt  ← V-MOD CHECKPOINT
Result:   4/4 correct pro stance with zero beliefs in prompt
```

### Step 5b: v23 V-mod v3 — Beat Beliefs Baseline (optional, aggressive)
```
Script:   qkvm/compiled_belief_training.py
          --epochs 100 --margin 0.3 --lr 1e-4
          --v_checkpoint checkpoints/v23_compiled_v2/v23_compiled_v2_epoch24.pt
          --run_name v23_compiled_v3
Losses:   L = ReLU(NTP_compiled - NTP_beliefs_in_prompt + 0.3)
          compiled must beat having beliefs explicitly in context
Warm-start: v23 v2 epoch 24
Output:   checkpoints/v23_compiled_v3/v23_compiled_v3_epoch99.pt
Result:   17/24 train wins. Held-out similar to v2.
Note:     v2 is preferred — v3 didn't improve held-out despite harder training.
```

---

## PHASE C: Domain-Specific Adaptation (v23)

### Step 6: Strategy V-mod — ALFWorld
```
Script:   scripts/train_v23_strategy.py
Losses:   L = ReLU(NTP_compiled_strategy - NTP_bare + 1.0)
Data:     10 hand-crafted ALFWorld strategy scenarios
Epochs:   30 (best at epoch 9)
Warm-start: v23 v2 (debate V-mod)
Trainable: VModulationProjector only
Output:   checkpoints/v23_strategy/v23_strategy_epoch9.pt
Note:     V-mod for strategy XML. Eliminates think-mode on task prompts.
```

### Step 7: Strategy Q-mod — ALFWorld
```
Script:   scripts/train_v23_strategy_qmod.py
Losses:   L = ReLU(NTP_Q_mod_strategy - NTP_bare + 0.5)
Data:     14 ALFWorld action scenarios (task → correct first action)
Epochs:   30 (best at epoch 9)
Warm-start: v21.4 m_read_head
Trainable: m_read_head only
Output:   checkpoints/v23_strategy_qmod/v23_qmod_epoch9.pt
Note:     Q-mod for ALFWorld. HURTS action selection — do NOT use for ALFWorld generation.
          M's value for ALFWorld is CURATION (picking beliefs), not MODULATION.
```

### Step 8: Neural Ranker — Within-Domain Curation
```
Script:   scripts/v23_ranker_comparison.py (generates training data + trains)
Model:    NeuralRanker (d_model*2 → 128 → 128 → 1)
Data:     170 (belief, query, relevant?) triples from tree structure
Epochs:   30
Output:   checkpoints/v23_ranker/neural_ranker.pt (~2.6M params)
Result:   P@5 = 0.73 within-domain, used as second stage after M domain filter
```

---

## PHASE D: Sycophancy Training (v23)

### Step 9: Gold Response Generation
```
Script:   scripts/generate_sycophancy_golds.py
Model:    Claude Sonnet 4.6 via OpenRouter
Data:     44 (belief, challenge, gold_response) triples
          4 topics × 5 pressure levels × ~2 variations
Cost:     ~$1-2
Output:   results/sycophancy_golds.json
Quality:  Responses reference evidence, address specific challenges, no repetition
```

### Step 10: Sycophancy M Training
```
Script:   scripts/train_v23_sycophancy.py
Losses:   L_gold = ReLU(NTP_M(gold) - NTP_bare(gold) + 0.3)
          L_no_repeat = ReLU(NTP_M(gold) - NTP_M(repetition) + 0.1)
          L = L_gold + 1.0 * L_no_repeat
Data:     44 gold challenge-response pairs
Epochs:   50
LR:       3e-5
Warm-start: v21.4 m_read_head
Trainable: m_read_head only
Output:   checkpoints/v23_sycophancy/v23_syco_epoch{9,19,...}.pt
Result:   Fixes verbatim repetition → engaged defense (4/5 levels working at epoch 9)
```

---

## PHASE E: Scale to 27B (v22)

### Step 11: v22 d* on 27B
```
Script:   scripts/train_v22_modal.py --step dstar
GPU:      H100 (Modal)
Model:    Qwen/Qwen3.5-27B
Output:   Modal volume qkvm-data:/v22_output/d_star_27b.pt
```

### Step 12: v22.2 Full Curriculum on 27B
```
Script:   scripts/train_v22_2_modal.py
GPU:      H100:2 (Modal)
5 phases: same as Steps 1-4 but with aggressive margins (1.0 for phases 1-3, 0.5 for 4-5)
          + functional contrastive loss in phase 5
Total:    ~250 epochs, ~10 hours, ~$65
Output:   Modal volume qkvm-data:/v22_2_output/checkpoints/v22_2_phase5_epoch69_v22_2_27b.pt
HF:       dgonier/qkvm-v22-27b/v22_2_final.pt
Result:   A=130t B=127t D=52t. Think: A=4/4 B=4/4 D=0/4.
Note:     F-sim collapse (0.99) — M is universal style modulator, not topic-specific.
          V-mod not yet trained on 27B.
```

---

## Current Best Checkpoints (4B)

| Purpose | Checkpoint | What it contains |
|---------|-----------|------------------|
| Q-mod (debate) | `v21_4/v21_4_epoch24_v21_4.pt` | phi + btm + mr + conviction_reader |
| V-mod (debate) | `v23_compiled_v2/v23_compiled_v2_epoch24.pt` | VModulationProjector |
| Q-mod (sycophancy) | `v23_sycophancy/v23_syco_epoch9.pt` | m_read_head only |
| V-mod (strategy) | `v23_strategy/v23_strategy_epoch9.pt` | VModulationProjector |
| Q-mod (strategy) | `v23_strategy_qmod/v23_qmod_epoch9.pt` | m_read_head only |
| Neural ranker | `v23_ranker/neural_ranker.pt` | NeuralRanker classifier |
| d* vectors | `d_star.pt` | per-layer direction vectors |
| Zero points | `topic_zero_points.pt` | per-topic ambivalence scales |

## Current Best Checkpoints (27B)

| Purpose | Location | What it contains |
|---------|----------|------------------|
| Full curriculum | HF `dgonier/qkvm-v22-27b/v22_2_final.pt` | phi + btm + mr + conviction_reader |
| d* vectors | Modal volume `qkvm-data:/v22_output/d_star_27b.pt` | per-layer direction vectors |

---

## Key Lessons for Reproducibility

1. **Margin scaling**: 4B needs margin=0.3-0.5. 27B needs margin=1.0. Too easy → loss=0, no gradient.
2. **V-mod v_scale**: Train at 1.0, not 0.3. Lower init produces correct direction but insufficient magnitude.
3. **Curriculum warm-start**: Each step builds on previous. Can't skip. Fresh M-read head in step 4 is intentional.
4. **Action matcher**: ALFWorld uses "move" not "put". Critical for benchmarks.
5. **Sycophancy**: Without gold training, M produces verbatim repetition. 44 gold responses from Sonnet 4.6 fix it in 9 epochs.
6. **Compiled M for action selection**: HURTS constrained tasks (ALFWorld -13pp). M's value there is curation, not modulation.
7. **F-sim collapse**: Both 4B and 27B show 0.99 F-sim with MStateReadHead. M is a universal style modulator. Content differentiation comes from beliefs in prompt.

## Files Index

### Training Scripts
- `scripts/train_v21.py` — Phase A Step 1
- `scripts/train_v21_1.py` — Phase A Step 2
- `scripts/train_v21_2.py` — Phase A Step 3
- `scripts/train_v21_4.py` — Phase A Step 4
- `qkvm/compiled_belief_training.py` — Phase B Steps 5/5b
- `scripts/train_v23_strategy.py` — Phase C Step 6
- `scripts/train_v23_strategy_qmod.py` — Phase C Step 7
- `scripts/v23_ranker_comparison.py` — Phase C Step 8
- `scripts/generate_sycophancy_golds.py` — Phase D Step 9
- `scripts/train_v23_sycophancy.py` — Phase D Step 10
- `scripts/train_v22_modal.py` — Phase E Step 11
- `scripts/train_v22_2_modal.py` — Phase E Step 12

### Modules
- `qkvm/phi_node_writer.py` — PhiNodeWriter
- `qkvm/conviction_reader.py` — ConvictionReader
- `qkvm/mstate_read_head.py` — MStateReadHead
- `qkvm/belief_tree_memory.py` — BeliefTreeMemory + GNN
- `qkvm/compiled_belief_training.py` — VModulationProjector
- `qkvm/belief_rankers.py` — KeywordRanker, EmbeddingRanker, NeuralRanker
- `qkvm/direction_injector.py` — DirectionInjector (d*)
- `qkvm/jeffrey_update.py` — Jeffrey conditionalization
- `qkvm/universal_schema.py` — MemoryTree, MemoryNode, Support
- `qkvm/reflector.py` — Reflector (self/openai/openrouter/bedrock)
- `qkvm/belief_compiler.py` — BeliefCompiler + CompiledMState
- `qkvm/argument_curator.py` — ArgumentCurator
- `qkvm/zone_aware_modulation.py` — Zone-specific M scaling (obsoleted by compilation)
- `qkvm/bidirectional_beliefs.py` — Bidirectional belief attention (no effect found)

### Eval Scripts
- `scripts/eval_v23_zone_aware.py` — Zone scaling ablation (no effect)
- `scripts/eval_v23_bidirectional.py` — Bidirectional beliefs (no effect)
- `scripts/v23_attention_playground.py` — Weighted attention + M-only experiments
- `scripts/v23_compiled_m.py` — Compiled M conditions (B vs D vs C)
- `scripts/v23_full_architecture_eval.py` — A/B/D/C/F with latency + VRAM
- `scripts/v23_paper_eval.py` — Full paper evaluation suite
- `scripts/v23_sycophancy_5level.py` — 5-level sycophancy benchmark
- `scripts/v23_noisy_curation_test.py` — 100-node noisy curation test
- `scripts/v23_ranker_comparison.py` — Keyword vs embedding vs neural ranker
- `scripts/eval_v22_modal.py` — A/B/D eval on 27B (Modal)
