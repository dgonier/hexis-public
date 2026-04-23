"""
v23 Compiled M Experiment: Can M compile beliefs into useful Q+V modulation?

Conditions:
  A: bare (no beliefs, no M)
  B: beliefs in prompt, no M
  D: beliefs in prompt + M (Q-only, current best)
  C1: compiled M (Q+V), no beliefs in prompt
  C2: compiled M (Q-only, no V), no beliefs in prompt
  C3: compiled M (Q+V) + beliefs in prompt (hybrid)

Key diagnostic: does C1 maintain correct stance without beliefs in context?
If yes → compiled M carries content through V-modulation.
If no → compiled M carries disposition only (V-mod untrained, just random).

Also tests with a NOVEL FACT not in model's training data to check
whether V-modulation can inject genuinely new content.

Usage:
    PYTHONUNBUFFERED=1 python scripts/v23_compiled_m.py
"""

import json, os, sys, random
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from hexis.model_hybrid import get_text_config
from hexis.belief_tree_memory import BeliefTreeMemory, build_topic_tree, get_pro_con_node_ids
from hexis.phi_node_writer import PhiNodeWriter
from hexis.mstate_read_head import MStateReadHead
from hexis.belief_compiler import BeliefCompiler, CompiledMState
from hexis.belief_prompt import load_classifications
from scripts.train_amplifier_v6_ppl import HELD_OUT_TOPICS

random.seed(42)
CHECKPOINT = "checkpoints/v21_4/v21_4_epoch24_v21_4.pt"


def build_conviction_xml(topic, side, classifications=None):
    if classifications is None: classifications = {}
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


