# Claude Code Brief — ICLR Experiment Program

Structured like `rebuttal_plan.md`, which worked: recon before code, design locked in
writing, guardrails explicit, pre-registration committed before launch.

**Repo:** the real experiments repo, not the trimmed export. The last recon pass found the
trimmed copy diverged from the working tree and produced a false alarm; confirm which tree
you are in before reporting anything.

**Authoritative numbers:** `notes/corrected_baselines.md`. The submitted A/B/D dispositional
rows are artifacts and must not be used as baselines, comparison points, or sanity checks.

---

## 0. Recon — do this first, report before writing any code

Report file paths plus a short summary for each. Do not begin implementation until this is
reviewed.

**0.1 The dispositional pipeline.** Confirm which script produced the corrected sycophancy
and stance runs. Prior recon found `scripts/benchmark_full_instruct.py`, not
`benchmarking/sycophancy_eval.py` — verify this is still true post-correction and identify
which script generated the 1,776-record corrected rerun. Report: decoding parameters,
`max_new_tokens`, judge model and temperature, exactly what the judge sees, topic list
construction, and how `side` is selected.

**0.2 The compile primitive.** `hexis/belief_compiler.py::BeliefCompiler.compile_from_m_state`
is φ for the dispositional path. Confirm. Report its input type, output structure (per-layer
M_A/M_B/E_A/E_B), wall time, and whether rank is a constructor argument or baked into the
checkpoint.

**0.3 The d\* injection path.** Find every place d\* is applied. Report whether it can be
disabled per-arm without touching the compiled modulation, and whether prefill-vs-decode
injection is independently controllable. **The submitted paper's claim that prefill-off was
the standard configuration is contradicted by the code** — report the actual current default
and do not trust comments.

**0.4 The reflection path as it now exists.** After the rebuttal build there is a working
session → reflect → tree edit → recompile loop. Report: what the reflector sees (full
transcript? truncated? which turns?), the edit op schema, where edits are applied, and
whether the loop can be redirected to write into *context* instead of into tensors. That
redirection is the pivot experiment; if it requires more than a delivery-layer change, stop
and report the design question rather than improvising.

**0.5 Rank.** Determine whether the trained checkpoint's rank is fixed at 16 or whether φ can
be instantiated at other ranks without retraining. This determines whether the rank sweep is
a two-day inference job or a two-week training job. Report both paths.

**0.6 Empty-generation guard.** Find whether the corrected pipeline now asserts on empty or
whitespace-only generations. If it does not, this is the first thing you build (see §2.1).

---

## 1. Experiment order

Run in this order. Each entry: what it decides, not just what it measures.

### Week 1 — front-load the results that could invalidate later work

**E.1 — Functional similarity across compiled belief sets.**
Compile N ≥ 12 distinct belief sets. On a fixed probe set of hidden states, compute the
*functional* deltas — ΔQ and ΔV as actually applied — and report the pairwise cosine
similarity matrix.

**Functional, not parameter-space.** The v10 lesson in the repo's own notes is that
parameters can separate while functional deltas remain identical (cosine 0.9999). Measure
what the model experiences.

Decides: whether compiled states carry belief-specific structure at all, and along which
axes they vary. Feeds directly into how strongly the dispositional-memory framing can be
written. Report the matrix, not a summary statistic.

**A.1 — `F − d*` isolation arm.**
Rerun the corrected sycophancy protocol with d\* disabled and compiled modulation unchanged.
Decides: how much of the 89% hold rate is attributable to compiled modulation versus the
steering vector. Blocking for the paper.

### Week 2 — the pivot

**B.1 — Reflection delivered as context vs compiled into tensors.**
Identical reflection output, two delivery channels. The context arm appends the reflection
text to the prompt (this is Reflexion). The tensor arm recompiles, as now.

Both arms must receive **byte-identical reflection text**. Generate the reflection once per
session, then fork the delivery. Do not run the reflector twice.

Decides whether the update loop is a second contribution or a reported detail. Design it as
carefully as the B-vs-F comparison it mirrors, because it is the same experiment on
self-authored content.

### Week 3 — mechanism

**C.1 — Rank sweep against hold rate.**
Two-stage, cheapest first:

*Stage 1, inference-only.* Take the trained rank-16 compiled state and SVD-truncate the
functional delta to effective rank r ∈ {1, 2, 4, 8, 16}. Run the protocol at each. This
answers "does hold rate depend on effective rank" in a day. It does not answer "does a
model trained at rank r behave this way" — state that limit when reporting.

*Stage 2, only if Stage 1 shows a curve.* Retrain φ at two or three ranks to confirm the
truncation result reflects trained capacity rather than a truncation artifact.

**C.2 — Constant-offset control.**
Mean-pool the functional delta across the probe set to produce a fixed per-layer offset
vector, and apply that instead of the input-dependent map. This is "the steering vector this
compiled state would be if it could not respond to input," and it isolates input-dependence
from content-derivation. With the existing CAA arm this completes the 2×2.

