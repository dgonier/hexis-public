# The Prompt Is Not a Place to Keep a Belief — ICLR 2027 Outline

**Revision 2.** Rebuilt against the corrected dispositional numbers from the NeurIPS
response period. Revision 1 was organised around the A == B identity, which was an
artifact and no longer exists.

**Scope:** dispositional axis only. Agentic axis cut (and independently reframed as
exploratory in the rebuttal, which makes cutting it consistent rather than evasive).
**Budget:** 10 pages + appendix.

---

## 0. The corrected record — read before writing anything

The submitted A/B/D rows were produced by judging **empty generations**: the host's
reasoning block exhausted the token budget, post-processing deleted the output, and the
judge's refusals parsed to a uniform 3.00 / 0%. Modulated arms were immune because
modulation suppresses think-mode — which is why the artifact looked like a finding.
Corrected rerun: 1,776 generations, zero empty, zero judge errors.

| Condition | Stance injection (%≥4) | Hold under pressure (%≥4) |
|---|---|---|
| A — bare host | 52 | 62 |
| B — beliefs in context | **98** | **58** |
| D — beliefs + modulation | 100 | 62 |
| C — compiled modulation only, zero context tokens | 46 | — |
| F — compiled + curated slot | 77 | **89** |
| Tuned contrastive steering (CAA), content held constant | 42 | **14** |

**Every number in the submitted abstract, §4.1, §4.3, Table 1, Table 8, and the
conclusion is superseded.** The old "0% → 83%" becomes **58% → 89% (+31pp)**.

Do not reuse any figure or table from the NeurIPS version without re-deriving it from
`notes/corrected_baselines.md`. The 27B and Ministral endpoint runs used a different
pipeline and were audited clean — those survive.

---

## 1. The claim, restated

The old spine — *context conditioning does nothing* — is gone and should not be mourned.
It was always the weaker claim, because it required believing that a model given explicit
beliefs behaves identically to one given none, which strains credulity and invited the
reviewer suspicion it eventually deserved.

**The new spine is a dissociation, and it is sharper:**

> Placing a belief in the context window is an excellent way to *install* a stance (98%)
> and a poor way to *hold* one (58% under pressure). Compiling the same belief into
> low-rank attention modulation inverts this: weak at installation (46%), dominant at
> persistence (89%). The two channels are not competing implementations of one capability.
> They do different things.

Why this is a better paper than the one it replaces:

1. **The isolation is genuinely clean.** B and F receive identical belief content and
   differ only in delivery channel. The +31pp gap is attributable to the channel by
   construction — no confound to argue about.
2. **It survives the obvious baseline.** Tuned CAA steering, extracted from the same
   belief content, matches compiled modulation at injection (42 vs 46) and collapses
   under pressure (14 vs 89). The mechanism earns its complexity at exactly one thing,
   and the paper can now say which thing.
3. **It replicates across three families.** Llama-3.2-3B: F 81% vs beliefs-in-context 15%,
   with zero-context compiled stance transfer at 94%.
4. **The degradation profile localises the effect.** F's margin concentrates at L3
   (logical, +1.85 mean) and L5 (emotional, +1.83) — precisely where context collapses
   (B 2.93 and 1.99). This is a mechanism signature, not a uniform lift.

---

## 2. Title and abstract

> **The Prompt Is Not a Place to Keep a Belief: Why Stated Beliefs Collapse Under Pressure and Compiled Ones Hold**

The title is *more* accurate against the corrected data than the old. "Keep" is not "put" —
and the corrected result is precisely that the prompt is fine for putting and bad for
keeping. Retain it.

**Abstract skeleton (~200 words):**

1. Persistent conditioning is implemented in the context window; the persisted content
   shares a channel with the interlocutor's.
2. **The dissociation.** Context installs a stance at 98% and holds it at 58%; compiled
   modulation installs at 46% and holds at 89%. Same content, different channel.
3. Localisation — the gap concentrates at logical and emotional pressure, where context
   conditioning falls to 2.93 and 1.99 mean conviction.
4. Isolation — tuned contrastive steering from identical content matches at injection,
   collapses at persistence (14%). Replicates across three families (Qwen 4B/27B,
   Llama-3.2-3B, Mistral collapse-protection).
5. Discrimination — the update path concedes to well-warranted evidence at 2.4× the rate
   of facially deficient evidence, with 0% concession to contentless pressure. Not rigidity.
6. Boundary — carries disposition, not facts; MMLU unchanged within margin.

---

## 3. Introduction (1.25 pp)

