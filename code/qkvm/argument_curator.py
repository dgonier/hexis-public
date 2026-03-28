"""
HEXIS v23: Two-stage argument curation.

Stage 1: M domain filter (between-topic)
  Uses M's perturbation direction to filter beliefs by topic relevance.
  M excels here: 100% precision on 100-node noisy curation test.

Stage 2: Conviction gate
  Removes weak/agnostic arguments. The curated slot is what the model
  generates FROM — weak arguments produce weak or flipped generation.

Stage 3: Base model query ranking (within-topic)
  Uses base model hidden states (no M) for semantic similarity between
  query and argument. M can't distinguish within a topic (all pro-UBI
  arguments have cosine ~0.95 in M-space), but the base model's
  representation space IS query-specific.

Stage 4: Novelty tiebreaker
  Among equally relevant, equally strong arguments, prefer the one
  with more novel content (specific numbers, citations, proper nouns).
  Novel content is what the slot is FOR — it's what compiled M can't carry.

Stage 5: Token budget packing
  Pack top arguments with their evidence into the token budget.

Usage:
    curator = ArgumentCurator(model, tokenizer, M_A, M_B, patched_layers)
    selected = curator.curate(arguments, query, token_budget=80)
    slot_xml = curator.build_slot(selected)
"""

import torch
import torch.nn.functional as F
import re

_STOPWORDS = frozenset({"the","a","an","is","are","was","were","be","been","being",
    "have","has","had","do","does","did","will","would","shall","should","may",
    "might","can","could","about","what","how","why","when","where","who","which",
    "that","this","these","those","it","its","of","in","on","at","to","for","with",
    "by","from","and","or","but","not","no","if","we","us","our","my","i","you"})


