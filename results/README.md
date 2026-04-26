# Paper-supporting raw data

This directory holds the raw experimental data backing the claims in `paper/main_v2.pdf`.
Anything cited in the paper text must have its source data here. If a result is not yet
clean enough to cite, it stays out of this tree until it is.

## Layout

```
results/
├── README.md                                      ← this file
├── benchmark_plan_v2.md                           ← experimental design plan
├── dispositional/                                 ← Phase D / sycophancy / stance
│   ├── sycophancy_golds.json                     ← gold-stance reference set
│   ├── 4b_sycophancy_5level/                     ← 4B M2, paper Table 2
│   │   └── v23_sycophancy_5level.json            ← per-(topic,cond,level) hold counts
│   ├── 27b_m2_sycophancy/                        ← Qwen3.6-27B scale validation, n=240
│   │   ├── m2_raw.jsonl                          ← per-trial outputs + judge scores
│   │   └── m2_summary.json                       ← aggregate hold/cap rates
│   └── ministral_m2_sycophancy/                  ← Ministral-8B scale validation
│       ├── m2_raw.jsonl
│       └── scale_validation_summary.json
└── agentic/                                       ← tau-bench airline runs
    ├── airline_4b_canonical/                     ← Apr 22 5-arm canonical (n=50/arm)
    │   └── SCOREBOARD_REPORT_apr22.md            ← writeup; raw jsonl reconstruction TBD
    ├── airline_4b_hard_panel_apr26/              ← Apr 26 hard-5 panel n=125
    │   └── embedscope_n125.jsonl
    └── airline_27b_hard_panel/                   ← Apr 26 27B hard panel
        ├── airline_qwen27b_hard_1777166273.jsonl
        └── airline_qwen27b_hard_1777166273.manifest.json
```

## Mapping to paper sections

| Paper claim | File |
|---|---|
| Table 2: 4B sycophancy F=88.9% vs A=57.8% | `dispositional/4b_sycophancy_5level/v23_sycophancy_5level.json` |
| 4B F vs A McNemar p=0.0001 (n=45 paired) | (computed from above) |
| 27B M2: hold 65% vs 41% (n=240) | `dispositional/27b_m2_sycophancy/m2_raw.jsonl` |
| Ministral M2: +3pp hold, -15pp cap | `dispositional/ministral_m2_sycophancy/m2_raw.jsonl` |
| Apr 22 airline canonical: C5 84% (42/50) p=0.007 | `agentic/airline_4b_canonical/SCOREBOARD_REPORT_apr22.md` (TODO: locate source jsonl) |
| Apr 26 4B hard-panel embedscope (loop-detector dev set) | `agentic/airline_4b_hard_panel_apr26/embedscope_n125.jsonl` |
| 27B airline hard panel: baseline 58% vs C9 60% | `agentic/airline_27b_hard_panel/airline_qwen27b_hard_1777166273.jsonl` |

## Open data hygiene gaps

1. **Apr 22 canonical airline scoreboard source**: The report at
   `agentic/airline_4b_canonical/SCOREBOARD_REPORT_apr22.md` reports
   baseline=31/50, C5=42/50 etc., but no single jsonl in the source `experiments/`
   repo reproduces those exact counts. The numbers are likely a reconstruction
   across multiple runs. The headline agentic claim in the paper depends on this
   data; the source jsonl(s) need to be located or the experiment re-run.

2. **AlfWorld results** (paper Table on Mind Tree online learning): the
   underlying data is dirty (mixed conditions, stale checkpoints) and is being
   re-run before adding here.

3. **Targeted loop-fix run (Apr 26)**: in flight, will be added here once
   complete and validated.

## Provenance protocol

When adding new data, every dataset directory must contain either:
- a `.manifest.json` file describing run parameters, model, date, panel, configs, OR
- a `README.md` documenting same

The expectation is: any reader of the paper can clone this repo and re-derive
every cited number from these files. Aggregates that can't be computed from
the raw data here are not citable in the paper.
