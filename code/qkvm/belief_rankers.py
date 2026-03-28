"""
Second-stage belief rankers for within-domain curation.

M filters to the right domain (100% precision on ALFWorld vs noise).
These rankers differentiate WITHIN the domain to pick the most
relevant beliefs for a specific query.

Three approaches:
  1. KeywordRanker: TF-IDF style keyword overlap (baseline, brittle)
  2. EmbeddingRanker: cosine similarity of base model embeddings (no training)
  3. NeuralRanker: tiny classifier trained on (belief, query, relevant?) triples
"""

import re
import math
from collections import Counter

import torch
import torch.nn as nn
import torch.nn.functional as F


class KeywordRanker:
    """TF-IDF style keyword overlap between belief and query."""

    def __init__(self):
        self.stopwords = set("the a an is are was were be been being have has had do does did "
                             "will would shall should may might can could to of in for on with "
                             "at by from it this that and or not".split())

    def _tokenize(self, text):
        words = re.findall(r'\b\w+\b', text.lower())
        return [w for w in words if w not in self.stopwords and len(w) > 2]

    def score(self, belief_text, query_text):
        b_words = Counter(self._tokenize(belief_text))
        q_words = Counter(self._tokenize(query_text))
        if not b_words or not q_words:
            return 0.0
        overlap = sum((b_words & q_words).values())
        return overlap / max(sum(q_words.values()), 1)


class EmbeddingRanker:
    """Cosine similarity of pooled hidden states from base model."""

    def __init__(self, model, tokenizer, device="cuda"):
        self.model = model
        self.tokenizer = tokenizer
        self.device = device
        self._cache = {}

    def _embed(self, text):
        key = text[:200]
        if key in self._cache:
            return self._cache[key]
        enc = self.tokenizer(text[:200], return_tensors="pt",
                             truncation=True, max_length=64).to(self.device)
        with torch.no_grad():
            out = self.model(input_ids=enc["input_ids"], output_hidden_states=True)
        emb = out.hidden_states[-1].mean(1).squeeze(0).float()
        emb = F.normalize(emb.unsqueeze(0), dim=-1).squeeze(0)
        self._cache[key] = emb
        return emb

    def score(self, belief_text, query_text):
        b_emb = self._embed(belief_text)
        q_emb = self._embed(query_text)
        return F.cosine_similarity(b_emb.unsqueeze(0), q_emb.unsqueeze(0)).item()


class NeuralRanker(nn.Module):
    """Tiny binary classifier: is this belief relevant to this query?

    Input: belief embedding + query embedding (from base model hidden states)
    Output: relevance probability

    ~500K params. Trains in minutes on synthetic triples.
    """

    def __init__(self, d_model=2560, hidden=128):
        super().__init__()
        self.d_model = d_model
        self.net = nn.Sequential(
            nn.Linear(d_model * 2, hidden),
            nn.SiLU(),
            nn.Linear(hidden, hidden),
            nn.SiLU(),
            nn.Linear(hidden, 1),
        )
        # Init small
        for p in self.parameters():
            if p.dim() >= 2:
                nn.init.normal_(p, std=0.02)

    def forward(self, h_belief, h_query):
        """
        Args:
            h_belief: (d_model,) pooled belief hidden state
            h_query: (d_model,) pooled query hidden state
        Returns:
            relevance probability (scalar)
        """
        combined = torch.cat([h_belief, h_query], dim=-1)
        return torch.sigmoid(self.net(combined)).squeeze(-1)

    def score(self, h_belief, h_query):
        with torch.no_grad():
            return self.forward(h_belief, h_query).item()


def train_neural_ranker(ranker, model, tokenizer, training_data, device="cuda",
                         epochs=30, lr=1e-3):
    """Train the neural ranker on (belief_text, query_text, relevant) triples.

    Args:
        ranker: NeuralRanker instance
        model: base LLM for embeddings
        tokenizer: tokenizer
        training_data: list of (belief_text, query_text, relevant_bool)
        device: cuda device
        epochs: training epochs
        lr: learning rate

    Returns:
        training history
    """
    optimizer = torch.optim.Adam(ranker.parameters(), lr=lr)

    # Pre-compute embeddings
    embed_cache = {}
    def get_emb(text):
        key = text[:200]
        if key not in embed_cache:
            enc = tokenizer(text[:200], return_tensors="pt",
                           truncation=True, max_length=64).to(device)
            with torch.no_grad():
                out = model(input_ids=enc["input_ids"], output_hidden_states=True)
            embed_cache[key] = out.hidden_states[-1].mean(1).squeeze(0).float().detach()
        return embed_cache[key]

    print(f"  Pre-computing {len(set(t[0] for t in training_data) | set(t[1] for t in training_data))} embeddings...")
    for belief, query, _ in training_data:
        get_emb(belief)
        get_emb(query)

    history = []
    for epoch in range(epochs):
        total_loss = 0
        correct = 0
        total = 0

        import random
        random.shuffle(training_data)

        for belief_text, query_text, relevant in training_data:
            optimizer.zero_grad()
            h_b = get_emb(belief_text)
            h_q = get_emb(query_text)
            pred = ranker(h_b, h_q)
            target = torch.tensor(float(relevant), device=device)
            loss = F.binary_cross_entropy(pred, target)
            loss.backward()
            optimizer.step()

            total_loss += loss.item()
            correct += int((pred > 0.5) == relevant)
            total += 1

        acc = correct / total
        avg_loss = total_loss / total
        history.append({"epoch": epoch, "loss": avg_loss, "accuracy": acc})
        if epoch % 10 == 0:
            print(f"    E{epoch:02d} loss={avg_loss:.4f} acc={acc:.2f}")

    return history
