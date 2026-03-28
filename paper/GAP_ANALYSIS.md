# Gap Analysis: What We Have vs What We Need

## Status Legend
- DONE = have clean numbers, ready for paper
- DIRTY = have numbers but need clean rerun
- STUB = section skeleton written with [XX] placeholders
- MISSING = no data, experiment not run

---

## Data Gaps (Experiments to Run)

### HIGH PRIORITY (paper won't submit without these)

| # | Experiment | Status | Blocking | Est. Time |
|---|-----------|--------|----------|-----------|
| 10-11 | Dilution sweep (D+F, 0-16K filler) | DIRTY | Table 4, abstract [XX] | overnight |
| 12-13 | Sycophancy sweep (7 rounds, 4+ topics) | DIRTY | Table 5, abstract [XX] | overnight |
| 16 | Full 5-condition LLM judge sweep | MISSING | Table 3 (main results table) | 1 day |

### MEDIUM PRIORITY (strengthen paper significantly)

| # | Experiment | Status | Blocking | Est. Time |
|---|-----------|--------|----------|-----------|
| 14 | d* orthogonality clean rerun | DIRTY | §5.7 number confirmation | 1 hour |
| 15 | Perplexity impact clean rerun | DIRTY | §5.7 number confirmation | 1 hour |
| 17 | ALFWorld learning curve (30 episodes) | MISSING | Figure 7 (learning plot) | 1 day |
| 19 | Curation ablation | MISSING | Appendix §J | half day |

### LOW PRIORITY (nice to have)

| # | Experiment | Status | Blocking | Est. Time |
|---|-----------|--------|----------|-----------|
| 18 | Multi-turn attractor fix | MISSING | Discussion §7.2 | ongoing |
| 20 | Online learning preferences | DIRTY | mention in §5 | half day |
| 21-26 | Scale validation (9B/27B) | MISSING | Appendix §L | 3-5 days |

---

## Section Gaps

### Abstract
- [XX] dilution % — needs experiment 10-11
- [XX] sycophancy % — needs experiment 12-13
- [XX] generation shortening % — can compute from existing data (D 52t vs B 138w)

### §1 Introduction
- Figure 1 placeholder — needs JSX → PDF rendering of fig-arch-comparison.jsx
- [XX] numbers in contributions — flow from experiments

### §2 Enmeshed Networks (NEW)
- Content is conceptual — mostly complete
- Need to verify Qwen3.5-4B-Base has 32 or 36 layers (check config)
- Design space table complete

### §3 HEXIS Architecture
- Training section is summary — full details deferred to Appendix A
- Need to verify: 32 vs 36 layers, layer types, which are patched
- d* extraction: 62 or 20+ topics? (paper-draft says 62, recipe says 20+)

### §4 Three-Layer Architecture
- Figure 4 placeholder — needs fig-three-layer.jsx → PDF
- [XX] dilution numbers — needs experiment 10-11
- All other data present

### §5 Experiments
- Table 3 (5-condition sweep): ALL [XX] — needs experiment 16
- Table 4 (dilution): ALL [XX] — needs experiments 10-11
- Table 5 (sycophancy): ALL [XX] — needs experiments 12-13
- Table 6 (ALFWorld): DONE
- Table 7 (curation): DONE
- §5.7 (orthogonality): DIRTY — needs clean reruns
- ALFWorld learning curve figure: MISSING — needs experiment 17

### §6 Related Work
- Mostly complete from paper-draft. Need to:
  - Add Schmidhuber fast weight programmers reference
  - Update any 2025-2026 references (check contemporaneous work)
  - Verify all citations are in references.bib

### §7 Discussion
- [XX] dilution numbers — same as above
- Multi-turn attractor: have description, mitigation is ongoing
- Credence sensitivity: complete (negative result)
- Unexplored design space: complete (conceptual)

### §8 Conclusion
- [XX] numbers flow from experiments

### Appendix
- All 16 sections are STUBs
- Source material exists for all of them (in plans/, observations/, reference docs)
- Priority: Training Curriculum (A), Architecture Evolution (B), Generation Examples (H)

---

## Figure Gaps

| Figure | Source | Status | Action |
|--------|--------|--------|--------|
| Fig 1: Arch comparison | fig-arch-comparison.jsx | HAVE JSX | Render to PDF/PNG |
| Fig 2: System overview | fig-system-overview.jsx | HAVE JSX | Render to PDF/PNG |
| Fig 3: Q/V modulation | fig-layer-modulation.jsx | HAVE JSX | Render to PDF/PNG |
| Fig 4: Three-layer | fig-three-layer.jsx | HAVE JSX | Render to PDF/PNG |
| Fig 5: Dilution curves | NEED DATA | MISSING | Run exp 10-11, then plot |
| Fig 6: Sycophancy | NEED DATA | MISSING | Run exp 12-13, then plot |
| Fig 7: ALFWorld curve | NEED DATA | MISSING | Run exp 17, then plot |

JSX → PDF: render in React, screenshot, or convert to TikZ/pgfplots for LaTeX.

---

## Template and Formatting

- [ ] Download official NeurIPS 2026 LaTeX template
- [ ] Update main_v2.tex to use neurips_2026.sty
- [ ] Set `\usepackage[preprint]{neurips_2026}` for arXiv
- [ ] Remove all author info for blind submission
- [ ] Add NeurIPS paper checklist (mandatory, doesn't count toward pages)
- [ ] Verify all figures fit within 5.5" text width
- [ ] 10pt Times New Roman, 11pt leading
- [ ] Total ≤ 9 content pages (not counting references + appendix)

---

## References to Add

- [ ] Schmidhuber (1992) fast weight programmers
- [ ] Check for 2025-2026 contemporaneous work on:
  - Implicit memory for LLMs
  - Enmeshed/side/parallel networks
  - Compiled representations
  - Mind Tree / cognitive schema approaches
- [ ] Qwen3.5 model paper (if available)
- [ ] ALFWorld citation
- [ ] Any NeurIPS 2025 papers on related topics

---

## Minimum Viable Paper (if time runs out)

9 pages on 4B results only. Still strong:
- §5: Tables 3-6 (all 4B, fill [XX] from experiments 10-16)
- Appendix: evolution narrative, training curriculum, generation examples
- Omit: scale validation (future work), learning curve (mention qualitatively)

The enmeshed network primitive + Mind Tree schema are the conceptual contributions.
4B validates the concept. Scale is explicitly future work.
