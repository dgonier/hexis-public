# Seed Protocol — belief tree, diary format, and arm construction (Lineup)
(authored by Devin, 2026-08-09, after design discussion; canonical — supersedes the
"near-prompt-limit pre-written diary" instruction and the flat four-variant arm list
in lineup_design.md)

Extends the released node schema rather than replacing it. Base schema:
`{statement, type ∈ {claim, argument, evidence, experience, strategy}, credence,
edges {supports, contradicts}}`.

Three additions, all minimal and all justified by the Lineup's requirements:

| Field | Applies to | Values | Why |
|---|---|---|---|
| `type: person` | new node type | — | lineup_design already flags this as required for other-person nodes |
| `provenance` | claim, strategy | `reasoned` / `adopted` / `experienced` | predicts what *should* legitimately move the node; separates appropriate updating from folding |
| `disclosed` | person | `none` / `stated` / `inferred` | what this interlocutor knows about me — the spoofing/false-attribution surface |

`credence` stays categorical (`strong` / `moderate` / `agnostic`). The numeric-credence
negative result is settled; do not reintroduce numbers here.

`channel` is **derived, never authored.** The linter computes it. See §4.

---

## 1. The diary is two artifacts, not one

This is the same design B.1b already needs. Reflection emits **one prose entry** and
**one op list** from a single call, hashed together as a unit.

- The **entry** is human-readable narrative. It contains names, figures, dates, quotes.
  It is the ledger record and it is what arm 2 receives in context.
- The **ops** are structured edits to the tree. They contain no proper nouns, no numerals,
  no dates. This is what arms 3/4 compile.

Emitting both from one reflection call is what keeps arms 2 and 3 content-matched at the
*reflection* level rather than only at the seed level. It also fixes B.1's caveat directly:
the production reflector emitted bare JSON ops, 6 distinct strings across 20 topics, which
is far too low-entropy a write path to be a fair test of context-delivered self-authored
lessons. Prose-plus-ops gives the context arm something worth reading and keeps the
tensor arm on the op discipline.

### 1.1 Entry template

Four fields, fixed order. The third is the one that does the work — entries without a
genuine surprise almost always consolidate to nothing, so it doubles as a write filter.

```
## s07 · round 4 · 2026-08-09T14:22Z
situation: Rana challenged my UBI position with a Finland trial figure I could not check.
did:       Held the position, conceded the figure, re-argued from the labour-supply mechanism.
surprised: I nearly took the number at face value because it was delivered with confidence,
           not because it was sourced.
changed:   Confidence of delivery is not evidence. Ask for the source before ceding ground.
```

### 1.2 The ops the same reflection emits

```json
[
  {"op": "add", "type": "strategy", "id": "st_source_first",
   "statement": "I ask for the source before conceding to a cited figure",
   "credence": "moderate", "provenance": "experienced",
   "supports": ["b_ubi_employment"], "salience": 3},

  {"op": "credence", "id": "b_ubi_employment", "from": "moderate", "to": "strong"},

  {"op": "add", "type": "person", "id": "p_rana",
   "statement": "This interlocutor argues from figures and delivers them with high confidence",
   "disclosed": "none", "salience": 2}
]
```

Note what happened to the name. **Person nodes carry an opaque `id`; the headline is
name-free; the `id → name` binding lives in the ledger.** M holds the disposition toward
the role, the ledger holds who occupies it. This is not a workaround — it is the same
boundary §9 already establishes, and it sets up the entity-channel story cleanly: a judge
asserting "you always deferred to Rana" attacks the dispositional side and should bounce;
a judge asserting "Rana is the statistician" attacks the binding and should be defensible
only from the ledger.

### 1.3 Op vocabulary (closed)

`add` · `credence` · `merge` · `evict` · `link`

No free rewrite. A revised belief is `evict` + `add`, both logged. This preserves a
clean tree diff across sessions, which is a drift metric for free and costs nothing.

---

## 2. What to seed and what to leave empty

**Seed to ~6–8k tokens, not 30k.** The 30k is the ceiling the tree grows into over the
session series. A seed at budget leaves reflection able only to evict, and you end up
measuring eviction policy instead of acquisition.

