"""Train a rank-16 LoRA on Qwen3.5-4B using a 1K-sample subset of AReaL
tau2 SFT data. Used as a control for the τ³-bench experiment.

Each AReaL record has:
  messages: [system, assistant, user, tool, ..., user]   (history)
  answer:   {role: assistant, content: ..., thinking: ..., tool_calls: [...]}
  metadata: {source_dialog_id, turn_index, scenario_id, correct, reward}

We train SFT on the answer (one assistant turn) given the conversation history.
"""
import argparse
import json
import os
import time
from pathlib import Path

import torch
from torch.utils.data import DataLoader, Dataset
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import LoraConfig, get_peft_model


def format_answer(answer: dict) -> str:
    """Render the AReaL `answer` dict back into chat-template-compatible
    assistant content. The Qwen tool format uses content + tool_calls.
    For SFT loss purposes we emit the literal text the model should produce.
    """
    content = answer.get('content') or ''
    thinking = answer.get('thinking') or ''
    tool_calls = answer.get('tool_calls') or []

    parts = []
    if thinking:
        parts.append(f"<think>\n{thinking}\n</think>")
    if content:
        parts.append(content)
    for tc in tool_calls:
        # Qwen ChatML tool-call format
        fn = tc.get('function', {})
        name = fn.get('name', '')
        args_raw = fn.get('arguments', '{}')
        if isinstance(args_raw, str):
            args = args_raw
        else:
            args = json.dumps(args_raw)
        parts.append(f'<tool_call>\n{{"name": "{name}", "arguments": {args}}}\n</tool_call>')
    return "\n".join(parts) if parts else ""


class TauSFTDataset(Dataset):
    def __init__(self, path, tokenizer, max_length=4096):
        self.records = [json.loads(l) for l in open(path)]
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self):
        return len(self.records)

    def __getitem__(self, idx):
        r = self.records[idx]
        messages = list(r.get('messages', []))
        answer = r.get('answer', {})
        target_str = format_answer(answer)

        # Append the answer as the final assistant turn for full-format,
        # then compute the prompt-only ids to mask.
        full_messages = messages + [{'role': 'assistant', 'content': target_str}]

        # Apply chat template
        try:
            full_text = self.tokenizer.apply_chat_template(full_messages, tokenize=False, add_generation_prompt=False)
            prefix_text = self.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        except Exception:
            # Fallback: simple concat
            full_text = '\n'.join(m.get('content', '') for m in full_messages)
            prefix_text = '\n'.join(m.get('content', '') for m in messages)

        full_ids = self.tokenizer(full_text, add_special_tokens=False).input_ids
        prefix_ids = self.tokenizer(prefix_text, add_special_tokens=False).input_ids
        prefix_len = len(prefix_ids)

        # Left-truncate to keep the answer + as much recent context as possible.
        # If full_ids > max_length, we cut from the LEFT (keeping the tail), then
        # adjust prefix_len so masking is correct.
        if len(full_ids) > self.max_length:
            cut = len(full_ids) - self.max_length
            full_ids = full_ids[cut:]
            new_prefix_len = max(0, prefix_len - cut)
            prefix_len = new_prefix_len

        labels = list(full_ids)
        for i in range(min(prefix_len, len(labels))):
            labels[i] = -100

        return {
            "input_ids": torch.tensor(full_ids, dtype=torch.long),
            "labels": torch.tensor(labels, dtype=torch.long),
            "attention_mask": torch.ones(len(full_ids), dtype=torch.long),
        }


def collate(batch):
    max_len = max(item["input_ids"].size(0) for item in batch)
    input_ids, labels, attention_mask = [], [], []
    for item in batch:
        pad = max_len - item["input_ids"].size(0)
        input_ids.append(torch.cat([item["input_ids"], torch.zeros(pad, dtype=torch.long)]))
        labels.append(torch.cat([item["labels"], torch.full((pad,), -100, dtype=torch.long)]))
        attention_mask.append(torch.cat([item["attention_mask"], torch.zeros(pad, dtype=torch.long)]))
    return {
        "input_ids": torch.stack(input_ids),
        "labels": torch.stack(labels),
        "attention_mask": torch.stack(attention_mask),
    }


