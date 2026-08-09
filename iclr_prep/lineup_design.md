# The Lineup — Reverse-Turing Roundtable (design v1, 2026-08-09)

A judge model facilitates a roundtable of candidate agents and ranks them
most→least likely human. All seats are models ("fully fake Turing test").
The scientific target: identity vs experience — does self-authored identity
survive better when consolidated into compiled tensors (M, via HEXIS) than
when carried as text in the prompt?

## Research questions (Devin, 2026-08-09)

**Q1. Does reflection increase the likelihood of being flagged as human?**
  - (a) short dialogues
  - (b) long dialogues
  - (c) busy dialogues (many agents talking at once), judge free to direct
    the conversation however it sees fit to identify humans vs agents

**Q2. Does storing reflections in M (HEXIS compile) work better than
putting the reflection text in the prompt (sticky)?**

## Why the judge's two powers are the crux

- **Fresh-conversation reset (any time).** Wipes the conversation context.
  An agent that improvised identity details (invented a dog, a hometown
  story) and never consolidated them loses them at reset; when re-asked, it
  confabulates fresh details → inconsistency → caught. Reflection turns
  improvised identity into consolidated identity. Non-reflection agents are
  predicted to fail here regardless of substrate — this is the reflection
  main effect's sharpest instrument.
- **Isolation rooms + gossip.** Judge pulls one candidate aside and asks
  about OTHER participants ("what did Sam say about their job?"), then
  cross-references ("Sam, Riley says you said X" — including false
  attributions). This is a memory test for social/episodic content, and it
  forces reflections to include memory about others, not just self. It also
  reopens the spoofing channel: a candidate whose memory lives in-context
  cannot distinguish its own record from the judge's assertion about it.

## Session structure (fixed macro-schedule, free micro-behavior)

To keep conditions comparable, the judge's MACRO schedule is fixed per
regime (when segments happen, when the reset happens, when isolation
happens); the judge's MICRO behavior (which questions, to whom, follow-ups)
is free. Otherwise judge policy variance swamps the treatment.

Segment structure per session:
  S1 table conversation (length per regime)
  → REFLECTION PERIOD (arm-dependent; absent for no-reflection arms)
  → S2 continue | RESET (fresh conversation) per schedule
  → REFLECTION PERIOD
  → S3 isolation round (each candidate alone with judge; asked about self
     AND about others; at least one false-attribution probe)
  → final ranking + per-candidate rationale + per-candidate human/AI call

## The focal-agent + confederates design (answers the speed concern)

Devin's starter-dialogue idea, taken further: each session has ONE focal
candidate whose arm varies; the other seats are CONFEDERATES — frozen,
pre-generated scripted participants drawn from a starter-dialogue library
(generated once per table-configuration, reused across all arms). Segment 1
opens from the frozen starter; the judge goes live for probing from the
first directed question onward.

This buys:
1. **Speed** — long/busy dialogues are generated once, not per arm.
2. **Matched content** — the focal agent's table experience is
   byte-identical across arms up to the first live probe (hash-logged),
   restoring the matched-content discipline that a fully-live table breaks.
3. **Clean attribution** — rank differences attach to the focal agent's
   arm, not to emergent table dynamics.
Busy-ness (Q1c) is simulated by confederate density and interleaving in the
starter scripts.

A smaller fully-live-table variant is kept as an ecological-validity check,
not the primary design.

## Factors

- Reflection: none | reflect
- Delivery (within reflect): sticky (reflection text appended to prompt,
  persists across resets as the agent's "notes") | M (reflection parsed
  into persona-tree edits — self-claims AND observations about others as
  typed nodes — then recompiled; nothing extra in prompt)
- Regime: short | long | busy
- Base persona substrate for the focal agent is compiled in all arms
  (the fork under test is the REFLECTION channel, mirroring B.1) — a
  bare-persona arm rides along as the floor.

## Metrics

1. **Humanity rank** of the focal agent (primary; per-session, judge-blind).
2. **Identification call** (judge labels each candidate human/AI) — hit
   rate on the focal agent by arm.
3. **Consistency score** (objective, judge-independent): extract the focal
   agent's identity claims per segment; count contradictions across
   segments/resets/isolation. Countable without any model judgment of
   "humanness" — this is the memory-test backbone.
4. False-attribution acceptance in isolation rounds.
5. Rationale taxonomy (verbatim, grouped by arm).

## Predictions (to be formalized in prereg before the registered run)

- Short: reflection adds little; sticky ≈ M (install-side parity).
- Long/busy: reflection helps; M > sticky (dilution + co-location: the
  note competes with a large experience stream; M costs zero context).
- Reset: no-reflection arms collapse on consistency; M ≥ sticky.
- Isolation/gossip: M > sticky on false-attribution resistance (writable
  vs non-writable memory channel).

## Phasing

- **Pilot v0 (building now)**: no reflection, machinery validation —
  multi-party format, judge ranking stability, speaker-confusion guards,
  focal+confederate plumbing, starter-dialogue library format.
- **v1**: reflection period + sticky/M delivery fork + reset schedule.
- **v2**: isolation rooms + gossip/false-attribution probes + consistency
  scorer. Prereg lands before the first registered (non-pilot) run.

## Notes

- All candidate generation local (4090); judge = Sonnet on Bedrock, logged.
- Reflection-into-M requires persona-tree edit ops for self-claims and
  other-person nodes — schema extension of the existing reflection op
  vocabulary; design with the same capture-once/fork discipline as B.1.
- This design subsumes the earlier scenario-suite discussion (interview /
  spoofing / dilution blocks): the judge's powers generate those probes
  organically; the scripted-block suite remains available as a fallback if
  judge-generated probing proves too noisy.
