# Claim Priorities and Experiment Queue, ICLR 2027 (Devin, 2026-08-19 — canonical)
(Coordinator reconciliation against program state appended at bottom. Original verbatim below.)

[Devin's full queue text saved verbatim — see conversation of 2026-08-19; Tier A/B/C/D claims,
experiments A.1-A.3, B.1-B.3, C.1-C.4, D.1-D.5, E.1-E.3, F.1-F.4, sequencing table,
stop rule Sep 8, prereg discipline with fixed thresholds for B.1/B.3/C.3.]

## Coordinator reconciliation (2026-08-19)

ALREADY DONE (with citations to analysis/):
- A.1 -> DONE Aug 8-9 as "Steering Audit" and BETTER than specified: corrected F is already
  d*-free (recon finding); ran F+d* dose sweep (-0.3/-6.4/-14.4pp at 0.05/0.10/0.20) and
  d*-only (21.1%). Tier B.5 answered. analysis/a1_summary.md.
- C.1 -> DONE Stage 1 as "Bottleneck": FLAT curve 88.6-93.3% at r in {1,2,4,8,16}
  (r=32 impossible by truncation; trained rank is 16). Per the queue's own rule the curve
  did not appear -> Stage 2 retrain unnecessary; framing changes instead ("persistence is
  low-dimensional"). analysis/c1_summary.md + c1c spectrum diagnostics (spread+decorrelated).
- C.2 -> DONE as "Taxidermy": frozen offset 88.9% ~= F. PLUS C.2b (not in queue): slot-only
  57.5% vs compiled-only-under-pressure 91.9% — resolves the attribution 2x2 cleanly and
  fills the never-measured C-hold cell. analysis/c2_summary.md, c2b_summary.md.
- E.1 -> DONE as "Fingerprints" + E.1b con-side prereg replication: dQ 0.996 (content-blind
  hold direction), dV 0.53 (belief-specific). C.4's Text-to-LoRA precedent (functional-space
  measurement, modest-positive = healthy) folds into the writeup as citation.
- B.1 -> DONE as registered (Aug 9): op-delivery variant, sticky 81.3 vs muscle 87.3
  (+6.0pp, INSIDE the pre-fixed 5-10pp inconclusive band); per-level curve directional
  (sticky 91.7->75.0, muscle flat). Instrument note: production reflector emits bare JSON
  ops. PLUS the Lineup registered run (42 sessions) on self-authored identity: reflection
  helps ONLY with a text substrate. TIER C RULE THEREFORE FIRES: B.1 did not land ->
  reflection reported as functional update path; learning claim -> future work.
- Tier B.2 (discrimination), B.3 (Llama third family), B.4 (MMLU p=0.11), B.1 (CAA) — all done.
- E.2 partial: Lineup capacity smoke merged k={3,8,12} claims with no install/coherence
  degradation at k=12 (mean-merge). E.2-on-sycophancy-protocol remains if wanted.
- Extra results not in queue: SC.1 external benchmarks (null AYS / Perez reversal — boundary
  on off-topic transfer), c1d threshold+amplify smoke (amplification HURTS hold: 100->33/20%
  at x2.0 — MUST be cited in C.3's prereg), The Lineup (mechanism confirmed/outcome missed).

GENUINELY REMAINING (new [LIT] items + original D-track + paper build):
- A.3 prior-strength stratification (free, scoring pass) — RUN FIRST
- B.3 length-matched noise control — NEAR-BLOCKING
- B.2 paraphrase-consistency probes (3x probes run)
- C.3 amplitude sweep beta, install vs retention scored separately (prereg must incorporate
  c1d: retention already known to degrade at x2.0; hypothesis is install rises before that)
- D.1 prefix tuning, D.2 compressed prompt, D.3 tree-vs-prose, D.4 adversarial steering
  extraction, D.5 perturbation stress test both channels
- E.3 null-belief control (cheap; scrambled-ledger adjacent but not identical)
- A.2 figure/table rebuild + entire paper scaffold (Track B) + related-work prose
- F.1-F.4 next-paper (F.2 benign length sweep is the cheapest stretch)

## Addendum (Devin, 2026-08-19): computational implications — serving properties subsection

The paper must state the compute story explicitly (TTFT, latency, asymptotics). Three
parts, to be written into the mechanism or isolation section as "Serving properties":

1. READ COST ~zero, exactly zero if folded: modulation adds O(d*r) per patched layer vs
   O(d^2) projections (~r/3d ~= 0.3% FLOPs at r=16); linearity permits folding
   W' = W + M_A M_B^T once per session -> zero per-token overhead (same equivalence C.2
   exploited). Verify fold is output-identical in the microbenchmark.
2. CONTEXT COST eliminated: belief-in-context pays O(N_b^2 + N_b*N_t) attention in EVERY
   prefill, grows TTFT, occupies KV-cache and context budget every session (measured
   live: ctx arms ran overflow-truncated on every move). Compiled: zero tokens, bare-model
   TTFT, full budget to the task, O(1) per query.
3. WRITE COST amortized and OFF THE CRITICAL PATH: one hypernetwork forward per belief
   update, schedulable on a parallel stream/device while serving continues, swapped at a
   session boundary — "washed into the compute," same scheduling class as prefix-cache
   warming. Reflection recompiles overlap the conversation. Family precedent:
   GenerativeAdapter's published 4x compute/memory reduction vs full-conversation
   prompting — cite; our addition is that the channel that saves the compute is the one
   that holds the stance.

Microbenchmark dispatched to the experiment queue (compile wall time, TTFT/tok/s for
bare vs B vs F vs folded-F, analytic FLOPs) -> analysis/serving_microbench.md.
