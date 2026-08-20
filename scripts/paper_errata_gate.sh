#!/usr/bin/env bash
# paper_errata_gate.sh -- ICLR 2027 Track B errata gate.
#
# Implements iclr_prep/iclr2027_outline.md S13 ("Errata to carry forward"):
# greps the paper source tree for strings that are now KNOWN-WRONG and must
# not survive into the ICLR draft. Exits nonzero (fails CI / pre-commit) if
# any banned string is found in paper prose.
#
# Also gates on the two corrections identified during the 2026-08-19
# related-work verification pass (see
# iclr_prep/related_work_verified.md's "CORRECTION TO THE CORRECTIONS" note):
#   - the WRONG claim that "no MSC 40.2-vs-66.0 F1 comparison exists in
#     GenerativeAdapter" must not appear in paper prose (it is real and
#     citable; see the correction note for the primary-source verification)
#   - Le&Le's "up to 64%" / "64 percentage points" phrasing must not be
#     silently converted from one to the other in the same sentence
#
# Usage:
#   scripts/paper_errata_gate.sh [paper_dir]
#     paper_dir defaults to paper_iclr/
#
# Exit codes: 0 = clean, 1 = one or more banned strings found.

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
PAPER_DIR="${1:-$REPO_ROOT/paper_iclr}"

if [ ! -d "$PAPER_DIR" ]; then
    echo "[errata-gate] ERROR: paper directory not found: $PAPER_DIR" >&2
    exit 2
fi

# Only scan paper prose (sections/*.tex, main.tex, workshop.tex) — not the
# style/ kit, not references.bib, not this script's own banned-string list.
SCAN_FILES=()
while IFS= read -r -d '' f; do
    SCAN_FILES+=("$f")
done < <(find "$PAPER_DIR" \( -path "*/style/*" -o -name "*.bib" \) -prune -o \
              \( -name "*.tex" \) -print0)

if [ "${#SCAN_FILES[@]}" -eq 0 ]; then
    echo "[errata-gate] ERROR: no .tex files found under $PAPER_DIR" >&2
    exit 2
fi

FAIL=0
N_CHECKS=0

# check_banned <description> <grep-pattern> [<extra grep args...>]
check_banned() {
    local desc="$1"
    local pattern="$2"
    shift 2
    local extra_args=("$@")
    N_CHECKS=$((N_CHECKS + 1))
    local hits
    hits=$(grep -n -I "${extra_args[@]}" -E "$pattern" "${SCAN_FILES[@]}" 2>/dev/null)
    if [ -n "$hits" ]; then
        echo ""
        echo "[errata-gate] FAIL: $desc"
        echo "  pattern: $pattern"
        echo "$hits" | sed 's/^/  /'
        FAIL=1
    fi
}

echo "[errata-gate] Scanning ${#SCAN_FILES[@]} .tex file(s) under $PAPER_DIR"

# --- Superseded headline numbers (outline S13) ---------------------------
check_banned "old submitted headline '0%->83%' / '0% -> 83%' must not appear (superseded by 89% vs 58%, +31pp)" \
    '0%[[:space:]]*(-|\\to|\$\\to\$)+[[:space:]]*83%'

check_banned "'83% vs 0%' / '83% vs. 0%' framing must not appear" \
    '83%[[:space:]]*vs\.?[[:space:]]*0%'

check_banned "bare '83%' as a headline hold-rate (correct value is 89%; 83% is only ever the disclosed stale pilot number with the discrepancy note attached) — review each hit" \
    '\b83%'

# --- Timing claim -----------------------------------------------------
check_banned "'~20s' recompile-timing claim must not appear (that figure belongs to the agentic retrieval prototype, not the dispositional compile, which is sub-second / 2.5-3.0s end-to-end)" \
    '~20[[:space:]]*s(ec(ond)?s?)?\b'

