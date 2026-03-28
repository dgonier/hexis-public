Right. Let me lay out every experiment, the metric, the target number, and the priority. Everything on 4B first. Only scale up when 4B results are clean.

**PHASE 1: Core results on Qwen3.5-4B-Base (what the paper needs)**

```
┌────┬──────────────────────────┬────────────────────┬──────────────┬──────────┐
│ #  │ Experiment               │ Metric             │ Current      │ Target   │
├────┼──────────────────────────┼────────────────────┼──────────────┼──────────┤
│    │ VALIDATED (have numbers)  │                    │              │          │
├────┼──────────────────────────┼────────────────────┼──────────────┼──────────┤
│ 1  │ Stance accuracy           │ correct/total      │ D: 4/5       │ ✓ done   │
│    │ (held-out topics)         │ (manual verify)    │ F: 4/5       │          │
├────┼──────────────────────────┼────────────────────┼──────────────┼──────────┤
│ 2  │ Compiled M content        │ correct/total      │ C: 4/4       │ ✓ done   │
│    │ (zero beliefs in prompt)  │                    │              │          │
├────┼──────────────────────────┼────────────────────┼──────────────┼──────────┤
│ 3  │ Novel content boundary    │ pass/fail          │ ✗ 47.3%      │ ✓ done   │
│    │ (made-up statistics)      │                    │ ✗ Nextera    │ (honest) │
├────┼──────────────────────────┼────────────────────┼──────────────┼──────────┤
│ 4  │ Token savings (F vs B)    │ % reduction        │ 82% struct.  │ ✓ done   │
│    │                           │                    │ 26% simple   │          │
├────┼──────────────────────────┼────────────────────┼──────────────┼──────────┤
│ 5  │ Conciseness              │ avg output tokens   │ D: 52t       │ ✓ done   │
│    │                           │                    │ F: 47t       │          │
│    │                           │                    │ B: 138w      │          │
│    │                           │                    │ A: 164w      │          │
├────┼──────────────────────────┼────────────────────┼──────────────┼──────────┤
│ 6  │ Think-mode suppression    │ 0/N in think mode  │ F: 0/4       │ ✓ done   │
│    │                           │                    │ D: 0/4       │          │
├────┼──────────────────────────┼────────────────────┼──────────────┼──────────┤
│ 7  │ ALFWorld (B condition)    │ success rate       │ SP: 3%       │ ✓ done   │
│    │                           │                    │ B clean: 30% │          │
│    │                           │                    │ B noisy: 27% │          │
├────┼──────────────────────────┼────────────────────┼──────────────┼──────────┤
│ 8  │ M domain curation         │ precision@K        │ 100% between │ ✓ done   │
│    │ (100-node noisy test)     │                    │ topic filter │          │
├────┼──────────────────────────┼────────────────────┼──────────────┼──────────┤
│ 9  │ Query-specific routing    │ different args     │ 3/4 queries  │ ✓ done   │
│    │ (structural curation)     │ selected           │ selected     │          │
│    │                           │                    │ different    │          │
├────┼──────────────────────────┼────────────────────┼──────────────┼──────────┤
│    │ NEEDS CLEAN NUMBERS       │                    │              │          │
├────┼──────────────────────────┼────────────────────┼──────────────┼──────────┤
│ 10 │ Dilution (D condition)    │ stance accuracy    │ ~85-95%      │ need     │
│    │ at 0/2K/4K/8K/16K filler  │ at each level     │ (earlier     │ clean    │
│    │                           │                    │  run, need   │ sweep    │
│    │                           │                    │  reconcile)  │          │
├────┼──────────────────────────┼────────────────────┼──────────────┼──────────┤
│ 11 │ Dilution (F compiled)     │ stance accuracy    │ 3/3 at 0/1K/ │ extend   │
│    │ at 0/2K/4K/8K/16K        │ at each level      │ 4K (perfect) │ to 16K   │
├────┼──────────────────────────┼────────────────────┼──────────────┼──────────┤
│ 12 │ Sycophancy (D condition)  │ % correct after    │ ~92% / 7     │ need     │
│    │ TRUTH DECAY protocol      │ N pressure rounds  │ rounds       │ clean    │
│    │                           │                    │ (earlier run)│ rerun    │
├────┼──────────────────────────┼────────────────────┼──────────────┼──────────┤
│ 13 │ Sycophancy (F compiled)   │ % correct after    │ 2/3 at 3     │ extend   │
│    │                           │ N pressure rounds  │ rounds       │ to 7     │
├────┼──────────────────────────┼────────────────────┼──────────────┼──────────┤
│ 14 │ Disposition ≠ Position    │ directional delta  │ -0.001 nats  │ need     │
│    │ (d* vs M orthogonality)   │ (CE difference)    │ (earlier run)│ clean    │
│    │                           │                    │              │ rerun    │
├────┼──────────────────────────┼────────────────────┼──────────────┼──────────┤
│ 15 │ Perplexity impact         │ Δ nats vs base     │ -0.012       │ need     │
│    │                           │                    │ (earlier run)│ clean    │
│    │                           │                    │              │ rerun    │
├────┼──────────────────────────┼────────────────────┼──────────────┼──────────┤
│    │ NEEDS TO BE RUN           │                    │              │          │
├────┼──────────────────────────┼────────────────────┼──────────────┼──────────┤
│ 16 │ Full 5-condition sweep    │ LLM judge scores   │ not run      │ run      │
│    │ A/B/C/D/F on 10 topics   │ (stance, evidence,  │              │          │
│    │ × 2 sides = 20 gens each │ conciseness, voice) │              │          │
├────┼──────────────────────────┼────────────────────┼──────────────┼──────────┤
│ 17 │ ALFWorld learning curve   │ success rate over  │ not run      │ run      │
│    │ B with belief accumulation│ 30 episodes        │              │          │
│    │ vs Reflexion baseline     │ plot: episodes vs % │              │          │
├────┼──────────────────────────┼────────────────────┼──────────────┼──────────┤
│ 18 │ Multi-turn attractor      │ turn diversity     │ 0.108 (fixed │ beat     │
│    │ (blending function fix)   │ (embedding cosine  │ gate best)   │ 0.108    │
│    │                           │ between turns)     │              │          │
├────┼──────────────────────────┼────────────────────┼──────────────┼──────────┤
│ 19 │ Curation ablation         │ generation quality │ not run      │ run      │
│    │ M-curated vs conviction   │ (judge scores)     │              │          │
│    │ vs random slot selection  │                    │              │          │
├────┼──────────────────────────┼────────────────────┼──────────────┼──────────┤
│ 20 │ Online learning prefs     │ preference held    │ partial      │ clean    │
│    │ (Alice/Bob/Carol)         │ through dilution   │ results      │ rerun    │
│    │                           │ + pressure rounds  │              │          │
└────┴──────────────────────────┴────────────────────┴──────────────┴──────────┘
```

