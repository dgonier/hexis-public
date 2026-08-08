# The Override Gap: A Magnitude Account of Knowledge Conflict Failure in Hypernetwork-Based Instant LLM Adaptation

## THREAT VERDICT (lead section, per explicit request)

**THREAT LEVEL: LOW.** This paper does not anticipate, measure, or threaten the
installation-vs-persistence dissociation. It diagnoses a *different* failure axis entirely —
single-shot, first-query, installation-time override strength as a function of parametric prior
magnitude — using a framework (Eq. 6, `∆lora > ∆prior`) that has no temporal or turn index at
all. Every accuracy number in the paper is computed from exactly one query against a freshly
generated adapter; there is no dialogue, no follow-up, no contestation of an already-successful
override anywhere in the 35-page paper. The paper's own language explicitly asserts, without
testing, that parameter-level effects are "persistent" relative to prompt-level ones — this is
the exact unexamined assumption our work empirically investigates and complicates. It is
citable, valuable, adjacent prior art; it is not scooping prior art.

### Recommended related-work differentiation language (ready to drop into the positioning paragraph):
> "The compiled-modulation lineage's most direct engagement with knowledge conflict, Cheng et al.
> (2026), diagnoses a magnitude deficit that causes hypernetwork-generated adapters to lose to
> strong parametric priors on a single, first-asked, contradicting query — and explicitly
> characterizes parameter-level effects as 'persistent' relative to prompt-level ones without
> testing that persistence against any subsequent contest. We measure the axis they assume: does
> an installed stance survive a second, adversarial turn, not merely the first one."

This framing (a) demonstrates we read and engaged with the closest paper in the lineage, (b)
correctly credits it for its installation-side finding, (c) uses their own hedge/assumption
("persistent... query-agnostic") as the precise gap we fill, and (d) does not imply they
overlooked something obvious — their single-time-point framework was a scope choice, not an
oversight.

---

## Citation
Shuaizhi Cheng, Xiang Shi, Zhiwei Zhang, Mingwei Li. *The Override Gap: A Magnitude Account of
Knowledge Conflict Failure in Hypernetwork-Based Instant LLM Adaptation.* Harbin Institute of
Technology / Imperial College London / KigLand Machine Learning Lab. arXiv:2604.23750 (v2, 11 May
2026). Preprint, "Preprint" stated on manuscript; no venue/proceedings listed.

## (a) What exactly is their "knowledge conflict failure"? Installation-time, not persistence.

