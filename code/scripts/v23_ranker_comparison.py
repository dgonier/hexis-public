"""
v23 Ranker Comparison: Keyword vs Embedding vs Neural for within-domain curation.

M filters domain (100% precision). These rankers pick the right beliefs
within the filtered set. Tests precision@5 on 6 ALFWorld queries.

Also generates training data for the neural ranker from the tree structure.

Usage:
    python scripts/v23_ranker_comparison.py
"""

import json, os, sys, random
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from qkvm.model_hybrid import get_text_config
from qkvm.belief_rankers import KeywordRanker, EmbeddingRanker, NeuralRanker, train_neural_ranker

random.seed(42)
torch.manual_seed(42)

# Import the same noisy tree from the curation test
from scripts.v23_noisy_curation_test import NOISE_NODES, ALFWORLD_NODES, TEST_QUERIES


def generate_training_data(alfworld_nodes, noise_nodes, n_negatives_per_positive=3):
    """Generate (belief, query, relevant) triples for neural ranker training.

    Positive pairs: ALFWorld belief matched with its relevant task queries.
    Negative pairs: noise belief with ALFWorld query, or wrong ALFWorld belief with query.
    """
    triples = []

    # Generate queries for each task type
    task_queries = {
        "put_kitchen": [
            "Find a saltshaker and put it on the cabinet",
            "Find a mug and put it on the shelf",
            "Find a plate and put it in the drawer",
        ],
        "put_bedroom": [
            "Find a pencil and put it on the shelf",
            "Find a book and put it on the desk",
            "Find an alarm clock and put it on the dresser",
        ],
        "clean": [
            "Clean a knife and put it on the countertop",
            "Clean a soapbar and put it in the cabinet",
            "Clean a cloth and put it on the shelf",
        ],
        "heat": [
            "Heat an apple and put it in the garbagecan",
            "Heat a mug and put it on the shelf",
        ],
        "cool": [
            "Cool a potato and put it in the microwave",
            "Cool a mug and put it in the cabinet",
        ],
        "examine": [
            "Examine the pencil with the desklamp",
            "Examine the book with the desklamp",
        ],
        "put_bathroom": [
            "Find a soapbar and put it on the countertop",
            "Find a towel and put it on the shelf",
        ],
    }

    for i, alf_node in enumerate(alfworld_nodes):
        relevant_tasks = alf_node.get("relevant_tasks", [])

        for task_type in relevant_tasks:
            queries = task_queries.get(task_type, [])
            for q in queries:
                # Positive: this belief IS relevant to this query
                triples.append((alf_node["content"], q, True))

        # Negative: this ALFWorld belief with queries from UNRELATED task types
        all_types = set(task_queries.keys())
        unrelated = all_types - set(relevant_tasks)
        for task_type in list(unrelated)[:2]:
            queries = task_queries.get(task_type, [])
            for q in queries[:1]:
                triples.append((alf_node["content"], q, False))

    # Negative: noise beliefs with ALFWorld queries
    all_queries = [q for qs in task_queries.values() for q in qs]
    for noise_node in noise_nodes[:30]:  # subset for speed
        for q in random.sample(all_queries, min(2, len(all_queries))):
            triples.append((noise_node["content"], q, False))

    random.shuffle(triples)
    pos = sum(1 for _, _, r in triples if r)
    neg = sum(1 for _, _, r in triples if not r)
    print(f"  Training data: {len(triples)} triples ({pos} positive, {neg} negative)")
    return triples