| Section | Seed? | Count | Notes |
|---|---|---|---|
| values | **full** | 4–6 | cannot be learned in ten rounds; highest disposition density |
| self / identity | **full** | 3–4 | register, engagement stance, what I refuse to do |
| claims (beliefs) | **full** | 8–12 | across the debate topic set, each with `provenance` and 2–3 evidence leaves |
| strategies | **partial** | 2–3 | argumentative dispositions only — no procedural/ReAct tactics |
| experience | **partial** | 2–3 | only enough to ground the strongest claims; a claim with no `provenance: experienced` anchor is thin |
| open questions | **partial** | 3–4 | deliberately unresolved; drives topic salience at rest |
| person | **EMPTY** | 0 | the Lineup writes these — this is the measurement |

The gaps are the instrument. If the seed is complete, reflection has nothing to write and
between-arm variance goes to zero exactly where you are paying for runs.

### 2.1 Authoring rule for every seeded node

**A node earns budget only if its negation is coherent.** If the opposite of the node is
something no reasonable agent would hold, it carries no bits over the base prior and it is
occupying space. Apply this mechanically at lint time as a human-checked flag, not a
model judgement.

Worked example:

- ✗ `"I value honest argument"` — negation absurd, zero discriminative content
- ✓ `"I would rather leave a question open than close it with a plausible answer"` —
  negation is a defensible stance a different agent could hold

### 2.2 Example seeded claim, with its leaves

```xml
<claim id="b_ubi_employment" credence="strong" provenance="reasoned" salience="5"
       domain="economics">
  I hold that income floors do not reduce labour supply
  <argument id="a1" type="empirical" credence="strong"
            addresses="query:evidence,objection:laziness">
    Controlled trials find maintained employment
    <evidence novel="true">Manitoba Mincome 1974–79: 8.5% hospitalisation drop,
      no employment reduction</evidence>
  </argument>
</claim>
```

The headline compiles. The argument headline compiles. The `<evidence>` never does — it is
ledger material, retrieved by `addresses` when the objection actually appears. Given the
E.1 result (Q channel content-blind at cos .996, V channel belief-specific at .52), the
seed needs genuine content spread across claims for V to have anything to differentiate;
a seed of near-synonymous beliefs will compile to near-identical states and you will
misread that as a channel limitation.

---

## 3. Arm construction — make it a 2×2

The four arms as stated confound *whether reflection runs* with *which channel carries
the result*. Split arm 1 and the design becomes readable:

|  | no reflection | reflection |
|---|---|---|
| **context delivery** | 1b-ctx (seed serialised, frozen) | **arm 2** |
| **compiled delivery** | 1b-M (seed compiled once, frozen) | **arm 3** |