### Week 4 — the dispositional-memory measurement

**S.1 — Topic salience at rest.**
Everything measured so far is a stance under attack. This measures disposition
unprompted: given open-ended prompts with no topic specified, does compiled disposition
shift what the model chooses to talk about?

Design carefully — this is the experiment most likely to produce a confound:
- Prompts must be genuinely topic-free ("What's on your mind?", "Pick something worth
  thinking about") and fixed across arms.
- Score with a blind classifier over a pre-registered topic taxonomy. The classifier must
  not see the belief tree or the condition.
- **Control for generic style shift.** A modulated model that simply becomes more verbose or
  more assertive could be misread as topic-shifted. Include a style-only arm or report
  length and register alongside topic distribution.
- Report the topic distribution, not a single divergence number.

### Weeks 5–6 — baselines

**D.1 Prefix tuning** at matched parameter count. Separates *outside the context window* from
*not inspectable as text*.
**D.3 Belief tree vs flat prose**, same propositional content, same compile path.
**D.2 Compressed prompt** at matched token count through the dilution sweep.
**E.2 Capacity sweep** k ∈ {1, 2, 4, 8, 16} beliefs in one compiled state.

---

## 2. Design factors — bake these into every run

### 2.1 Generation validity, asserted not assumed

The single most expensive error in this project's history was empty generations from
unmodulated arms being scored as a uniform value, producing a headline result that did not
exist. **Modulated arms were immune, which is why nobody noticed.**

Every run must, per record:
- log raw generation length before any post-processing
- log whether a reasoning block opened and whether it closed
- assert non-empty, non-whitespace output
- **fail the run loudly on any empty generation rather than continuing**

Every run must, per arm, report the count of empties. A run reporting zero empties in the
modulated arm and nonzero in the baseline arm is not a finding — it is the same bug.

### 2.2 Matched content across arms

Where two arms are supposed to differ only in delivery channel, verify that at the byte
level and log a hash of the content each arm received. This applies to B vs F, to B.1, and
to D.3. Assert equality; do not construct the content twice.

### 2.3 Configuration logged per record, never inferred

Every row logs: checkpoint hash, commit hash, rank, d\* enabled/scale, prefill on/off,
v-scale, judge model ID, decoding parameters, seed, topic, side, arm. The prefill erratum
happened because configuration was documented in prose instead of logged in data.

### 2.4 Judge blindness

The judge sees probe, pressure turn, and response. Never the arm, the condition label, the
tree, or the retrieved nodes. Same judge model and temperature across every arm in a
comparison. If a new judge is needed, run it against the existing corrected records first
and report agreement before using it for anything.

### 2.5 Trials under greedy decoding

Decoding is greedy, so repeated trials on identical input are identical. A "trial" is only
meaningful if the input varies. Either author distinct pressure turns per trial, or set
trials to 1 and take statistical power from the topic count. State which, in the
pre-registration, before launch.

### 2.6 Unit of analysis

Topics, not sessions. Sessions within a topic are correlated. Bootstrap CIs over topics.
Report n topics prominently; these are 20–24-topic experiments and the writeups should never
imply otherwise.

### 2.7 Exclusions

Infrastructure errors only, logged individually with reason. No outcome-based exclusion of
any kind, ever. Report raw and post-exclusion denominators in every table.

### 2.8 Never overwrite

New results to new files under `results/<experiment>_<run_id>.jsonl`. Prior results are
immutable. Resume-from-partial via the existing `run_id` dedup pattern.

---

## 3. Pre-registration

Before each experiment launches, commit a short file to `notes/` stating: the prediction,
the primary metric, the analysis plan, the exclusion rule, and what result would count as a
negative. Commit before the run, not after.

For B.1 and C.1 in particular, fix in advance what magnitude counts as the effect. These are
the two experiments where a stopping point or a threshold chosen after seeing data would be
the most damaging thing in the paper.

Negative results are reported. If the rank sweep is flat, that is a finding about the
mechanism and it changes the paper's title rather than getting rerun.

---

## 4. Guardrails

- Do not modify: existing pressure-turn content, judge prompts, φ training code, any
  checkpoint, anything under `results/` from prior runs.
- Do not tune a baseline arm less carefully than the treatment arm. The CAA baseline was
  tuned honestly on training topics with a degeneracy guard; hold every future baseline to
  that standard and document the tuning procedure.
- If an experiment requires building something that does not exist, **stop and report the
  design question.** Do not improvise it. The reflection loop was correctly flagged this way
  last time and the flag was worth more than the code would have been.
- If a result contradicts `notes/corrected_baselines.md`, stop and report. Do not reconcile
  it silently.

---

## 5. Reporting

Per experiment, write `analysis/<experiment>_summary.md` containing: the primary table with
raw denominators, the per-topic breakdown, exclusion log, the empty-generation count per arm,
exact reproduce command, and a one-paragraph plain-language statement of the result suitable
for pasting into the paper. Flag anything surprising rather than smoothing it.
