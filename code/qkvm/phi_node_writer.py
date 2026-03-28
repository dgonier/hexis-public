"""
Stage 3: PhiNodeWriter — experience text → belief tree node embedding updates.

After a debate, each speech/argument/evidence is an experience.
Each experience is linked to specific belief tree nodes.
Phi reads base model hidden states from the experience text
and produces a gated delta to the linked node's embedding.
"""

import torch
import torch.nn as nn
from typing import Dict, List

from qkvm.belief_tree_memory import BeliefTreeMemory
from qkvm.belief_tree import BeliefTree


class PhiNodeWriter(nn.Module):
    """Phi's job: experience text → node embedding updates.

    Takes base model hidden states from experience text and the
    current node embedding, produces a gated delta.
    """

    def __init__(self, d_model=2560, d_node=128):
        super().__init__()
        self.d_model = d_model
        self.d_node = d_node

        # Encode experience hidden states → d_node
        self.experience_encoder = nn.Sequential(
            nn.Linear(d_model, 256),
            nn.SiLU(),
            nn.Linear(256, d_node),
        )

        # Update projection: (experience_encoding, current_node_embed) → delta
        self.update_proj = nn.Sequential(
            nn.Linear(d_node * 2, d_node),
            nn.SiLU(),
            nn.Linear(d_node, d_node),
            nn.Tanh(),
        )

        # Gate: how much to update this node
        self.gate_proj = nn.Linear(d_node * 2, 1)
        nn.init.constant_(self.gate_proj.bias, 2.0)  # start with gate open

    def forward(self, h_experience: torch.Tensor,
                current_node_embedding: torch.Tensor) -> torch.Tensor:
        """
        Args:
            h_experience: (batch, seq, d_model) — base model hidden states on experience text
            current_node_embedding: (d_node,) — current embedding of the linked node

        Returns:
            gated_delta: (d_node,) — delta to add to node embedding
        """
        # Pool hidden states and cast to float32
        if h_experience.dim() == 3:
            h_pooled = h_experience.mean(dim=1).float()  # (batch, d_model)
        elif h_experience.dim() == 2:
            h_pooled = h_experience.float()  # already (batch, d_model)
        else:
            h_pooled = h_experience.unsqueeze(0).float()  # (d_model,) -> (1, d_model)

        # Encode experience
        z_exp = self.experience_encoder(h_pooled)  # (batch, d_node)

        # Mean over batch dim if needed
        if z_exp.dim() > 1:
            z_exp = z_exp.mean(dim=0)  # (d_node,)

        # Combine with current node state
        combined = torch.cat([z_exp, current_node_embedding])  # (d_node * 2,)
        delta = self.update_proj(combined)  # (d_node,)
        gate = torch.sigmoid(self.gate_proj(combined))  # (1,)

        return gate * delta


def write_experiences_to_tree(
    experience_texts: List[str],
    linked_node_ids: List[str],
    phi_writer: PhiNodeWriter,
    btm: BeliefTreeMemory,
    tree: BeliefTree,
    base_model,
    tokenizer,
    device: torch.device,
    lr: float = 0.1,
):
    """Write a list of experiences into the belief tree.

    Each experience updates its linked node's embedding, then
    message passing propagates the change through the tree.

    Args:
        experience_texts: list of experience strings
        linked_node_ids: list of node IDs each experience links to
        phi_writer: the PhiNodeWriter module
        btm: BeliefTreeMemory with current embeddings
        tree: the BeliefTree structure
        base_model: frozen base LLM
        tokenizer: tokenizer for base model
        device: compute device
        lr: learning rate for embedding updates (how much delta to apply)
    """
    for exp_text, node_id in zip(experience_texts, linked_node_ids):
        # Get hidden states from base model
        enc = tokenizer(exp_text[:300], return_tensors="pt",
                       truncation=True, max_length=256)
        ids = enc["input_ids"].to(device)

        with torch.no_grad():
            outputs = base_model(input_ids=ids, output_hidden_states=True)
        h_exp = outputs.hidden_states[-1]  # (1, seq, d_model)

        # Get current node embedding
        current_embed = btm.get_embedding(node_id)

        # Compute delta
        delta = phi_writer(h_exp, current_embed)

        # Apply update
        new_embed = current_embed + lr * delta
        btm.set_embedding(node_id, new_embed)

    # Propagate through tree
    btm.propagate(tree)