def train(args):
    print(f"[lora-tau2] loading {args.model}")
    tokenizer = AutoTokenizer.from_pretrained(args.model, trust_remote_code=True)
    if tokenizer.pad_token_id is None:
        tokenizer.pad_token = tokenizer.eos_token
    model = AutoModelForCausalLM.from_pretrained(
        args.model, torch_dtype=torch.bfloat16, trust_remote_code=True,
        device_map="cuda",
        attn_implementation="eager",  # avoids some flash-attn paths that OOM
    )
    # Re-enable gradient checkpointing (without it, OOM at step 1 on 80GB H100
    # for Qwen3.5-4B with full-attention hybrid layers + max_length=2048).
    # With lr=5e-5 + grad clip 1.0 + LoRA params in fp32, NaN is unlikely.
    model.gradient_checkpointing_enable()
    if hasattr(model, 'config'):
        model.config.use_cache = False

    print(f"[lora-tau2] applying LoRA r={args.rank} on q_proj,v_proj")
    lora_cfg = LoraConfig(
        r=args.rank,
        lora_alpha=args.rank * 2,
        target_modules=["q_proj", "v_proj"],
        lora_dropout=0.0,
        bias="none",
        task_type="CAUSAL_LM",
    )
    model = get_peft_model(model, lora_cfg)
    model.print_trainable_parameters()
    # Cast LoRA params to fp32 for numerical stability (base stays bf16)
    for n, p in model.named_parameters():
        if p.requires_grad:
            p.data = p.data.float()
    model.train()

    print(f"[lora-tau2] loading {args.data}")
    ds = TauSFTDataset(args.data, tokenizer, max_length=args.max_length)
    print(f"[lora-tau2]   {len(ds)} samples")
    loader = DataLoader(ds, batch_size=args.batch_size, shuffle=True, collate_fn=collate)

    opt = torch.optim.AdamW(
        [p for p in model.parameters() if p.requires_grad],
        lr=args.lr, weight_decay=0.0, eps=1e-7,
    )

    metrics = {"epochs": [], "loss": [], "step_losses": [], "early_stopped": False}
    t0 = time.time()
    step = 0
    nan_streak = 0
    # Early-stopping state (rolling mean plateau)
    rolling_window = 100
    plateau_patience = 200  # stop if no new min across this many consecutive steps
    best_rolling = float("inf")
    steps_since_best = 0
    early_stop = False
    for epoch in range(args.epochs):
        if early_stop: break
        epoch_loss = 0.0
        n = 0
        for batch in loader:
            batch = {k: v.to("cuda") for k, v in batch.items()}
            out = model(**batch)
            loss = out.loss
            opt.zero_grad()
            if torch.isnan(loss) or torch.isinf(loss):
                nan_streak += 1
                step += 1
                if nan_streak >= 5:
                    raise RuntimeError(f"loss diverged: {loss.item()} for {nan_streak} steps")
                continue
            nan_streak = 0
            loss.backward()
            torch.nn.utils.clip_grad_norm_([p for p in model.parameters() if p.requires_grad], 1.0)
            opt.step()
            epoch_loss += loss.item()
            n += 1
            step += 1
            metrics["step_losses"].append((step, loss.item()))
            if step <= 10 or step % 25 == 0:
                elapsed = time.time() - t0
                # Rolling-mean over last rolling_window steps
                recent_losses = [l for _, l in metrics["step_losses"][-rolling_window:]]
                rolling = sum(recent_losses) / len(recent_losses)
                print(f"[lora-tau2]   step {step}  loss={loss.item():.4f}  "
                      f"rolling{len(recent_losses)}={rolling:.4f}  best={best_rolling:.4f}  "
                      f"plateau={steps_since_best}  elapsed={elapsed:.0f}s")
            # Update plateau tracking after the rolling window has filled
            if len(metrics["step_losses"]) >= rolling_window:
                rolling = sum(l for _, l in metrics["step_losses"][-rolling_window:]) / rolling_window
                if rolling < best_rolling - 1e-3:
                    best_rolling = rolling
                    steps_since_best = 0
                else:
                    steps_since_best += 1
                if steps_since_best >= plateau_patience:
                    print(f"[lora-tau2] EARLY STOP at step {step}: "
                          f"rolling{rolling_window} mean has not improved for {steps_since_best} steps "
                          f"(best={best_rolling:.4f}, current={rolling:.4f})")
                    early_stop = True
                    metrics["early_stopped"] = True
                    metrics["stop_step"] = step
                    break
        avg = epoch_loss / max(1, n)
        metrics["epochs"].append(epoch)
        metrics["loss"].append(avg)
        print(f"[lora-tau2] epoch {epoch+1}/{args.epochs} avg_loss={avg:.4f}")

    print(f"[lora-tau2] saving to {args.output}")
    Path(args.output).mkdir(parents=True, exist_ok=True)
    model.save_pretrained(args.output)
    tokenizer.save_pretrained(args.output)
    json.dump(metrics, open(f"{args.output}/training_metrics.json", "w"), indent=2)
    print(f"[lora-tau2] done. wall: {time.time()-t0:.0f}s")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="Qwen/Qwen3.5-4B")
    ap.add_argument("--data", default="/home/dgonier/experiments/data/areal_tau2/tau2_sft_1k_balanced.jsonl")
    ap.add_argument("--output", default="/home/dgonier/experiments/checkpoints/lora_tau2_r16")
    ap.add_argument("--rank", type=int, default=16)
    ap.add_argument("--epochs", type=int, default=2)
    ap.add_argument("--lr", type=float, default=5e-5)
    ap.add_argument("--batch-size", type=int, default=1)
    ap.add_argument("--max-length", type=int, default=4096)
    args = ap.parse_args()
    train(args)