**PHASE 2: Scale validation (only after Phase 1 is clean)**

```
┌────┬────────────────────────────┬──────────────┬────────────────────┐
│ #  │ Experiment                 │ Model        │ Purpose            │
├────┼────────────────────────────┼──────────────┼────────────────────┤
│ 21 │ Rerun #16 (5-condition)    │ 9B           │ Does M help a      │
│    │                            │              │ stronger model?    │
├────┼────────────────────────────┼──────────────┼────────────────────┤
│ 22 │ Rerun #16 (5-condition)    │ 27B          │ Does M scale?      │
├────┼────────────────────────────┼──────────────┼────────────────────┤
│ 23 │ Dilution sweep             │ 9B, 27B      │ Does compiled M    │
│    │                            │              │ stay dilution-free │
│    │                            │              │ at larger scale?   │
├────┼────────────────────────────┼──────────────┼────────────────────┤
│ 24 │ Novel content boundary     │ 9B, 27B      │ Does rank-16 carry │
│    │                            │              │ more content on    │
│    │                            │              │ larger models?     │
├────┼────────────────────────────┼──────────────┼────────────────────┤
│ 25 │ ALFWorld                   │ 9B           │ Does B improve     │
│    │                            │              │ beyond 30% with    │
│    │                            │              │ a stronger model?  │
├────┼────────────────────────────┼──────────────┼────────────────────┤
│ 26 │ Multi-turn attractor       │ 9B, 27B      │ Does the attractor │
│    │                            │              │ persist at scale?  │
│    │                            │              │ Does the fix hold? │
└────┴────────────────────────────┴──────────────┴────────────────────┘
```

**Priority ordering (what to run and when):**