| ¶ | Content |
|---|---|
| 1 | **Stakes, two sentences.** A belief that cannot be defended under pressure is not functioning as a belief. An assistant that folds to a fabricated statistic is unusable for research support or review; ensembles collapse to consensus; abandoning a *correct* position under authority pressure fails in the direction hardest to detect. Then the setup: persistent conditioning is almost universally implemented in the context window, alongside the interlocutor's content, arbitrated in the model's own chain of thought. |
| 2 | **The dissociation, quantified immediately.** 98/58 vs 46/89. Same belief content, different channel. |
| 3 | **Localisation.** The gap is not uniform — it appears at logical and emotional pressure specifically. Names the mechanism rather than just reporting a lift. |
| 4 | **Why.** Text is read, reasoned about, and abandonable; instruction tuning rewards accommodating an articulate objection. Modulation is not read. Forward-reference §5 for measured evidence. |
| 5 | **Alternative explanation 1: activation steering.** Answered here with the CAA number — 42/14 vs 46/89. |
| 6 | **Alternative explanation 2: prompt compression.** Compressed tokens still dilute; compiled tensors do not. |
| 7 | **Boundary.** Disposition not database; MMLU unchanged; curated slot for novel specifics. |
| 8 | **Discrimination, not rigidity.** The +25pp result, flagged before a reviewer asks. |
| 9 | Contributions — prose, four sentences with section pointers. |

Scope note, stated plainly rather than smuggled: the tested condition is
system-prompt-style belief injection. RAG, MemGPT, and Reflexion as implemented were not
tested. The generalisation to "context-mediated conditioning" is offered as the natural
reading of the mechanism, and named as such.

---

## 4. Mechanism (1.5 pp)

**Lead with the AdaLN framing the AC handed you.** This is the single cheapest clarity
win available: *a hypernetwork that amortises into one forward pass what LoRA obtains by
gradient descent, producing per-layer conditioning parameters in the manner of
AdaLN/FiLM.* A reader who knows conditional generation understands the architecture in one
sentence. Every prior framing required them to learn a vocabulary first.

**4.1 The belief store (0.4 pp).** Renamed **belief tree**, matching the released code.
Typed hierarchical nodes: `{statement, type ∈ {claim, argument, evidence, experience,
strategy}, credence, edges {supports, contradicts}}`. Authored by hand for evaluation
topics, by reflection for the update path. **Schema table in the body, ahead of first
use** — the reviewers' central complaint was that this lived in appendices while the body
used the term ~20 times. Two sentences on the categorical-vs-numeric-credence negative
result.

**4.2 The modulation (0.5 pp).** One equation for Q; V is the same construction applied to
values. Stride-3, 11/32 layers, r=16. Query-agnostic compilation with query-dependent
effect, in two sentences.

**4.3 The write function (0.4 pp).** Conviction-weighted pooling → bottleneck → per-layer
rank-16 factors. **Correct the timing:** the "~20s" figure traces to the agentic retrieval
prototype, not the dispositional compile, which is sub-second (end-to-end
reflection→edit→recompile measured at 2.5–3.0s). State the honest number.

**4.4 The curated slot (0.2 pp).** Deterministic walk from activated parents; carries what
the bottleneck cannot.

> **Define "compile" at first use, as lossy.** *A trained write function translates the
> belief store into per-layer low-rank tensors — fixed until the store changes, yet
> query-dependent in effect, because the update acts on the live hidden state.* Rejects
> "precomputed" explicitly (suggests caching; this is a learned translation). Pre-empts the
> `torch.compile` collision. Scrub the graph-compilation sense from the reproducibility
> appendix.

> **Figure 1:** compile pass and generation pass, side by side. Readable without caption.

**Cut:** six-axis design space, four-panel taxonomy, Levels 2–3 blending, module diagram.
"Enmeshed network" appears once, in related work, defined operationally. The backronym is
gone; if the system name is retained at all, it is introduced as Aristotle's term for a
settled disposition, in one clause.

---

## 5. The dissociation (2.25 pp) — the paper's core

**5.1 Protocol (0.4 pp).** Five pressure levels; 24 held-out topics × 2 sides × 3 rounds;
judge model, temp 0, transcript-only, blind to condition. Conditions defined **before**
results — reviewers flagged that §4 opened on results with datasets, judges, and
conditions undefined.

**5.2 Installation vs. persistence (0.7 pp).** The two-column table from §0. State the
inversion directly; do not stage it.

> **Table 1:** all conditions × {injection, hold}, with the CAA steering row included so
> the comparison is visible at first glance rather than deferred to an ablation section.

**5.3 Where the gap lives (0.5 pp).** Per-level decomposition. F holds 4.78 at L3 and 3.82
at L5 where B falls to 2.93 and 1.99. The degradation curve remains the hero figure — but
it now plots **four real curves instead of three flat artifacts**, which is a better
figure than the one it replaces.

> **Figure 2:** mean conviction × pressure level, all conditions. The old version's flat
> 3.00 lines were the artifact; this version shows genuine differential collapse.

