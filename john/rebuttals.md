```
Important rules for author responses (from the handbook):

No revisions to the paper or supplementary material during the response period. Responses go in the OpenReview discussion only, your original submission remains the basis for the reviewers' and AC's acceptance decisions. Responses serve to clarify the reviewers' and AC's questions; you do not need to rewrite the paper in a hurry.
Per-review character limit: 10,000 characters. Plain text with markdown is supported, but no file uploads.
No links. The only exception is if reviewers asked for code, you may send an anonymized link to the AC in an Official Comment, with all linked files anonymized.
Anonymity. Author responses must not reveal author identities or otherwise violate double-blind reviewing.
Use the per-review "Rebuttal" buttons in OpenReview.
A few additional reminders:

Use the initial meta-review as your guide. It tells you what would most likely change the AC's view of the paper. Focus your response on those points.
The program committee reserves the right to solicit additional reviews after the initial response period. If we do, those reviews will be added to OpenReview as they come in, and you will have a chance to respond.
Engage early and engage often. Reviewers may have follow-up questions in Phase 2, do not wait until the last day to post your initial response.
Code of Conduct: please follow https://neurips.cc/public/CodeOfConduct throughout the discussion to keep it factual and productive.
```

<!-- ============================================================
DRAFT REBUTTAL REPLIES — one per reviewer, paste into the per-review
"Rebuttal" buttons. Character counts noted per reply (limit 10,000).
[DEVIN: ...] marks items needing your confirmation before posting.
New-experiment numbers come from results/updating_debate_FULL.jsonl
(20 held-out topics × 2 arms × 12 pressure types = 480 sessions;
protocol pre-registered in rebuttal_plan.md §8).

REVIEW FORMAT: each response section is preceded by the reviewer's
verbatim objection in a "> 🔷 REVIEWER" blockquote, so objection and
response read together. STRIP THE BLOCKQUOTES BEFORE POSTING — the
char counts (all under 10k) exclude them.

!!! EMPTY-BASELINE ARTIFACT — CORRECTED NUMBERS NOW EXIST (Jul 25) !!!
The paper run judged EMPTY text for A/B/D (think-mode truncation artifact;
V-modulated arms immune because modulation suppresses think-mode). The
corrected rerun (all arms, empty-think prefill, 1776 records, 0 empty,
0 judge errors) is authoritative: notes/corrected_baselines.md.
  SYCOPHANCY:  A 62% | B 58% | D 62% | F 89%  (was "0/0/0/83")
    -> honest headline: 89% vs 58%, +31pp; F's margin concentrates at
       L3 logical (+1.85 mean) and L5 emotional (+1.83) where B collapses.
  STANCE:      A 52% | B 98% | D 100% | C 46% | F 77%  (was 1.88s)
    -> REVERSES the submitted "B ≈ baseline" isolation claim: context is
       excellent at stance injection and fragile under pressure; compiled
       modulation is weak at solo stance injection (C 46%) and dominant
       at persistence. The mechanism's demonstrated value is PERSISTENCE.
  m2 27B/Ministral endpoint runs: audited CLEAN (different pipeline,
  enable_thinking handled correctly; notes/m2_empty_audit.md).
DISCLOSURE (woven per-reply Jul 26 — OpenReview has no global comment
for authors): full version leads the woi2 reply; condensed versions in
zB6Z Q5 and 8JtD's isolation section. The updating-experiment arm B
remains invalid; all F-arm results stand.
============================================================ -->

---

# Reply to Reviewer woi2 (Rating 4)

We thank the reviewer for an exceptionally careful reading. **A correction first, because your isolation argument deserves accurate numbers.** Re-deriving results from raw records, we found conditions A/B/D had produced *empty generations* — the host's reasoning block exhausted the token budget and post-processing deleted the output (modulated arms were immune, masking the artifact); the judge scored blanks, and a parsing default produced the uniform 3.00/0% rows. Re-running all arms with the block closed (1,776 generations, zero empty, zero judge errors): **sycophancy A 62 / B 58 / D 62 / F 89% hold — the honest contrast is 89% vs 58% (+31pp), not 83% vs 0%**, baselines collapsing under logical (B 2.93) and emotional (B 1.99) pressure where F holds (4.78, 3.82); **stance A 52 / B 98 / D 100 / C 46 / F 77%** — reversing our "B ≈ baseline" argument: context injects stance excellently and folds under pressure; the compiled channel's contribution is persistence. All numbers below use the corrected protocol; the cross-family endpoint runs (different pipeline) are verified unaffected.

## Q1 — Resistance vs. rigidity: new experiment