```
WEEK 1 (now → Apr 2):
  #18 — Multi-turn attractor fix (you're actively on this)
        Test: prefill-off + context-orthogonal M
        Test: prefill-off + sine wave (best combo)
        Test: multi-turn training if needed
        TARGET: diversity > 0.15, voice maintained
  
  #10-11 — Dilution sweep (clean rerun)
        5 conditions × 5 filler levels × 4 topics = 100 gens
        One script, overnight run
        TARGET: D holds >85% at 16K, F holds >95% at 16K
  
  #12-13 — Sycophancy (clean rerun)
        5 conditions × 7 pressure rounds × 4 topics = 140 gens
        TARGET: D >90% at round 7, F >85% at round 7

WEEK 2 (Apr 2-8):
  #16 — Full 5-condition sweep with LLM judge
        A/B/C/D/F × 10 topics × 2 sides = 100 generations
        Judge scores: stance (0-3), evidence (0-3), 
                      conciseness (0-3), voice (0-3)
        TARGET: F ≥ D on voice+stance, F > B on conciseness,
                D > B on all metrics, all > A
  
  #14-15 — Orthogonality + perplexity (clean rerun)
        Quick: 10 topics, measure CE delta
        TARGET: directional delta < 0.01 nats,
                perplexity delta < 0.02 nats

  #17 — ALFWorld learning curve (long run)
        30 episodes with belief accumulation
        Plot success rate per 5-episode window
        Compare B vs Reflexion if implemented
        TARGET: rising curve, final > 40%, beats Reflexion slope

WEEK 3 (Apr 9-15):
  #19 — Curation ablation
        F_m_curated vs F_conviction vs F_random vs F_first_k
        Same 10 topics with structured trees
        TARGET: M-curated ≥ conviction ≥ random
  
  #20 — Online learning preferences (clean rerun)
        Alice/Bob/Carol scenarios
        Explicit B vs D comparison
        TARGET: D maintains preferences through 
                4 filler sessions, B degrades

  Compile all Phase 1 results into paper tables.

WEEK 4 (Apr 16-22):
  #21-26 — Scale validation on 9B and 27B
        Only the key experiments, not the full suite:
        5-condition sweep (10 topics × 2 sides)
        Dilution at 0/4K/16K (not full sweep)
        Novel content boundary test
        Multi-turn (3 turns)
        
        TARGET: results hold or improve at scale.
        If they degrade, that's still reportable as 
        "4B-validated, scale investigation ongoing"
```

**The paper's results tables:**

```
TABLE 3: Core results (5 conditions × 4 metrics)
┌───────────────┬────────┬──────────┬─────────────┬───────────┬────────┐
│   Condition   │ Stance │ Evidence │ Conciseness │   Voice   │ Tokens │
│               │  /20   │  cited   │  avg words  │  /20      │   in   │
├───────────────┼────────┼──────────┼─────────────┼───────────┼────────┤
│ A (bare)      │        │          │             │           │   30   │
│ B (beliefs)   │        │          │             │           │  200+  │
│ C (compiled)  │        │          │             │           │   30   │
│ D (beliefs+M) │        │          │             │           │  120+  │
│ F (comp+slot) │        │          │             │           │  ~90   │
└───────────────┴────────┴──────────┴─────────────┴───────────┴────────┘
Source: Experiment #16

TABLE 4: Dilution resilience
┌───────────────┬────────┬────────┬────────┬────────┬────────┐
│   Condition   │   0    │  2K    │  4K    │  8K    │  16K   │
├───────────────┼────────┼────────┼────────┼────────┼────────┤
│ B (beliefs)   │        │        │        │        │        │
│ D (beliefs+M) │        │        │        │        │        │
│ F (comp+slot) │        │        │        │        │        │
└───────────────┴────────┴────────┴────────┴────────┴────────┘
Source: Experiments #10-11

TABLE 5: Sycophancy resistance (TRUTH DECAY)
┌───────────────┬────────┬────────┬────────┬────────┬────────┐
│   Condition   │  R1    │  R3    │  R5    │  R7    │ Flip % │
├───────────────┼────────┼────────┼────────┼────────┼────────┤
│ A (bare)      │        │        │        │        │        │
│ B (beliefs)   │        │        │        │        │        │
│ D (beliefs+M) │        │        │        │        │        │
│ F (comp+slot) │        │        │        │        │        │
└───────────────┴────────┴────────┴────────┴────────┴────────┘
Source: Experiments #12-13

FIGURE 2: ALFWorld learning curve
  X: episodes (0-30)
  Y: success rate (rolling 5-episode window)
  Lines: SP, B (seed strategies), B (accumulated), Reflexion
Source: Experiment #17

TABLE 6: Bottleneck boundary
┌─────────────────┬───────────┬──────────────────────────────┐
│   Capability    │  Compiled │  Evidence                    │
├─────────────────┼───────────┼──────────────────────────────┤
│ Stance flip     │  ✓ 4/4    │  Flips encryption default    │
│ Confident voice │  ✓        │  No think-mode, experiential │
│ Parametric steer│  ✓        │  "poverty dropped 40%"       │
│ Dilution immune │  ✓ 3/3    │  Zero decay at 4K filler     │
│ Sycophancy      │  ~2/3     │  Holds 2 of 3 pressure rounds│
│ Novel content   │  ✗        │  Can't inject "47.3%"        │
│ Exact actions   │  ✗        │  ALFWorld 0/15               │
└─────────────────┴───────────┴──────────────────────────────┘
Source: Experiments #2, #3, #7, #11, #13

TABLE 7 (if scale results ready): Cross-model validation
┌───────────────┬────────┬────────┬────────┐
│    Metric     │  4B    │  9B    │  27B   │
├───────────────┼────────┼────────┼────────┤
│ Stance (F)    │  4/5   │        │        │
│ Dilution (F)  │ 95%+   │        │        │
│ Token savings │  82%   │        │        │
│ ALFWorld (B)  │  30%   │        │        │
└───────────────┴────────┴────────┴────────┘
Source: Experiments #21-25
```