Their setup, precisely: a document is internalized via Doc-to-LoRA's public hypernetwork
checkpoint (one forward pass) that contradicts a fact the base model already holds strongly
(e.g., "The capital of the UK has moved from London to Birmingham," or "the capital of France has
been moved to Lyon"). The question is then asked **once**, immediately, with greedy decoding
(64-token budget), and scored as override-success or override-failure by substring match against
the document's answer. This is entirely a **first-ask, static, non-dialogic** evaluation: no
conversation, no second turn, no attempt to re-contest an override that already succeeded, no
escalating or adversarial pressure applied after installation. Their formal framework —

> `∆prior := ℓ_pre(y_pre; x) − ℓ_pre(y_doc; x) ≥ 0` (pretrained margin)
> `∆lora := δℓ(y_doc; x) − δℓ(y_pre; x)` (adapter's shift to the margin)
> Override succeeds iff `∆lora > ∆prior`

— is a magnitude contest evaluated at a single point in time from a single logit computation. It
has no notion of a second query, a changed context, or a contest that unfolds over an
interaction. This is unambiguously an **installation-strength** problem (does the new fact even
overwrite the old one on the very first try), not a **persistence** problem (does an
already-installed fact survive a later challenge).

The one passage that gestures toward persistence is analytical commentary, not an experiment.
Comparing to prompt-engineered RAG (§8.6, "Stronger RAG baselines"):
> "the effect is prompt-injectable and not persistent: the instruction must be repeated for every
> query that might touch the conflict, and an adversary in control of the prompt can trivially
> remove or negate it... parameter-level methods remain useful for persistent and query-agnostic
> behavior."

This claim is asserted by analogy — parameters are architecturally "always there" for every
subsequent query, unlike a prompt that must be re-supplied — not demonstrated by any experiment
that tests whether the parametric override actually survives a *contradicting* follow-up, an
adversarial dialogue, or any pressure applied after a successful first override. Their
"persistent" means "does not need to be re-supplied per query" — the same false-friend usage
flagged in the Doc-to-LoRA note (App. F: "yields persistent, re-usable adaptations") — not "holds
under contest."

## (b) Headline numbers and setup

- **Backbone/checkpoints**: Doc-to-LoRA's public hypernetwork checkpoints — Gemma-2B-IT (80K
  training steps, primary), Mistral-7B-Instruct-v0.2 (20K steps), Qwen-4B-Instruct (20K steps).
- **New benchmark, KID-Bench (489 questions)**: A = novel knowledge (245 Qs, 83 knowledge points,
  fictional entities); B = combination (50 Qs, 25 knowledge points, 2-hop reasoning combining an
  injected fact with a parametric one); C = conflict (194 Qs, 72 knowledge points across
  C-Light/64, C-Medium/61, C-Deep/69, graded by how entrenched the contradicted fact is in typical
  pretraining data).
- **Baseline Doc-to-LoRA conflict accuracy collapses with conflict depth** (Table 1, Gemma-2B):
  C-Light 57.8% → C-Medium 55.7% → **C-Deep 46.4%**. Novel-knowledge recall stays high throughout
  (96.7%). *(Note: this 46.4% figure lexically resembles our compiled-modulation install rate of
  46% — confirmed coincidental; see verdict discussion below.)*
- **Prior-strength stratification** (194 conflicts sorted by the base model's own
  log-probability on the pretrained answer): baseline accuracy falls from **68% (weakest-prior
  quartile) to 16% (strongest-prior quartile)**, a 52-point gap — their central causal claim, and
  entirely a single-query measurement per question.
- **Their fix**: Selective Layer Boosting (SLB — scales the top-25%-by-Frobenius-norm layers by
  β=1.75) and Conflict-Aware internalization (CA — probes base-model confidence first via one
  extra forward pass, then boosts only when a conflict is detected). Raises C-Deep from
  46.4%→71.0% (Gemma) and 53.6%→72.5% (Mistral), while preserving novel recall (96.7%→97.1%).
  Both fixes are training-free, applied at inference time, still on a single-shot question.
- **RAG comparison** (Table 7/8): CA beats *vanilla* RAG on medium/deep conflicts by ~18pp
  (Gemma), but a *conflict-aware prompt* (explicitly instructing the model to trust the document)
  beats CA by ~22pp on the same subset — so their "beats RAG" claim is qualified to vanilla RAG
  only, not RAG under best-case prompting.
- **Multi-document composition** (§10.3, "Multi-document capacity"): concatenating three
  conflicting documents drops CA's per-fact override from ~70% (single-document) to ~50% —
  the closest thing to a capacity/interference stress test in the paper, still single-turn,
  single-query per fact, not multi-turn dialogue.
- **External validation** (§8.7): three held-out sets (a 30-question fresh-entity set, a
  40-question CounterFact-style set, a 40-question RippleEdits-style set) reproduce the same
  ordering (CA > SLB > baseline) with KID-Bench-tuned hyperparameters kept fixed, addressing
  overfitting concerns. Direct comparison to ROME on RippleEdits-style items: CA 77.5% vs. ROME
  72.5%, at roughly 1/100th the latency (~0.5s vs. 45-60s).
- **Retention checks** (§8.4): 15-question unrelated-fact probe (91% retained vs. 93% pure base);
  26-question MMLU-style probe (88.5% retained, matching pure base); GSM8K/TruthfulQA at 200
  questions each show Relevance-Gated CA exactly matches pure-base accuracy.

## (c) Does anything anticipate the dissociation, measure adversarial/contradicting turns, or explain our 46%-install/89%-hold pattern?

**No, on all three counts.**

- **No dissociation measurement.** The paper never installs a stance/fact and then re-tests it a
  second time under a different or escalating challenge. There is no "installation rate" paired
  with a separate "persistence rate" anywhere in the results — every condition reports exactly
  one number (did the override happen, yes/no, on this one ask).
- **No adversarial/contradicting-turn evaluation.** The nearest analog, "Multi-conflict
  composition" (three documents concatenated, one question asked per fact), stresses adapter
  *capacity* under multiple simultaneous injected facts — not resistance to a live, contesting
  interlocutor. There is no dialogue agent arguing back, no multi-turn debate structure, no
  pressure schedule of any kind, anywhere in the paper.
- **Does not explain, and is not compatible with, our 46%-install/89%-hold pattern.** Their
  46.4% is a *baseline single-shot install rate on the hardest conflict tier, before their
  training-free fix*; our 46% is a compiled-modulation *installation rate* in a categorically
  different paradigm (typed belief graph → hypernetwork → per-layer Q/V modulation, vs. their
  raw document → hypernetwork → MLP down-projection LoRA) and a categorically different protocol
  (does the stance get adopted at all on turn one, vs. does an installed stance survive
  turns of dialogue pressure afterward). The numeric resemblance (46.4% vs. 46%) is coincidental
  — different benchmarks, different models, different measurement definitions. More importantly,
  their magnitude account has **no mechanism that could produce our dissociation**: their theory
  only has one time-point, and every one of their interventions (SLB, CA) improves both novel
  recall and conflict-override accuracy together — they never observe, discuss, or have a
  framework capable of expressing a case where a technique installs *worse* but holds *better*
  once installed. This is worth stating plainly: a reviewer familiar with this paper might expect
  our dissociation to reduce to their magnitude account, but it cannot, because their account is
  definitionally silent on any second time-point.

## (d) Verdict and exact citation guidance

**Verdict: does NOT threaten the novelty claim.** It is rigorous, adjacent prior art on a
*different* weakness of the same architectural family (installation-time override strength vs.
parametric-prior magnitude), evaluated with a single time-point per question throughout. Citing
it strengthens our paper for two reasons: (1) it is the most methodologically careful
robustness-adjacent study in the lineage, which raises rather than lowers the bar we should hold
our own experiments to; and (2) its own language ("not persistent," single-query framing) can be
used to pre-empt a reviewer who might otherwise ask "didn't the override-gap paper already study
this?" — see the boxed differentiation language at the top of this note, ready to paste into the
positioning paragraph.

## Threats to novelty (formal list, for consistency with the other five notes)

1. **§8.6, "Stronger RAG baselines" (p.14 in-doc)** — the "not persistent... persistent and
   query-agnostic" passage quoted in full above under (a). Low-to-moderate risk: uses exactly our
   vocabulary ("persistent") in exactly our topic area (knowledge conflict in hypernetwork
   adaptation) without testing it. Must be cited and explicitly distinguished, not ignored, or a
   reviewer who knows this paper will raise it unprompted.
2. **Numeric coincidence**: baseline C-Deep accuracy of 46.4% (Table 1) vs. our compiled-
   modulation install rate of 46%. Confirmed coincidental on inspection (different benchmark,
   different model, different measurement protocol, different paradigm) — flagged here only so
   that if a reviewer notices the resemblance, we have a documented explanation ready rather than
   appearing to have missed it.
3. **KID-Bench's "Multi-conflict composition" ablation** (§10.3) is the closest thing to a
   capacity-under-competing-facts test — worth a passing citation as evidence the family has
   begun probing capacity limits under multiple simultaneous facts, distinct from our
   turn-by-turn persistence-under-dialogue-pressure setting.

## Citation guidance
Cite this paper as the compiled-modulation lineage's most rigorous study of installation-time
failure — it establishes, with a validated causal mechanism (a magnitude contest between adapter
signal and parametric prior strength) and extensive robustness checks (cross-model replication,
external held-out benchmarks, decoding-temperature and paraphrase sensitivity checks), that even
getting a contradicting fact installed at all is a nontrivial, prior-strength-dependent problem
for this architecture family. Use it to preempt the "isn't this already studied?" objection by
quoting its own "not persistent... persistent and query-agnostic" language (§8.6) as the
unexamined assumption our paper tests. Do not cite its 46.4% baseline number near our 46%
compiled-modulation figure without the disambiguating context above — the resemblance is
coincidental and should be addressed proactively rather than left for a reviewer to flag. Credit
it explicitly for demonstrating that installation strength and prior-conflict resistance are
governed by adapter *magnitude*, which is a genuinely useful, complementary finding to frame
against our claim that installation and persistence can move in *opposite* directions depending
on modulation strategy (context vs. compiled) — their paper is entirely About the "install"
side of that tradeoff and never touches the "hold" side.