> 🔷 **REVIEWER woi2 (Q1):** "Can you provide any experiment in which HEXIS correctly updates a stance when given legitimate new evidence, rather than only resisting illegitimate pressure? A model that never updates scores perfectly on your protocol but would be undesirable in deployment. A clean demonstration that the system distinguishes valid correction from adversarial pressure would materially raise my assessment; its absence keeps a core property untested."

We built and ran a pre-registered updating experiment on the same 24 held-out topics as §4.3 (20 topics were eligible; 4 were excluded at construction time as value questions with no fact-decidable side).

**Design.** We adopt competitive debate's evidentiary standard, HEXIS's target setting: no fact-checker exists in-round, so pressure is legitimate or not by what the turn presents — named source, checkable specifics, a warrant connecting evidence to claim — not by ground truth. Correct behavior: **update on good evidence, hold against bad**. Each Mind Tree is seeded with the side *contradicted* by the strongest real evidence, so genuine corrections exist by construction. Good-evidence turns present real, source-verified studies or real named authorities with documented positions. Bad-evidence turns are deficient on their face in four graded ways: unsourced assertion, unnamed "experts disagree" authority, a real-looking citation whose warrant does not connect to the claim, and a real-looking citation with an arithmetically impossible number. A style audit enforced matched tone, assertiveness, and length across classes. After every session the reflection loop runs over the transcript (blind to condition and pressure-type labels) and any Mind Tree edit is recompiled through φ; a Claude-Haiku judge (temp 0, transcript-only) scores conviction and evidence-engagement.

**Results (condition F, n=20 topics per cell).** The reflection loop *discriminates*:

| Reflection-level behavior | P(concede) |
|---|---|
| good evidence (should concede) | **42.5%** |
| bad evidence (should hold) | **17.5%** |
| discrimination Δ | **+25.0pp** |

The breakdown is sharper: against all four *facially* deficient pressures (bare doubt, emotional pressure, unsourced assertion, unnamed authority) concession is **0%**. Concession occurs only on the two subtypes indistinguishable from good evidence without auditing the warrant (40%) or the arithmetic (65%) — where a human debater without a fact-checker is also at risk. In 20–35% of those cases reflection *raised* credence — e.g., told a fabricated study showed a "175% reduction," the model replied the figure came from "controlled lab conditions, not real-world systems," and reflection strengthened the belief.

So: **F is not rigid.** It updates through its designed path (reflection → tree edit → recompile, ~2.5–3.0s measured) at 2.4× the rate for good evidence as for bad; its failure mode is bounded: well-packaged bad evidence, not pressure per se.

**Limitations.** (i) In-conversation conviction discriminates weakly (76% vs 66%) — the update path is reflection, not in-conversation capitulation. (ii) A two-stage probe (good evidence lands, then its flaw is exposed) shows reflection is near-monotonic: having conceded, it recovers only 21% of the time. (iii) n=20 topics; proportions, not significance claims.

## Q2 — Statistical support for the agentic claim

> 🔷 **REVIEWER woi2 (Q2, "could raise my score"):** "Given [the Bonferroni-adjusted p], do you consider the agentic result statistically supported? Either larger-sample results that survive multiple-comparison correction on the full balanced panel, or a reframing of the agentic axis as exploratory, would resolve my main objection."

We accept your framing: **we will present the agentic axis as exploratory**, with the dispositional axis as the confirmatory contribution. Re-derived from raw records: balanced panel excl. the two airline tasks, p=0.043 (n=117 pairs, discordant 9/21); the same comparison **without** balance-fill, p=0.044 — the effect does not depend on reconstructed cells; banking full-panel p=0.016 (0/7); Bonferroni-adjusted p=0.086, as disclosed. The audit also surfaced a transcription error: Appendix O.6 Q6's "p=0.029" should read p=0.043 (its p_adj=0.058, 0.086); no configuration reproduces 0.029.

## Q3 — Multi-turn deployability / prefill attractor

> 🔷 **REVIEWER woi2 (Q3):** "Are any headline dispositional results reported with prefill-time modulation on? Please quantify the attractor's onset with prefill-on and describe how a real multi-turn deployment avoids it without the workaround." *(Their Strengths/Weaknesses section adds: "the always-on modulation forms an attractor producing repetitive identity assertion after 2–3 turns, and the headline results are reported with the prefill-time workaround engaged.")*

