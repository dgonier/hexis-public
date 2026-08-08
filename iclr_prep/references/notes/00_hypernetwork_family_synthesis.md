# Hypernetwork Family Synthesis — Cross-Paper Index

Covers: GenerativeAdapter (Chen et al. 2024/25), SHINE (Liu et al. 2026), Doc-to-LoRA (Charakorn
et al. 2026), Text-to-LoRA (Charakorn et al. 2025), and the override-gap paper (Cheng et al.
2026) as an analysis/intervention study on top of Doc-to-LoRA. Full per-paper detail in the
sibling notes files.

## What the family optimizes

All five papers pursue a single throughline: **how cheaply and quickly can a hypernetwork map
some conditioning signal into weight-space modulation of a frozen host LM, such that a single
subsequent readout (F1, accuracy, ROUGE-L, or override success) approaches the quality of
keeping that signal in-context** — while paying a fraction of in-context prompting's compute,
memory, or latency cost. GenerativeAdapter and Doc-to-LoRA condition on documents/dialogue
history; SHINE conditions on general "meaningful" text with a full-layer-coverage architecture;
Text-to-LoRA conditions on short task descriptions to elicit latent skills rather than inject
knowledge; the override-gap paper doesn't propose a new hypernetwork at all, but diagnoses and
patches *why* Doc-to-LoRA's single-shot override succeeds or fails as a function of how strongly
the base model already believes the contradicted fact. Every paper's efficiency story — F1-per-
FLOP, F1-per-byte, latency-vs-oracle — is the actual contribution being sold; accuracy gaps
against full in-context prompting are consistently reframed as acceptable costs of that
efficiency, never as capability or robustness failures in their own right (GenerativeAdapter
Table 1 is the cleanest example: 40.2 vs. 66.0 F1 explicitly framed as a "4x" compute/storage
win, not a shortfall).

## What the family never measures

**No paper in the compiled-modulation lineage — including the one paper that studies
knowledge-conflict override (Cheng et al. 2026) — measures whether an installed context survives
contradiction or adversarial follow-up after that installation.** Every evaluation across all
five papers, without exception, is a single time-point readout against a static gold answer,
computed once, immediately after (or, in override-gap's case, immediately as part of)
installation, with the underlying context/document/task-description held fixed throughout the
measurement. There is no dialogue agent contesting an installed stance, no repeated query under
escalating pressure, no multi-turn adversarial protocol anywhere in the corpus.

Two results come close enough to warrant explicit, careful disclosure rather than omission:

- **SHINE's Figure 6, "F1 Score vs. Conversation Turn"** (turns 1–15, MS MARCO MQA) shows real
  degradation across turns — but the independent variable is *accumulating conversation length*,
  and SHINE's own causal account attributes the decline to long-context inference difficulty, not
  belief erosion or contradiction. No adversarial or contesting turn is ever introduced; the
  underlying facts never change.
- **Doc-to-LoRA's Appendix C.4, "Knowledge Interference"** shows the adapter over-applies
  internalized content to unrelated queries (F1 drops below the base model when the query and
  the internalized document are deliberately mismatched) — a real robustness-adjacent failure,
  but in the opposite direction from ours: theirs is "the adapter fires when it shouldn't," ours
  is "the adapter/context fails to hold when it's directly and legitimately contested."

The override-gap paper is the family's most sophisticated near-miss: it builds a full causal
theory (a logit-magnitude contest, `∆lora > ∆prior`) and a validated, released benchmark
(KID-Bench) specifically for knowledge-conflict resolution, and even uses the word "persistent"
in exactly our topic area — but its entire framework operates at a single time-point per
question. It has no mechanism for expressing, let alone measuring, a case where installation and
persistence move in opposite directions, because it never asks the same question twice. Its own
language (§8.6: parameter-level methods are "persistent and query-agnostic," contrasted with
prompts that must be "repeated for every query") states our exact research question as an
unexamined assumption rather than a tested finding.

## Structured/typed conditioning — closest overlap with the belief graph

None of the five papers condition on anything resembling a typed graph, schema, or symbolic
representation. All natural-language conditioning is raw text (documents, dialogue,
context strings); Text-to-LoRA's one-hot task-ID ablation (used only for pure LoRA
compression, not zero-shot generation) is the single most "structured" input in the corpus, and
it is a categorical index, not a graph. SHINE's own Appendix C.6 draws the sharpest internal
distinction on this axis, contrasting its full-context knowledge-injection conditioning against
Text-to-LoRA's short-description style/behavior-elicitation conditioning — useful supporting
evidence that conditioning-signal *type* determines what an adapter can do, but not itself
evidence that any family member used structured input.

## The strongest defensible sentence

**"No paper in the compiled-modulation lineage — including the one paper that studies
knowledge-conflict override (Cheng et al. 2026) — measures whether an installed context survives
contradiction or adversarial follow-up after that installation; every evaluation in the family,
without exception, is a single time-point readout against a static gold answer."**

## Threat summary (full detail in per-paper notes)

| Paper | Threat level | Nearest overlap | Why it doesn't threaten the dissociation |
|---|---|---|---|
| GenerativeAdapter | None | — | Purely single-shot F1/accuracy/PPL; frames all gaps as compute cost |
| SHINE | Low-Moderate | Fig. 6 multi-turn F1 decay | Decay from context-length accumulation, not contest; no adversarial turns |
| Doc-to-LoRA | Low | App. C.4 knowledge interference | Over-application to unrelated queries, opposite failure direction from ours |
| Text-to-LoRA | None | — | Task-skill elicitation benchmarks, purely single-shot, no temporal axis at all |
| Override Gap (Cheng et al. 2026) | **Low** | Whole paper's topic (knowledge conflict) | Single-time-point magnitude theory; "persistent" is asserted, never tested; no mechanism for install/persist dissociation |

## Recommended related-work paragraph structure
1. Establish the lineage (GenerativeAdapter → Text-to-LoRA/Doc-to-LoRA → SHINE) as the
   architectural ancestry HEXIS owns and extends (per-layer, multi-module, typed-graph
   conditioning where the family used raw text).
2. Cite GenerativeAdapter's Table 1 (40.2 vs. 66.0 F1) as the family's clearest example of
   treating installation gaps as compute trade-offs.
3. Cite SHINE's Fig. 6 explicitly, with the context-length-vs-contest distinction stated in our
   own words immediately after the citation, so a reviewer cannot mistake it for a persistence
   result we overlooked.
4. Cite the override-gap paper using the boxed differentiation language in
   `override_gap_2604.23750.md` — this is the single most important citation in the related-work
   section, because it is the paper most likely to prompt a reviewer's "hasn't this been done?"
   question, and the one we are best equipped to answer directly.
