#!/usr/bin/env bash
# Compile the HEXIS paper (main_v2.tex) end-to-end with bibliography.
# Run from anywhere: produces paper/main.pdf at the paper root.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC_DIR="$SCRIPT_DIR/sections"
JOB="main_v2"

cd "$SRC_DIR"

run_pdflatex() {
    local pass=$1
    echo "[compile] pdflatex pass $pass"
    if ! pdflatex -interaction=nonstopmode -halt-on-error "$JOB.tex" >"/tmp/${JOB}_pass${pass}.log" 2>&1; then
        echo "[compile] pdflatex pass $pass FAILED. Last errors:"
        echo "----------------------------------------"
        grep -A 2 -E "^!|Fatal error" "/tmp/${JOB}_pass${pass}.log" | head -40 || tail -40 "/tmp/${JOB}_pass${pass}.log"
        echo "----------------------------------------"
        echo "Full log: /tmp/${JOB}_pass${pass}.log  (also $SRC_DIR/$JOB.log)"
        exit 1
    fi
}

run_pdflatex 1

echo "[compile] bibtex"
if ! bibtex "$JOB" >/tmp/${JOB}_bibtex.log 2>&1; then
    echo "[compile] bibtex FAILED:"
    cat /tmp/${JOB}_bibtex.log
    echo "Also see $SRC_DIR/$JOB.blg"
    exit 1
fi

run_pdflatex 2
run_pdflatex 3

cp "$SRC_DIR/$JOB.pdf" "$SCRIPT_DIR/main.pdf"
echo "[compile] done -> $SCRIPT_DIR/main.pdf"