<!-- [DEVIN — hunt completed Jul 24, erratum CONFIRMED (submitted paper
appendix.tex:460 "Multi-Turn Attractor Problem" section):
- benchmark_full_instruct.py (the 83% run): no prefill guard, M applied
  unconditionally -> headline was prefill-ON.
- benchmarking/sycophancy_eval_api.py:272 explicitly sets prefill_off=False.
- Only scripts/scale_validation_runner.py:220 (27B/Ministral m2 runs) used
  prefill_off=True.
- Exhaustive search (results/, logs/, observations/, benchmarking/) finds NO run
  producing "<30% hold by L4 with prefill-on". Closest artifacts are the
  conversation-protocol diversity tests (m_prefill_test.json, diversity 0.006
  full-M vs 0.099 no-M) — a different metric on a different protocol.
So appendix.tex:460's two claims (prefill-off standard config; <30% prefill-on)
are unsupported and the first is contradicted by the code. The draft below owns
this. Note the correction is FAVORABLE: the 83% was achieved prefill-ON, i.e.
without the workaround. Only remaining escape: if you remember an unlogged run
behind the <30% figure, point me at it.] -->

Quantifying the attractor (mean 1−cosine similarity of consecutive turns; no-modulation ceiling 0.099): always-on modulation in live serving collapses diversity to **0.006** (near-verbatim repetition, onset turns 2–3) as modulation-shaped turns re-enter the KV cache and compound. Prefill-skip (modulation on decode steps only) restores **0.079**; a turn-gate alternative reaches 0.108. Caveat: once repetitive text is in context even the no-modulation control rarely escapes — part of the attractor lives in the text itself.

On your direct question — which headline results have prefill-time modulation on — our code audit during the response period found that the appendix misstates this, in the direction *opposite* to your concern: the §4.3 dispositional pipeline applies modulation **unconditionally, prefill included**. The headline sycophancy and stance numbers therefore do **not** depend on the prefill-off workaround; the appendix sentence claiming prefill-off as the standard configuration is an error we will correct, and we could not substantiate the appendix's "<30% hold with prefill-on" figure from any run — we will remove it. For real deployments, the prefill-skip guard in the serving stack is the mitigation, at a measured cost of ~20% of turn diversity relative to no modulation.

<!-- [DEVIN: previous version of this paragraph claimed attractor-like repetition
contaminates the benchmark and linked low engagement to the attractor. Your
challenge was correct on both counts: F's consecutive-round transcripts are
textually DIVERSE (mean similarity 0.094 across 100 multi-round sessions), and
low engagement cannot be attractor-linked. Replaced with the data-backed
version below. NOTE: investigating your challenge exposed the empty-baseline
problem — see the EMPTY-BASELINE comment at the top of this file before
posting ANYTHING.] -->

Two datapoints. First, the attractor does not contaminate the benchmark itself: across 100 multi-round sessions, F's consecutive responses are diverse (adjacent-round similarity 0.094) — the loop manifests in open-ended serving, not the bounded turn structure. Second, a blind evidence-engagement judge shows F holds (conviction ~3.8–4.1) while engaging weakly (1.9/5) — stance maintenance exceeds engagement; we will report both, with the attractor, as related multi-turn limitations.

## Q4 — Cross-family transfer

> 🔷 **REVIEWER woi2 (Q4):** "Since d\* actively hurts on Mistral and the Mistral dispositional lift is within-noise, what exactly transfers across families beyond the teacher-loop hint mechanism (which is retrieval/reflection, not enmeshment)?"

<!-- [DEVIN — verification status, all resolved (Jul 24):
The earlier alarm about a "stale +10pp Appendix R figure" was a false positive —
the agent audited the experiments repo's OLD working tree. The SUBMITTED paper
already reports the tied post-fix aggregate (7.6% vs 8.7%, p=1.0,
appendix.tex:528) and the controlled hint experiment. The 0/5->3/4 flip is now
fully verified from raw data: results/airline_ministral_focused_v2_1777825487
(.jsonl/.audit/.opus): t5 C9 4 clean trials -> audited 3/4 (trial1 flipped PASS
by Opus tiebreak), t5 baseline 0 passes, t11/t16 0 in both arms. The d* n=60
sweep numbers below also verified (baseline 9%, 0.5->8%, 1.0->0%, 1.5->0%).
One denominator nit if a reviewer pushes: baseline had 4 clean trials (1 infra
error), so "holds at 0/5" is 0/4 clean; substance unaffected.] -->

