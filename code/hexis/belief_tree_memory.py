"""
Stage 1: BeliefTreeMemory — learned node embeddings on existing BeliefTree.

Augments the existing Phase 1 BeliefTree with learned 128-dim embeddings
per node, edge-typed message passing for embedding propagation, and
GRU update for experience-driven embedding changes.

Two parallel state channels on the SAME graph:
  tree.nodes[node_id].credence -> float     (explicit, updated by BayesianUpdater)
  self.embeddings[node_id]     -> vec(128)  (implicit, updated by phi + message passing)
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import List, Dict, Optional, Tuple

from hexis.belief_tree import BeliefTree, BeliefNode, NodeType


# Edge type mapping
EDGE_SUPPORTS = 0
EDGE_OPPOSES = 1
EDGE_ENTAILS = 2      # parent→child structural edge
EDGE_CONTRADICTS = 3


class BeliefTreeMemory(nn.Module):
    """Augments an existing BeliefTree with learned node embeddings.

    The BeliefTree already has nodes, typed edges, and credences.
    This adds:
      - Learned embedding per node (d_node-dim, nn.Parameter)
      - Edge-typed message passing for embedding propagation
      - GRU update for combining messages into new embeddings
    """

    def __init__(self, d_node=128, d_edge=64, n_message_passes=2):
        super().__init__()
        self.d_node = d_node
        self.d_edge = d_edge
        self.n_passes = n_message_passes

        # Node embeddings stored as regular dict of tensors (not ParameterDict)
        # because node IDs are dynamic. We register them manually for optimization.
        self._embeddings: Dict[str, torch.Tensor] = {}

        # Edge type embedding
        self.edge_embedding = nn.Embedding(4, d_edge)
        # 0=SUPPORTS, 1=OPPOSES, 2=ENTAILS, 3=CONTRADICTS

        # Message function: (source_embed, target_embed, edge_type, source_credence) → message
        cat_dim = d_node * 2 + d_edge + 1
        self.message_fn = nn.Sequential(
            nn.Linear(cat_dim, d_node),
            nn.SiLU(),
            nn.Linear(d_node, d_node),
        )

        # GRU update: message + current_embed → new_embed
        self.update_fn = nn.GRUCell(d_node, d_node)

        # Projection from base model hidden states to node embedding (for init)
        self.node_init_proj = nn.Sequential(
            nn.Linear(1, d_node),  # placeholder, replaced in init_from_tree
        )

    def init_from_tree(self, tree: BeliefTree, d_model: int, device: torch.device):
        """Initialize node embeddings and set up the init projection.

        Call this ONCE when constructing from a tree. Embeddings start
        as small random vectors. Use init_embeddings_from_model() to
        initialize from base model hidden states on node text.
        """
        # Replace init projection with correct input dim
        self.node_init_proj = nn.Sequential(
            nn.Linear(d_model, self.d_node),
            nn.SiLU(),
            nn.Linear(self.d_node, self.d_node),
        ).to(device)

        # Initialize embeddings as small random vectors
        for node_id in tree.nodes:
            self._embeddings[node_id] = torch.randn(
                self.d_node, device=device) * 0.01

        self._tree = tree

    def init_embeddings_from_model(self, base_model, tokenizer, tree: BeliefTree,
                                    device: torch.device):
        """Initialize node embeddings from base model hidden states on node text.

        Call after init_from_tree(). Runs each node's text through the base
        model and projects the pooled hidden state to d_node dims.
        """
        self.eval()
        with torch.no_grad():
            for node_id, node in tree.nodes.items():
                enc = tokenizer(node.statement[:300], return_tensors="pt",
                               truncation=True, max_length=256)
                ids = enc["input_ids"].to(device)
                outputs = base_model(input_ids=ids, output_hidden_states=True)
                h_pooled = outputs.hidden_states[-1].mean(dim=1)  # (1, d_model)
                embed = self.node_init_proj(h_pooled).squeeze(0)   # (d_node,)
                self._embeddings[node_id] = embed.detach().clone()

    @property
    def embeddings(self) -> Dict[str, torch.Tensor]:
        return self._embeddings

    def get_embedding(self, node_id: str) -> torch.Tensor:
        return self._embeddings[node_id]

    def set_embedding(self, node_id: str, embed: torch.Tensor):
        self._embeddings[node_id] = embed

    def get_edge_type(self, parent_node: BeliefNode, child_node: BeliefNode) -> int:
        """Determine edge type from node types and tree structure."""
        # Parent→child is structural (ENTAILS)
        return EDGE_ENTAILS

    def get_edges(self, tree: BeliefTree) -> List[Tuple[str, str, int]]:
        """Get all edges as (source_id, target_id, edge_type) triples.

        Includes both parent→child (ENTAILS) and evidence stance edges
        (SUPPORTS/OPPOSES based on node placement in the tree).
        """
        edges = []
        for node_id, node in tree.nodes.items():
            for child_id in node.children_ids:
                child = tree.nodes[child_id]
                # Evidence nodes: use SUPPORTS/OPPOSES based on subtree side
                # For now, structural edges are ENTAILS
                edges.append((node_id, child_id, EDGE_ENTAILS))
                # Bidirectional
                edges.append((child_id, node_id, EDGE_ENTAILS))
        return edges

    def propagate(self, tree: BeliefTree):
        """Message passing over tree edges. Call after any embedding update.

        Runs n_passes rounds of message passing. Each round:
        1. Compute messages along all edges
        2. Aggregate incoming messages per node (mean)
        3. Update node embedding via GRU
        """
        edges = self.get_edges(tree)

        for _ in range(self.n_passes):
            # Collect messages per target node
            incoming: Dict[str, List[torch.Tensor]] = {
                nid: [] for nid in tree.nodes
            }

            for src_id, tgt_id, edge_type in edges:
                msg = self._compute_message(src_id, tgt_id, edge_type, tree)
                incoming[tgt_id].append(msg)

            # Update embeddings
            for nid, messages in incoming.items():
                if messages:
                    agg = torch.stack(messages).mean(dim=0)  # (d_node,)
                    old_embed = self._embeddings[nid]
                    new_embed = self.update_fn(
                        agg.unsqueeze(0),
                        old_embed.unsqueeze(0),
                    ).squeeze(0)
                    self._embeddings[nid] = new_embed

    def _compute_message(self, src_id: str, tgt_id: str,
                          edge_type: int, tree: BeliefTree) -> torch.Tensor:
        """Compute a single message from src to tgt along edge_type."""
        h_src = self._embeddings[src_id]
        h_tgt = self._embeddings[tgt_id]
        device = h_src.device

        r = self.edge_embedding(torch.tensor(edge_type, device=device))
        cr = torch.tensor([tree.nodes[src_id].credence],
                          device=device, dtype=h_src.dtype)

        msg_input = torch.cat([h_src, h_tgt, r, cr])  # (d_node*2 + d_edge + 1)
        return self.message_fn(msg_input)

    def get_perspective_embeddings(self, node_ids: List[str],
                                    tree: BeliefTree) -> Tuple[torch.Tensor, torch.Tensor]:
        """Get embeddings and credences for a perspective (subset of nodes).

        Returns:
            embed_stack: (n_nodes, d_node)
            cred_stack:  (n_nodes,)
        """
        embeds = []
        creds = []
        for nid in node_ids:
            embeds.append(self._embeddings[nid])
            creds.append(tree.nodes[nid].credence)

        embed_stack = torch.stack(embeds)
        cred_stack = torch.tensor(creds, device=embed_stack.device,
                                  dtype=embed_stack.dtype)
        return embed_stack, cred_stack

    def clone_embeddings(self) -> Dict[str, torch.Tensor]:
        """Return a detached copy of all embeddings (for resetting after writes)."""
        return {nid: e.detach().clone() for nid, e in self._embeddings.items()}

    def restore_embeddings(self, saved: Dict[str, torch.Tensor]):
        """Restore embeddings from a saved copy."""
        for nid, e in saved.items():
            self._embeddings[nid] = e


def build_topic_tree(topic_data: dict) -> BeliefTree:
    """Build a minimal BeliefTree from a topic dict (from data_200_topics or train_amplifier).

    Creates:
      - Root node: the probe question
      - 3 pro evidence nodes (SUPPORTS edge implied)
      - 3 con evidence nodes (OPPOSES edge implied)

    The stance_A/stance_B are stored as metadata, not as nodes.
    """
    tree = BeliefTree()
    root_id = tree.add_root(topic_data["probe"], credence=0.5)

    # Pro evidence (experiences_A)
    for exp in topic_data.get("experiences_A", []):
        tree.add_child(root_id, NodeType.EVIDENCE, exp,
                       weight=1.0, credence=0.8)

    # Con evidence (experiences_B)
    for exp in topic_data.get("experiences_B", []):
        tree.add_child(root_id, NodeType.EVIDENCE, exp,
                       weight=1.0, credence=0.8)

    return tree


def get_pro_con_node_ids(tree: BeliefTree, n_pro: int = 3) -> Tuple[List[str], List[str]]:
    """Get pro and con node IDs from a topic tree built by build_topic_tree.

    Convention: first n_pro children of root are pro, rest are con.
    Both lists include the root node (shared context).
    """
    root = tree.nodes[tree.root_id]
    children = root.children_ids

    pro_ids = [tree.root_id] + children[:n_pro]
    con_ids = [tree.root_id] + children[n_pro:]
    return pro_ids, con_ids
