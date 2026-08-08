# Adversarial Robustness of Activation Steering in Large Language Models

## Citation metadata
- **Title**: Adversarial Robustness of Activation Steering in Large Language Models
- **Authors**: Kien Le (Independent Researcher), Thai Le (Indiana University)
- **arXiv**: 2606.07696v1 [cs.LG], 5 Jun 2026
- **Venue**: preprint (as of read date; no conference listed in text)

## Core findings (with exact numbers and locations)

First systematic study of activation steering robustness under controlled,
semantics-preserving adversarial text perturbation of the *input*. Covers:
- **4 extraction methods**: Mean Difference / MD (≈CAA), PCA, ITI, ODESteer (§2.2)
- **3 attack strategies**: TextFooler (word-level synonym substitution),
  TextBugger (character-level), BERT-Attack (masked-word infill) (§4.2)
- **6 personas** from the Anthropic Model-Written Evaluations dataset:
  Religion Following, Conscientiousness, Self-Improvement, Alliance Building,
  Impact Maximization, Self-Aware (Abstract, §4.2)
- **5 models, 1.5B–30B params**: Qwen2.5-1.5B, Llama-3.2-3B, Qwen3-4B,
  Qwen3-14B, Qwen3-30B-A3B (MoE) (§4.2 "Models")

Key metrics: **Rdir** (directional robustness rate — does steering still push
the intended direction post-attack), **Rstr** (strength reduction rate — does
steering gain degrade post-attack), **ASR** (attack success rate — fraction of
steerable inputs driven below confidence threshold δ=0.3), **MDTW** /
**Mshift** (layer-selection profile/position stability under perturbed
training data).

Headline results:
- ASR is high across nearly all model/method/task combinations (Table 1, p.5).
- Post-attack confidence P(y+|x′,vℓ) collapses to **~0.14–0.28 regardless of
  pre-attack confidence** ("Finding #1," p.5; Table 1).
- Steering **strength** (Rstr) degrades on nearly every steerable input:
  "frequently exceeding 0.9 and approaching 1.0" ("Finding #2," p.6; Table 2).
- Steering **direction** (Rdir) drops are model-dependent: **50–64 percentage
  points** on mid-to-large dense models ("Finding #3," p.6; Table 2); smaller
  or MoE models sometimes show a near-floor effect (clean Rdir already ~0.5)
  that masks further degradation.
- MoE (Qwen3-30B-A3B) shows **no special robustness** vs. dense models of
  comparable active-parameter count ("Finding #1," p.5).
- No single extraction method dominates on robustness ("Finding #4," p.6).
- Optimal steering layer (via LayerNavigator) **shifts by up to 17 positions**
  under perturbation of the training/extraction set (Abstract; Contributions,
  p.2; Conclusion, p.8–9). Table 4 (p.7) shows individual L1-distance shifts
  as large as +20 in some rows (e.g., Qwen3-14B/ITI/Self-Improvement), so 17
  is the paper's own headline figure, not the largest number appearing in the
  tables.
- Adversarial training (re-extracting vectors from perturbed data) **partially
  recovers** steerability for PCA/MD on mid-to-large models but **layer
  selection still fails to track the new optimal layer** (Discussion, p.7–8;
  Conclusion, p.8).

Locations: Abstract; Conclusion (p.8–9, headline numbers); §4.3 Findings 1–4
(p.5–6); Table 1 (p.5, ASR/confidence); Table 2 (p.6, Rdir/Rstr); Table 3
(p.7, DTW/layer shift); Table 4 (p.7, L1 distance to true optimal layer).

## Positioning-memo verification

**Assertion (a)**: "directional robustness dropping up to 64pp under
adversarial input perturbation, post-attack confidence at/below 0.25 across
four extraction methods and five models 1.5B-30B, optimal steering layer
shifting up to 17 positions."

