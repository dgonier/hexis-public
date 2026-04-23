"""
Stage 5: MStateReadHead — belief tree node embeddings → per-layer M_A, M_B.

For Q-modulation through existing InputModulator hooks:
    x_Q = x + mod_scale * (x @ M_A) @ M_B^T

Encodes CONTENT DISPOSITION — what the agent attends to.
Not direction (that's d*). Not conviction (that's ConvictionReader).
"""

import torch
import torch.nn as nn
import torch.nn.functional as F


class MStateReadHead(nn.Module):
    def __init__(self, d_node=128, d_model=2560, rank=16, n_layers=11,
                 max_norm=1.5):
        super().__init__()
        self.d_model = d_model
        self.rank = rank
        self.max_norm = max_norm

        self.m_proj_A = nn.ModuleList([
            nn.Linear(d_node, d_model * rank) for _ in range(n_layers)
        ])
        self.m_proj_B = nn.ModuleList([
            nn.Linear(d_node, d_model * rank) for _ in range(n_layers)
        ])
        self.mod_scales = nn.ParameterList([
            nn.Parameter(torch.tensor(1.0)) for _ in range(n_layers)
        ])

        for proj in list(self.m_proj_A) + list(self.m_proj_B):
            nn.init.normal_(proj.weight, std=0.02)

    def _norm_clamp(self, t):
        n = t.norm().clamp(min=1e-8)
        if n > self.max_norm:
            t = t * (self.max_norm / n)
        return t

    def forward(self, embed_stack, cred_stack):
        """
        Args:
            embed_stack: (n_nodes, d_node) from perspective
            cred_stack: (n_nodes,) credences

        Returns:
            list of (M_A, M_B, mod_scale) per layer
        """
        weights = F.softmax(cred_stack * 5.0, dim=0)
        disposition = (weights.unsqueeze(-1) * embed_stack).sum(dim=0)

        outputs = []
        for l in range(len(self.m_proj_A)):
            M_A = torch.tanh(self.m_proj_A[l](disposition)).reshape(
                self.d_model, self.rank)
            M_B = torch.tanh(self.m_proj_B[l](disposition)).reshape(
                self.d_model, self.rank)
            M_A = self._norm_clamp(M_A)
            M_B = self._norm_clamp(M_B)
            outputs.append((M_A, M_B, self.mod_scales[l]))

        return outputs
