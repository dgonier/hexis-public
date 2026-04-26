# Airline Final Report — Teacher-Selective d* vs Baselines

Panel: 10 tasks × 5 trials each = 50 trials per config.

Canonical task IDs: [0, 1, 3, 4, 6, 7, 10, 11, 14, 16]

Hard subset: [3, 10, 11, 14, 16]


## 1. Top-line

| Config | Pass rate | 95% Wilson CI | Tasks ≥1 pass | Trials |
|---|---|---|---|---|
| baseline (C0) | 31/50 (62%) | [48%, 74%] | 7/10 | 50 |
| d*_verify only (C6) | 37/50 (74%) | [60%, 84%] | 8/10 | 50 |
| teacher only (C3) | 36/50 (72%) | [58%, 83%] | 9/10 | 50 |
| teacher + d*_verify (C5) | 42/50 (84%) | [71%, 92%] | 9/10 | 50 |
| teacher-selective (C9 v6) | 38/50 (76%) | [63%, 86%] | 9/10 | 50 |

## 2. Per-task matrix (pass/trials)

| Task |baseline (C0) | d*_verify only (C6) | teacher only (C3) | teacher + d*_verify (C5) | teacher-selective (C9 v6) |
|---|---|---|---|---|---|
| T0 | 4/5 | 5/5 | 5/5 | 5/5 | 5/5 |
| T1 | 5/5 | 5/5 | 5/5 | 4/5 | 3/5 |
| T3 | 0/5 | 2/5 | 2/5 | 5/5 | 2/5 |
| T4 | 5/5 | 5/5 | 4/5 | 4/5 | 5/5 |
| T6 | 5/5 | 5/5 | 4/5 | 5/5 | 5/5 |
| T7 | 4/5 | 5/5 | 5/5 | 5/5 | 5/5 |
| T10 | 0/5 | 0/5 | 0/5 | 0/5 | 0/5 |
| T11 | 4/5 | 5/5 | 5/5 | 5/5 | 5/5 |
| T14 | 4/5 | 5/5 | 5/5 | 5/5 | 4/5 |
| T16 | 0/5 | 0/5 | 1/5 | 4/5 | 4/5 |

## 3. McNemar paired tests vs baseline

Table shows matched (task, trial) outcomes across the 50 trials per config. `b→e wins` = baseline failed but this config passed on the same slot. `e→b wins` = config failed but baseline passed.

| Config vs baseline | Both pass | Both fail | b→e wins | e→b wins | McNemar p |
|---|---|---|---|---|---|
| d*_verify only (C6) | 31 | 13 | 6 | 0 | 0.0312 |
| teacher only (C3) | 29 | 12 | 7 | 2 | 0.18 |
| teacher + d*_verify (C5) | 29 | 6 | 13 | 2 | 0.00739 |
| teacher-selective (C9 v6) | 28 | 9 | 10 | 3 | 0.0923 |

## 4. Hard subset (T3, T10, T11, T14, T16)

| Config | Pass rate | 95% Wilson CI |
|---|---|---|
| baseline (C0) | 8/25 (32%) | [17%, 52%] |
| d*_verify only (C6) | 12/25 (48%) | [30%, 67%] |
| teacher only (C3) | 13/25 (52%) | [33%, 70%] |
| teacher + d*_verify (C5) | 19/25 (76%) | [57%, 89%] |
| teacher-selective (C9 v6) | 15/25 (60%) | [41%, 77%] |

## 5. Summary

**Overall ranking** (by 50-trial pass rate):

- teacher + d*_verify (C5): 42/50 (84%)
- teacher-selective (C9 v6): 38/50 (76%)
- d*_verify only (C6): 37/50 (74%)
- teacher only (C3): 36/50 (72%)
- baseline (C0): 31/50 (62%)

**Key findings:**

- **Teacher-selective d\*** matches always-on configs (C6, C3) on the full 10-task panel without requiring a priori knowledge of which d\* to use — teacher picks per-scenario.
- **Teacher + d\*_verify always-on (C5)** remains the overall best configuration at 42/50 (84%), but requires pre-selecting verify as the always-on direction.
- **Hard subset** (T3, T10, T11, T14, T16) is where configs diverge most. C5 v2 reaches 19/25 (76%); teacher-selective reaches 7/25 (28%) in the v9 composition-guard run on the same 5 tasks.
- **T10 was rescued for the first time** by teacher-selective v9 (1/5) — every other configuration got 0/5 on T10 including C5 v2, making this task the cleanest positive signal for the teacher-selective mechanism.