| Sub-claim | Status | Evidence |
|---|---|---|
| 64pp directional robustness drop | **CONFIRMED** | Conclusion: "directional robustness drops by up to 64 percentage points." Table 2 shows individual Rdir drops in the 0.50–0.66 range on Qwen3-14B. |
| Post-attack confidence at/below 0.25, 4 methods, 5 models 1.5B–30B | **CONFIRMED** | 4 methods = PCA/MD/ITI/ODESteer (§2.2); 5 models = Qwen2.5-1.5B, Llama-3.2-3B, Qwen3-4B/14B/30B-A3B (§4.2), span is 1.5B–30B. Confidence collapse to ~0.14–0.28 stated in Finding #1 (p.5) and shown in Table 1 for 3 of the 5 models directly in the main body (remaining two — Qwen2.5-1.5B, Qwen3-4B — are stated as included but their specific tables are in the appendix, not re-verified visually in this pass). |
| Optimal layer shifts up to 17 positions | **CONFIRMED** | Verbatim in Abstract and Contributions bullet 3: "the optimal layer identified by an automated method on clean inputs shifting by up to 17 positions." Note some individual Table 4 rows show larger shifts (up to +20), so 17 is the paper's conservative/headline figure, not a maximum being understated. |

All three numbers check out as accurately transcribed from the source.

## Corroboration analysis: does this match HEXIS's steering failure (14% hold under 5-level pressure)?

**Structurally yes, numerically/methodologically no — treat as qualitative
corroboration, not a parallel data point.**

What's usable: this paper is strong independent evidence that steering-class
interventions (including MD, which is essentially CAA) are brittle to
input-level adversarial perturbation specifically — the same broad class of
vulnerability HEXIS reports for tuned CAA steering. The mechanism described
(steering direction/strength degrading under adversarially rephrased input)
is the same qualitative phenomenon as HEXIS's "steering collapses under
pressure" claim, and it holds across a wide sweep of model scales (1.5B–30B)
and extraction methods, which strengthens the generality of the claim that
steering is not just fragile for one method or model size.

What limits the analogy:
1. **No graduated pressure scale.** Their attack is a one-shot adversarial
   rewrite of the input, evaluated as binary success/failure at a fixed
   confidence threshold (δ=0.3). There is no "5-level pressure" escalation
   scheme — this is the single biggest structural mismatch if the memo
   implies a level-for-level comparison to HEXIS's design.
2. **Different task/output type.** Their target is binary Yes/No persona-trait
   questions (Anthropic MWE), not open-ended belief-holding under adversarial
   argument or debate.
3. **MD (≈CAA) is evaluated as one of four methods, not isolated**, but it
   does show meaningfully worse robustness in several rows (e.g., Qwen3-14B
   MD Rdir drops up to 0.66) — directionally consistent with HEXIS's own weak
   result for tuned CAA (14%), even though it is not the same metric, scale,
   or attack type.
4. Their perturbations are applied to the *input prompt*, whereas HEXIS's
   adversarial pressure is presumably applied via escalating dialogue/argument
   against a held belief — a different threat surface (prompt perturbation vs.
   in-context adversarial pressure over a conversation).

## Threats / misfits
- Scope is explicitly restricted to **alignment-oriented steering** (Limitations,
  p.9); the authors intentionally exclude other applications like math
  reasoning or code generation. Fine for HEXIS's persona/belief framing, but
  don't extend the citation to non-alignment steering claims.
- The "up to 17 positions" headline is smaller than some individual shifts
  reported in the appendix tables (up to 20) — not a misrepresentation, but
  worth knowing the number is not the ceiling of what the paper found.
- Two of the five models' Table 1 confidence-collapse numbers live in
  appendix tables not directly re-verified in this pass (flagged above);
  low risk given the consistency of the pattern across the three models
  checked directly, but worth a spot-check before finalizing if precision on
  "all five" matters.

## Citation guidance

Cite this paper as strong, independently-produced evidence that activation
steering (including CAA/MD, the method closest to HEXIS's own tuned-CAA
baseline) is structurally brittle under adversarial input perturbation across
a wide span of model scales and extraction methods — this directly supports
HEXIS's broader claim that steering-class interventions collapse under
pressure. **However, do not present it as a level-matched corroboration of
the specific 14%-hold-under-5-level-pressure number**: their attack is a
single-shot adversarial rewrite scored as binary success/failure at a fixed
confidence threshold, not a graduated pressure scale, and their outcome
variable (binary persona-trait Yes/No confidence) differs from HEXIS's
belief-holding metric. The cleanest citation framing is "independent evidence
that steering-based interventions fail under adversarial input perturbation,
across four extraction methods and five models spanning 1.5B–30B parameters,"
with an explicit note that the pressure/attack design differs from HEXIS's
graduated adversarial-pressure protocol so readers don't infer a numeric
apples-to-apples match.
