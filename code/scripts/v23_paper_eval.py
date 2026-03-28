"""
v23 Paper Evaluation: Full A/B/D/C/F comparison + ablations.

Tests:
1. Generation quality: 8 topics, all conditions
2. Dilution: F at 0/1000/2000/4000 filler
3. Novel content: made-up statistics
4. Curation ablation: M-curated vs conviction-sorted vs random

Usage:
    PYTHONUNBUFFERED=1 python scripts/v23_paper_eval.py
"""

import json, os, sys, random, time
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import torch
import torch.nn.functional as F_nn
from transformers import AutoModelForCausalLM, AutoTokenizer
from qkvm.model_hybrid import get_text_config
from qkvm.belief_tree_memory import BeliefTreeMemory, build_topic_tree, get_pro_con_node_ids
from qkvm.phi_node_writer import PhiNodeWriter
from qkvm.mstate_read_head import MStateReadHead
from qkvm.compiled_belief_training import VModulationProjector, pad_or_truncate_beliefs, BELIEF_WINDOW, build_conviction_xml
from qkvm.argument_curator import ArgumentCurator
from scripts.train_amplifier_v6_ppl import HELD_OUT_TOPICS
from qkvm.data_200_topics import HELD_OUT_200

random.seed(42)
CHECKPOINT = "checkpoints/v21_4/v21_4_epoch24_v21_4.pt"
V_CHECKPOINT = "checkpoints/v23_compiled_v2/v23_compiled_v2_epoch24.pt"
SLOT_BUDGET = 120  # increased from 80