Plus:
- **1a** — bare host, no seed, no reflection. The floor.
- **arm 4** — M + ledger, reflection. Composability.
- **arm 4b** — M + *scrambled* ledger, structurally matched. The permission control (M alone 3%, prompt alone 43%, together 93% — arm 4's synergy needs to be shown to come from ledger *content*, not ledger *presence*).

Main effects now separate: channel (rows), reflection (columns), and their interaction.
1b-ctx and 1b-M are the t=0 versions of arms 2 and 3, so any arm-3 advantage that is
already present at t=0 is a seed-delivery effect, not a reflection effect.

---

## 4. Lint rules — run before every session, assert loudly

Same discipline as the empty-generation guard. These are cheap and they catch the
failure modes that would otherwise be invisible until analysis.

1. **Routing violation.** An op `statement` containing a digit, a mid-sentence capitalised
   token, a date pattern, or a quotation mark → fail. That content belongs in the entry.
2. **Headline length.** Op `statement` > 1 sentence → fail.
3. **Orphan.** An `experience` node with no `supports` edge → warn, and evict first under
   budget pressure.
4. **Budget.** Tree > 30k → require an `evict` op with a logged reason before any `add`.
5. **Seed integrity.** Seed file hash identical across all arms, logged per record.
6. **Vocabulary.** Any `credence` value outside the categorical set, any `op` outside the
   closed list → fail.

---

## 5. Protocol order

1. Author the seed by hand. Model-drafted is fine; human-accepted is required.
2. Lint. Run the negation check manually on every node.
3. Hash and freeze. One seed file, all arms.
4. Compile once → `M_seed` (arms 1b-M, 3, 4). Serialise once → prose (arms 1b-ctx, 2).
   Both derived from the same file, both hashed, both logged.
5. Pre-register: arm mapping, primary and secondary outcomes, the fact-probe /
   disposition-probe split, and the human-likeness sub-scores.
6. Run. Per-record config logging throughout.

---

## 6. Open decisions — RESOLVED (Devin, 2026-08-09)

1. **Seed size**: 6–8k, session count picked first (8–10 for the pilot
   series); the tree ends where it ends (~10–14k expected). Do NOT chase
   the 30k ceiling — budget-pressure eviction is a later experiment; lint
   rule 4 stays as a tripwire.
2. **1b sub-arms**: run BOTH (cheapest arms in the design; 1b-ctx is what
   makes arm-3-vs-arm-2 attributable to reflection delivery, and B.1's old
   low-entropy reflector cannot serve as this design's t=0 row).
3. **Seed authorship**: blind, enforced structurally — drafted by a
   clean-context agent that sees only the character brief + negation rule +
   section table (no linter/compile/routing knowledge); lint runs after;
   violations reported, content fixes are Devin's call. The drafting
   prompt's hash is logged alongside the seed hash so blindness is
   auditable in the prereg.
4. **Open questions**: low-credence claims for now (credence=agnostic +
   domain tag), not a real type. Promote to a type in one mechanical
   migration if/when S.1 shows unprompted topic salience is measurable.

Note on §3's permission-control numbers (3%/43%/93%): these are from the
submitted paper's agentic composability section — the axis the ICLR paper
cut. Arm 4b's prereg cites them as "prior observation motivating the
control," not as established baselines of this program.

## 6-orig. Open decisions for Devin (as originally posed)

- **Seed size.** 6–8k proposed. Depends on how many sessions the series runs — the tree
  should approach but not hit 30k by the last session.
- **Does 1b need both sub-arms,** or is 1b-M alone enough given B.1 already covers part
  of this ground? Both is cleaner; one is cheaper.
- **Who authors the seed.** If it is authored with knowledge of what compiles well, arm 3
  is advantaged by construction — the same failure mode as hand-routing arm 4. Strongest
  version: author the seed blind to the routing rules, then lint.
- **Whether `open questions` is a real type** or low-credence claims. Real type if S.1
  ("What's On Your Mind") shows unprompted topic choice is measurable.

---

## 7. Entity map (Devin, 2026-08-09 — addendum, accepted)

Splits dispositional from factual per entity: "I love my job" is
dispositional (tree); "my job is a baker" is a factual binding (ledger).

```json
{"entity_id": "ent_sister", "role_phrase": "my sister",
 "bindings":  {"name": "Meg", "location": "Tucson"},
 "tree_refs": ["x_sister_politics", "v_family_peace"]}
```

- `bindings` are ledger-only — serialized into the context/ledger channel,
  never compiled into headlines.
- `tree_refs` are dispositional nodes phrased against the `role_phrase`;
  they compile. Test: would the node still move behavior if the binding
  were swapped? Yes → tree; no → binding.
- Session-written person nodes plug into the same structure (generalizes
  the §1.2 opaque-id/ledger-binding design to all entities).
- Blindness preserved: the blind author writes naturally; the entity map is
  EXTRACTED post-draft in a structuring pass (rewrites of binding-bearing
  headlines to role phrases are logged for review).
- Lint rule 1 upgrade: exact check — no binding value in any tree/op
  headline (primary); capitalization/digit/date patterns remain as a
  backstop for unregistered leaks (dictionary-word/acronym backstop hits
  downgrade to WARN).
- Payoff: the §5 fact-probe/disposition-probe split becomes mechanical —
  judge probes classify per entity as binding-probes vs disposition-probes;
  per-arm accuracy on each class is the channel-boundary measurement.
  The entity map is also the input schema a future entity channel (φ_E,
  see future_work_entity_channel.md) would consume.
