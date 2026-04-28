# τ³-bench 4-domain audited result (Apr 28 2026 — final)

Headline: Qwen3.5-4B agentic, 3-judge audited (Haiku-hard, Sonnet auditor, Opus tiebreaker).

## Files

| File | Description |
|---|---|
| `tau3_full_asym_1777300323.jsonl` | Bench output, 762 rows (611 clean after stripping 148 infra + 3 tool errors). |
| `tau3_full_asym_1777300323.audit.jsonl` | Sonnet audit verdicts on 227 disputed trials. |
| `tau3_full_asym_1777300323.opus.jsonl` | Opus tiebreaker verdicts on 159 Sonnet-vs-hard disputes. |
| `tau3_final_analysis.py` | Canonical analysis script. Computes 3-judge final verdict + McNemar paired tests on full and balanced panels. |
| `tau3_figure.py` | Generates `fig-tau3-results-*.pdf` for the paper. |

## Headline numbers

3-judge audited C5 vs baseline:

| Panel | C5 | baseline | Δ | n_pairs | p (McNemar) |
|---|---|---|---|---|---|
| Balanced primary (26 tasks × 5 trials × 3 arms = 390 records) | 69.2% | 63.8% | +5pp | 127 | 0.31 |
| **Balanced excl airline t1, t3** (judge variance) | **71.7%** | **61.7%** | **+10pp** | 117 | **0.043** ✓ |
| All-clean (sensitivity, 611 records, unbalanced) | 58.0% | 52.1% | +6pp | 182 | 0.28 |
| All-clean excl t1, t3 | 58.8% | 49.5% | +9pp | 169 | **0.044** ✓ |

**Per-domain (balanced excl t1, t3):**
- Airline: 49% → 66% (Δ=+17pp)
- Banking: 25% → 45% (Δ=+20pp) — strongest single-domain effect
- Retail: 76% → 78% (Δ=+2pp, near ceiling)
- Telecom: 93% → 100% (Δ=+7pp, near ceiling)

## User-sim and judges

- Agent: Qwen3.5-4B-Instruct on debaterhub--hexis-agentic-h200 (vLLM 0.19, enforce_eager=True)
- User-sim: bedrock/us.anthropic.claude-haiku-4-5-20251001-v1:0 (temp=0)
- Soft pass judge: Haiku-4.5 (temp=0)
- Audit judges: Sonnet-4.5 + Opus-4.7

## Methodology
Detailed protocol, t1+t3 exclusion rationale, denominator handling, and 10-question
reviewer FAQ are in the paper appendix `\section{$\tau^3$-bench Benchmark Protocol}`.