def main():
    print("=" * 70)
    print("v23 PAPER EVALUATION")
    print("=" * 70)

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
    pw = PhiNodeWriter(d_model=d_model, d_node=d_node).to(device); pw.load_state_dict(ck["phi_writer"]); pw.eval()
    mr = MStateReadHead(d_node=d_node, d_model=d_model, rank=cfg["rank"], n_layers=len(patched_layers)).to(device)
    mr.load_state_dict(ck["m_read_head"]); mr.eval()
    btm_t = BeliefTreeMemory(d_node=d_node, d_edge=64, n_message_passes=2)
    btm_t.init_from_tree(build_topic_tree({"probe":"init","experiences_A":["a"],"experiences_B":["b"]}), d_model=d_model, device=device)
    btm_t = btm_t.to(device); btm_t.load_state_dict(ck["btm_template"])

    v_ck = torch.load(V_CHECKPOINT, map_location="cpu", weights_only=False)
    v_proj = VModulationProjector(d_model=d_model, rank=cfg["rank"], n_layers=len(patched_layers)).to(device)
    v_proj.load_state_dict(v_ck["v_proj"]); v_proj.eval()

    print(f"  Loaded v21.4 + v23 V-mod, slot_budget={SLOT_BUDGET}")

    # Helpers
    def encode_text(text):
        enc = tokenizer(text[:300], return_tensors="pt", truncation=True, max_length=128)
        with torch.no_grad(): out = model(input_ids=enc["input_ids"].to(device), output_hidden_states=True)
        return out.hidden_states[-1].mean(1).float().squeeze(0)

    def get_q_mod(topic, side):
        tree = build_topic_tree(topic)
        pi, ci = get_pro_con_node_ids(tree, n_pro=len(topic["experiences_A"]))
        btm = BeliefTreeMemory(d_node=d_node, d_edge=64, n_message_passes=2)
        btm.edge_embedding=btm_t.edge_embedding; btm.message_fn=btm_t.message_fn
        btm.update_fn=btm_t.update_fn; btm.node_init_proj=btm_t.node_init_proj
        for nid, nd in tree.nodes.items():
            h = encode_text(nd.statement); btm._embeddings[nid] = btm.node_init_proj(h.unsqueeze(0)).squeeze(0).detach()
        btm.propagate(tree)
        exp = topic["experiences_A"] if side=="pro" else topic["experiences_B"]
        eid = (pi if side=="pro" else ci)[1:]
        for e, nid in zip(exp, eid):
            h = encode_text(e)
            with torch.no_grad(): d = pw(h, btm.get_embedding(nid))
            btm.set_embedding(nid, (0.95*btm.get_embedding(nid)+0.1*d).detach())
        btm.propagate(tree)
        persp = pi if side=="pro" else ci
        for pid in persp[1:]: tree.nodes[pid].credence = 0.80
        es, cs = btm.get_perspective_embeddings(persp, tree)
        with torch.no_grad(): ml = mr(es, cs)
        return ml

    def compile_v(xml):
        enc_b = tokenizer(xml, return_tensors="pt", truncation=True, max_length=BELIEF_WINDOW).to(device)
        padded, mask = pad_or_truncate_beliefs(enc_b["input_ids"], max_len=BELIEF_WINDOW, pad_id=tokenizer.pad_token_id)
        with torch.no_grad(): out = model(input_ids=padded, output_hidden_states=True)
        hidden = {li: out.hidden_states[ln+1].float() for li, ln in enumerate(patched_layers)}
        with torch.no_grad(): vl = v_proj(hidden, mask)
        return vl

    def install_hooks(q_layers=None, v_layers=None):
        handles = []
        for li, ln in enumerate(patched_layers):
            parts = []
            if q_layers: MA, MB, qs = q_layers[li]; parts.append(("q", MA, MB, qs))
            if v_layers: EA, EB, vs = v_layers[li]; parts.append(("v", EA, EB, vs))
            if not parts: continue
            def mk(ps):
                def h(mod, args, kwargs=None):
                    x = args[0] if args else kwargs.get("hidden_states")
                    if x is None: return args, kwargs
                    dev, dt = x.device, x.dtype; xm = x
                    for kind, a, b, s in ps:
                        p = torch.matmul(torch.matmul(x, a.to(dev,dt)), b.to(dev,dt).T); xm = xm + s * p
                    if args: return (xm,)+args[1:], kwargs
                    kw = dict(kwargs) if kwargs else {}; kw["hidden_states"]=xm; return args, kw
                return h
            handles.append(model.model.layers[ln].register_forward_pre_hook(mk(parts), with_kwargs=True))
        return handles

    def gen(prompt, hooks_fn=None, max_new=150):
        hooks = hooks_fn() if hooks_fn else []
        enc = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=3500).to(device)
        in_toks = enc["input_ids"].shape[1]
        torch.cuda.synchronize(); t0 = time.perf_counter()
        with torch.no_grad():
            out = model.generate(enc["input_ids"], max_new_tokens=max_new, do_sample=False, pad_token_id=tokenizer.eos_token_id)
        torch.cuda.synchronize(); elapsed = time.perf_counter() - t0
        for h in hooks: h.remove()
        text = tokenizer.decode(out[0, enc["input_ids"].shape[1]:], skip_special_tokens=True)
        for m in ["\nuser\n", "\nUser:"]:
            if m in text: text = text[:text.index(m)]
        return text.strip(), elapsed, in_toks

    sys_msg = "You hold strong convictions. Argue your position directly."

    # Use more held-out topics
    topics = list(HELD_OUT_TOPICS)[:5] + list(HELD_OUT_200)[:3]

    # =========================================================
    # TEST 1: Generation quality across conditions
    # =========================================================
    print(f"\n{'='*70}")
    print("TEST 1: GENERATION QUALITY (A/B/D/C/F)")
    print(f"{'='*70}")

    summary = {c: {"pro": 0, "in_toks": [], "out_toks": [], "times": []} for c in "ABDCF"}

    for topic in topics:
        xml = build_conviction_xml(topic, "pro", max_tokens=BELIEF_WINDOW, tokenizer=tokenizer)
        xml_toks = len(tokenizer.encode(xml))
        q_layers = get_q_mod(topic, "pro")
        v_layers = compile_v(xml)

        # M-curated slot
        curator = ArgumentCurator(model, tokenizer, q_layers[0][0], q_layers[0][1], patched_layers, device)
        selected = curator.curate_from_topic(topic, "pro", topic["probe"], token_budget=SLOT_BUDGET)
        slot_xml = curator.build_slot(selected)

        prompt_bare = f"<|im_start|>system\n{sys_msg}<|im_end|>\n<|im_start|>user\n{topic['probe']}<|im_end|>\n<|im_start|>assistant\n"
        prompt_full = f"{xml}\n\n{prompt_bare.replace('<|im_start|>system', '<|im_start|>system')}"
        prompt_slot = f"{slot_xml}\n\n{prompt_bare.replace('<|im_start|>system', '<|im_start|>system')}"

        for cond, prompt, hk in [
            ("A", prompt_bare, None),
            ("B", prompt_full, None),
            ("D", prompt_full, lambda: install_hooks(q_layers=q_layers)),
            ("C", prompt_bare, lambda: install_hooks(q_layers=q_layers, v_layers=v_layers)),
            ("F", prompt_slot, lambda: install_hooks(q_layers=q_layers, v_layers=v_layers)),
        ]:
            text, elapsed, in_t = gen(prompt, hooks_fn=hk)
            out_t = len(text.split())
            t_lower = text[:300].lower()
            is_pro = any(s in t_lower for s in ["yes","should","must","essential","support","need","necessary"])
            is_con = any(s in t_lower for s in ["no,","no.","should not","against","shouldn't"])
            pro = is_pro and not is_con

            summary[cond]["pro"] += int(pro)
            summary[cond]["in_toks"].append(in_t)
            summary[cond]["out_toks"].append(out_t)
            summary[cond]["times"].append(elapsed * 1000)

        print(f"  {topic['id'][:20]:20s} xml={xml_toks:3d}t slot={len(tokenizer.encode(slot_xml)):3d}t | " +
              " ".join(f"{c}={'✓' if summary[c]['pro'] > sum(1 for t2 in topics[:topics.index(topic)] for _ in [0]) else '?'}" for c in "ABDCF"))
        sys.stdout.flush()

    n = len(topics)
    print(f"\n{'Cond':<4s}  {'Pro':>5s}  {'InTok':>6s}  {'OutTok':>7s}  {'Time':>8s}")
    print("-" * 40)
    for c in "ABDCF":
        s = summary[c]
        print(f"{c:<4s}  {s['pro']:>3d}/{n}  {sum(s['in_toks'])/n:>6.0f}  {sum(s['out_toks'])/n:>7.0f}  {sum(s['times'])/n:>7.0f}ms")

    # =========================================================
    # TEST 2: Dilution for F
    # =========================================================
    print(f"\n{'='*70}")
    print("TEST 2: DILUTION (F condition)")
    print(f"{'='*70}")

    filler_unit = "User: How do noise-cancelling headphones work?\nAssistant: They use destructive interference.\n\n"
    test_topics = topics[:4]

    for filler_level in [0, 1000, 2000, 4000]:
        filler = (filler_unit * (filler_level // 50))[:filler_level * 4] if filler_level > 0 else ""
        correct = 0
        for topic in test_topics:
            xml = build_conviction_xml(topic, "pro", max_tokens=BELIEF_WINDOW, tokenizer=tokenizer)
            q_layers = get_q_mod(topic, "pro")
            v_layers = compile_v(xml)
            curator = ArgumentCurator(model, tokenizer, q_layers[0][0], q_layers[0][1], patched_layers, device)
            selected = curator.curate_from_topic(topic, "pro", topic["probe"], token_budget=SLOT_BUDGET)
            slot_xml = curator.build_slot(selected)

            prompt = (f"{slot_xml}\n\n<|im_start|>system\n{sys_msg}<|im_end|>\n"
                      f"<|im_start|>user\n{filler}{topic['probe']}<|im_end|>\n<|im_start|>assistant\n")
            text, _, _ = gen(prompt, hooks_fn=lambda: install_hooks(q_layers=q_layers, v_layers=v_layers))
            t = text[:300].lower()
            if any(s in t for s in ["yes","should","must","support","need"]): correct += 1

        print(f"  Filler {filler_level:5d}: {correct}/{len(test_topics)}")

    # =========================================================
    # TEST 3: Novel content
    # =========================================================
    print(f"\n{'='*70}")
    print("TEST 3: NOVEL CONTENT (F should cite specifics from slot)")
    print(f"{'='*70}")

    novel_topic = {
        "id": "four_day_week", "probe": "Should companies adopt 4-day work weeks?",
        "stance_A": "Yes, 4-day work weeks dramatically improve both productivity and retention",
        "experiences_A": [
            "Our 2024 study at Nextera Labs showed 47.3% improvement in employee retention with 4-day weeks. N=3,400 across 12 offices.",
            "Productivity per hour increased 18.7% in the 4-day group, fully offsetting the lost day.",
            "Healthcare costs dropped 23% in the pilot group compared to control.",
        ],
        "reasoning_A": [
            "Reduced hours increase per-hour productivity through decreased burnout and improved focus",
            "The economic case is clear: retention savings plus healthcare savings exceed the cost of the lost day",
            "Employee satisfaction and recruitment advantages create a competitive moat",
        ],
        "stance_B": "No", "experiences_B": ["No data"], "reasoning_B": [],
    }

    xml = build_conviction_xml(novel_topic, "pro", max_tokens=BELIEF_WINDOW, tokenizer=tokenizer)
    q_layers = get_q_mod(novel_topic, "pro")
    v_layers = compile_v(xml)
    curator = ArgumentCurator(model, tokenizer, q_layers[0][0], q_layers[0][1], patched_layers, device)
    selected = curator.curate_from_topic(novel_topic, "pro", novel_topic["probe"], token_budget=SLOT_BUDGET)
    slot_xml = curator.build_slot(selected)

    # B: full beliefs in prompt
    prompt_b = f"{xml}\n\n<|im_start|>system\n{sys_msg}<|im_end|>\n<|im_start|>user\n{novel_topic['probe']}<|im_end|>\n<|im_start|>assistant\n"
    text_b, _, _ = gen(prompt_b)

    # F: compiled + curated slot
    prompt_f = f"{slot_xml}\n\n<|im_start|>system\n{sys_msg}<|im_end|>\n<|im_start|>user\n{novel_topic['probe']}<|im_end|>\n<|im_start|>assistant\n"
    text_f, _, _ = gen(prompt_f, hooks_fn=lambda: install_hooks(q_layers=q_layers, v_layers=v_layers))

    # C: compiled only
    prompt_c = f"<|im_start|>system\n{sys_msg}<|im_end|>\n<|im_start|>user\n{novel_topic['probe']}<|im_end|>\n<|im_start|>assistant\n"
    text_c, _, _ = gen(prompt_c, hooks_fn=lambda: install_hooks(q_layers=q_layers, v_layers=v_layers))

    print(f"  B (full beliefs): {text_b[:200]}")
    print(f"  F (comp+slot):    {text_f[:200]}")
    print(f"  C (compiled only):{text_c[:200]}")
    print(f"\n  Novel fact check:")
    for label, text in [("B", text_b), ("F", text_f), ("C", text_c)]:
        has_47 = "47" in text
        has_nextera = "nextera" in text.lower()
        has_18 = "18" in text[:200]
        has_23 = "23%" in text
        print(f"    {label}: 47.3%={has_47} Nextera={has_nextera} 18.7%={has_18} 23%={has_23}")

    # =========================================================
    # TEST 4: Curation ablation
    # =========================================================
    print(f"\n{'='*70}")
    print("TEST 4: CURATION ABLATION (M-curated vs conviction vs random)")
    print(f"{'='*70}")

    ablation_topics = topics[:4]

    for method in ["m_curated", "conviction", "random", "first_k"]:
        correct = 0
        total_out = 0

        for topic in ablation_topics:
            xml = build_conviction_xml(topic, "pro", max_tokens=BELIEF_WINDOW, tokenizer=tokenizer)
            q_layers = get_q_mod(topic, "pro")
            v_layers = compile_v(xml)

            # Build arguments list
            side_key = "A"
            reasonings = topic.get(f"reasoning_{side_key}", [])
            experiences = topic.get(f"experiences_{side_key}", [])
            stance = topic.get(f"stance_{side_key}", "")
            args = []
            if stance: args.append({"text": stance[:150], "type": "claim", "evidence": [], "conviction": "strong"})
            for i, r in enumerate(reasonings):
                args.append({"text": r, "type": "empirical", "evidence": [experiences[i]] if i < len(experiences) else [], "conviction": "strong" if i == 0 else "moderate"})

            if method == "m_curated":
                curator = ArgumentCurator(model, tokenizer, q_layers[0][0], q_layers[0][1], patched_layers, device)
                selected = curator.curate(args, topic["probe"], token_budget=SLOT_BUDGET)
            elif method == "conviction":
                # Sort by conviction (strong first)
                conv_order = {"strong": 0, "moderate": 1, "agnostic": 2, "weak": 3}
                selected = sorted(args, key=lambda a: conv_order.get(a.get("conviction", "moderate"), 2))
            elif method == "random":
                selected = random.sample(args, min(len(args), 3))
            elif method == "first_k":
                selected = args[:3]

            slot_xml = "<arguments>\n"
            toks_used = 15
            for arg in selected:
                entry = f'  <argument conviction="{arg.get("conviction","moderate")}">\n    {arg["text"][:150]}\n'
                for ev in arg.get("evidence", []):
                    entry += f"    <evidence>{ev[:100]}</evidence>\n"
                entry += "  </argument>\n"
                if toks_used + len(tokenizer.encode(entry)) > SLOT_BUDGET: break
                slot_xml += entry
                toks_used += len(tokenizer.encode(entry))
            slot_xml += "</arguments>"

            prompt = (f"{slot_xml}\n\n<|im_start|>system\n{sys_msg}<|im_end|>\n"
                      f"<|im_start|>user\n{topic['probe']}<|im_end|>\n<|im_start|>assistant\n")
            text, _, _ = gen(prompt, hooks_fn=lambda: install_hooks(q_layers=q_layers, v_layers=v_layers))
            t = text[:300].lower()
            if any(s in t for s in ["yes","should","must","support","need"]): correct += 1
            total_out += len(text.split())

        avg_out = total_out / len(ablation_topics)
        print(f"  {method:<14s}: pro={correct}/{len(ablation_topics)} avg_out={avg_out:.0f}t")

    print(f"\n  Saved to results/v23_paper_eval.json")
    os.makedirs("results", exist_ok=True)
    with open("results/v23_paper_eval.json", "w") as f:
        json.dump({"summary": {c: {k: v if not isinstance(v, list) else sum(v)/len(v) for k, v in s.items()} for c, s in summary.items()}}, f, indent=2)


if __name__ == "__main__":
    main()