class ArgumentCurator:
    """Two-stage argument curation: M for domain, base model for query specificity."""

    def __init__(self, model, tokenizer, M_A_layer0, M_B_layer0,
                 patched_layers, device="cuda"):
        self.model = model
        self.tokenizer = tokenizer
        self.M_A = M_A_layer0
        self.M_B = M_B_layer0
        self.patched_layers = patched_layers
        self.device = device

    def _get_base_embedding(self, text):
        """Get base model embedding (last layer, mean-pooled). No M modulation."""
        enc = self.tokenizer(text[:300], return_tensors="pt",
                             truncation=True, max_length=128).to(self.device)
        with torch.no_grad():
            out = self.model(input_ids=enc["input_ids"], output_hidden_states=True)
        return out.hidden_states[-1].mean(1).float().squeeze(0)

    def _get_perturbation_direction(self, text):
        """Get M's perturbation direction for a text (topic-level signal)."""
        enc = self.tokenizer(text[:200], return_tensors="pt",
                             truncation=True, max_length=64).to(self.device)
        with torch.no_grad():
            out = self.model(input_ids=enc["input_ids"], output_hidden_states=True)
        h = out.hidden_states[self.patched_layers[0] + 1].mean(1).squeeze(0).float()
        perturb = torch.matmul(
            torch.matmul(h, self.M_A.to(h.device, h.dtype)),
            self.M_B.to(h.device, h.dtype).T
        )
        return F.normalize(perturb.unsqueeze(0), dim=-1)

    def _keyword_overlap(self, query, text):
        """Jaccard-style keyword overlap between query and argument text."""
        q_words = set(re.findall(r'\w+', query.lower())) - _STOPWORDS
        t_words = set(re.findall(r'\w+', text.lower())) - _STOPWORDS
        if not q_words:
            return 0.0
        return len(q_words & t_words) / len(q_words)

    def _structural_relevance(self, query, arg):
        """Score argument relevance using XML tree structure.

        The tree structure encodes routing information:
        - argument.type tells you WHAT KIND of reasoning it is
        - counterargument.text tells you WHAT OBJECTION it addresses
        - evidence nodes tell you WHAT FACTS support it

        Query classification → structural matching:
          "What does research show?" → experiential, empirical args
          "Won't people stop X?" → counterarguments addressing that objection
          "Is it economically viable?" → empirical, consequentialist args
          "How does it work?" → mechanistic args
          "What's the legal basis?" → analogical args
        """
        q = query.lower()
        arg_type = arg.get("type", "")
        arg_text = arg.get("text", "").lower()

        score = 0.0

        # Query intent → argument type matching
        research_signals = ["research", "study", "data", "evidence", "pilot",
                            "experiment", "trial", "findings", "results"]
        experience_signals = ["experience", "what's it like", "firsthand",
                              "personal", "managed", "worked"]
        economic_signals = ["economy", "economic", "cost", "afford", "budget",
                            "money", "spend", "pay", "hurt", "fiscal", "expensive"]
        mechanism_signals = ["how does", "how do", "mechanism", "designed",
                             "algorithm", "exploit", "architecture", "work"]
        legal_signals = ["legal", "law", "precedent", "constitutional",
                         "amendment", "judicial", "court", "rights"]
        feasibility_signals = ["feasible", "possible", "enforce", "implement",
                               "practical", "can we", "is it possible"]
        objection_signals = ["won't", "wouldn't", "but what about", "what if",
                             "stop", "quit", "lazy", "destroy", "fail", "hurt"]

        # Match query intent to argument type
        if any(s in q for s in research_signals):
            if arg_type in ("experiential", "empirical"):
                score += 0.4
        if any(s in q for s in experience_signals):
            if arg_type == "experiential":
                score += 0.5
        if any(s in q for s in economic_signals):
            if arg_type in ("empirical", "consequentialist"):
                score += 0.4
        if any(s in q for s in mechanism_signals):
            if arg_type == "mechanistic":
                score += 0.5
        if any(s in q for s in legal_signals):
            if arg_type == "analogical":
                score += 0.5
        if any(s in q for s in feasibility_signals):
            if arg_type in ("empirical", "mechanistic"):
                score += 0.3

        # Objection matching: does the query raise an objection
        # that this argument's text or evidence directly addresses?
        if any(s in q for s in objection_signals):
            # Check if argument text contains the objected concept
            q_content = set(re.findall(r'\w+', q)) - _STOPWORDS
            arg_content = set(re.findall(r'\w+', arg_text)) - _STOPWORDS
            # Direct word overlap on the objection
            objection_overlap = len(q_content & arg_content) / max(len(q_content), 1)
            score += 0.4 * objection_overlap

            # Also check evidence for direct rebuttals
            for ev in arg.get("evidence", []):
                ev_words = set(re.findall(r'\w+', ev.lower())) - _STOPWORDS
                ev_overlap = len(q_content & ev_words) / max(len(q_content), 1)
                score += 0.2 * ev_overlap

        return min(score, 1.0)

    def score_novelty(self, text):
        """Score how much novel content a text contains.

        High novelty = specific numbers, names, citations that
        the model probably can't reconstruct from parametric knowledge.
        """
        markers = 0
        markers += len(re.findall(r'\d+\.\d+%?', text))
        markers += len(re.findall(r'(?:19|20)\d{2}', text))
        markers += len(re.findall(r'[A-Z][a-z]+\s+(?:Lab|Institute|University|Study|Foundation|Center)', text))
        markers += len(re.findall(r'[Nn]=?\s*[\d,]+', text))
        markers += len(re.findall(r'\$[\d,.]+', text))
        markers += len(re.findall(r'\d+[%]', text))
        return min(markers / 5.0, 1.0)

    def curate(self, arguments, query, token_budget=80, domain_threshold=0.3):
        """Two-stage curation: M domain filter → base model query ranking.

        Args:
            arguments: list of dicts with keys:
                text, type, evidence (list of str), conviction
            query: the user's question
            token_budget: max tokens for the curated slot
            domain_threshold: minimum M-perturbation similarity for domain filter

        Returns:
            list of selected arguments with scores
        """
        query_dir = self._get_perturbation_direction(query)
        query_emb = self._get_base_embedding(query)

        scored = []
        for arg in arguments:
            full_text = arg["text"]
            for ev in arg.get("evidence", []):
                full_text += " " + ev

            # --- Stage 1: M domain filter ---
            arg_dir = self._get_perturbation_direction(full_text)
            domain_sim = F.cosine_similarity(query_dir, arg_dir).item()

            # --- Stage 2: Conviction + type gate ---
            conv = arg.get("conviction", "moderate")
            if conv in ("weak", "agnostic", "disbelieve"):
                # Weak arguments excluded from slot — they cause stance flips
                continue
            if arg.get("type") == "rebuttal":
                # Rebuttals excluded from slot — their objection text creates
                # polarity ambiguity in compressed form. They work in full
                # context (B) but confuse generation in curated slots.
                continue

            # --- Stage 3: Query-specific ranking ---
            # Three signals: semantic similarity, structural match, keyword overlap
            arg_emb = self._get_base_embedding(full_text)
            query_sim = F.cosine_similarity(
                query_emb.unsqueeze(0), arg_emb.unsqueeze(0)
            ).item()
            struct_sim = self._structural_relevance(query, arg)
            keyword_sim = self._keyword_overlap(query, full_text)

            # --- Stage 4: Novelty (for packing priority, not selection) ---
            evidence_novelty = max(
                (self.score_novelty(ev) for ev in arg.get("evidence", [""])),
                default=0.0
            )
            warrant_novelty = self.score_novelty(arg["text"])
            novelty = 0.6 * evidence_novelty + 0.4 * warrant_novelty

            # --- Relevance score ---
            # Structural match is the primary routing signal — it uses
            # the XML tree's type/supports/refutation annotations to
            # match query intent to argument function.
            conviction_score = 1.0 if conv == "strong" else 0.6
            score = (0.30 * struct_sim +       # structural match (tree position)
                     0.25 * query_sim +         # semantic similarity
                     0.15 * keyword_sim +       # keyword overlap
                     0.15 * conviction_score +  # argument strength
                     0.15 * domain_sim)         # topic alignment (M)

            scored.append({
                **arg,
                "score": score,
                "query_sim": query_sim,
                "struct_sim": struct_sim,
                "keyword_sim": keyword_sim,
                "domain_sim": domain_sim,
                "novelty": novelty,
                "evidence_novelty": evidence_novelty,
                "conviction_score": conviction_score,
            })

        scored.sort(key=lambda x: x["score"], reverse=True)

        # --- Stage 5: Token budget packing ---
        # Pack by relevance order. Within each argument, keep highest-novelty evidence.
        selected = []
        tokens_used = 15  # XML overhead

        for arg in scored:
            arg_xml = self._argument_to_xml(arg)
            arg_tokens = len(self.tokenizer.encode(arg_xml))

            if tokens_used + arg_tokens <= token_budget:
                selected.append(arg)
                tokens_used += arg_tokens
            else:
                # Try trimming: keep warrant + highest-novelty evidence that fits
                trimmed = self._trim_evidence(arg, token_budget - tokens_used)
                if trimmed:
                    selected.append(trimmed)
                    tokens_used += len(self.tokenizer.encode(
                        self._argument_to_xml(trimmed)))
                else:
                    # Warrant-only if it fits
                    warrant_only = {**arg, "evidence": []}
                    wo_xml = self._argument_to_xml(warrant_only)
                    wo_tokens = len(self.tokenizer.encode(wo_xml))
                    if tokens_used + wo_tokens <= token_budget:
                        selected.append(warrant_only)
                        tokens_used += wo_tokens
                # Continue — try packing smaller arguments too

        return selected

    def _trim_evidence(self, arg, remaining_budget):
        """Keep the argument warrant but reduce evidence to fit budget."""
        evidence = arg.get("evidence", [])
        if not evidence:
            return None

        ev_scored = [(ev, self.score_novelty(ev)) for ev in evidence]
        ev_scored.sort(key=lambda x: x[1], reverse=True)

        trimmed = {**arg, "evidence": []}
        for ev, nov in ev_scored:
            test = {**trimmed, "evidence": trimmed["evidence"] + [ev]}
            test_xml = self._argument_to_xml(test)
            if len(self.tokenizer.encode(test_xml)) <= remaining_budget:
                trimmed["evidence"].append(ev)
            else:
                break

        if not trimmed["evidence"]:
            return None
        return trimmed

    def _argument_to_xml(self, arg):
        """Convert argument dict to XML string."""
        arg_type = arg.get("type", "")
        type_attr = f' type="{arg_type}"' if arg_type else ""
        conv = arg.get("conviction", "moderate")

        if arg_type == "rebuttal":
            # Format rebuttals so model reads them as refutations, not claims
            xml = f'  <rebuttal conviction="{conv}">\n'
            xml += f"    Objection: {arg['text'][:120]}\n"
            for ev in arg.get("evidence", []):
                xml += f"    <refutation>{ev[:100]}</refutation>\n"
            xml += "  </rebuttal>\n"
        else:
            xml = f'  <argument conviction="{conv}"{type_attr}>\n'
            xml += f"    {arg['text'][:150]}\n"
            for ev in arg.get("evidence", []):
                xml += f"    <evidence>{ev[:100]}</evidence>\n"
            xml += "  </argument>\n"
        return xml

    def build_slot(self, selected_arguments):
        """Build curated slot XML from selected arguments."""
        xml = "<arguments>\n"
        for arg in selected_arguments:
            xml += self._argument_to_xml(arg)
        xml += "</arguments>"
        return xml

    def curate_from_topic(self, topic, side, query, token_budget=80):
        """Convenience: extract arguments from topic dict and curate."""
        side_key = "A" if side == "pro" else "B"
        reasonings = topic.get(f"reasoning_{side_key}", [])
        experiences = topic.get(f"experiences_{side_key}", [])

        arguments = []
        for i, r in enumerate(reasonings):
            arg = {
                "text": r,
                "type": "empirical" if i == 0 else "consequentialist",
                "evidence": [experiences[i]] if i < len(experiences) else [],
                "conviction": "strong" if i == 0 else "moderate",
            }
            arguments.append(arg)

        stance = topic.get(f"stance_{side_key}", "")
        if stance:
            arguments.insert(0, {
                "text": stance[:150],
                "type": "claim",
                "evidence": [],
                "conviction": "strong",
            })

        return self.curate(arguments, query, token_budget)