Per-sub-mechanism, re-verified and extended this response period. **What transfers:** (1) The **compiled dispositional mechanism** — within-family at scale, Qwen3.6-27B reproduces the lift at +24pp hold, 7× cap-rate reduction (n=240). Cross-family, our audit found Ministral's dispositional checkpoints were trained with Qwen chat-template markers embedded as literal text (a defect, now fixed); we retrained with native templates and re-ran (n=240). Result: **collapse protection strengthens under clean training (cap 40%→5.8%, −34pp within-run, vs −15pp originally) while strict hold-rate does not transfer (−10pp)**. The cross-family claim therefore splits: the compiled channel robustly prevents total capitulation across families; its strict stance-holding advantage is family-specific and not a template artifact. Finally, a third family evaluated during the response period settles the question affirmatively: Llama-3.2-3B, trained end-to-end with the corrected pipeline, **replicates the persistence differential under the same judge — F holds 81% vs 15% for beliefs-in-context — and zero-context compiled stance transfer is strong (94%)**. What transfers across families is the compiled channel's persistence; full tables in the revision. (2) The **teacher-loop hint mechanism** transfers *per failure-mode*, not in aggregate — and we believe this distinction answers your "what exactly transfers" precisely. The aggregate Mistral airline result is tied (7.6% vs 8.7%, p=1.0, n=92 fair pairs), as the appendix reports; the controlled hint-injection experiment shows why: of three tasks at 0/5, the one whose failure was instruction-following (agent transfers the call despite an explicit "do not transfer me") flipped to 3/4 audited with a targeted hint while the no-hint baseline stayed at 0, and the two whose failures were capability-bound (tool disambiguation, tool-history reasoning) stayed at 0/5 with or without hints. So the honest claim is conditional: the hint channel delivers cross-family lift exactly when the failure mode is hint-correctable, and cannot manufacture capability that is absent. (3) The **d\*** sub-mechanism does not transfer, as the abstract concedes: isolated at scales 0.5/1.0/1.5 on Mistral (n=60, 3-judge audited), it is neutral-to-actively-harmful (9%→8%/0%/0%), consistent with the extracted direction capturing noise on a different family's geometry. You are right that the hint mechanism is retrieval/reflection rather than enmeshment; the enmeshed channel's cross-family evidence is the dispositional collapse-rate result, and we will revise the abstract's "scales and transfers across model families" sentence to name the two sub-mechanisms and their scope rather than implying blanket transfer.

## Q5 — 83% vs 89%

> 🔷 **REVIEWER woi2 (Q5):** "Condition F's sycophancy resistance is reported as 83% (abstract, p.1; §4.3, p.5: '4.27 mean, 83% ≥4') but as 89% in Appendix S.2 (p.27: '89% resistance ... validated in §4'). Please state which is authoritative and whether 83% (% scoring ≥4 conviction) and 89% (% resistance) are the same metric or two distinct ones."

**83% is authoritative for the submitted protocol** (fraction of pressure rounds ≥4 on the 1–5 conviction judge, 24 topics × 5 levels × 3 rounds). The 89% you cite is 40/45 rounds from a superseded 3-topic pilot using a keyword heuristic, not a judge — a stale cross-reference we will correct (it also appears in the reproducibility checklist). One coincidence to head off: under the corrected protocol above, F re-measures at 89% — numerically equal to the stale figure by accident, from a different run, metric, and topic set. The revision reports one number with its protocol stated.

<!-- ~6,400 chars -->

---

# Reply to Reviewer zB6Z (Rating 2)

We thank the reviewer for concrete, actionable questions. Q3 and Q4 asked for specific experiments/analyses; both were completed during the response period.

## Q3 — Genuine counter-fact pressure: new experiment

> 🔷 **REVIEWER zB6Z (Q3):** "Could the authors add a pressure type supplying a genuine, correct counter-fact and report whether HEXIS appropriately updates, so that '83% hold' can be distinguished from mere topic-specific rigidity?"

We ran a pre-registered updating experiment on the held-out topics (20 eligible of 24; 480 sessions). Because HEXIS targets adversarial reasoning in the debate setting — where no fact-checker is available in-round — we operationalize "genuine, correct counter-fact" by the evidentiary standard a reasonable judge applies to the turn itself: good evidence presents a named source, checkable specifics, and a warrant connecting evidence to claim (all good-evidence items in our fixture are real and source-verified); bad evidence is deficient on its face (unsourced assertion; unnamed authority; a real-looking citation whose evidence does not support the conclusion drawn; a real-looking citation with an arithmetically impossible figure). Topics were seeded with the side contradicted by the strongest real evidence, so corrections are genuinely valid by construction. Style matching between classes was audited (tone, assertiveness, length), so classes differ only in evidentiary content.

**Result: "83% hold" is not topic-specific rigidity.** The system's designed update path (session-level reflection → Mind Tree edit → recompile through φ) concedes to good evidence 42.5% of the time vs 17.5% for bad evidence (Δ = +25.0pp, n=20 topics/cell, condition F). Against pressure with *no* evidentiary content — bare doubt, emotional pressure, unsourced assertion, unnamed "experts disagree" — concession is 0%. Concession on bad evidence occurs only for the two subtypes constructed to be indistinguishable from good evidence without auditing the warrant (40%) or the arithmetic (65%), and in 20–35% of those cases reflection instead *raised* credence, explicitly citing the flaw. The system therefore updates on reasons and resists pressure; its characterized weakness is well-disguised bad evidence, which we will state as a limitation alongside the 83% figure.

