"""HEXIS: Compiled Dispositional Memory Through Enmeshed Networks.

This is the paper-companion subset of the HEXIS library. The public release
exposes the enmeshed modules and training entry points needed to reproduce
the paper's headline results and to port HEXIS to a new base model via the
adapter system (see `hexis.adapters`).

Subset scope (not all internal modules are shipped):
  - config, adapters, train (CLI wrapper)
  - enmeshed components: argument_curator, belief_compiler, belief_rankers,
    belief_tree_memory, direction_injector, mstate_read_head, phi_node_writer,
    conviction_reader, compiled_belief_training
  - training data: data_200_topics

Usage:
    from hexis.adapters import get_preset
    preset = get_preset("ministral-8b")

    # Or drive the full pipeline:
    #   python -m hexis.train --preset ministral-8b
"""
from __future__ import annotations

from .config import QKVMConfig

__version__ = "0.1.0"

__all__ = ["QKVMConfig"]
