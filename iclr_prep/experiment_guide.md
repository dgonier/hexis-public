# Experiment Guide — Names, Questions, Status

File prefixes keep the short codes (e1_, a1_, b1_ ...) for artifact continuity; prose and
discussion use the names. Each name is the question the experiment answers.

| Name | Code | Question | Status |
|---|---|---|---|
| Fingerprints | E.1 | Do different beliefs compile to different functional effects? | DONE — Q channel: one fingerprint (cos .996); V channel: belief-specific (.52) |
| Fingerprints: Con Side | E.1b | Does the Q/V split replicate on held-out con-side compiles? | prereg'd, running |
| Steering Audit | A.1 | How much of the 89% hold is compiled modulation vs d*? | prereg'd, arms running (F-anchor gate + F+d*x3 + d*-only) |
| Sticky Note vs. Muscle Memory | B.1 | Does WHERE a self-authored lesson is stored (context vs tensors) change whether it survives fresh pressure? | Sat build, Sun run — the pivot |
| Bottleneck | C.1 | How narrow can the compiled channel get (rank 16->1, SVD) before persistence fails? | stretch goal |
| Taxidermy | C.2 | Does the modulation frozen into a constant offset (mean delta) still work — isolating input-responsiveness? | queued (completes 2x2 with CAA arm) |
| What's On Your Mind | S.1 | Does compiled disposition shift unprompted topic choice? (disposition at rest) | week of Aug 11 |
| Invisible Ink | D.1 | Prefix tuning: unreadable but in-context — is the operative property readability or position? | Aug 15+ |
| Shorthand | D.2 | Compressed prompt at matched tokens — compression or channel? | Aug 15+ |
| Blueprint vs. Essay | D.3 | Typed belief tree vs flat prose, same content — does schema matter? | Aug 15+ |
| Full House | E.2 | How many beliefs per compiled state before interference? | nice-to-have |

Standing rules (all runs): prereg committed before launch; guards fail-loud on empties;
judge blind, Haiku temp 0; topics are the unit of analysis; never overwrite; summary in
analysis/<code>_summary.md with raw denominators + reproduce command.

Key result so far — Fingerprints: the two modulation channels dissociate INTERNALLY
(Q = content-blind hold-firm machinery, V = belief content), echoing the paper's external
install-vs-persist dissociation. Registered pooled-dQ metric reads negative as registered;
the per-channel split is elevated via the pre-registered Con Side confirmation.