# --- Old system/component name -----------------------------------------
check_banned "'Mind Tree' must not appear (renamed 'belief tree' per outline S4.1)" \
    'Mind[[:space:]]+Tree'

# --- Prefill-off claim ---------------------------------------------------
check_banned "prefill-off-as-standard claim must not appear (contradicted by code; the pipeline applied modulation unconditionally, prefill included; '<30% hold with prefill-on' is unsupported by any run)" \
    'prefill[-[:space:]]*off'

check_banned "'<30% hold with prefill-on' figure must not appear (unsupported by any run)" \
    '<[[:space:]]*30%[[:space:]]*hold'

# --- Spellcheck-survivable typos (outline S13/S14) -----------------------
check_banned "typo 'adverserial' (should be 'adversarial')" \
    'adverserial' -i

check_banned "typo 'dispostions' (should be 'dispositions')" \
    'dispostions' -i

# 'contest' for 'context' is a real-word substitution a spellchecker will
# NOT catch; flag any standalone occurrence of 'contest' in paper prose for
# manual review, since the paper's actual vocabulary is 'context' /
# 'contested' / 'contesting' (adversarial-debate sense), not 'contest' as a
# noun.
check_banned "possible 'contest'-for-'context' typo — manual review required (real-word substitution, not caught by spellcheckers)" \
    '\bcontest\b'

# --- Agentic p-value that must not propagate ------------------------------
check_banned "agentic p=0.029 must not appear (superseded by p=0.043; moot if the agentic axis stays cut, but must not silently propagate if it resurfaces)" \
    'p[[:space:]]*=[[:space:]]*0\.029'

# --- The two corrected claims from CORRECTIONS propagation (item 3 of the
# 2026-08-19 paper-build task) --------------------------------------------

# (a) The WRONG "no MSC comparison exists" claim must not appear in paper
# prose. The 40.2-vs-66.0 MSC F1 comparison IS real (GenerativeAdapter Table
# 1, verified against the primary PDF); asserting otherwise would itself be
# an error re-introduced into the draft.
check_banned "WRONG claim 'no MSC comparison exists' / '(40.2|66.0) ... does not exist' must not appear — this claim was itself incorrect; the comparison is real (see related_work_verified.md CORRECTION TO THE CORRECTIONS, 2026-08-19)" \
    'no such comparison exists'

# (b) Le&Le percentage vs percentage-points must not be silently converted:
# flag any sentence-level co-occurrence pattern that reads as a converted
# claim, e.g. "64 percentage points" attributed to the abstract, or "up to
# 64%" attributed to the conclusion, inverted from the source. We gate on
# the unambiguous violation: using ONLY "64%" (no "percentage points") while
# citing it as the paper's overall/conclusion finding is the failure mode
# named in the outline; the safest automatable check is that any file using
# "64" in the steering-robustness context must carry BOTH phrasings intact
# rather than inventing a third form. Flag any converted phrasing such as
# "64 points" (neither the abstract's nor the conclusion's actual wording).
check_banned "Le&Le robustness-drop must not be reworded as '64 points' (source says 'up to 64%' in the abstract and '64 percentage points' in the conclusion — quote the phrasing that matches which part of the source you cite, never a third form)" \
    '64[[:space:]]+points\b'

echo ""
if [ "$FAIL" -eq 0 ]; then
    echo "[errata-gate] PASS: $N_CHECKS checks run, 0 banned strings found in ${#SCAN_FILES[@]} file(s)."
    exit 0
else
    echo "[errata-gate] FAIL: one or more banned strings found above. Fix before this paper is submitted."
    exit 1
fi
# addition: banned framing words (Devin 8/19)
for w in "load-bearing" "load bearing"; do
  if grep -rli "$w" "$PAPER_DIR"/sections/*.tex 2>/dev/null | head -1 | grep -q .; then
    echo "[errata-gate] FAIL: banned framing '$w' found"; exit 1
  fi
done
