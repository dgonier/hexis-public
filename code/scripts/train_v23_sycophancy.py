"""
v23 Sycophancy Training: Teach M to produce belief-grounded, contextually
responsive defenses instead of verbatim repetition.

Two-loss training:
  L_gold:    NTP(gold_response | challenge + M) must be low
             (M must make the model produce the gold-quality response)
  L_no_repeat: NTP(gold_response | M) < NTP(repetition | M)
               (M must prefer gold engagement over repetition)

Uses gold responses from Claude Sonnet 4.6.
Warm-starts from v21.4 Q-mod. Trains m_read_head only.

Usage:
    PYTHONUNBUFFERED=1 python scripts/train_v23_sycophancy.py
"""

import json, os, sys, random, time
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import torch
import torch.nn.functional as F
from transformers import AutoModelForCausalLM, AutoTokenizer
from qkvm.model_hybrid import get_text_config
from qkvm.belief_tree_memory import BeliefTreeMemory, build_topic_tree, get_pro_con_node_ids
from qkvm.phi_node_writer import PhiNodeWriter
from qkvm.mstate_read_head import MStateReadHead

random.seed(42)
torch.manual_seed(42)
CHECKPOINT = "checkpoints/v21_4/v21_4_epoch24_v21_4.pt"


def main():
    print("=" * 60)
    print("v23 SYCOPHANCY TRAINING (gold engagement > repetition)")
    print("=" * 60)

    # Load golds
    with open("results/sycophancy_golds.json") as f:
        golds = json.load(f)
    print(f"  Gold responses: {len(golds)}")

    tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen3.5-4B-Base", trust_remote_code=True)
    if tokenizer.pad_token is None: tokenizer.pad_token = tokenizer.eos_token
    model = AutoModelForCausalLM.from_pretrained(
        "Qwen/Qwen3.5-4B-Base", dtype=torch.bfloat16, device_map="auto", trust_remote_code=True)
    model.eval()
    for p in model.parameters(): p.requires_grad = False
    device = next(model.parameters()).device

    cfg_m = get_text_config(model.config)
    d_model = cfg_m.hidden_size
    patched_layers = list(range(0, cfg_m.num_hidden_layers, 3))

    ck = torch.load(CHECKPOINT, map_location="cpu", weights_only=False)
    cfg = ck["config"]; d_node = cfg["d_node"]

    pw = PhiNodeWriter(d_model=d_model, d_node=d_node).to(device)
    pw.load_state_dict(ck["phi_writer"]); pw.eval()
    for p in pw.parameters(): p.requires_grad = False

    btm_t = BeliefTreeMemory(d_node=d_node, d_edge=64, n_message_passes=2)
    btm_t.init_from_tree(build_topic_tree({"probe": "init",
        "experiences_A": ["a"], "experiences_B": ["b"]}), d_model=d_model, device=device)
    btm_t = btm_t.to(device); btm_t.load_state_dict(ck["btm_template"])
    for p in btm_t.parameters(): p.requires_grad = False

    # M-read head: trainable
    mr = MStateReadHead(d_node=d_node, d_model=d_model, rank=cfg["rank"],
                         n_layers=len(patched_layers)).to(device)
    mr.load_state_dict(ck["m_read_head"])
    trainable = sum(p.numel() for p in mr.parameters())
    print(f"  Trainable: {trainable/1e6:.1f}M (m_read_head)")

    optimizer = torch.optim.AdamW(mr.parameters(), lr=3e-5, weight_decay=0.01)
    os.makedirs("checkpoints/v23_sycophancy", exist_ok=True)

    # Load topic data
    from scripts.train_amplifier_v6_ppl import HELD_OUT_TOPICS
    topics_by_id = {t["id"]: t for t in HELD_OUT_TOPICS}

    def encode_text(text):
        enc = tokenizer(text[:300], return_tensors="pt", truncation=True, max_length=128)
        with torch.no_grad():
            out = model(input_ids=enc["input_ids"].to(device), output_hidden_states=True)
        return out.hidden_states[-1].mean(1).float().squeeze(0)

    def get_q_mod(topic, side="pro"):
        tree = build_topic_tree(topic)
        pi, ci = get_pro_con_node_ids(tree, n_pro=len(topic["experiences_A"]))
        btm = BeliefTreeMemory(d_node=d_node, d_edge=64, n_message_passes=2)
        btm.edge_embedding = btm_t.edge_embedding; btm.message_fn = btm_t.message_fn
        btm.update_fn = btm_t.update_fn; btm.node_init_proj = btm_t.node_init_proj
        for nid, nd in tree.nodes.items():
            h = encode_text(nd.statement)
            btm._embeddings[nid] = btm.node_init_proj(h.unsqueeze(0)).squeeze(0).detach()
        btm.propagate(tree)
        exp = topic["experiences_A"] if side == "pro" else topic["experiences_B"]
        eid = (pi if side == "pro" else ci)[1:]
        for e, nid in zip(exp, eid):
            h = encode_text(e)
            with torch.no_grad(): delta = pw(h, btm.get_embedding(nid))
            btm.set_embedding(nid, (0.95 * btm.get_embedding(nid) + 0.1 * delta).detach())
        btm.propagate(tree)
        persp = pi if side == "pro" else ci
        for pid in persp[1:]: tree.nodes[pid].credence = 0.80
        es, cs = btm.get_perspective_embeddings(persp, tree)
        ml = mr(es, cs)  # LIVE graph
        return ml

    def install_hooks(q_layers):
        handles = []
        for li, ln in enumerate(patched_layers):
            MA, MB, s = q_layers[li]
            def mk(a, b, s_):
                def h(mod, args, kwargs=None):
                    x = args[0] if args else kwargs.get("hidden_states")
                    if x is None: return args, kwargs
                    xm = x + s_ * torch.matmul(torch.matmul(x, a.to(x.device, x.dtype)), b.to(x.device, x.dtype).T)
                    if args: return (xm,) + args[1:], kwargs
                    kw = dict(kwargs) if kwargs else {}; kw["hidden_states"] = xm; return args, kw
                return h
            handles.append(model.model.layers[ln].register_forward_pre_hook(mk(MA, MB, s), with_kwargs=True))
        return handles

    def statement_ntp(prompt, statement):
        full = prompt + statement
        ids = tokenizer(full, return_tensors="pt", max_length=1536, truncation=True).input_ids.to(device)
        p_len = tokenizer(prompt, return_tensors="pt", max_length=1536, truncation=True).input_ids.shape[1]
        tgt = ids.clone(); tgt[0, :p_len] = -100
        logits = model(input_ids=ids).logits
        sl = logits[:, :-1, :].contiguous()
        tl = tgt[:, 1:].contiguous()
        return F.cross_entropy(sl.view(-1, sl.size(-1)), tl.view(-1), ignore_index=-100)

    # Build belief XMLs per topic
    def build_xml(topic, side="pro"):
        side_key = "A" if side == "pro" else "B"
        stance = topic.get(f"stance_{side_key}", topic["probe"])
        reasonings = topic.get(f"reasoning_{side_key}", [])
        experiences = topic.get(f"experiences_{side_key}", [])
        xml = '<beliefs>\n  <claim conviction="strong">\n'
        xml += f"    {stance}\n"
        for i, r in enumerate(reasonings[:3]):
            conv = "strong" if i == 0 else "moderate"
            xml += f'    <argument conviction="{conv}" supports="claim">\n      {r}\n'
            if i < len(experiences):
                xml += f'      <evidence conviction="{conv}" supports="argument">\n        {experiences[i]}\n      </evidence>\n'
            xml += "    </argument>\n"
        xml += "  </claim>\n</beliefs>"
        return xml

    sys_msg = "You hold strong convictions. Defend your position when challenged, referencing your evidence."
    margin_gold = 0.3
    lambda_no_repeat = 1.0

    print(f"  margin_gold={margin_gold}, lambda_no_repeat={lambda_no_repeat}")
    print(f"\n{'='*60}\nTRAINING\n{'='*60}\n")

    history = []
    for epoch in range(50):
        t0 = time.time()
        epoch_gold_loss = 0.0
        epoch_repeat_loss = 0.0
        wins = 0
        total = 0

        random.shuffle(golds)

        for gold in golds:
            topic = topics_by_id.get(gold["topic"])
            if topic is None:
                continue

            optimizer.zero_grad()

            xml = build_xml(topic, gold["side"])
            q_layers = get_q_mod(topic, gold["side"])

            # Build challenge prompt (beliefs + initial + challenge)
            challenge_prompt = (
                f"{xml}\n\n<|im_start|>system\n{sys_msg}<|im_end|>\n"
                f"<|im_start|>user\n{topic['probe']}<|im_end|>\n"
                f"<|im_start|>assistant\n{gold['initial_response'][:200]}<|im_end|>\n"
                f"<|im_start|>user\n{gold['challenge']}<|im_end|>\n"
                f"<|im_start|>assistant\n"
            )

            # L_gold: M + challenge → gold response should have low NTP
            hooks = install_hooks(q_layers)
            ntp_gold = statement_ntp(challenge_prompt, gold["gold_response"])
            for h in hooks: h.remove()

            with torch.no_grad():
                ntp_gold_bare = statement_ntp(challenge_prompt, gold["gold_response"])

            L_gold = F.relu(ntp_gold - ntp_gold_bare.detach() + margin_gold)

            # L_no_repeat: gold response should score better than repetition
            repetition = gold["initial_response"][:200]
            hooks = install_hooks(q_layers)
            ntp_repeat = statement_ntp(challenge_prompt, repetition)
            for h in hooks: h.remove()

            # DPO-style: prefer gold over repetition
            L_repeat = F.relu(ntp_gold - ntp_repeat.detach() + 0.1)

            L = L_gold + lambda_no_repeat * L_repeat
            L.backward()

            epoch_gold_loss += L_gold.item()
            epoch_repeat_loss += L_repeat.item()
            if ntp_gold.item() < ntp_gold_bare.item():
                wins += 1
            total += 1

        torch.nn.utils.clip_grad_norm_(mr.parameters(), 1.0)
        optimizer.step()

        elapsed = time.time() - t0
        row = {"epoch": epoch, "time": elapsed,
               "L_gold": epoch_gold_loss / max(total, 1),
               "L_repeat": epoch_repeat_loss / max(total, 1),
               "wins": f"{wins}/{total}"}
        history.append(row)

        if epoch % 5 == 0:
            print(f"E{epoch:03d} [{elapsed:.0f}s] gold={row['L_gold']:.4f} "
                  f"repeat={row['L_repeat']:.4f} wins={row['wins']}")
            sys.stdout.flush()

        if (epoch + 1) % 10 == 0:
            path = f"checkpoints/v23_sycophancy/v23_syco_epoch{epoch}.pt"
            torch.save({"epoch": epoch, "m_read_head": mr.state_dict(),
                        "config": cfg, "history": history}, path)
            print(f"  Saved: {path}")

    print(f"\nDone. Final: {history[-1]}")


if __name__ == "__main__":
    main()
