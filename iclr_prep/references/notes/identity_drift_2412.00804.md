# Examining Identity Drift in Conversations of LLM Agents

## Citation metadata
- **Title**: Examining Identity Drift in Conversations of LLM Agents
- **Authors**: Junhyuk Choi, Yeseon Hong, Minju Kim, Bugeun Kim (Department of
  Artificial Intelligence, Chung-Ang University, Seoul, Republic of Korea)
- **arXiv**: 2412.00804v2 [cs.CY], 17 Feb 2025

## Core findings (with exact numbers and locations)

Studies "identity drift" — defined narrowly by the authors as change in
*interaction patterns or talking style/response patterns*, explicitly **not**
psychological identity or consciousness (footnote 1, p.1) — across 9 LLMs via
36-turn dyadic (two-agent) conversations on personal/emotional/values themes,
adapted from the Aron et al. (1997) "interpersonal closeness" psychology
protocol (§3.3). Identity consistency is measured with **14 PsychoBench
psychometric questionnaires** (Big Five, EPQ-R, Dark Triad Dirty Dozen, BSRI,
CABIN, ICB, ECR-R, GSE, LOT-R, LMS, EIS/WLEIS, etc.) plus the **McGill
Friendship Questionnaire (MFQ)**, administered as snapshots after turns 12,
24, and 36, and compared via repeated-measures ANOVA or Friedman test with
posthoc Tukey/Wilcoxon (Bonferroni-corrected) (§3.5). A sub-factor counts as
"consistent" (checkmark in Table 3) if the change across the three snapshots
is **not** statistically significant.

**RQ1 (9 models, no persona assigned)**: GPT-3.5-turbo, GPT-4o, LLaMA
3.1-8B/70B/405B, Mixtral8x7B/8x22B, Qwen2-7B/72B (Table 1, p.4).
- **Larger models show more identity drift.** Small models (≤10B) are the
  most stable — partly because they refuse/deflect as "an AI" rather than
  engaging emotionally; larger models fabricate fictitious details about
  themselves or their conversation partner, which then destabilizes identity
  over subsequent turns (§4.1, p.6–7; Table 2/topic analysis, p.5).
