"""
Stage 2: DirectionInjector — injects fixed d* at learned conviction magnitude.

Math at each patched layer:
    attn_output' = attn_output + conviction * base_scale * d*_L

d* is a buffer (never trained). conviction is a scalar from ConvictionReader.
base_scale=10.0 validated by probe (81% at scale 10).
"""

import torch
import torch.nn as nn


class DirectionInjector(nn.Module):
    """Injects fixed d* direction into post-attention residual stream."""

    def __init__(self, d_star_dict, base_scale=10.0):
        """
        Args:
            d_star_dict: {layer_idx: d* tensor (d_model,)} from extract_d_star.py
            base_scale: fixed multiplier. 10.0 validated by probe.
        """
        super().__init__()
        self.base_scale = base_scale
        self.layer_indices = sorted(d_star_dict.keys())

        # Register d* as BUFFERS — never trained
        for layer_idx, d_vec in d_star_dict.items():
            self.register_buffer(f'd_star_{layer_idx}', d_vec.clone())

    def get_d_star(self, layer_idx):
        return getattr(self, f'd_star_{layer_idx}')

    def forward(self, attn_output, layer_idx, conviction):
        """
        Args:
            attn_output: (batch, seq, d_model)
            layer_idx: int
            conviction: scalar tensor in [-1, +1]

        Returns:
            attn_output + conviction * base_scale * d*
        """
        d_star = self.get_d_star(layer_idx).to(attn_output.device, attn_output.dtype)
        conv = conviction.to(attn_output.device) if hasattr(conviction, 'to') else conviction
        injection = conv * self.base_scale * d_star
        return attn_output + injection.unsqueeze(0).unsqueeze(0)


def install_direction_hooks(base_model, direction_injector, conviction, patched_layers):
    """Install d* injection hooks on attention outputs.

    Args:
        base_model: the base LLM
        direction_injector: DirectionInjector instance
        conviction: scalar tensor in [-1, +1]
        patched_layers: list of layer indices

    Returns:
        list of hook handles (call .remove() to clean up)
    """
    layers = base_model.model.layers
    handles = []

    for layer_idx in patched_layers:
        layer = layers[layer_idx]
        attn = getattr(layer, 'self_attn', None) or getattr(layer, 'linear_attn', None)

        if attn is not None:
            def make_hook(di, li, conv):
                def hook(module, input, output):
                    if isinstance(output, tuple):
                        h = output[0]
                        h = di.forward(h, li, conv)
                        return (h,) + output[1:]
                    return di.forward(output, li, conv)
                return hook

            handle = attn.register_forward_hook(make_hook(direction_injector, layer_idx, conviction))
            handles.append(handle)

    return handles


def remove_direction_hooks(handles):
    """Remove all direction injection hooks."""
    for h in handles:
        h.remove()
