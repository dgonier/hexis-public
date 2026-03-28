"""
v23 Strategy V-mod Training: Retrain V-modulation on strategy XML.

Uses the universal <memory><node type="strategy"> schema with
ALFWorld-style content. Warm-starts from v2 checkpoint (debate-trained)
and fine-tunes to also carry strategy disposition + content.

The training data: hand-crafted strategy trees covering ALFWorld task types.
Each tree has 3-6 strategies with support observations.

Loss: compiled Q+V (no strategies in prompt) must beat bare baseline
on generating task-appropriate first actions.

Usage:
    PYTHONUNBUFFERED=1 python scripts/train_v23_strategy.py
"""

import argparse, json, os, sys, random, time
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import torch
import torch.nn.functional as F
from transformers import AutoModelForCausalLM, AutoTokenizer
from qkvm.model_hybrid import get_text_config
from qkvm.belief_tree_memory import BeliefTreeMemory, build_topic_tree, get_pro_con_node_ids
from qkvm.phi_node_writer import PhiNodeWriter
from qkvm.mstate_read_head import MStateReadHead
from qkvm.compiled_belief_training import VModulationProjector, pad_or_truncate_beliefs, BELIEF_WINDOW
from qkvm.universal_schema import MemoryTree, Support

random.seed(42)
torch.manual_seed(42)

CHECKPOINT = "checkpoints/v21_4/v21_4_epoch24_v21_4.pt"
V_CHECKPOINT = "checkpoints/v23_compiled_v2/v23_compiled_v2_epoch24.pt"

