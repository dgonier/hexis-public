# τ³-bench LoRA-SFT control bench (Apr 28 2026)

Reviewer-driven control: how much of HEXIS's lift comes from training procedure vs architecture?
Answer: on the LoRA-trained domains (airline, retail, telecom), task-specific LoRA-SFT wins; on
held-out domain (banking_knowledge), LoRA fails catastrophically (0% — malformed tool calls).

## Setup
- **Host**: Qwen3.5-4B (instruct)
- **Adapter**: rank-16 LoRA on q_proj+v_proj, all 32 attention layers, alpha=32
- **Training data**: 1,000 random samples (333 each from airline/retail/telecom) from
  `inclusionAI/AReaL-tau2-data` SFT split (33,531 total)
- **Compute**: 1× H200, 871 steps, AdamW lr=5e-5, gradient clipping 1.0, fp32 LoRA params,
  bf16 base, max_length=4096, left-truncation. Early-stopped at rolling-100 plateau (200 step
  patience). Wall: ~55 minutes, ~$10 Modal.
- **Leakage check**: 0 substring matches between AReaL training samples and our 24-task
  evaluation panel; only 20/33,531 records contained a generic refund-policy phrase.

## Files
| File | Description |
|---|---|
| `tau3_lora_baseline_1777423414.jsonl` | Bench output, 130 trials |
| `tau3_lora_baseline_1777423414.audit.jsonl` | Sonnet audit, 30 disputed trials |
| `tau3_lora_baseline_1777423414.opus.jsonl` | Opus tiebreaks, 7 trials |
| `train_lora_tau2.py` | Trainer with early-stop |
| `train_lora_tau2_modal.py` | Modal H200 wrapper |
| `lora_endpoint_app.py` | vLLM serve endpoint with LoRA + tool-calling |

## Headline numbers (3-judge audited, balanced 20-cell head-to-head, 60 paired trials per config)

| Domain | Baseline | HEXIS-C5 | LoRA-SFT |
|---|---|---|---|
| airline (LoRA-trained) | 67% | 67% | **75%** |
| retail (LoRA-trained) | 74% | 85% | **93%** |
| telecom (LoRA-trained) | 89% | **100%** | 89% |
| **Overall (LoRA-trained)** | 73% | 80% | **85%** |
| banking_knowledge (UNSEEN by LoRA) | 25% | **45%** | **0% (all malformed JSON)** |

LoRA wins on its trained distribution; HEXIS is the only method that handles a held-out
domain at deploy time (POST /v1/state/banking_knowledge/init compiles a domain-specific
phi_R in ~20s, then the teacher loop accumulates failure-mode hints).