def main():
    print("=" * 60)
    print("RANKER COMPARISON: Keyword vs Embedding vs Neural")
    print("=" * 60)

    tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen3.5-4B-Base", trust_remote_code=True)
    if tokenizer.pad_token is None: tokenizer.pad_token = tokenizer.eos_token
    model = AutoModelForCausalLM.from_pretrained(
        "Qwen/Qwen3.5-4B-Base", dtype=torch.bfloat16, device_map="auto", trust_remote_code=True)
    model.eval()
    for p in model.parameters(): p.requires_grad = False
    device = next(model.parameters()).device
    d_model = get_text_config(model.config).hidden_size

    # Build rankers
    kw_ranker = KeywordRanker()
    emb_ranker = EmbeddingRanker(model, tokenizer, device)
    neural_ranker = NeuralRanker(d_model=d_model, hidden=128).to(device)

    # Generate training data and train neural ranker
    print("\nTraining neural ranker...")
    train_data = generate_training_data(ALFWORLD_NODES, NOISE_NODES)
    history = train_neural_ranker(neural_ranker, model, tokenizer, train_data,
                                   device=device, epochs=30, lr=1e-3)
    print(f"  Final: loss={history[-1]['loss']:.4f} acc={history[-1]['accuracy']:.2f}")

    # Save neural ranker
    os.makedirs("checkpoints/v23_ranker", exist_ok=True)
    torch.save({"state_dict": neural_ranker.state_dict(), "history": history},
               "checkpoints/v23_ranker/neural_ranker.pt")

    # Pre-compute embeddings for neural ranker
    def get_emb(text):
        enc = tokenizer(text[:200], return_tensors="pt", truncation=True, max_length=64).to(device)
        with torch.no_grad():
            out = model(input_ids=enc["input_ids"], output_hidden_states=True)
        return out.hidden_states[-1].mean(1).squeeze(0).float()

    # Build full node list (ALFWorld only — M already filtered out noise)
    # Simulate M's first stage: only ALFWorld nodes pass
    filtered_nodes = ALFWORLD_NODES  # M would give us these 15

    print(f"\n{'='*60}")
    print("WITHIN-DOMAIN RANKING (M already filtered to ALFWorld)")
    print(f"  Nodes to rank: {len(filtered_nodes)}")
    print(f"{'='*60}")

    K = 5
    results = {r: {"precision": [], "details": []} for r in ["keyword", "embedding", "neural"]}

    for qi, query_info in enumerate(TEST_QUERIES):
        query = query_info["query"]
        relevant_indices = set(query_info["relevant_alfworld"])

        print(f"\n  Query {qi+1}: {query[:50]}...")
        print(f"  Ground truth relevant: {sorted(relevant_indices)}")

        for ranker_name in ["keyword", "embedding", "neural"]:
            scores = []
            for i, node in enumerate(filtered_nodes):
                if ranker_name == "keyword":
                    s = kw_ranker.score(node["content"], query)
                elif ranker_name == "embedding":
                    s = emb_ranker.score(node["content"], query)
                elif ranker_name == "neural":
                    h_b = get_emb(node["content"])
                    h_q = get_emb(query)
                    s = neural_ranker.score(h_b, h_q)
                scores.append((i, s))

            scores.sort(key=lambda x: x[1], reverse=True)
            top_k_indices = set(idx for idx, _ in scores[:K])
            precision = len(top_k_indices & relevant_indices) / K

            results[ranker_name]["precision"].append(precision)
            top_k_contents = [(idx, scores[rank][1], "★" if idx in relevant_indices else " ")
                              for rank, (idx, _) in enumerate(scores[:K])]

            print(f"    {ranker_name:10s}: p@{K}={precision:.2f} | top-{K}: {[f'{idx}{m}' for idx, _, m in top_k_contents]}")

    # Summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    print(f"\n{'Ranker':<12s}  {'Mean P@5':>8s}  {'Min':>5s}  {'Max':>5s}")
    print("-" * 35)
    for name in ["keyword", "embedding", "neural"]:
        precs = results[name]["precision"]
        mean_p = sum(precs) / len(precs)
        print(f"{name:<12s}  {mean_p:>8.2f}  {min(precs):>5.2f}  {max(precs):>5.2f}")

    # Save
    with open("results/v23_ranker_comparison.json", "w") as f:
        json.dump(results, f, indent=2, default=str)
    print(f"\n  Saved to results/v23_ranker_comparison.json")


if __name__ == "__main__":
    main()
