# The Cost of Consensus: Isolated Self-Correction Prevails Over Unguided Homogeneous Multi-Agent Debate

## Citation metadata
- **Title**: The Cost of Consensus: Isolated Self-Correction Prevails Over
  Unguided Homogeneous Multi-Agent Debate
- **Authors**: Blaž Bertalanič, Carolina Fortuna (Jožef Stefan Institute,
  Ljubljana, Slovenia)
- **arXiv**: 2605.00914v1 [cs.MA], 29 Apr 2026
- **Venue**: ACM conference format (venue anonymized/blinded in the PDF —
  "Conference'17" placeholder; verify actual venue before final bibliography
  if it has since been assigned one)

## Core findings (with exact numbers and locations)

Controlled empirical study of homogeneous multi-agent debate: **N=10 agents**,
**R=3 rounds**, three 7–8B models (Qwen2.5-7B, Llama-3.1-8B, Ministral-3-8B),
on two high-difficulty benchmarks (GSM-Hard, MMLU-Hard subset of college
physics/math/logic/econometrics/accounting), compared against isolated
self-correction and a stochastic noise-injection control (unrelated peer
rationales, to isolate semantic content from prompt-length effects) (§3,
Figure 2).

**Three decomposed failure pathways** (Abstract; §4.1.2; Table 2, Table 3):
1. **Sycophantic conformity** — agents adopt the modal peer answer regardless
   of validity. **Modal sycophancy rate up to 85.5%** (Qwen2.5-7B,
   MMLU-Hard). Table 3 (p.9): Qwen 73.4% (GSM-Hard) / 85.5% (MMLU-Hard);
   Ministral 26.5% / 80.5%; Llama 58.4% / 70.2%.
2. **Contextual fragility** — expanded peer context destabilizes previously
   correct reasoning regardless of peer content. **Vulnerability rate up to
   70.0%** (Ministral-3-8B, GSM-Hard; Table 2, p.9).
3. **Consensus collapse** — plurality voting discards correct answers already
   present in the generation pool. **Oracle gap up to 32.3 percentage
   points** (Ministral-3-8B, GSM-Hard; Table 3, p.9).

**Economics**: debate costs **2.1×–3.4× more tokens** than isolated
self-correction for equal-or-worse accuracy — up to **28,631 tokens/problem**
(Ministral, MMLU-Hard) vs. 6,170–12,831 for self-correction (Table 4, p.10;
Abstract). Cost driven almost entirely by prompt-side O(N×K) peer-rationale
routing overhead, not output-token generation (§4.3).

**Statistical significance**: McNemar's test with continuity correction,
p<0.05 threshold; debate significantly underperformed the best control in 4
of 6 model-dataset pairs (Table 1); two Llama comparisons (GSM-Hard p=0.155,
MMLU-Hard p=0.131) did not reach significance and are noted by the authors as
"directional rather than conclusive."

**Robustness/ablation findings** (§4.4):
- Communication density K∈{2,4,9}: sycophancy saturates fast — GSM-Hard
  modal sycophancy at K=2 (69.4%) is already within 4pp of K=9 (73.4%).
  Accuracy never exceeds self-correction at any K.
- Temperature T=0.4 vs. 0.7: greater initial diversity does **not** reduce
  sycophancy — it *increases* on GSM-Hard (+3.4pp) and stays near-ceiling on
  MMLU-Hard.
- Preliminary Qwen2.5-**32B** replication: sycophancy reaches **95.4%**, the
  highest in the study — suggesting the problem intensifies, not attenuates,
  with scale (Conclusion, p.11; §4.4 discussion, Appendix K referenced).

Locations: Abstract; Table 1 (p.9, accuracy/token cost); Table 2 (p.9,
consensus/vulnerability/recovery rates); Table 3 (p.9, modal sycophancy/
oracle accuracy/team accuracy/oracle gap — the key table for verification);
Table 4 (p.10, token economics breakdown); §4.2 "The Oracle Gap" (p.9–10, the
exact sentences confirming both verification sub-claims); §4.4 Robustness
Analysis (p.10–11, K/T/32B ablations); Conclusion (p.11).

## Positioning-memo verification

**Assertion (c)**: "modal sycophancy rate is the strongest predictor of the
team-vs-oracle gap, and teams discard correct reasoning when sycophancy
exceeds 70%."

