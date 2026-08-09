# Experiment Guide — Names, Questions, Status

File prefixes keep the short codes (e1_, a1_, b1_ ...) for artifact continuity; prose and
discussion use the names. Each name is the question the experiment answers.

| Name | Code | Question | Status |
|---|---|---|---|
| Fingerprints | E.1 | Do different beliefs compile to different functional effects? | DONE — Q channel: one fingerprint (cos .996); V channel: belief-specific (.52) |
| Fingerprints: Con Side | E.1b | Does the Q/V split replicate on held-out con-side compiles? | DONE — SPLIT REPLICATED: dQ off-diag .9959 (>.99), dV .5314 range .77 (<.8, >.3); both prereg legs pass. Q = content-blind hold machinery, V = belief content, on both sides. |
| Steering Audit | A.1 | How much of the 89% hold is compiled modulation vs d*? | DONE (all 5 arms, 1800 records, 0 empties). DECIDED (Aug 8, Devin): d* LEAVES THE PAPER. Audit is the license: F-anchor 86.9% [79.2,93.3] reproduces 89%; F+d* dose-dependently HURTS (-0.3pp @.05, -6.4pp @.10, -14.4pp @.20); d*-only collapses to 21.1% — a second fixed-direction method in the CAA regime (14%). One appendix sentence discloses training-time signal + this ablation; main body F = compiled M + curated slot, zero d* mentions. |
| Sticky Note vs. Muscle Memory | B.1 | Does WHERE a self-authored lesson is stored (context vs tensors) change whether it survives fresh pressure? | RUNNING — 3 arms (sticky/muscle/no-reflection control), prereg e823090b; smoke then full 20-topic overnight run |
| Bottleneck | C.1 | How narrow can the compiled channel get (rank 16->1, SVD) before persistence fails? | stretch goal |
| Taxidermy | C.2 | Does the modulation frozen into a constant offset (mean delta) still work — isolating input-responsiveness? | queued (completes 2x2 with CAA arm) |
| What's On Your Mind | S.1 | Does compiled disposition shift unprompted topic choice? (disposition at rest) | week of Aug 11 |
| Invisible Ink | D.1 | Prefix tuning: unreadable but in-context — is the operative property readability or position? | Aug 15+ |
| Shorthand | D.2 | Compressed prompt at matched tokens — compression or channel? | Aug 15+ |
| Blueprint vs. Essay | D.3 | Typed belief tree vs flat prose, same content — does schema matter? | Aug 15+ |
| Full House | E.2 | How many beliefs per compiled state before interference? | nice-to-have |
| Standard Candle | SC.1 | Do the results replicate on the field's standard sycophancy benchmarks (Sharma are-you-sure flip rate; Perez conformity rate)? | queued behind B.1 (Aug 8, Devin) — external-validity anchor; reuses benchmarking/sycophancy_perez.py harness + vendored datasets |

Standing rules (all runs): prereg committed before launch; guards fail-loud on empties;
judge blind, Haiku temp 0; topics are the unit of analysis; never overwrite; summary in
analysis/<code>_summary.md with raw denominators + reproduce command.

Key result so far — Fingerprints: the two modulation channels dissociate INTERNALLY
(Q = content-blind hold-firm machinery, V = belief content), echoing the paper's external
install-vs-persist dissociation. Registered pooled-dQ metric reads negative as registered;
the per-channel split is elevated via the pre-registered Con Side confirmation.