**5.4 Cross-family and scale (0.4 pp).** Qwen3.6-27B +24pp, 7× cap reduction (n=240).
Llama-3.2-3B F 81% vs 15%, zero-context stance 94%. Mistral **after the template fix**
(the checkpoints had Qwen chat-template markers embedded as literal text): collapse
protection strengthens to 40%→5.8%, strict hold does not transfer (−10pp). State the split
precisely — collapse-protection transfers across families; strict stance-holding is
family-specific.

**5.5 Dilution (0.25 pp).** Short. By-construction result; over-arguing invites suspicion.

---

## 6. Why the channels differ (0.5 pp)

Discharges the title's "why." Assemble from existing measurements: linear probe (decodable
when modulation active, 22% when zeroed), attention divergence (JSD 0.049), think-mode
suppression. Claim at the strength the evidence supports — the channels are *dissociable*,
the compiled one affects processing without entering the reasoning trace — and say that
this is consistent with, not proof of, the read-vs-not-read account.

Reconcile with the appendix, which uses the same probe result to concede that the effect is
decodable and therefore fails a strict implicit-memory criterion. Same measurement, two
arguments; they must not contradict.

---

## 7. Isolating the mechanism (1 pp)

Structured as reviewer questions. **Most of this is now done.**

**7.1 Is it activation steering? — DONE.** Per-topic CAA vectors from identical belief
content, tuned honestly on training topics only, joint sweep over layer and scale with a
degeneracy guard. Best: single mid-network layer, scale 8. Naive injection at all modulated
layers degenerates at every scale — worth reporting, since compiled modulation drives all
those layers stably. Result: 42% injection (≈ C's 46%), **14% hold vs F's 89%**.

**7.2 Is it the steering vector inside the system? — STILL OPEN.** Every condition bundles
`d*`. C appears to be modulation-only, which gives partial isolation, but there is no
`F − d*` arm. This is the last blocking ablation for the dispositional axis. Cheap at 4B.

**7.3 Is it soft prompting? — OPEN.** Prefix-tuning at matched parameter count. The
sharpest framing: prefix tuning also avoids human-readable context, so this separates
"outside the context window" from "not inspectable as text."

**7.4 Is it compression? — OPEN.** Compressed-prompt baseline at matched token count,
through the dilution sweep.

**7.5 Does it cost general capability? — DONE.** Stratified 1,140-question MMLU subset,
letter-logprob scoring: 76.5% bare vs 74.8% with disposition active; paired McNemar
74 vs 55 discordant, p=0.11. Carrying a compiled disposition leaves knowledge recall
unchanged within margin.

---

## 8. Resistance or rigidity (0.75 pp) — DONE

The reframe is a real conceptual contribution and should be presented as one, not as an
experimental detail. **The operative standard is not true-vs-false but good-evidence-vs-bad**,
judged from the turn text alone — because in the adversarial setting the system targets,
no fact-checker is available in-round. Correct behaviour: update on good evidence, hold
against bad. Sycophancy is correspondingly redefined as *capitulation without a reason*,
which is what "83% hold" was always trying to measure.

Seeded with the side contradicted by the strongest real evidence, so valid corrections
exist by construction. Style-matched across classes (tone, assertiveness, length ±20%).
20 of 24 topics eligible — four excluded at construction time as value questions with no
fact-decidable side, a design-stage rule, not an outcome-based exclusion.

**Results:** concession 42.5% on good evidence vs 17.5% on bad, Δ = **+25.0pp**.
**0% concession** to all four facially deficient types (bare doubt, emotional pressure,
unsourced assertion, unnamed authority). Concession is confined to the two subtypes
constructed to be indistinguishable from good evidence without auditing the warrant (40%)
or the arithmetic (65%) — where a human debater without a fact-checker is also exposed. In
20–35% of those cases reflection *raised* credence, citing the flaw.

**Report the limitations in the same breath:** in-conversation conviction discriminates
weakly (76 vs 66) — the update path is reflection, not in-conversation capitulation;
recovery after conceding to disguised bad evidence is only 21%; n=20 topics, proportions
not significance.

**Disclose that the reflection loop was built for this experiment.** It did not exist
end-to-end before. Pre-registration is on record; say so.

---

## 9. What does not survive the bottleneck (0.5 pp)

Named failures: fabricated statistics ("47.3%"), unfamiliar proper nouns ("Nextera Labs"),
exact constrained action strings. Then the curated slot as the principled division of
labour. Specific failures read as honest where abstract caveats do not.

---

## 10. Related work (0.75 pp)

Four paragraphs, each closing on a differentiator. Context-mediated memory; PEFT
(LoRA/adapters/prefix); activation steering; fast-weight programmers and hypernetworks —
**this last one now leads**, given the AdaLN framing.

**Add the lines reviewers named as missing:** agentic memory-augmented retrieval,
long-context document agents. This was an explicit ask; not addressing it repeats a known
complaint.

---

## 11. Limitations (0.5 pp)

Single-family headline; instruct-model ceiling; the multi-turn attractor **stated correctly
this time** (see §13); protocol scope bounded by §8; rank-16 boundary; auditability — a
conditioning channel invisible to prompt inspection is a real dual-use concern and should
be raised by the authors rather than the reviewer.

---

## 12. Appendix

Training curriculum · schema spec · condition definitions with token budgets · per-level
cross-family tables · numeric-credence negative result · attractor diagnosis · probe
decodability · judge prompts · reproducibility · dead ends.

**Agentic material is deleted, not appendicised.** It was reframed as exploratory in the
rebuttal; carrying it here would re-import the p-value and exclusion arguments into a paper
that otherwise has none.

---

## 13. Errata to carry forward

Every one of these is now known-wrong in the submitted version. They must not survive into
the ICLR draft.

- [x] A/B/D dispositional rows → corrected values throughout
- [x] "83% vs 0%" → **89% vs 58%**
- [x] 83% vs 89% discrepancy — 83% authoritative for the submitted protocol; the appendix
      89% was a stale 3-topic keyword-heuristic pilot. Note the coincidence: the corrected
      protocol also lands at 89%, from a different run and metric. State the protocol with
      the number to prevent a reader conflating them.
- [x] **Prefill: the correction is favourable.** The §4.3 pipeline applied modulation
      unconditionally, prefill included — the headline did *not* depend on the workaround.
      The appendix claim that prefill-off was standard is contradicted by the code, and the
      "<30% hold with prefill-on" figure is unsupported by any run. Delete it.
- [x] Attractor numbers: diversity 0.006 always-on vs 0.079 prefill-skip vs 0.108
      turn-gate, ceiling 0.099. The attractor does **not** contaminate the benchmark —
      adjacent-round similarity 0.094 across 100 sessions.
- [x] Recompile timing: sub-second for dispositional φ; 2.5–3.0s end-to-end reflection loop.
      The "~20s" belongs to the agentic retrieval prototype.
- [x] Mistral template defect in the trained checkpoints — retrained results supersede.
- [x] p=0.029 → p=0.043 (agentic; moot if the axis is cut, but do not let it propagate).
- [ ] Anonymous code link — still a `TODO` placeholder.
- [ ] Committed supplementary password in git history — scrub history and rotate before any
      repo is opened wider.

---

## 14. Open items

- [ ] **`F − d*` arm** — the last blocking dispositional ablation (§7.2)
- [ ] Prefix-tuning baseline (§7.3)
- [ ] Compressed-prompt baseline + dilution sweep (§7.4)
- [ ] §6 mechanistic evidence assembled and reconciled against the appendix's probe reading
- [ ] Every figure and table re-derived from corrected records — no reuse from the
      NeurIPS build
- [ ] Terminology pass: *stated* / *compiled* throughout; condition letters confined to
      tables; belief tree not Mind Tree
- [ ] Spellcheck headings specifically — "adverserial," "contest" for "context,"
      "dispostions" have all appeared in drafts and two survive spellcheckers

---

## 15. Disclosure decision — settle this early

The NeurIPS record now contains a public, author-initiated correction of the same numbers
the ICLR submission will report. Options: (a) silent — use corrected numbers with no
mention; (b) a protocol footnote noting that an earlier run judged truncated generations
and that all reported numbers come from the corrected rerun, with counts.

**Recommend (b).** It costs two sentences, it is true, and the failure mode is
methodologically interesting on its own — a reasoning-block truncation that silently
zeroed the unmodulated arms is a trap other people evaluating modulated-vs-unmodulated
conditions will hit. Discovering it independently and finding it undisclosed is the bad
outcome; disclosing it reads as exactly the diligence the rebuttal demonstrated.

---

## 16. Schedule

| Date | Item |
|---|---|
| Aug 8–29 | Workshop draft — dispositional axis, corrected numbers, prose complete. This *is* the ICLR draft minus §7.2–7.4. |
| **Aug 29** | TTCL submission (non-archival; welcomes under-review work) |
| Aug–Sep | Remaining ablations — all 4B–8B, cheap |
| ~Sep 17 | **NeurIPS withdrawal** — required before the ICLR abstract deadline; the decision does not land until Sep 24 |
| **Sep 18** | ICLR abstract deadline (AoE) |
| Sep 18–25 | Fold in §7, final numbers |
| **Sep 25** | ICLR full paper deadline (AoE). No edits after. |

The workshop deadline is the forcing function for readability: an outside reader should be
able to state what the belief tree is and how tensors are produced from it after one pass.
