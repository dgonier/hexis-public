"""Top-level orchestrator for HEXIS training pipelines.

Chains the Phase A-D training recipe into a single command so porting to
a new model is one invocation:

    python -m hexis.train --preset ministral-8b
    python -m hexis.train --preset qwen3.6-35b-a3b --phases dispositional
    python -m hexis.train --preset ministral-8b --phases agentic
    python -m hexis.train --preset ministral-8b --phases a,b,d  # fine-grained
    python -m hexis.train --preset ministral-8b --dry-run       # print commands only

Phase aliases:
  - "all"           = everything (default): d_star, a (v21+v21_1+v21_2+v21_4), b, d, agentic
  - "dispositional" = d_star, a, b, d
  - "agentic"       = agentic_d_star (d_star_repeat, d_star_prompted directions, d_star_tools)
  - "a"             = Phase A full (v21, v21_1, v21_2, v21_4)
  - "b"             = Phase B compiled V-mod (compiled_belief_training.py)
  - "d"             = Phase D sycophancy
  - "d_star"        = dispositional d* extraction only

Smoke mode (--smoke): truncates epoch counts to fast values for sanity-checking
a new model without committing to the full training run. Prints a very clear
banner so you never confuse a smoke-run checkpoint with a real one.
"""
from __future__ import annotations

import argparse
import os
import shlex
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path

from hexis.adapters import get_preset, list_presets
from hexis.adapters.model_preset import ModelPreset

REPO_ROOT = Path(__file__).resolve().parent.parent


# ------------------ phase definitions --------------------------------------

@dataclass
class PhaseSpec:
    name: str
    script: str
    description: str
    default_epochs: int
    smoke_epochs: int
    # Whether the script has an --epochs CLI arg. Extraction scripts don't.
    takes_epochs: bool = True
    # Extra CLI fragments to pass (besides --preset). Empty means no extras.
    extra_args: list[str] = None

    def __post_init__(self):
        if self.extra_args is None:
            self.extra_args = []

    def command(self, preset: ModelPreset, smoke: bool) -> list[str]:
        cmd = [
            sys.executable, self.script,
            "--preset", preset.name,
        ]
        if self.takes_epochs:
            epochs = self.smoke_epochs if smoke else self.default_epochs
            cmd.extend(["--epochs", str(epochs)])
        cmd.extend(self.extra_args)
        return cmd


# Phase definitions. Epoch counts per M_canonical_recipe.md.
DISPOSITIONAL_PHASES: list[PhaseSpec] = [
    PhaseSpec(
        name="d_star",
        script="scripts/extract_d_star.py",
        description="Stage 1 — Extract dispositional d* direction vectors",
        default_epochs=0,
        smoke_epochs=0,
        takes_epochs=False,
    ),
    PhaseSpec(
        name="a.v21",
        script="scripts/train_v21.py",
        description="Phase A Step 2a — Base content (v21)",
        default_epochs=100,
        smoke_epochs=5,
        extra_args=[],
    ),
    PhaseSpec(
        name="a.v21_1",
        script="scripts/train_v21_1.py",
        description="Phase A Step 2b — Conviction calibration (v21.1)",
        default_epochs=125,
        smoke_epochs=5,
        extra_args=[],
    ),
    PhaseSpec(
        name="a.v21_2",
        script="scripts/train_v21_2.py",
        description="Phase A Step 2c — Ranking (v21.2)",
        default_epochs=100,
        smoke_epochs=5,
        extra_args=[],
    ),
    PhaseSpec(
        name="a.v21_4",
        script="scripts/train_v21_4.py",
        description="Phase A Step 2d — M with beliefs (v21.4)",
        default_epochs=25,
        smoke_epochs=5,
        extra_args=[],
    ),
    PhaseSpec(
        name="b",
        script="hexis/compiled_belief_training.py",
        description="Phase B — Compiled V-modulation (v23_compiled)",
        default_epochs=100,
        smoke_epochs=5,
        extra_args=[],
    ),
    PhaseSpec(
        name="d",
        script="scripts/train_v23_sycophancy.py",
        description="Phase D — Sycophancy training (v23_sycophancy)",
        default_epochs=50,
        smoke_epochs=5,
        extra_args=[],
    ),
]

# Agentic extraction. No gradient updates — extraction per direction.
AGENTIC_PHASES: list[PhaseSpec] = [
    PhaseSpec(
        name="agentic.d_star_repeat",
        script="scripts/extract_d_star_repeat.py",
        description="Agentic — d*_repeat (novel vs repeated tool calls)",
        default_epochs=0,
        smoke_epochs=0,
        takes_epochs=False,
    ),
    # d_star_no_early_termination requires positive/negative prompt files —
    # can't be run blindly without those inputs. Skipped here; the wrapper
    # prints a note if this phase is requested.
    # PhaseSpec(
    #     name="agentic.d_star_no_early_termination",
    #     script="scripts/extract_d_star_prompted.py",
    #     ...
    # ),
    PhaseSpec(
        name="agentic.d_star_tools",
        script="scripts/extract_d_star_tools_v2.py",
        description="Agentic — d*_tool catalog (per-tool direction vectors)",
        default_epochs=0,
        smoke_epochs=0,
        takes_epochs=False,
    ),
]


