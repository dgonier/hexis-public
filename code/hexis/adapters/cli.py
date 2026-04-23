"""CLI helpers for integrating adapter presets into training / extraction scripts.

Pattern:

    from hexis.adapters.cli import add_preset_args, resolve_preset_args

    ap = argparse.ArgumentParser()
    add_preset_args(ap, default_preset="qwen3.5-4b",
                    agentic=False,  # True for agentic extractors (different stride default)
                    output_subpath="d_star.pt")
    # ... script-specific args ...
    args = ap.parse_args()
    preset = resolve_preset_args(args)
    # After this call args.model, args.stride, args.output are all populated,
    # falling through to preset defaults when the user didn't specify.

This keeps every script's edits to ~3 lines.
"""
from __future__ import annotations

import argparse

from . import get_preset, list_presets
from .model_preset import ModelPreset


def add_preset_args(
    ap: argparse.ArgumentParser,
    *,
    default_preset: str = "qwen3.5-4b",
    agentic: bool = False,
    output_subpath: str | None = None,
    add_training_args: bool = False,
    training_phase: str = "a",
) -> None:
    """Add --preset / --model / --stride / --output args to an ArgumentParser.

    After parse_args(), call resolve_preset_args(args) to fill in defaults
    from the preset.

    `agentic`: if True, default stride is max(preset.stride, 6) to match
    the historical agentic-extractor convention of stride=6.

    `output_subpath`: the path suffix appended to preset.checkpoint_base
    when `--output` is not specified. E.g. "d_star.pt" or
    "agentic/d_star_repeat.pt".
    """
    ap.add_argument(
        "--preset",
        default=default_preset,
        help=f"Model preset name. Available: {', '.join(list_presets())}",
    )
    ap.add_argument(
        "--model",
        default=None,
        help="Override preset.hf_id (e.g., for -Base variants).",
    )
    ap.add_argument(
        "--stride",
        type=int,
        default=None,
        help=(
            "Override preset.stride"
            + (" (agentic default=6)" if agentic else "")
        ),
    )
    if output_subpath is not None:
        ap.add_argument(
            "--output",
            default=None,
            help=(
                f"Output path (default: <preset.checkpoint_base>/{output_subpath})"
            ),
        )
    if add_training_args:
        ap.add_argument(
            "--rank", type=int, default=None,
            help="Override preset.rank (recipe: 16 @ 4B, 32 @ 8-9B, 32-64 @ 27B+)",
        )
        ap.add_argument(
            "--margin", type=float, default=None,
            help="Override preset.margin_base (recipe: 0.3 @ 4B, 1.0 @ 27B)",
        )
        ap.add_argument(
            "--lr", type=float, default=None,
            help=f"Override preset.lr_phase_{training_phase}",
        )
    # Stash config on the parser so resolve can read it back
    ap.set_defaults(
        _preset_agentic=agentic,
        _preset_output_subpath=output_subpath,
        _preset_training_phase=training_phase if add_training_args else None,
    )


def resolve_preset_args(args: argparse.Namespace) -> ModelPreset:
    """Fill in args.model / args.stride / args.output from the chosen preset.

    Must be called after parse_args(). Returns the resolved preset for
    callers that want other fields (rank, margin_base, etc.).
    """
    preset = get_preset(args.preset)
    if getattr(args, "model", None) is None:
        args.model = preset.hf_id
    if getattr(args, "stride", None) is None:
        default_stride = preset.stride
        if getattr(args, "_preset_agentic", False):
            default_stride = max(preset.stride, 6)
        args.stride = default_stride
    subpath = getattr(args, "_preset_output_subpath", None)
    if subpath is not None and getattr(args, "output", None) is None:
        args.output = f"{preset.checkpoint_base}/{subpath}"
    # Training args fall-through
    training_phase = getattr(args, "_preset_training_phase", None)
    if training_phase is not None:
        if getattr(args, "rank", None) is None:
            args.rank = preset.rank
        if getattr(args, "margin", None) is None:
            args.margin = preset.margin_base
        if getattr(args, "lr", None) is None:
            args.lr = getattr(preset, f"lr_phase_{training_phase}")
    # Also stash the resolved preset so scripts can access preset-only fields
    args.preset_obj = preset
    return preset