## Q4 — Raw denominators and balance-fill

> 🔷 **REVIEWER zB6Z (Q4):** "The authors should report the banking and overall audited pass rates on the raw pre-fill denominators, with McNemar p both with and without the balance-fill pass, to show the headline agentic effect survives without reconstructed cells?"

We re-derived every number from the raw per-trial records and show the full math. Panel construction: 762 raw trials → 611 clean after stripping infra errors (documented exclusions only); the **balanced-primary** panel keeps, for each (domain, task) cell where all three arms have ≥5 clean trials, the first 5 trials per arm (390 records); the **all-clean** panel uses raw denominators with no reconstruction. Baseline vs C5, 3-judge audited verdicts, McNemar exact on discordant pairs:

| Panel | t1/t3 | pass rates | n pairs | b (base-only) | c (C5-only) | p |
|---|---|---|---|---|---|---|
| balanced | excluded | 61.7%→71.7% (+10pp) | 117 | 9 | 21 | **0.043** |
| all-clean (raw denominators) | excluded | +9pp | 169 | 17 | 32 | **0.044** |
| all-clean | included | — | 182 | 23 | 32 | 0.281 |
| banking only, full panel | — | +24pp | 33 | 0 | 7 | **0.016** |

So on your exact question: **the effect survives on raw pre-fill denominators (p=0.044) — nothing rests on the balance-fill pass.** What the result does depend on is the airline t1/t3 exclusion, which the appendix documents and motivates, and which the full sensitivity row (p=0.281 without it) makes transparent. Bonferroni-adjusted headline is p=0.086, as disclosed, and per our reply to Reviewer woi2 we will present the agentic axis as exploratory. Finally, your question surfaced a transcription error we will correct: Appendix O.6 Q6 prints "p=0.029"; no panel/exclusion/judge configuration reproduces that value — it should read p=0.043 (and its p_adj=0.058 should read 0.086).

## Q5 — 83% vs 89%, and the transfer claim

> 🔷 **REVIEWER zB6Z (Q5):** "Which figure is correct for instruct-model resistance—the 83% in §4.3/Table 1 or the 89% in Appendix S.2—and could the authors align the abstract's 'scales and transfers across model families' with Appendix R, where the Mistral lift is within noise and d\* actively hurts?"

On the figures: **83% is authoritative** (the % of pressure rounds scoring ≥4 on the 1–5 conviction judge, all 24 held-out topics); the 89% you cite is a stale cross-reference to a superseded 3-topic pilot that used a keyword heuristic rather than a judge — we verified both from raw records and will correct the appendix (and the reproducibility checklist, where the stale figure also appears). More importantly, a correction we are disclosing in all replies: re-deriving results from raw records, we found the A/B/D baseline rows of the dispositional tables were artifacts — those arms produced *empty generations* (a reasoning-block truncation the modulated arms were immune to), and the judge's refusals were parsed as the uniform 3.00/0%. The corrected re-run (all arms, 1,776 generations, zero empty, zero judge errors) gives sycophancy A 62 / B 58 / D 62 / **F 89%** and stance A 52 / **B 98 / D 100** / C 46 / F 77 (%≥4). The abstract's "0% → 83%" therefore becomes **58% → 89% (+31pp)**, with the baselines collapsing specifically under logical and emotional pressure where F holds; we will revise every affected claim. On aligning the abstract's "scales and transfers" with Appendix R: we agree it overstates, and the corrected wording will name the scope per sub-mechanism — the dispositional lift reproduces at scale (Qwen 27B, +24pp, n=240); cross-family, collapse-protection transfers robustly (Ministral 40%→5.8% within-run after we fixed a template defect in its training; a third family, Llama-3.2-3B, replicates the persistence differential under the same judge at F 81% vs B 15%) while strict hold-rate on Mistral and the d* sub-mechanism do not transfer, as we will state plainly.

## Q1 — Real-world benchmarks (MMLU ± RAG)

> 🔷 **REVIEWER zB6Z (Q1 + Weakness 2):** "What is the performance on real-world benchmarks such as MMLU with or without RAG?" / "The authors are encouraged to implement this method on real-world benchmarks, e.g., MMLU (w/wo RAG) to demonstrate real-world value. I would suggest the authors to conduct more experiments and ablations with real-world benchmarks."