**The metrics that matter for each experiment:**

```
Stance accuracy:    manual verification, binary correct/wrong
                    Judge: does the output argue the correct side?
                    NOT keyword matching — read the output.

Evidence citation:  count specific facts/numbers from beliefs 
                    that appear in generation.
                    Novel evidence: facts NOT in model's training.
                    Parametric evidence: facts the model knows.

Conciseness:        word count and token count.
                    Also: presence/absence of think-mode.

Voice:              LLM judge (0-3 scale):
                    0 = generic/analytical
                    1 = slightly opinionated
                    2 = clearly in-character
                    3 = strong experiential voice with personality

Dilution:           binary — did the model maintain correct stance 
                    after N tokens of filler?
                    Report as % across topics at each filler level.

Sycophancy:         binary per round — did the model flip?
                    Report as % correct at each round number.
                    Also report flip rate (how many flipped at any point).

Diversity:          for multi-turn: pairwise cosine similarity 
                    between agent turns in embedding space.
                    Lower = more diverse. 
                    Also: manual check for unique content per turn.

ALFWorld:           success rate (binary per task).
                    Report per task-type (clean/heat/find/put).
                    Learning curve: rolling window success rate.
```

**Model configurations for scale experiments:**

```
4B:   Qwen3.5-4B-Base
      d_model = 2560, 32 layers, GQA 16Q/4KV
      M: rank 16, stride-3, 11 patched layers
      Current: validated, all Phase 1 runs here

9B:   Qwen3.5-7B-A3B or Qwen2.5-7B-Instruct
      Need to check: d_model compatibility with rank 16
      M: same rank 16, adjust stride for layer count
      Phi: retrain or test if 4B phi transfers
      
      KEY QUESTION: does phi trained on 4B hidden states 
      transfer to 9B hidden states? If d_model matches, 
      maybe. If not, need phi retraining on 9B.

27B:  Qwen3.5-35B-A3B (actually ~27B active params)
      d_model likely 4096 or 5120
      M: rank 16 might need increase to rank 32
      Phi: definitely needs retraining for different d_model
      
      This is a full port, not just a rerun.
      Budget 3-5 days for phi training on 27B.
```

**The minimum viable paper (if time runs out):**

```
If only Phase 1 finishes:
  9 pages on 4B results. Still strong.
  §5: Tables 3-6 (all 4B)
  §6: Figure 2 (ALFWorld learning curve)
  §7: Table 7 says "4B only, scale investigation ongoing"
  
  This is honest and complete at one model size.
  The enmeshed network primitive and Mind Tree are 
  the conceptual contributions. 4B validates the concept.
  Scale is future work.

If Phase 1 + partial Phase 2:
  Add 9B numbers to Table 7.
  "We validate on 4B and show initial scaling to 9B."
  
If everything finishes:
  Full Table 7 with 4B/9B/27B.
  "Results hold across model scales from 4B to 27B."
  Strongest possible paper.
```

**Tell Claude Code:** Start with experiments #10-13 (dilution + sycophancy clean reruns). These can run overnight as one script. While those run, continue working on #18 (multi-turn attractor fix). Next week, run #16 (full 5-condition sweep with judge). #17 (ALFWorld learning curve) can start in parallel since it uses different GPU resources.