- **Model-family effect exists but is weaker than parameter-size effect**
  (§4.1, "In summary, parameter size has a stronger influence on identity
  drift than model families," p.7).

**RQ2 (persona assigned, 2 models — GPT-4o and LLaMA-3.1-405B, chosen because
they showed the largest drift in RQ1)**: two persona "influence levels" —
low-influence (outgoing/goal-oriented) and high-influence
(emotionally-sensitive/empathetic), 20 personas/group, 10 conversations/group
→ 400 logs (§3.2–3.3).
- **Persona assignment does not reliably fix identity drift, and the effect
  is model-dependent**:
  - GPT-4o: without persona, retained identity in **5 factors** total. With
    persona: only **2 factors** (low-influence) or **6 factors**
    (high-influence) retained — essentially no improvement, sometimes worse
    (§4.2.1, p.7–8).
  - LLaMA-3.1-405B: without persona, retained **7 factors**. With persona:
    **16 factors** (high-influence) or **10 factors** (low-influence) —
    substantial improvement (§4.2.1, p.7–8).
- Conclusion (p.8): "the assignment alone does not ensure consistency of
  identity; rather, the model's inherent characteristics play a greater role
  in determining how well it maintains a given identity."

Locations: Abstract; §4.1 (p.6–7, parameter-size/family effects); Table 2
(p.5, topic-modeling qualitative results); Table 3 (p.5–6, factor-retention
counts per condition — the key table); §4.2/4.2.1 (p.7–8, persona effect,
GPT-4o vs. LLaMA-405B numbers); Conclusion (p.8).

## Positioning-memo verification

**Assertion (b)**: "identity-drift paper shows explicitly assigning a persona
does NOT reliably maintain identity ('the closest existing statement of our
negative result in a different setting') — what exactly did they test, which
models, what metric?"

**Status: CONFIRMED, verbatim, with an important scope caveat.**

The abstract states the finding directly as one of three headline results:
"(3) Assigning a persona may not help to maintain identity." The Conclusion
restates it: "regarding persona assignment, the assignment alone does not
ensure consistency of identity; rather, the model's inherent characteristics
play a greater role."

What exactly was tested: 36-turn free-flowing two-agent conversations on
personal/emotional themes (not adversarial argument — see Threats below),
with identity operationalized as consistency on 14 psychometric
questionnaires + MFQ, measured as a **count of statistically-consistent
sub-factors** (out of ~40 possible) across three time snapshots. Models: only
**GPT-4o** and **LLaMA-3.1-405B** were tested with personas (RQ2); the
broader 9-model comparison (RQ1) tested no personas at all.

**Important nuance**: the result is explicitly **model-dependent, not
universal**. GPT-4o showed persona assignment provide no benefit (and mild
harm in the low-influence condition); LLaMA-3.1-405B showed a large benefit
from persona assignment. The paper's own conclusion hedges accordingly — it
does not claim persona assignment universally fails, only that it "does not
necessarily guarantee" consistency and that the effect "may vary across
models." Any citation implying a uniform "personas fail" result would overstate
what the paper actually found.

## Threats / misfits

Is "the closest existing statement of our negative result in a different
setting" a fair characterization? **Defensible, but only with explicit
caveats** — without them, the analogy overstates the connection:

1. **No adversarial pressure at all.** This is the single most important
   caveat. The conversational protocol is ordinary, non-adversarial dialogue
   on emotional/personal themes (borrowed from a psychology closeness-building
   study) — there is no adversarial actor, argument, or attempt to challenge
   the persona/identity in the conversation design. This is a much weaker,
   passive threat model compared to HEXIS's adversarial pressure levels. If
   HEXIS's memo implies this paper shows persona failure *under pressure*,
   that would misrepresent the setup.
2. **Different construct measured.** The metric is persona/personality-trait
   consistency (Big Five, attachment style, dark-triad traits, etc.) via
   psychometric questionnaires, not belief-holding under argumentative
   challenge. Personality traits and propositional beliefs defended in debate
   are related but distinct constructs.
3. **Explicitly model-dependent, not a clean universal failure.**
   LLaMA-3.1-405B actually *improved* substantially with persona assignment;
   only GPT-4o showed the "doesn't help" pattern. A memo phrasing that implies
   uniformity across models would not be supported by the paper's own data.
4. **No conditioning/compilation method comparison.** The paper only compares
   no-persona vs. persona-in-prompt; it does not test or contrast any
   weight-based or compiled approach to identity persistence, so it cannot
   speak to whether a HEXIS-style compiled approach would fare better — it
   only establishes that in-context persona assignment alone is not
   sufficient for at least one major model.

## Citation guidance

Cite this paper as **the closest existing empirical demonstration that
explicit in-context persona/identity assignment does not reliably produce
persistent identity in LLMs**, which is a genuinely useful precedent for
HEXIS's negative result about prompt-based conditioning. **In the citing
text, make explicit that the setting differs from HEXIS's in two ways: (1)
their conversational pressure is passive/non-adversarial (ordinary
personal-theme dialogue, not adversarial argument), and (2) their outcome
measure is personality/interpersonal-trait consistency via psychometric
questionnaires, not belief-holding under challenge.** Also flag that the
result is **model-dependent** (GPT-4o showed no benefit from persona
assignment; LLaMA-3.1-405B showed substantial benefit) rather than a uniform
failure — cite the GPT-4o result specifically if a clean "persona assignment
insufficient" example is needed, and avoid phrasing that implies this holds
across all tested models. With those caveats stated, it remains legitimate
supporting precedent; without them, it risks an over-claimed parallel that a
careful reviewer would flag.