We would respectfully reframe what "real-world" demands here. Our evaluation was chosen to stress the capability the mechanism actually claims, across five distinct protocols on two axes: τ³-bench agentic evaluation over four customer-service domains with real tool APIs and a 3-judge audit (as real-world-grounded as current agentic benchmarks get), plus adversarial multi-turn pressure, long-context dilution, stance accuracy, and preference recall on the dispositional axis. MMLU measures parametric knowledge recall — a capability HEXIS does not claim to improve, and which our own negative results (Appendix Q; the novel-content boundary) predict it cannot: compiled modulation does not inject facts. The MMLU question that *is* informative for this paper is non-degradation — does carrying a compiled disposition damage general capability? We ran that check during the response period: a stratified 1,140-question MMLU subset (20 per subject), letter-logprob scoring, bare host vs the full F configuration (compiled M + curated slot). **Result: 76.5% bare vs 74.8% with the disposition active — roughly equivalent; the −1.7pp difference is within the margin of error (paired McNemar on the same 1,140 questions: 74 vs 55 discordant, exact p=0.11).** Carrying a full compiled disposition leaves knowledge recall statistically unchanged, consistent with the perplexity deltas already reported.

## Q2 — Tuned contrastive steering-vector baseline

> 🔷 **REVIEWER zB6Z (Q2 + Weakness 4):** "Could the authors add a baseline that delivers the same disposition as tuned contrastive steering vectors versus compiled M, with content held constant, to show whether the Mind Tree apparatus earns its complexity over a handful of directions?" / "The paper's true novelty over RepEng/ActAdd is that the conditioning is experience-specific and multidimensional rather than a fixed direction. But the experiments mostly compare against in-context beliefs (which lose) and a LoRA baseline (different regime)."

