# User-sim & review-LLM model ledger per dataset

Tracks which Bedrock model was used for the user-simulator (and review judge) on
each dataset in `results/`. Important because:

1. The Apr 22 canonical airline run used **Sonnet-4.5** as user-sim. Numbers
   from this era can't be directly compared to runs using a different user-sim.
2. After Apr 25 we hit Sonnet daily-quota walls multiple times, forcing some
   runs to mid-flight swap to **Haiku-4.5**. Cross-family validation (Ministral,
   27B) was always on Haiku per the [scale-validation handoff](../../experiments/CLAUDE.md)
   convention to stay TPM-safe.
3. If we later want to rerun any cell on Sonnet for parity, this file is the
   source of truth for what was originally measured under what conditions.

## Datasets

| Dataset | n | User-sim | Review LLM | Notes |
|---|---|---|---|---|
| `dispositional/4b_sycophancy_5level/v23_sycophancy_5level.json` | 60 cells (3 topics × 4 cond × 5 lvl × 3 trials) | n/a (no agentic) | LLM judge | Generated Mar 27, no user-sim — direct stance/conviction prompts. Judge was Claude Sonnet (LiteLLM). |
| `dispositional/27b_m2_sycophancy/m2_raw.jsonl` | 240 | n/a | Sonnet-4.5 (judge) | Apr 24 paper-grade scale validation run on Qwen3.6-27B. |
| `dispositional/ministral_m2_sycophancy/m2_raw.jsonl` | 240 | n/a | Sonnet-4.5 (judge) | Apr 25 v3 — tokenizer_mode=hf fix + v_scale=0.5. |
| `agentic/airline_27b_hard_panel/airline_qwen27b_hard_1777166273.jsonl` | 100 | Sonnet-4.5 | Sonnet-4.5 | Apr 26 27B hard panel, baseline 58% vs C9 60%. |
| `agentic/airline_4b_canonical/SCOREBOARD_REPORT_apr22.md` | 250 | Sonnet-4.5 | Sonnet-4.5 | Apr 22 canonical 5-arm scoreboard. **Source jsonl lost** (likely written to /tmp and cleaned, or stored on a now-retired Modal volume). |
| `agentic/airline_4b_canonical/airline_5arm_apr25_v3.jsonl` | 150 (n=30/arm × 5 arms) | Sonnet-4.5 (started) → swapped mid-flight to Haiku-4.5 after rate-limit | Sonnet-4.5 (started) → Haiku-4.5 | Apr 25 22:13 rerun after UNIVERSAL_RULES sessionless-leak fix. Stripped 6 rate-limit-errored trials before swap; saved as `.pre_haiku_swap` backup. Mixed user-sim — see Apr 25 memory. |
| `agentic/airline_4b_hard_panel_apr26/embedscope_n125.jsonl` | 125 | Haiku-4.5 (temp=0) | Haiku-4.5 | Apr 26 hard-5 panel after embedding-scoped retrieval shipped. Pre-loop-detector. |

## In-flight (not yet in hexis-public)

| Dataset | Started | n target | User-sim | Status | Notes |
|---|---|---|---|---|---|
| `tau3_alldomain_haiku_1777243935.jsonl` | Apr 26 16:52 | 600 | **Haiku-4.5** (temp=0) | running | After Sonnet daily quota blew on prior 422-trial run. Aim: paper-grade all-domain comparison (4 domains × 10 tasks × 5 trials × baseline+C3+C5). |
| `tau3_alldomain_sonnet_partial_clean.jsonl` | Apr 26 16:33 | 600 (only 118 clean) | Sonnet-4.5 (until quota blew) | KILLED | Salvaged 118 non-errored trials (mostly airline + retail seed); banking & telecom had zero before quota hit. Held for cross-validation only — not paper-grade. |

## Convention going forward

- **User-sim default:** Haiku-4.5 (`bedrock/us.anthropic.claude-haiku-4-5-20251001-v1:0`), temp=0, TPM-safe at conc 30.
- **Review LLM default:** Haiku-4.5 (same).
- **When to use Sonnet:** Only on small panels (<30 trials) where TPM headroom is comfortable, OR when a specific user-sim's reasoning is required for the experiment's validity claim.
- **Always log in this ledger** before adding a new dataset to `results/`.
