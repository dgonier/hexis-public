# Future work / discussion — a third channel for entities (2026-08-09)

Captured from design discussion (Devin): if entities could be effectively
stored — possibly as a third channel alongside what exists now — the
combination could be very powerful. Not in scope for the ICLR paper's
experiments; belongs in Discussion/Future Work and on the research roadmap.

## The channel architecture as it stands

| Channel | Substrate | Carries | Doesn't carry | Writable by interlocutor? |
|---|---|---|---|---|
| Compiled M (Q/V modulation) | attention, low-rank | disposition: stance, values, hold-behavior | novel proper nouns, exact strings, precise values (§9 bottleneck) | no |
| Curated slot | private prompt prefix | exact text: quotes, names, ledger facts | persistence under pressure (it's still text) | no (private channel) |
| Conversation context | shared window | experience: the current interaction | — | yes — that's the point |

The paper's evidence for the boundary: §9 (rank-16 drops "Nextera Labs",
"47.3%"), C-condition install at 46%, Fingerprints (dV is a coarse content
direction, cos ~0.5 — not token-precise storage), and the hypernetwork
family's own recall gap (GenerativeAdapter 40.2 vs 66.0 F1).

## The proposed third channel: entity memory in weights

Entity storage (My_Dog → {name, breed, age}; people, places, artifacts,
relations) as weight-level associations, via a mechanism actually suited to
token-precise facts:

- **ROME/MEMIT-family rank-one/rank-few MLP edits** — target MLP key-value
  memories, the known locus of factual association, instead of attention
  Q/V. "φ compiles dispositions; an entity editor installs facts." The
  natural first experiment: a φ_E hypernetwork trained to emit MEMIT-style
  edits from typed entity nodes of the same belief graph.
- Alternatives: recall-objective retraining of φ (predicted low ceiling at
  low rank — the family's results suggest this), or per-entity micro-LoRAs
  (interference and capacity questions at scale).

## Why the pairing is powerful

A persistent agent with all three: disposition that survives pressure and
context resets (M), an inspectable text ledger for exact reference (slot),
and entity knowledge that is *generatively available* — usable in fluent
recall without occupying context budget and without being writable by the
interlocutor. That last property matters: an entity channel in weights
inherits M's spoof-resistance (the Lineup's isolation/gossip test — a judge
asserting "your dog is named Rex" has nothing in-weights to bind to).
Combined with the reflection loop, entity edits become the sanctioned
pathway for experience → identity on the factual axis, with an explicit,
inspectable update gate — mirroring the credence-op gate on the
dispositional axis.

## Open research questions

1. Interference: how many entities before MEMIT-style edits degrade base
   capability or each other? (The E.2 capacity sweep is the dispositional
   analog.)
2. Typed-graph → edit compilation: can a hypernetwork learn to emit correct
   entity edits zero-shot (φ_E), or does each entity need an optimization
   step?
3. Channel routing: given a belief graph with mixed node types, what routes
   to M vs slot vs entity edits? The graph schema already types nodes —
   routing could be schema-driven.
4. Eval: entity-recall under pressure + spoofing (does weight-stored entity
   memory resist false attribution the way compiled stance does?).

## Paper placement

- Discussion/Future Work paragraph in the ICLR paper: the three-channel
  division of labor, with §9 reframed as the boundary that motivates it
  (consistent with the dispositional-memory positioning: the failure to
  store facts is a category boundary, not a defect).
- Optional appendix receipt if run: the persona-entity boundary probe
  (compile persona trees with entity nodes; probe recall bare/C/F; ~1h).
  Queued behind the Lineup pilot; §9's existing evidence suffices if time
  is short.
