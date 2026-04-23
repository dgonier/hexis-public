"""
HEXIS v23: Universal Memory Schema.

One XML schema for all scenarios — strategies, beliefs, preferences, observations.
Each node has the same structure regardless of domain.

The schema is designed so phi processes identical token patterns
(conviction labels, support nodes, type attributes) across all domains.
No retraining needed when switching from debate to ALFWorld to user preferences.
"""

from dataclasses import dataclass, field
from typing import Optional
import json


@dataclass
class Support:
    """Evidence supporting a memory node."""
    type: str  # success, failure, testimony, data, inference
    content: str
    source: str = ""  # task_7, debate_3, user_session_5
    recency: str = "recent"  # recent, established, old


@dataclass
class MemoryNode:
    """Universal memory node — works for any domain."""
    id: str
    type: str  # strategy, belief, preference, observation
    content: str  # the claim/recommendation/observation
    conviction: str = "agnostic"  # strong, moderate, agnostic, weak, disbelieve
    credence: float = 0.5
    domain: str = ""  # search, navigation, trade, user, etc.
    expandable: bool = True
    supports: list = field(default_factory=list)

    def add_support(self, support: Support):
        self.supports.append(support)

    def to_xml(self, include_supports=True, max_supports=3):
        attrs = f'type="{self.type}" conviction="{self.conviction}" id="{self.id}"'
        if self.domain:
            attrs += f' domain="{self.domain}"'
        if self.expandable:
            attrs += f' expandable="true"'

        xml = f'  <node {attrs}>\n    {self.content}\n'
        if include_supports and self.supports:
            for s in self.supports[-max_supports:]:
                src = f' source="{s.source}"' if s.source else ""
                xml += f'    <support type="{s.type}"{src}>{s.content}</support>\n'
        xml += '  </node>\n'
        return xml


class MemoryTree:
    """Universal memory tree — holds nodes of any type."""

    def __init__(self):
        self.nodes: dict[str, MemoryNode] = {}
        self._next_id = 0

    def create_node(self, type: str, content: str, conviction: str = "weak",
                     domain: str = "", supports: list = None) -> MemoryNode:
        self._next_id += 1
        node_id = f"n{self._next_id}"
        node = MemoryNode(
            id=node_id, type=type, content=content,
            conviction=conviction, credence=conviction_to_credence(conviction),
            domain=domain, supports=supports or [],
        )
        self.nodes[node_id] = node
        return node

    def get_node(self, node_id: str) -> Optional[MemoryNode]:
        return self.nodes.get(node_id)

    def remove_node(self, node_id: str):
        self.nodes.pop(node_id, None)

    def to_xml(self, include_supports=True, max_nodes=20, token_budget=None,
               tokenizer=None):
        """Build XML for the full tree or within a token budget."""
        xml = "<memory>\n"
        # Sort by conviction (strong first)
        conv_order = {"strong": 0, "moderate": 1, "agnostic": 2, "weak": 3, "disbelieve": 4}
        sorted_nodes = sorted(self.nodes.values(),
                               key=lambda n: conv_order.get(n.conviction, 2))

        tokens_used = 10  # overhead
        for i, node in enumerate(sorted_nodes[:max_nodes]):
            entry = node.to_xml(include_supports=include_supports)
            if token_budget and tokenizer:
                entry_toks = len(tokenizer.encode(entry))
                if tokens_used + entry_toks > token_budget:
                    continue
                tokens_used += entry_toks
            xml += entry

        xml += "</memory>"
        return xml

    def to_dict(self):
        return {nid: {
            "type": n.type, "content": n.content,
            "conviction": n.conviction, "credence": n.credence,
            "domain": n.domain,
            "supports": [{"type": s.type, "content": s.content,
                          "source": s.source, "recency": s.recency}
                         for s in n.supports],
        } for nid, n in self.nodes.items()}

    def from_dict(self, data):
        self.nodes.clear()
        for nid, d in data.items():
            node = MemoryNode(
                id=nid, type=d["type"], content=d["content"],
                conviction=d["conviction"],
                credence=d.get("credence", conviction_to_credence(d["conviction"])),
                domain=d.get("domain", ""),
                supports=[Support(**s) for s in d.get("supports", [])],
            )
            self.nodes[nid] = node
            id_num = int(nid.lstrip("n")) if nid.startswith("n") and nid[1:].isdigit() else 0
            self._next_id = max(self._next_id, id_num)

    def save(self, path):
        with open(path, "w") as f:
            json.dump(self.to_dict(), f, indent=2)

    def load(self, path):
        with open(path) as f:
            self.from_dict(json.load(f))


CONVICTION_TO_CREDENCE = {
    "strong": 0.90, "moderate": 0.70, "agnostic": 0.50,
    "weak": 0.30, "disbelieve": 0.10,
}

CREDENCE_RANGES = [
    (80, 100, "strong"), (60, 80, "moderate"), (40, 60, "agnostic"),
    (20, 40, "weak"), (0, 20, "disbelieve"),
]


def conviction_to_credence(conv):
    return CONVICTION_TO_CREDENCE.get(conv, 0.5)


def credence_to_conviction(cr):
    pct = int(cr * 100)
    for lo, hi, label in CREDENCE_RANGES:
        if lo <= pct < hi:
            return label
    return "agnostic"
