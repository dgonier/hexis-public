# NeurIPS 2026 Submission Guidelines — Key Constraints

## Critical Dates

| Milestone | Date |
|-----------|------|
| Abstract submission deadline | **May 4, 2026 AOE** |
| Full paper submission deadline | **May 6, 2026 AOE** |
| Author notification | September 24, 2026 AOE |
| Conference | December 6-12, 2026 (San Diego area) |

**Author additions/removals prohibited after May 4.** Title/abstract editable until May 6 but placeholders risk desk rejection.

## Page Limits

- **Main paper: 9 content pages** (figures/tables count)
- References + paper checklist + appendix do NOT count
- **Appendix: unlimited pages**, up to 100MB
- Camera-ready: 10 content pages
- PDF max: 50MB, supplementary ZIP: 100MB

## Formatting

- Official NeurIPS 2026 LaTeX template (mandatory)
- Text area: 5.5" wide, 9" tall; left margin: 1.5"
- Font: 10pt Times New Roman, 11pt leading
- Use `\usepackage[preprint]{neurips_2026}` for arXiv
- **Style violations = desk rejection**

## Contribution Types

Must select one: General, Theory, Use-Inspired, Concept & Feasibility, Negative Results.
HEXIS is likely **"General"** or **"Use-Inspired"**.

## Review Criteria (scored 1-4 each)

- **Quality**: Technical soundness, well-supported claims
- **Clarity**: Clear writing, sufficient detail for reproducibility
- **Significance**: Community impact, advancement of understanding
- **Originality**: Novel insights

## Key Policies

- **Double-blind**: No identifying info. Self-cite as "Smith et al." not "our prior work"
- **Dual submission**: No simultaneous archival submissions
- **Preprints**: Allowed on arXiv. Must NOT say "Under review at NeurIPS"
- **Contemporaneous work cutoff**: March 1, 2026
- **AI content**: If LLM is non-standard component of method, describe in experimental setup. Routine assistance = no disclosure needed.
- **Ethics review**: Possible flag by reviewers. Code of Ethics covers human subjects, privacy, societal impact.
- **Reproducibility**: Paper checklist mandatory. Code submission strongly encouraged (anonymized ZIP).
- **OpenReview profiles**: All authors must have updated profiles by May 6
- **At least one author must register in-person** for accepted papers

## Rebuttal

- Per-review: 10,000 characters
- Markdown/LaTeX supported
- New results permissible but original submission is basis for decision

## Our Timeline (5 weeks)

- **Week 1 (Mar 28 - Apr 3)**: Run clean benchmark reruns (#10-13), fix multi-turn attractor
- **Week 2 (Apr 4 - 10)**: Full 5-condition sweep (#16), orthogonality/perplexity reruns
- **Week 3 (Apr 11 - 17)**: ALFWorld learning curve, curation ablation, compile Phase 1 tables
- **Week 4 (Apr 18 - 24)**: Scale validation (9B/27B), paper writing sprint
- **Week 5 (Apr 25 - May 4)**: Final writing, figures, proofreading, submit abstract May 4