# ====================================================================
# Strategy training data: ALFWorld-style task scenarios
# ====================================================================
STRATEGY_SCENARIOS = [
    {
        "id": "pick_kitchen",
        "probe": "You need to find and pick up an item in the kitchen.",
        "stance": "go to countertop 1",
        "strategies": [
            {"content": "Survey the room before opening containers. Check visible surfaces first.",
             "conviction": "strong", "domain": "search",
             "supports": [{"type": "success", "content": "Found apple on countertop after surveying"}]},
            {"content": "Kitchen items like food and utensils are usually on countertops or in drawers.",
             "conviction": "strong", "domain": "kitchen",
             "supports": [{"type": "success", "content": "Found knife on countertop 1"},
                          {"type": "success", "content": "Found bread on countertop 2"}]},
            {"content": "If a container is closed, open it before looking inside.",
             "conviction": "moderate", "domain": "search",
             "supports": [{"type": "success", "content": "Found bowl inside closed cabinet after opening"}]},
        ],
    },
    {
        "id": "pick_bedroom",
        "probe": "You need to find and pick up an item in the bedroom.",
        "stance": "go to desk 1",
        "strategies": [
            {"content": "In bedrooms, check the desk and shelves first for small items.",
             "conviction": "strong", "domain": "bedroom",
             "supports": [{"type": "success", "content": "Found pencil on desk 1"},
                          {"type": "success", "content": "Found book on shelf 2"}]},
            {"content": "Look on dressers and nightstands for personal items.",
             "conviction": "moderate", "domain": "bedroom",
             "supports": [{"type": "success", "content": "Found alarm clock on dresser"}]},
        ],
    },
    {
        "id": "pick_bathroom",
        "probe": "You need to find and pick up an item in the bathroom.",
        "stance": "go to countertop 1",
        "strategies": [
            {"content": "Bathroom items like soap and toiletries are on countertops or in cabinets.",
             "conviction": "strong", "domain": "bathroom",
             "supports": [{"type": "success", "content": "Found soapbar on countertop 1"},
                          {"type": "success", "content": "Found towel in cabinet 2"}]},
            {"content": "Check the toilet area and bathtub for cleaning supplies.",
             "conviction": "weak", "domain": "bathroom",
             "supports": [{"type": "failure", "content": "Nothing useful near toilet"}]},
        ],
    },
    {
        "id": "clean_task",
        "probe": "You need to clean an item and put it somewhere.",
        "stance": "go to sinkbasin 1",
        "strategies": [
            {"content": "To clean an item: first find it, take it, go to sinkbasin, use clean action.",
             "conviction": "strong", "domain": "process",
             "supports": [{"type": "success", "content": "Cleaned knife at sinkbasin successfully"},
                          {"type": "success", "content": "Cleaned plate at sinkbasin"}]},
            {"content": "After cleaning, go to the destination and put the item down.",
             "conviction": "strong", "domain": "process",
             "supports": [{"type": "success", "content": "Put clean knife on countertop after cleaning"}]},
        ],
    },
    {
        "id": "heat_task",
        "probe": "You need to heat an item and put it somewhere.",
        "stance": "go to microwave 1",
        "strategies": [
            {"content": "To heat an item: find it, take it, go to microwave, use heat action.",
             "conviction": "strong", "domain": "process",
             "supports": [{"type": "success", "content": "Heated apple in microwave"}]},
            {"content": "Food items that need heating are usually on countertops or in fridge.",
             "conviction": "moderate", "domain": "kitchen",
             "supports": [{"type": "success", "content": "Found egg on countertop for heating task"}]},
        ],
    },
    {
        "id": "cool_task",
        "probe": "You need to cool an item and put it somewhere.",
        "stance": "go to fridge 1",
        "strategies": [
            {"content": "To cool an item: find it, take it, go to fridge, use cool action.",
             "conviction": "strong", "domain": "process",
             "supports": [{"type": "success", "content": "Cooled potato in fridge"}]},
        ],
    },
    {
        "id": "examine_task",
        "probe": "You need to examine an item with a desklamp.",
        "stance": "go to desklamp 1",
        "strategies": [
            {"content": "For examine tasks: find the item first, then bring it to the desklamp.",
             "conviction": "strong", "domain": "process",
             "supports": [{"type": "success", "content": "Examined pencil under desklamp"}]},
            {"content": "Desklamps are usually on desks in bedrooms or offices.",
             "conviction": "moderate", "domain": "bedroom",
             "supports": [{"type": "success", "content": "Found desklamp on desk 1"}]},
        ],
    },
    {
        "id": "put_task",
        "probe": "You need to put an item on a specific location.",
        "stance": "First find the item, then take it to the destination.",
        "strategies": [
            {"content": "For put tasks: 1) find the item by searching locations, 2) take it, 3) go to destination, 4) put it down.",
             "conviction": "strong", "domain": "process",
             "supports": [{"type": "success", "content": "Put saltshaker on shelf following this sequence"}]},
            {"content": "Take items immediately when you see them. Don't examine or wait.",
             "conviction": "strong", "domain": "efficiency",
             "supports": [{"type": "success", "content": "Taking immediately saved 3 steps vs examining first"}]},
        ],
    },
    {
        "id": "navigation",
        "probe": "You need to navigate efficiently between locations.",
        "stance": "go to the most likely location first",
        "strategies": [
            {"content": "Visit locations systematically. Never revisit a location you already checked.",
             "conviction": "strong", "domain": "navigation",
             "supports": [{"type": "success", "content": "Systematic search found item in 3 steps vs random 8 steps"}]},
            {"content": "Start with the most likely location based on item type before trying others.",
             "conviction": "moderate", "domain": "navigation",
             "supports": [{"type": "success", "content": "Going to countertop first for food items saves time"}]},
        ],
    },
    {
        "id": "two_items",
        "probe": "You need to find two items and put them somewhere.",
        "stance": "Find and deliver the first item before searching for the second.",
        "strategies": [
            {"content": "For two-item tasks: find and deliver one item completely before starting on the second.",
             "conviction": "strong", "domain": "process",
             "supports": [{"type": "success", "content": "Completed two-soapbar task by doing one at a time"}]},
            {"content": "Both items of the same type may be in different locations. Check multiple surfaces.",
             "conviction": "moderate", "domain": "search",
             "supports": [{"type": "success", "content": "Found second soapbar on different countertop"}]},
        ],
    },
]


def build_strategy_xml(scenario):
    """Build universal schema XML from a scenario."""
    tree = MemoryTree()
    for s in scenario["strategies"]:
        supports = [Support(**sup) for sup in s.get("supports", [])]
        tree.create_node(
            type="strategy", content=s["content"],
            conviction=s["conviction"], domain=s.get("domain", ""),
            supports=supports,
        )
    return tree.to_xml()


