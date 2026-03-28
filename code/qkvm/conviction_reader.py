"""
ConvictionReader: belief tree state → conviction.

REVISED for v21.1: Conviction IS the posterior credence, not a separate signal.
    conviction = 2 × Cr(resolution) - 1

The formal conviction comes from Jeffrey conditionalization on the credences.
The neural prediction is trained to match it, giving the system a Bayesian anchor.
"""

import torch
import torch.nn as nn
import torch.nn.functional as F

from qkvm.jeffrey_update import credence_to_conviction


class ConvictionReader(nn.Module):
    def __init__(self, d_node=128):
        super().__init__()
        # Predicts posterior credence from tree state
        self.credence_predictor = nn.Sequential(
            nn.Linear(d_node, 64),
            nn.SiLU(),
            nn.Linear(64, 1),
            nn.Sigmoid(),  # outputs [0,1] = credence
        )

    def forward(self, embed_stack, cred_stack, resolution_credence=None):
        """
        Args:
            embed_stack: (n_nodes, d_node) from perspective
            cred_stack: (n_nodes,) credences
            resolution_credence: float, the formal Jeffrey posterior (if available)

        Returns:
            formal_conviction: from Jeffrey conditionalization (if resolution_credence given)
            predicted_conviction: from neural network
        """
        # Neural prediction from embeddings
        weights = F.softmax(cred_stack * 5.0, dim=0)
        aggregate = (weights.unsqueeze(-1) * embed_stack).sum(dim=0)
        predicted_credence = self.credence_predictor(aggregate).squeeze()
        predicted_conviction = 2 * predicted_credence - 1

        # Formal conviction from tree credences
        if resolution_credence is not None:
            formal_conviction = credence_to_conviction(resolution_credence)
            return formal_conviction, predicted_conviction
        else:
            return predicted_conviction
