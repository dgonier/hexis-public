# HEXIS Paper v2 — Section Plan for NeurIPS 2026

## Paper Identity

**Title**: HEXIS: Compiled Dispositional Memory Through Enmeshed Networks
**Contribution type**: General (or Use-Inspired)
**Base model**: Qwen3.5-4B-Base (primary), with 27B scale validation
**9 pages** main + unlimited appendix

---

## Section Budget (9 pages)

| Section | Pages | Status |
|---------|-------|--------|
| Abstract | 0.3 | REWRITE needed — align with enmeshed network framing |
| 1. Introduction | 1.2 | REWRITE needed — butcher analogy + enmeshed network primitive |
| 2. Enmeshed Networks | 1.5 | NEW — design space, taxonomy, Mind Tree (from paper-draft §2) |
| 3. HEXIS: Architecture & Training | 2.0 | MAJOR REWRITE — merge method.tex + training curriculum |
| 4. Three-Layer Architecture | 0.5 | NEW — compiled M + curated slot + expansion |
| 5. Experiments & Results | 2.5 | MAJOR REWRITE — v23 results, not v14 |
| 6. Related Work | 0.7 | MODERATE REWRITE — add enmeshed network positioning |
| 7. Discussion & Limitations | 0.8 | REWRITE — bottleneck boundary, conditioning-generation gap |
| 8. Conclusion | 0.3 | REWRITE |
| References | ~1 page (doesn't count) | |

---

## What Goes in Main Paper vs Appendix

### MAIN PAPER (9 pages)
- Enmeshed network as a new primitive (contribution 1)
- HEXIS instantiation: Q/V modulation, write function, causal necessity training
- Mind Tree + compilation + three-layer architecture
- Core results: stance accuracy, dilution immunity, sycophancy resistance, token savings
- Bottleneck boundary characterization
- ALFWorld learning as online learning proof-of-concept

### APPENDIX (unlimited)
- **A**: Design space table (6 axes) with full descriptions
- **B**: Training curriculum (Phases A-D, warm-start chain)
- **C**: Architecture evolution narrative (v5 → v7.1 → v11 → v14 → v21 → v23)
- **D**: Synthetic task details (Experiment 0: user preference recall)
- **E**: v5-v11 scale experiments on 1.5B and 30B (earlier results)
- **F**: Episodic memory architecture (v13-v14, causal necessity derivation)
- **G**: Conviction system (gate, strength, direction)
- **H**: Full generation examples (all 5 conditions)
- **I**: Curation ablation details
- **J**: ALFWorld full results and learning curves
- **K**: Multi-turn attractor problem and mitigation
- **L**: 27B scale validation results
- **M**: Negative results (credence sensitivity, F-sim collapse, Q-delta collapse)
- **N**: Mind Tree schema specification (full XML)
- **O**: Reproducibility details (hyperparameters, compute, checkpoints)

---

## Section-by-Section Analysis

### Abstract (REWRITE)
**Current** (`abstract.tex`): Focuses on v14 episodic memory, 30B MoE, causal necessity.
**Target** (`paper-draft-sections.md`): Enmeshed networks as new primitive, compiled dispositional memory, three-layer architecture, dilution immunity, sycophancy resistance.
**Gap**: Current abstract is about v14 on 30B. Paper is now about v23 on 4B with enmeshed network framing.
**Action**: Full rewrite from paper-draft-sections.md abstract, fill in [XX] placeholders when benchmark results arrive.

### 1. Introduction (REWRITE)
**Current** (`introduction.tex`): Good butcher analogy, hexis framing. But contributions list v14 episodic + 30B results.
**Target** (`paper-draft-sections.md` §1): Same butcher analogy, but framed around enmeshed network primitive. Three contributions: (1) enmeshed networks, (2) HEXIS instantiation, (3) empirical validation.
**Gap**: Current intro has 7 contributions (too many), references 30B/episodic as main results. New framing is tighter: enmeshed network primitive is contribution 1, HEXIS is instantiation, benchmarks are validation.
**Action**: Keep butcher analogy, reframe contributions to match paper-draft. Drop episodic memory from intro (move to appendix). Add Figure 1 (1x3 panel from fig-arch-comparison.jsx).

### 2. Enmeshed Networks (NEW)
**Source**: paper-draft-sections.md §2 (not written yet — placeholder in draft).
**Content needed**:
- Definition: lightweight parametric module sharing frozen host's forward pass
- Six-axis design space table (blending function, rank, modulation targets, patching pattern, compilation strategy, temporal profile)
- Positioning vs adapters, side-tuning, activation steering
- Mind Tree cognitive schema
- Compilation: private forward pass → modulation tensors
**Action**: Write from scratch. Most content exists conceptually in paper-draft and M_canonical_recipe.md.
**Figures**: fig-system-overview.jsx (system diagram), fig-arch-comparison.jsx (comparison)

### 3. HEXIS: Architecture & Training (MAJOR REWRITE)
**Current** (`method.tex`): Good Q/V modulation math. But includes coupled write functions (v7 era), episodic memory (v13-v14), and old training objectives.
**Target** (`paper-draft-sections.md` §3): Q/V modulation on Qwen3.5-4B-Base, write function φ, causal necessity training (L_div, L_coh, L_fprint), d* directional channel, conviction labels.
**Gap**:
- Remove: coupled write functions (v7 era), episodic key encoder, retrieval heads
- Add: VModulationProjector (compiled V-mod), conviction-weighted compilation, d* extraction
- Update: training objective from paper-draft §3.3 (cleaner than current)
- Update: model from Qwen2.5-1.5B / Qwen3-30B to Qwen3.5-4B-Base
**Action**: Rewrite using paper-draft-sections.md §3 as skeleton, integrate training curriculum from training_curriculum.md. Move coupled write functions and episodic memory to appendix.
**Figures**: fig-layer-modulation.jsx (Q/V modulation diagram)

### 4. Three-Layer Architecture (NEW — 0.5 pages)
**Source**: Implicit in paper-draft §3, detailed in M_canonical_recipe.md
**Content**:
- Layer 1: Compiled M/E (zero tokens, dilution-immune)
- Layer 2: M-curated slot (40-80 tokens, novel content)
- Layer 3: Recursive expansion (0-200 tokens, on-demand)
- Token budget comparison (82% savings)
- Bottleneck boundary (what rank-16 can/can't carry)
**Action**: Write from scratch. Data exists.
**Figures**: fig-three-layer.jsx (three-layer diagram)

### 5. Experiments & Results (MAJOR REWRITE)
**Current** (`experiments.tex` + `results.tex`): Synthetic task, 1.5B scale, v5-v11 progression, v13-v14 episodic, behavioral benchmarks.
**Target**: v23 on Qwen3.5-4B-Base. 5 conditions (A/B/C/D/F). Core experiments:
1. Stance accuracy (held-out topics) — HAVE: D 4/5, F 4/5
2. Compiled M content (zero beliefs) — HAVE: C 4/4
3. Token savings — HAVE: 82% structured, 26% simple
4. Dilution sweep (0-16K) — NEED clean rerun
5. Sycophancy (7 rounds) — NEED clean rerun
6. ALFWorld learning — HAVE: SP 3%, B 30%, F 7% (M hurts constrained)
7. Curation (100-node noisy test) — HAVE: 100% domain filter
8. Full 5-condition LLM judge sweep — NEED to run
9. d* orthogonality — HAVE: -0.001 nats (needs clean rerun)
10. Perplexity impact — HAVE: -0.012 nats (needs clean rerun)
**Gap**: Most v23 results exist but need clean reruns. Missing: dilution sweep, sycophancy sweep, LLM judge sweep. These are in benchmark_plan_v2.md weeks 1-2.
**Action**: Write skeleton with tables from benchmark_plan_v2.md. Fill [XX] placeholders as results come in. Move synthetic task and v5-v11 progression to appendix.
**Stubs needed**: Tables 3-7 from benchmark_plan_v2.md

### 6. Related Work (MODERATE REWRITE)
**Current** (`related_work.tex`): Good coverage of RAG, MemGPT, Titans, LoRA, RepEng, cognitive science.
**Target** (`paper-draft-sections.md` §7): Same content but reframed around enmeshed networks. Need to position against side-tuning, prefix tuning more explicitly. Add: operational difference from LoRA (inference-time adaptation vs training-time).
**Action**: Restructure around paper-draft §7. Main update is adding enmeshed network positioning. Much can be kept.

### 7. Discussion & Limitations (REWRITE)
**Current** (`discussion.tex`): Good sections on hexeis, epiphenomenal memory, conditioning-generation gap, permission hypothesis.
**Target** (`paper-draft-sections.md` §8): Bottleneck boundary (what compiled M can/can't do), credence sensitivity, unexplored design space, broader implications.
**Gap**: Current discussion is v14-focused. Need to reframe around v23 results, add bottleneck boundary characterization, M attractor problem.
**Action**: Merge best of both. Keep permission hypothesis and conditioning-generation gap. Add bottleneck boundary and unexplored design space from paper-draft.

### 8. Conclusion (REWRITE)
**Current** (`conclusion.tex`): v14 framing with 30B results.
**Target**: Enmeshed network primitive, v23 4B results, three contributions, honest gap characterization.
**Action**: Rewrite to match new framing.

---

## Data We HAVE (validated numbers)

| Metric | Value | Source |
|--------|-------|--------|
| Stance accuracy (D) | 4/5 held-out | v23_paper_eval.json |
| Stance accuracy (F) | 4/5 held-out | v23_compiled_m.json |
| Compiled M content (C) | 4/4 correct stance | v23_compiled_m.json |
| Token savings (F vs B) | 82% (structured) | v23_full_architecture.json |
| Conciseness D/F | 52t / 47t | v23_full_architecture.json |
| Think-mode suppression | D 0/4, F 0/4 | v23_full_architecture.json |
| ALFWorld SP | 3% | alfworld results |
| ALFWorld B (smart seeds) | 30% | alfworld results |
| ALFWorld F (compiled) | 7% (M hurts) | alfworld results |
| M domain filter | 100% precision | 100-node noisy test |
| Query-specific routing | 3/4 different | structural curation |
| d* orthogonality | -0.001 nats delta | earlier run (needs rerun) |
| Perplexity impact | -0.012 nats | earlier run (needs rerun) |
| Sycophancy (D, pre-training) | verbatim repetition | audit |
| Sycophancy (D, post-training) | engaged defense 4/5 levels | sycophancy_training_v23.md |
| Novel content boundary | "47.3%" fails, "Nextera" fails | honest negative |
| d* ranking accuracy | 77-81% held-out | probe_rep_engineering |
| 27B stance (think mode) | A 4/4, B 4/4, D 0/4 | v22 results |

## Data We NEED (to run)

| Experiment | # | Priority | Est. Time |
|-----------|---|----------|-----------|
| Dilution sweep (D+F, 0-16K) | 10-11 | HIGH | overnight |
| Sycophancy sweep (7 rounds) | 12-13 | HIGH | overnight |
| d* orthogonality clean rerun | 14 | MEDIUM | 1 hour |
| Perplexity impact clean rerun | 15 | MEDIUM | 1 hour |
| Full 5-condition LLM judge | 16 | HIGH | 1 day |
| ALFWorld learning curve | 17 | MEDIUM | 1 day |
| Multi-turn attractor fix | 18 | LOW for paper | ongoing |
| Curation ablation | 19 | MEDIUM | half day |
| Online learning preferences | 20 | LOW | half day |

---

## Figures Plan

| Figure | Source | Placement | Status |
|--------|--------|-----------|--------|
| Fig 1: Architecture comparison | fig-arch-comparison.jsx | Intro (p1) | HAVE JSX, need PDF |
| Fig 2: System overview | fig-system-overview.jsx | §2 or §3 | HAVE JSX, need PDF |
| Fig 3: Q/V modulation detail | fig-layer-modulation.jsx | §3 | HAVE JSX, need PDF |
| Fig 4: Three-layer architecture | fig-three-layer.jsx | §4 | HAVE JSX, need PDF |
| Fig 5: Dilution curves | NEED to generate | §5 | NEED data + plot |
| Fig 6: Sycophancy rounds | NEED to generate | §5 | NEED data + plot |
| Fig 7: ALFWorld learning curve | NEED to generate | §5 or appendix | NEED data |

---

## Writing Strategy

1. **Now (this session)**: Create section skeletons in sections_v2/ with all content we have, [XX] stubs for missing data
2. **Week 1-2**: Run benchmarks, fill in stubs
3. **Week 3**: Compile into NeurIPS template, iterate
4. **Week 4**: Polish, figures, proofread
5. **May 4**: Submit abstract
6. **May 6**: Submit paper