def main():
    print("=" * 60)
    print("v23 STRATEGY V-MOD TRAINING")
    print("=" * 60)

    tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen3.5-4B-Base", trust_remote_code=True)
    if tokenizer.pad_token is None: tokenizer.pad_token = tokenizer.eos_token
    model = AutoModelForCausalLM.from_pretrained(
        "Qwen/Qwen3.5-4B-Base", dtype=torch.bfloat16, device_map="auto", trust_remote_code=True)
    model.eval()
    for p in model.parameters(): p.requires_grad = False
    device = next(model.parameters()).device

    config = get_text_config(model.config)
    d_model = config.hidden_size
    patched_layers = list(range(0, config.num_hidden_layers, 3))

    ck = torch.load(CHECKPOINT, map_location="cpu", weights_only=False)
    cfg = ck["config"]; d_node = cfg["d_node"]
    pw = PhiNodeWriter(d_model=d_model, d_node=d_node).to(device)
    pw.load_state_dict(ck["phi_writer"]); pw.eval()
    for p in pw.parameters(): p.requires_grad = False
    mr = MStateReadHead(d_node=d_node, d_model=d_model, rank=cfg["rank"],
                         n_layers=len(patched_layers)).to(device)
    mr.load_state_dict(ck["m_read_head"]); mr.eval()
    for p in mr.parameters(): p.requires_grad = False
    btm_t = BeliefTreeMemory(d_node=d_node, d_edge=64, n_message_passes=2)
    btm_t.init_from_tree(build_topic_tree({"probe": "init",
        "experiences_A": ["a"], "experiences_B": ["b"]}), d_model=d_model, device=device)
    btm_t = btm_t.to(device); btm_t.load_state_dict(ck["btm_template"])
    for p in btm_t.parameters(): p.requires_grad = False

    # V-mod: warm-start from v2 (debate-trained)
    v_proj = VModulationProjector(d_model=d_model, rank=cfg["rank"],
                                   n_layers=len(patched_layers)).to(device)
    v_ck = torch.load(V_CHECKPOINT, map_location="cpu", weights_only=False)
    v_proj.load_state_dict(v_ck["v_proj"])
    print(f"  Warm-started V-mod from debate checkpoint (epoch {v_ck.get('epoch', '?')})")

    trainable = sum(p.numel() for p in v_proj.parameters())
    print(f"  V-mod trainable: {trainable/1e6:.1f}M")
    print(f"  Strategy scenarios: {len(STRATEGY_SCENARIOS)}")

    optimizer = torch.optim.AdamW(v_proj.parameters(), lr=1e-4, weight_decay=0.01)
    os.makedirs("checkpoints/v23_strategy", exist_ok=True)

    def encode_text(text):
        enc = tokenizer(text[:300], return_tensors="pt", truncation=True, max_length=128)
        with torch.no_grad():
            out = model(input_ids=enc["input_ids"].to(device), output_hidden_states=True)
        return out.hidden_states[-1].mean(1).float().squeeze(0)

    def get_q_mod_from_strategies(strategies):
        """Get Q-mod from strategy texts via phi pipeline."""
        texts = [s["content"] for s in strategies[:6]]
        topic = {"id": "strat", "probe": "task strategy",
                 "experiences_A": texts, "experiences_B": ["none"]}
        tree = build_topic_tree(topic)
        pi, _ = get_pro_con_node_ids(tree, n_pro=len(texts))
        btm = BeliefTreeMemory(d_node=d_node, d_edge=64, n_message_passes=2)
        btm.edge_embedding=btm_t.edge_embedding; btm.message_fn=btm_t.message_fn
        btm.update_fn=btm_t.update_fn; btm.node_init_proj=btm_t.node_init_proj
        for nid, nd in tree.nodes.items():
            h = encode_text(nd.statement)
            btm._embeddings[nid] = btm.node_init_proj(h.unsqueeze(0)).squeeze(0).detach()
        btm.propagate(tree)
        for t, nid in zip(texts, pi[1:]):
            h = encode_text(t)
            with torch.no_grad(): delta = pw(h, btm.get_embedding(nid))
            btm.set_embedding(nid, (0.95*btm.get_embedding(nid)+0.1*delta).detach())
        btm.propagate(tree)
        for pid in pi[1:]: tree.nodes[pid].credence = 0.80
        es, cs = btm.get_perspective_embeddings(pi, tree)
        with torch.no_grad(): ml = mr(es, cs)
        return ml

    def compile_v(xml):
        enc_b = tokenizer(xml, return_tensors="pt", truncation=True, max_length=BELIEF_WINDOW).to(device)
        padded, mask = pad_or_truncate_beliefs(enc_b["input_ids"], max_len=BELIEF_WINDOW, pad_id=tokenizer.pad_token_id)
        with torch.no_grad():
            out = model(input_ids=padded, output_hidden_states=True)
        hidden = {li: out.hidden_states[ln+1].float() for li, ln in enumerate(patched_layers)}
        return v_proj(hidden, mask)

    def install_qv_hooks(q_layers, v_layers):
        handles = []
        for li, ln in enumerate(patched_layers):
            MA, MB, qs = q_layers[li]; EA, EB, vs = v_layers[li]
            def mk(a,b,qs_,ea,eb,vs_):
                def h(mod, args, kwargs=None):
                    x = args[0] if args else kwargs.get("hidden_states")
                    if x is None: return args, kwargs
                    dev,dt = x.device, x.dtype
                    qm = torch.matmul(torch.matmul(x, a.to(dev,dt)), b.to(dev,dt).T)
                    vm = torch.matmul(torch.matmul(x, ea.to(dev,dt)), eb.to(dev,dt).T)
                    xm = x + qs_ * qm + vs_ * vm
                    if args: return (xm,)+args[1:], kwargs
                    kw = dict(kwargs) if kwargs else {}; kw["hidden_states"]=xm; return args, kw
                return h
            handles.append(model.model.layers[ln].register_forward_pre_hook(
                mk(MA,MB,qs,EA,EB,vs), with_kwargs=True))
        return handles

    def statement_ntp(prompt, statement):
        full = prompt + statement
        ids = tokenizer(full, return_tensors="pt", max_length=1024, truncation=True).input_ids.to(device)
        p_len = tokenizer(prompt, return_tensors="pt", max_length=1024, truncation=True).input_ids.shape[1]
        tgt = ids.clone(); tgt[0, :p_len] = -100
        logits = model(input_ids=ids).logits
        sl = logits[:, :-1, :].contiguous(); tl = tgt[:, 1:].contiguous()
        return F.cross_entropy(sl.view(-1, sl.size(-1)), tl.view(-1), ignore_index=-100)

    # Training
    sys_msg = "You are a household task agent. What action should you take first?"
    margin = 1.0
    print(f"  Margin: {margin}, LR: 1e-4")
    print(f"\n{'='*60}\nTRAINING\n{'='*60}\n")

    history = []
    for epoch in range(30):
        t0 = time.time()
        epoch_loss, wins, total = 0.0, 0, 0

        for scenario in STRATEGY_SCENARIOS:
            optimizer.zero_grad()

            xml = build_strategy_xml(scenario)
            q_layers = get_q_mod_from_strategies(scenario["strategies"])
            v_layers = compile_v(xml)

            prompt = (f"<|im_start|>system\n{sys_msg}<|im_end|>\n"
                      f"<|im_start|>user\n{scenario['probe']}<|im_end|>\n"
                      f"<|im_start|>assistant\n")

            # Baseline: bare
            with torch.no_grad():
                ntp_base = statement_ntp(prompt, scenario["stance"])

            # Test: compiled Q+V
            hooks = install_qv_hooks(q_layers, v_layers)
            ntp_compiled = statement_ntp(prompt, scenario["stance"])
            for h in hooks: h.remove()

            L = F.relu(ntp_compiled - ntp_base.detach() + margin)
            L.backward()
            epoch_loss += L.item()
            if ntp_compiled.item() < ntp_base.item(): wins += 1
            total += 1

        torch.nn.utils.clip_grad_norm_(v_proj.parameters(), 1.0)
        optimizer.step()

        row = {"epoch": epoch, "time": time.time() - t0,
               "loss": epoch_loss / max(total, 1), "wins": f"{wins}/{total}"}
        history.append(row)

        if epoch % 5 == 0:
            print(f"E{epoch:03d} [{row['time']:.0f}s] loss={row['loss']:.4f} wins={row['wins']}")
            sys.stdout.flush()

        if (epoch + 1) % 10 == 0:
            path = f"checkpoints/v23_strategy/v23_strategy_epoch{epoch}.pt"
            torch.save({"epoch": epoch, "v_proj": v_proj.state_dict(),
                        "config": {"d_model": d_model, "rank": cfg["rank"],
                                    "n_layers": len(patched_layers)},
                        "history": history}, path)
            print(f"  Saved: {path}")

    print(f"\nDone. Final: {history[-1]}")


if __name__ == "__main__":
    main()