def main():
    print("=" * 70)
    print("v23 COMPILED M EXPERIMENT")
    print("=" * 70)

    tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen3.5-4B-Base", trust_remote_code=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    base_model = AutoModelForCausalLM.from_pretrained(
        "Qwen/Qwen3.5-4B-Base", dtype=torch.bfloat16, device_map="auto",
        trust_remote_code=True)
    base_model.eval()
    for p in base_model.parameters():
        p.requires_grad = False
    device = next(base_model.parameters()).device

    cfg_m = get_text_config(base_model.config)
    d_model = cfg_m.hidden_size
    n_layers = cfg_m.num_hidden_layers
    patched_layers = list(range(0, n_layers, 3))

    ck = torch.load(CHECKPOINT, map_location="cpu", weights_only=False)
    cfg = ck["config"]
    d_node = cfg["d_node"]

    pw = PhiNodeWriter(d_model=d_model, d_node=d_node).to(device)
    pw.load_state_dict(ck["phi_writer"]); pw.eval()
    mr = MStateReadHead(d_node=d_node, d_model=d_model, rank=cfg["rank"],
                         n_layers=len(patched_layers)).to(device)
    mr.load_state_dict(ck["m_read_head"]); mr.eval()
    btm_t = BeliefTreeMemory(d_node=d_node, d_edge=64, n_message_passes=2)
    btm_t.init_from_tree(build_topic_tree({"probe": "init",
        "experiences_A": ["a"], "experiences_B": ["b"]}), d_model=d_model, device=device)
    btm_t = btm_t.to(device)
    btm_t.load_state_dict(ck["btm_template"])

    classifications = load_classifications()
    print(f"  Loaded v21.4 epoch {ck['epoch']}")

    # Create compiler
    compiler = BeliefCompiler(base_model, tokenizer, pw, mr, btm_t,
                               patched_layers, d_node=d_node, rank=cfg["rank"])

    def install_q_only_hooks(m_layers):
        handles = []
        for l_idx, layer_num in enumerate(patched_layers):
            M_A, M_B, mod_scale = m_layers[l_idx]
            def make_hook(ma, mb, s):
                def hook(module, args, kwargs=None):
                    x = args[0] if args else kwargs.get("hidden_states")
                    if x is None: return args, kwargs
                    mod = torch.matmul(x, ma.to(x.device, x.dtype))
                    xm = x + s * torch.matmul(mod, mb.to(x.device, x.dtype).T)
                    if args: return (xm,) + args[1:], kwargs
                    kw = dict(kwargs) if kwargs else {}; kw["hidden_states"] = xm
                    return args, kw
                return hook
            handles.append(base_model.model.layers[layer_num].register_forward_pre_hook(
                make_hook(M_A, M_B, mod_scale), with_kwargs=True))
        return handles

    def generate(prompt, hooks_fn=None, max_new=200):
        hooks = hooks_fn() if hooks_fn else []
        enc = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=3500).to(device)
        with torch.no_grad():
            out = base_model.generate(
                enc["input_ids"], max_new_tokens=max_new, do_sample=False,
                pad_token_id=tokenizer.pad_token_id or tokenizer.eos_token_id)
        for h in hooks: h.remove()
        text = tokenizer.decode(out[0, enc["input_ids"].shape[1]:], skip_special_tokens=True)
        for marker in ["\nuser\n", "\nUser:", "\nassistant\n"]:
            if marker in text: text = text[:text.index(marker)]
        return text.strip()

    def get_m_layers(topic, side="pro"):
        """Get standard M-state layers (Q-only, existing pipeline)."""
        return compiler.compile_from_m_state(topic, side)  # returns CompiledMState

    # === Run experiments ===
    topics = list(HELD_OUT_TOPICS)[:5]
    sys_msg = "You hold strong convictions on this topic based on your experience. Argue your position directly."

    all_results = {}

    for topic in topics:
        print(f"\n{'='*60}")
        print(f"  {topic['probe'][:60]}")
        print(f"{'='*60}")

        xml = build_conviction_xml(topic, "pro", classifications)

        prompt_with_beliefs = (
            f"{xml}\n\n<|im_start|>system\n{sys_msg}<|im_end|>\n"
            f"<|im_start|>user\n{topic['probe']}<|im_end|>\n"
            f"<|im_start|>assistant\n"
        )
        prompt_no_beliefs = (
            f"<|im_start|>system\n{sys_msg}<|im_end|>\n"
            f"<|im_start|>user\n{topic['probe']}<|im_end|>\n"
            f"<|im_start|>assistant\n"
        )

        # Compile M from beliefs
        compiled_qv = compiler.compile_from_m_state(topic, "pro")

        # Q-only compiled (zero out V)
        compiled_q = CompiledMState()
        for layer_num, (M_A, M_B, E_A, E_B, qs, vs) in compiled_qv.layers.items():
            compiled_q.add_layer(layer_num, M_A, M_B,
                                torch.zeros_like(E_A), torch.zeros_like(E_B),
                                q_scale=qs, v_scale=0.0)

        results = {}

        # A: bare
        text_a = generate(prompt_no_beliefs)
        results["A_bare"] = {"text": text_a[:500], "tokens": len(text_a.split())}
        print(f"  A (bare)      [{results['A_bare']['tokens']:>3d}t]: {text_a[:120]}")

        # B: beliefs only
        text_b = generate(prompt_with_beliefs)
        results["B_beliefs"] = {"text": text_b[:500], "tokens": len(text_b.split())}
        print(f"  B (beliefs)   [{results['B_beliefs']['tokens']:>3d}t]: {text_b[:120]}")

        # D: beliefs + M (Q-only, standard)
        text_d = generate(prompt_with_beliefs,
                         hooks_fn=lambda: compiler.install_compiled_hooks(compiled_q))
        results["D_beliefs_M"] = {"text": text_d[:500], "tokens": len(text_d.split())}
        print(f"  D (bel+Q)     [{results['D_beliefs_M']['tokens']:>3d}t]: {text_d[:120]}")

        # C1: compiled Q+V, NO beliefs in prompt
        text_c1 = generate(prompt_no_beliefs,
                          hooks_fn=lambda: compiler.install_compiled_hooks(compiled_qv))
        results["C1_compiled_QV"] = {"text": text_c1[:500], "tokens": len(text_c1.split())}
        print(f"  C1 (Q+V only) [{results['C1_compiled_QV']['tokens']:>3d}t]: {text_c1[:120]}")

        # C2: compiled Q-only, NO beliefs in prompt
        text_c2 = generate(prompt_no_beliefs,
                          hooks_fn=lambda: compiler.install_compiled_hooks(compiled_q))
        results["C2_compiled_Q"] = {"text": text_c2[:500], "tokens": len(text_c2.split())}
        print(f"  C2 (Q only)   [{results['C2_compiled_Q']['tokens']:>3d}t]: {text_c2[:120]}")

        # C3: compiled Q+V + beliefs in prompt (hybrid)
        text_c3 = generate(prompt_with_beliefs,
                          hooks_fn=lambda: compiler.install_compiled_hooks(compiled_qv))
        results["C3_hybrid"] = {"text": text_c3[:500], "tokens": len(text_c3.split())}
        print(f"  C3 (hybrid)   [{results['C3_hybrid']['tokens']:>3d}t]: {text_c3[:120]}")

        # Check stance for each condition
        for cond, r in results.items():
            t = r["text"][:300].lower()
            pro = any(s in t for s in ["yes", "should", "must", "essential", "support", "need"])
            con = any(s in t for s in ["no,", "should not", "against", "oppose"])
            r["stance"] = "pro" if pro and not con else "con" if con else "neutral"

        all_results[topic["id"]] = results
        sys.stdout.flush()

    # === Summary ===
    print(f"\n\n{'='*70}")
    print("SUMMARY")
    print(f"{'='*70}")

    conditions = ["A_bare", "B_beliefs", "D_beliefs_M",
                   "C1_compiled_QV", "C2_compiled_Q", "C3_hybrid"]

    print(f"\n{'Condition':<16s}  {'Avg Tok':>8s}  {'Pro Stance':>11s}  {'Confident':>10s}")
    print("-" * 50)
    for cond in conditions:
        toks, pro_count, total = [], 0, 0
        for tid, results in all_results.items():
            if cond in results:
                toks.append(results[cond]["tokens"])
                if results[cond]["stance"] == "pro": pro_count += 1
                total += 1
        if toks:
            print(f"{cond:<16s}  {sum(toks)/len(toks):>8.0f}  "
                  f"{pro_count:>5d}/{total:<4d}  "
                  f"{'yes' if sum(toks)/len(toks) < 80 else 'no':>10s}")

    # Key diagnostic
    print(f"\n  KEY: Does compiled M (C1, no beliefs) maintain pro stance?")
    c1_pro = sum(1 for r in all_results.values() if r.get("C1_compiled_QV", {}).get("stance") == "pro")
    c2_pro = sum(1 for r in all_results.values() if r.get("C2_compiled_Q", {}).get("stance") == "pro")
    print(f"    C1 (Q+V compiled): {c1_pro}/{len(all_results)} pro stance")
    print(f"    C2 (Q-only compiled): {c2_pro}/{len(all_results)} pro stance")
    print(f"    If C1 > C2, V-modulation carries content!")
    print(f"    If C1 == C2 == low, compiled M can't carry content alone.")

    os.makedirs("results", exist_ok=True)
    with open("results/v23_compiled_m.json", "w") as f:
        json.dump(all_results, f, indent=2)
    print(f"\n  Saved to results/v23_compiled_m.json")


if __name__ == "__main__":
    main()