| Sub-claim | Status | Evidence |
|---|---|---|
| Modal sycophancy is the strongest predictor of the oracle gap | **CONFIRMED as a verbatim authorial claim** — but see nuance below | §4.2: "Across all configurations, the modal sycophancy rate was the strongest predictor of the oracle gap." |
| 70% threshold; teams discard correct reasoning above it | **CONFIRMED, near-verbatim, for the cases it covers** | §4.2: "Where sycophancy exceeded 70% (Qwen on both datasets, and all three models on MMLU-Hard), teams consistently discarded correct reasoning in favor of premature consensus." Table 3 values >70%: Qwen GSM-Hard 73.4% (gap 5.7pp), Qwen MMLU-Hard 85.5% (gap 13.7pp), Ministral MMLU-Hard 80.5% (gap 19.0pp), Llama MMLU-Hard 70.2% (gap 24.3pp). |

**Important qualitative-predictor nuance**: the "strongest predictor" claim is
the authors' own narrative conclusion drawn from pattern-matching across six
model-dataset rows in Table 3 — it is **not** a formal statistical procedure
(no regression, no reported coefficients/R², no formal comparison isolating
sycophancy against other candidate predictors like vulnerability rate or
consensus strength). The claim is accurately quoted, but citing it as an
independently statistically-validated result (rather than the authors' own
qualitative reading of their data) would overstate the paper's methodological
rigor on this specific point.

**Important three-mode-taxonomy nuance**: the 70% threshold holds cleanly for
the four rows above, but the paper's own **largest** oracle gap in the entire
study — Ministral-3-8B on GSM-Hard, **32.3 percentage points** — occurs at a
sycophancy rate of only **26.5%** (well below 70%). That gap is explicitly
attributed to a *different* failure pathway: **contextual fragility**
(vulnerability rate 70.0% on that same row), not sycophancy. The paper's own
taxonomy has three distinct, model-dependent mechanisms (sycophantic
conformity / contextual fragility / consensus collapse), and its single most
dramatic result is driven by the mechanism that is *not* sycophancy. Citing
the 70%-threshold claim without this context risks implying sycophancy is the
sole or dominant driver of oracle gaps generally, which the paper explicitly
does not claim.

## Threats / misfits
- **Narrow model scope**: primary results are 7–8B parameter models only
  (Qwen2.5-7B, Llama-3.1-8B, Ministral-3-8B). The 32B/95.4%-sycophancy result
  is explicitly labeled "preliminary" (single model, presumably limited
  runs) — useful supporting context but shouldn't be cited with the same
  confidence as the main 7-8B results.
- **Venue is a placeholder/blinded** in the extracted text ("Conference'17,
  Washington, DC, USA" with "nnnnnnn.nnnnnnn" DOI) — this looks like an
  ACM submission template not yet filled in with a real venue; verify actual
  publication venue before finalizing the bibliography entry.
- Two of six model-dataset debate-vs-self-correction comparisons (both Llama)
  did **not** reach statistical significance (p=0.155, p=0.131) — the
  authors are appropriately transparent about this, but a citation asserting
  "debate always underperforms self-correction" would overstate results for
  Llama specifically.
- The stochastic noise-injection control is not a "pure" noise baseline (it
  injects real, coherent reasoning about *unrelated* problems, not random
  tokens) — the authors flag this themselves as leaving open some incidental
  transfer-of-useful-patterns confound; doesn't affect the sycophancy/oracle-
  gap claims directly but is worth knowing if citing the noise-control
  comparisons elsewhere.

## Citation guidance

Cite this paper as strong empirical support that **sycophantic conformity in
homogeneous multi-agent LLM debate causes teams to discard independently-
generated correct answers**, with modal sycophancy rates reaching 85.5% and
oracle gaps up to 32.3 percentage points in a controlled 7–8B-model study.
**When citing the "strongest predictor" language, attribute it explicitly as
the authors' own qualitative conclusion from their data** rather than
presenting it as an independently statistically-established result, since no
formal predictor-comparison procedure (regression, ablation) backs that
specific phrase. **When citing the 70% sycophancy threshold, note that the
paper's own largest oracle gap is driven by a different mechanism
(contextual fragility, not sycophancy)** — the three-mode taxonomy
(sycophantic conformity / contextual fragility / consensus collapse) means
sycophancy is a strong but not exclusive driver of the team-vs-oracle gap,
and citations should avoid implying sycophancy alone explains oracle-gap
variance across all conditions. The paper is most defensibly cited for the
specific, well-supported claim that high (>70%) modal sycophancy reliably
co-occurs with teams discarding correct reasoning — not as a general
statement that sycophancy is the sole determinant of consensus failure.