# ------------------ phase selection ----------------------------------------

ALIAS_MAP = {
    "all": None,  # resolved below
    "dispositional": [p.name for p in DISPOSITIONAL_PHASES],
    "agentic": [p.name for p in AGENTIC_PHASES],
    "d_star": ["d_star"],
    "a": ["a.v21", "a.v21_1", "a.v21_2", "a.v21_4"],
    "b": ["b"],
    "d": ["d"],
}
ALIAS_MAP["all"] = ALIAS_MAP["dispositional"] + ALIAS_MAP["agentic"]


def resolve_phases(spec: str) -> list[PhaseSpec]:
    """Parse --phases argument into a list of PhaseSpec objects.

    Accepts:
      - aliases from ALIAS_MAP ("all", "dispositional", "agentic", "a", "b", "d", "d_star")
      - explicit phase names ("a.v21", "agentic.d_star_repeat")
      - comma-separated mix ("a,b,d", "dispositional,agentic.d_star_repeat")
    """
    all_phases = {p.name: p for p in DISPOSITIONAL_PHASES + AGENTIC_PHASES}
    tokens = [t.strip() for t in spec.split(",")]
    selected_names: list[str] = []
    for t in tokens:
        if t in ALIAS_MAP:
            for n in ALIAS_MAP[t]:
                if n not in selected_names:
                    selected_names.append(n)
        elif t in all_phases:
            if t not in selected_names:
                selected_names.append(t)
        else:
            raise SystemExit(
                f"unknown phase: {t!r}. Valid: "
                f"aliases={list(ALIAS_MAP)}, phases={list(all_phases)}"
            )
    return [all_phases[n] for n in selected_names]


# ------------------ runner -------------------------------------------------

def run_phase(phase: PhaseSpec, preset: ModelPreset, *, smoke: bool,
              dry_run: bool, env: dict | None = None) -> int:
    """Execute one phase. Returns subprocess returncode (0 = ok)."""
    cmd = phase.command(preset, smoke)
    print()
    print("=" * 70)
    print(f"[hexis.train] {phase.name}: {phase.description}")
    print(f"  preset:  {preset.name} ({preset.hf_id})")
    print(f"  epochs:  {phase.smoke_epochs if smoke else phase.default_epochs}"
          f"{'  [SMOKE]' if smoke else ''}")
    print(f"  cmd:     {' '.join(shlex.quote(c) for c in cmd)}")
    print("=" * 70)
    if dry_run:
        print("[hexis.train] dry run — not executing")
        return 0

    t0 = time.time()
    result = subprocess.run(
        cmd, cwd=str(REPO_ROOT),
        env={**os.environ, **(env or {})},
    )
    wall = time.time() - t0
    print(f"\n[hexis.train] {phase.name} exited rc={result.returncode} "
          f"in {wall/60:.1f}min")
    return result.returncode


def main() -> int:
    ap = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=__doc__,
    )
    ap.add_argument("--preset", required=True,
                    help=f"Model preset. Available: {', '.join(list_presets())}")
    ap.add_argument("--phases", default="all",
                    help="Phases to run. Aliases: all, dispositional, agentic, "
                         "a, b, d, d_star. Or explicit phase names (comma-sep). "
                         "Examples: 'all', 'dispositional', 'a,b,d', 'agentic.d_star_repeat'")
    ap.add_argument("--smoke", action="store_true",
                    help="Truncate epochs to 5 per phase for sanity-checking. "
                         "Checkpoints will be named [SMOKE] — do NOT use for real training.")
    ap.add_argument("--dry-run", action="store_true",
                    help="Print commands without executing.")
    ap.add_argument("--stop-on-fail", action="store_true", default=True,
                    help="Stop the pipeline on first phase failure (default: True)")
    ap.add_argument("--continue-on-fail", dest="stop_on_fail", action="store_false",
                    help="Continue running subsequent phases even if one fails")
    args = ap.parse_args()

    preset = get_preset(args.preset)
    phases = resolve_phases(args.phases)

    print("=" * 70)
    print(f"[hexis.train] starting pipeline")
    print(f"  preset:   {preset.name}  (d_model={preset.d_model}, "
          f"n_layers={preset.n_layers}, rank={preset.rank})")
    print(f"  phases:   {[p.name for p in phases]}")
    print(f"  smoke:    {args.smoke}")
    print(f"  dry_run:  {args.dry_run}")
    print("=" * 70)

    failed: list[str] = []
    t_pipeline = time.time()
    for phase in phases:
        rc = run_phase(phase, preset, smoke=args.smoke, dry_run=args.dry_run)
        if rc != 0:
            failed.append(phase.name)
            if args.stop_on_fail:
                print(f"\n[hexis.train] STOPPING — {phase.name} failed (rc={rc}).")
                break

    total = time.time() - t_pipeline
    print("\n" + "=" * 70)
    print(f"[hexis.train] pipeline complete in {total/60:.1f}min")
    if failed:
        print(f"[hexis.train] FAILED phases: {failed}")
        return 1
    print("[hexis.train] all phases succeeded.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