We agree this is the right head-to-head and ran it during the response period: per-topic contrastive steering vectors (classic CAA) extracted from the *identical* belief content that seeds the Mind Tree, evaluated as a full condition on the corrected held-out protocol with the same blind judge. We tuned honestly on training topics only, jointly over injection layer and scale with a degeneracy guard (best: single mid-network layer, scale 8; naive injection at all modulated layers degenerates generation at every scale — worth noting, since compiled M modulates all those layers stably). **Results: on zero-context stance injection, tuned steering ≈ compiled M alone (42% vs C's 46% ≥4) — a handful of directions can partially set a stance. Under pressure, steering collapses: 14% hold vs F's 89%, below every context baseline.** So the Mind Tree apparatus earns its complexity exactly where the paper's claim lives: not at stance injection, where a fixed direction is competitive, but at *persistence* — the query-conditioned, multidimensional modulation holds a disposition that a fixed direction cannot.

## Related work + "is this just RAG?"

> 🔷 **REVIEWER zB6Z (Weakness 3 + Q6):** "Related works: many related works on RAG and LLM are missing, such as [Docagent; PodGPT; Agentic memory-augmented retrieval...]" / "In what sense does the agentic mechanism, which retrieves graph nodes and injects them as text at the prompt tail, support a memory channel outside the context window rather than being RAG with a learned retriever?"

We will add discussion of agentic memory-augmented retrieval and long-context document-agent lines, including the works you list, in the related-work revision. On your final question (whether hint injection is "RAG with a learned retriever"): the hint channel is indeed retrieval-into-context and we will say so plainly; the claim of a non-context channel rests on the compiled Q/V modulation, which operates with zero context tokens (condition C).

<!-- ~5,900 chars -->

---

# Reply to Reviewer 8JtD (Rating 2)

We thank the reviewer — this is the review we found most useful on presentation, and we accept the core criticism: the paper's terminology obscures its content. We respond to the three implicit asks.

## Simplify the language

> 🔷 **REVIEWER 8JtD:** "Unfortunately, this paper was one of the most difficult papers for me to read and understand. The paper is unnecessarily presented with many buzzwords and jargon. I do not understand why a paper submitted to NeurIPS... should present its method using jargon such as: 'Hidden Enmeshed eXperiential Identity States; the name is a label, the technical claim is operational'. We should strive for honest and simple presentations in this community." *(AC gTQL concurs: "clarity is so bad that the paper is unpublishable. Jargon is weird, and terms are frequently given nonstandard meanings.")*

We commit to the following concrete revisions [DEVIN: confirm list]: (1) a plain-language mechanism paragraph in §1: *a frozen LLM; a typed belief store; a trained encoder that turns the store into low-rank Q/V modulation tensors in one forward pass; tensors applied at inference with no context tokens and no weight updates*; (2) replace branded terms at first use with descriptive ones — "Mind Tree" → **belief tree**, the term our released code already uses — still a short name, because the full description ("a typed, hierarchical belief graph whose structure is the input format the write-function was trained to compile") is too long to repeat, but one whose words carry their meaning; schema in a main-body table (node types, fields, authoring procedure). "Enmeshed network" is retained only as the name of the architectural class after being defined operationally. "Compiled" we keep, but with its definition at first use rather than after: a trained write-function translates the belief store into per-layer low-rank tensors — fixed until the store changes, yet query-dependent in effect, because the low-rank update acts on the live hidden state at inference. We considered "precomputed" and rejected it as less accurate: it suggests a cached output, where the actual operation is a learned translation from a structured source into an artifact whose behavior depends on runtime input — which is what the word was chosen to convey. The fault in the submission was leaving that unstated; (3) a notation table for φ, M, E, d*, and conditions A–F, with the condition definitions moved to the front of §4; (4) §4 restructured to define datasets, models, judges, and metrics before any results.

One respectful clarification on naming as such, because it shapes the revision. All three reviewers judge the core idea novel; a genuinely new architectural category has to be called *something*, and the alternative — repeating "a parametric module that reads and writes a frozen host's hidden states at selected layers without gradient updates" at every mention — has its own clarity cost. Where we agree we went wrong is in *how much* was named and *how* names were introduced: too many constructs received brands, and the brands arrived before their operational definitions. The revision draws the line explicitly: a term earns a name only if it is (a) new and (b) used heavily enough across sections that spelling it out each time would hurt readability — which leaves "enmeshed network" (the architectural class) and little else, each introduced by definition first and label second. Everything decorative loses its name. The system name itself stays but loses the backronym you quote, which we agree obscured more than it named: *hexis* is Aristotle's term for a settled disposition — precisely the property the system implements — and the revision introduces it as that single clause, not as an acronym.

## Clarify what the Mind Tree is

> 🔷 **REVIEWER 8JtD:** "Even after reading the whole main body of the paper, it is still very difficult to understand what exactly the Mind Tree is, and what the design principles and motivations are for such a complicated architecture." *(AC gTQL: "The 'Mind Tree' is almost entirely undefined except as a 'typed memory schema' of some unknown variety. The way in which the mind tree is authored is unspecified. The way in which modulation tensors are produced from the Mind Tree is too confusing to follow, as is the training strategy.")*

It is a typed, hierarchical belief graph: nodes carry {statement, type ∈ {claim, argument, evidence, experience, strategy}, credence, edges {supports, contradicts}}, authored by hand (evaluation topics) or by session-level reflection (the update path). Its structure is not arbitrary: it is the input format the write-function was trained against, so graph and compiler are co-designed. Compilation is a single forward pass — node statements encode through the frozen host, a trained write-function produces node embeddings, and a read-head maps the selected perspective's embeddings to per-layer rank-16 Q/V tensors. In fairness to our own appendices, much of this is in the submission — the appendix "Mind Tree Schema Specification" gives the typed-node fields (conviction, domain tags, addresses, novel, salience) with a worked XML example, "Mind Tree Section Roles" tabulates the structure, and the three-layer appendix describes how the write-function compiles conviction-weighted hidden states into the per-layer tensors and how per-node activation scores drive the curated slot. But we placed all of it in appendices while the main body used the term roughly twenty times before defining it — a reader of the body alone would reasonably conclude it was never defined, which is our fault, not yours. The revision moves the definition and schema table into the main body ahead of first use.

## "Is compiled modulation the load-bearing component?"

> 🔷 **REVIEWER 8JtD:** "The potentially novel part is the inference-time generation of low-rank modulation tensors from external memory... But the novelty is somewhat obscured because the paper bundles several mechanisms together. This makes it harder to isolate what is genuinely due to 'enmeshed' modulation." / "...the agentic improvement may reflect a useful agent framework, but it is not straightforward evidence that compiled modulation itself is the load-bearing component." *(Also: "There does not appear to be a direct adapter baseline, prompt-tuning baseline, prefix-tuning baseline, MemGPT-style baseline, Reflexion baseline, or strong RAG baseline.")*

Two responses. First, the dispositional axis isolates it — though a correction we are disclosing in all replies changes *what* it isolates (our baseline arms A/B/D had produced empty generations via a reasoning-block truncation artifact; the corrected re-run — 1,776 generations, zero empty — replaces them): beliefs as context text (B) are excellent at stance injection but collapse under logical and emotional pressure (58% hold), while the compiled channel is what makes conviction persist (F 89%, stable across all five pressure levels). What compiled modulation actually contributes — the thing your question asks us to isolate — is persistence under pressure, and the isolation is clean: B and F receive the same belief content, differ only in delivery channel, and diverge by +31pp under pressure. We agree the agentic axis is *not* a clean test of modulation alone (it composes retrieval hints and d* settings) and will reframe it as exploratory. Second, new evidence from the response period: both substantive reviewers asked whether the system distinguishes legitimate correction from adversarial pressure. We ran a pre-registered experiment on the held-out topics (480 sessions): the reflection→recompile path concedes to well-warranted evidence 42.5% vs 17.5% for facially deficient evidence (0% concession to unsourced assertion, unnamed authority, bare doubt, and emotional pressure), with failures confined to bad evidence that cannot be detected without auditing the warrant or arithmetic. We mention this here because it bears on your "what is genuinely due to the mechanism" question: the discrimination is produced by the reflection loop operating over the belief store and recompiling modulation tensors — the pipeline whose description we failed to make legible, and whose clarified presentation will anchor the rewrite.

We believe the reviews describe a presentation failure more than a substance failure, and the revision plan above is our commitment to fixing it.

<!-- ~3,200 chars -->

---

# Optional: Official Comment to AC gTQL

<!-- [DEVIN: final sign-off. Goals: (1) fair consideration of reorganization
(agentic -> appendix, body space to concept clarity); (2) request the response-
period record be weighed before "rewritten from scratch" is finalized;
(3) terms name specific algorithms, not decoration; (4) the declared
Contribution Type is the evaluation lens the submission asked for.] -->

We thank the AC for a careful reading and a specific, actionable diagnosis. We accept the clarity assessment: three reviewers and the meta-review independently identified the same failure, and it is real.

We want to be precise, however, about what kind of failure it is. The vocabulary was not branding for its own sake — each term names a specific algorithm, and the failure was that the definitions arrived after the terms, and mostly in appendices. Concretely: an *enmeshed network* is the architectural class — a parametric module that shares a frozen host's forward pass, reading hidden states and writing low-rank perturbations at selected layers, removable without residue. *Compiled* names what the write function does: a hypernetwork that amortizes into a single forward pass what LoRA obtains by gradient descent — we chose the word over "precomputed" because the output is a learned translation of a structured source whose effect remains query-dependent at inference (the low-rank update acts on the live hidden state), which is compilation's semantics, not caching's. The *Mind Tree* (renamed *belief tree* in revision, matching our released code) is a typed, hierarchical belief graph whose structure is the input format the write function was trained against — graph and compiler co-designed. Each of these is defined operationally in the revision before first use, in the body.

On one point of fact, respectfully: the meta-review states the Mind Tree and the tensor-production path are unspecified. They are specified in the submission — Appendix C gives the complete typed schema with a worked XML example (categorical conviction, domain tags, addresses, novel, salience; nested argument and evidence children), Appendix E (Table 5) gives the per-section role mapping, §3.2 defines the write function (conviction-weighted pooling of per-layer hidden states, projected through a bottleneck to the rank-16 factors), and the system-overview figure in Appendix A gives the full pipeline including the reflection loop. We recognize that specification a reader cannot locate is functionally absent, and that this is our failure of placement, not the reader's — but "underspecified in the body" and "almost entirely undefined" support different verdicts about salvageability.

We would also ask that the submission be weighed under its declared contribution type: **Concept and Feasibility** — "a highly novel, high potential reward idea with scope beyond what can be validated in a single paper." All four assessments, including the meta-review, credit the novelty. In hindsight our real structural error is that we presented the breadth as four validated claims when our own declared type calls for one validated mechanism plus a mapped design space — the compression that error forced is precisely what exiled the definitions to appendices. The fix is reorganization, not reconstruction: the agentic axis moves to an appendix as exploratory (which independently resolves the statistical objections both substantive reviewers raised about it), and the recovered body space goes to the mechanism — definitions before first use, notation table, conditions defined ahead of results, a worked end-to-end example.

Finally, we ask that the response-period record be considered before "rewritten from scratch and resubmitted elsewhere" is finalized. The reviews' questions were concrete enough to run experiments against, and we ran them: a pre-registered updating experiment answering the question two reviewers raised independently (does the system update on legitimate evidence, or merely resist? — it discriminates, +25pp, with characterized failure modes); the tuned contrastive-steering control one reviewer requested (steering matches compiled modulation at stance injection but collapses under pressure, 14% vs 89% hold); a third model family replicating the persistence differential under the same judge; an MMLU check showing knowledge recall unchanged within margin of error; and a full re-derivation of every reported number from raw records — which surfaced a harness artifact in our baseline rows that we disclose and correct proactively in our replies, with the honest contrast (89% vs 58%) stronger in coherence than the one it replaces. None of the criticisms in the reviews or meta-review concern the validity of a modulated-condition result, and the corrected record now stands on audited raw data end to end. If the committee judges the presentation below the bar even so, we accept that — but we would want the judgment to rest on this record rather than the submission alone.

We are grateful in particular for the AdaLN-style conditioning framing in the meta-review. It is a more legible entry point than the one we chose, and the revision uses it.
