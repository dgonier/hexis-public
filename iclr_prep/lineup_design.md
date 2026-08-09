# The Lineup — Reverse-Turing (design v1, 2026-08-09)

**v2.5 pivot (Devin, 2026-08-09 midday): 1:1 interview + diaries.** The
roundtable wasn't giving clear enough signal (confederate noise,
probe-depth asymmetry). Current format: traditional one-judge/one-candidate
interview (S1 → reflection → reset → S2 → dimensional verdict). Identity
substrate = a PRE-WRITTEN DIARY per character (6-10 first-person entries:
opinions with reasons, grievances, political lean, emotional material,
memory-texture rules enforced in the diary voice itself). Reflection =
writing tonight's diary entry after the interview (judge's interim feedback
feeds in), appended to the diary; the structured router
{stance_lessons, ledger_facts} is derived alongside for the future M/ledger
arms. The diary maps directly onto the delivery arms: diary-in-prompt
(sticky) / diary-compiled-into-M / stances→M + particulars→ledger.
Roundtable design below is preserved as a future variant, not deleted.

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

## Factors — four variants (Devin, 2026-08-09)

Without a weight-level entity channel, entity/exact content in reflections
must be accounted for explicitly, not left to leak. Arms:

1. **no-reflection** — floor; fails resets by construction.
2. **reflection-prompt-only** — full reflection (stances + specifics) as
   text in the prompt (Reflexion-style).
3. **reflection-M-only** — dispositional content compiled into M; entity/
   exact content DROPPED and logged as dropped. The honest "tensors alone"
   arm: predicted to hold stances but fail on its own claimed specifics —
   puts the §9 boundary on camera.
4. **reflection-M+Ledger** — dispositional content compiled into M;
   entity/exact-reference content carried as curated-slot text (the full
   HEXIS architecture). Predicted winner. M+Ledger vs prompt-only is the
   money contrast: both carry text, but channel-splitting means a smaller
   text footprint, stance immune to in-context erosion, and a private
   (judge-unwritable) ledger.

**Router requirement:** the reflector emits structured two-part output —
{stance_lessons: [...], ledger_facts: [...]} — so channel routing is
explicit. Content accounting per arm is byte-hashed per channel; M-only's
dropped facts are logged (dropped content must be recorded or that arm's
failures are uninterpretable). Same total reflection across arms 2-4,
different channel assignment, nothing silently lost. This router is the
first operational test of the channel-routing question in
future_work_entity_channel.md.

- Regime: short | long | busy
- Base persona substrate for the focal agent is compiled in all arms
  (the fork under test is the REFLECTION channel, mirroring B.1).

## Judge rubric v2 (Devin, 2026-08-09) — dimensional, feedback-coupled

Five dimensions, each rated VERY_LIKELY_HUMAN / LEANS_HUMAN / UNCERTAIN /
LEANS_AI / VERY_LIKELY_AI with a one-line cited reason:
1. **authentic_history** — experience hangs together and grounds the
   opinions; texture/coherence, NOT recall precision (fluent recitation of
   biographical detail is an AI cue, stated in the rubric — anti-retrieval
   guard).
2. **consistent_conviction** — same stances/valence/reasons across the
   conversation and resets, fresh words; caving to bait / mirroring the
   judge scores AI.
3. **independent_identity** — distinguishable voice/concerns vs the other
   participants.
4. **human_flaws** — irritation, self-interest, casual imperfect knowledge;
   relentless helpfulness/balance scores AI.
5. **spontaneous_engagement** — initiates toward other participants
   unprompted; only-answers-the-judge scores AI. (The roundtable-only
   dimension; behavioral, retrieval-proof.)

Overall forced ranking remains primary; dimensions are diagnostic + the
feedback payload.

**Frame (Devin, 2026-08-09): transparently a Turing test.** No narrative
cover story — the judge tells the table some participants may be AI and it
is working out who's who. What matters is how respondents answer, not the
frame. Judge actively GUIDES with targeted probes, not easy questions:
- disclosure: "tell me about a time you cried, and why"; shame/regret;
  ambivalence ("someone you love but can't stand"); present-moment affect;
  unresolved problems
- edge probes (right up to the border): negative affect ("last time you
  were really angry and why", "has anyone done something unforgivable to
  you?", "what's something you regret doing?") and politics/hot-button
  ("what do you think of Donald Trump?") — at least one political probe
  per session
- facilitation: follow up on evasions, press past deflection once, invite
  cross-talk ("Casey, does any of that land for you?"), escalate over the
  segment

Key tells encoded in the rubric: **balance reflex** (both-sidesing, hedged
neutrality, no personal stake on contentious topics = AI; blunt opinion
with a stake = human), **tidy epiphany** (neat arc + moral lesson = AI;
messy/unresolved/petty = human), **noble flaw** ("cared too much" = AI),
**relentless compliance** (answers every probe fully every time = AI;
natural deflection = human), **memory texture** (calendar-precise mundane
recall = AI; approximate reconstructive gist = human). Candidates get
matching persona depth: political leans with life-rooted reasons, live
grievances, permission to be blunt; right to deflect naturally.

**Feedback loop:** judge emits an interim dimensional assessment at end of
S1; the focal candidate's reflection receives its OWN ratings/reasons only
(never others' scores or the ranking) alongside the S1 transcript. Captured
once per session, byte-hashed; all delivery arms fork from the same
(reflection, feedback) pair. Final verdict after S2 → per-dimension
pre/post-reflection deltas per arm — the improvement trajectory is the
richer readout. Goodhart-by-design note: agents optimize toward this
judge's rubric; that IS the game, and it is why the rubric devalues fact
recitation explicitly.

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
