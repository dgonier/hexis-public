# Notes: Debating with More Persuasive LLMs Leads to More Truthful Answers

## Citation metadata

- **Title**: Debating with More Persuasive LLMs Leads to More Truthful Answers
- **Authors**: Akbir Khan*, John Hughes*, Dan Valentine* (equal contribution), Laura Ruis, Kshitij Sachan, Ansh
  Radhakrishnan, Edward Grefenstette, Samuel R. Bowman, Tim Rocktäschel, Ethan Perez. Affiliations: University
  College London, Speechmatics, MATS, Anthropic, Redwood Research, FAR AI.
- **Venue**: **Confirmed from the PDF text itself**: "Proceedings of the 41st International Conference on
  Machine Learning, Vienna, Austria. PMLR 235, 2024." — i.e., **ICML 2024**, published in PMLR volume 235.
- **Venue correction (important)**: the extracted text contains **no "best paper" designation anywhere**. Do
  **not** cite this as an ICML 2024 best paper without independent verification from ICML's own award
  announcements — the claim is not supported by the paper itself and should be treated as unverified/likely
  incorrect as currently stated in project notes.
- **arXiv**: `arXiv:2402.06782v4 [cs.AI]`, last revised 25 Jul 2024.
- **BibTeX key suggestion**: `khan2024debating`

## Precise headline empirical numbers

All figures are on the QuALITY reading-comprehension dataset (Pang et al. 2022), HARD subset, in an
information-asymmetric setup: expert debaters/consultants see the source text, non-expert judges do not.

- **Non-expert human judges**: 88% accuracy using debate, vs. **60%** naive baseline (no expert access at all),
  vs. **78%** with consultancy (single expert, non-adversarial baseline).
- **Non-expert LLM judges**: 76% accuracy using debate, vs. **48%** naive baseline, vs. **54%** with consultancy.
- **Expert human ceiling** (full text access): cited from Pang et al. (2022) at **89%** on the HARD subset,
  used as an approximate upper-bound reference, not independently re-measured by Khan et al.
- Across all protocols, human judges outperform LLM judges — the paper explicitly flags this as suggesting
  "limitations of current LLMs for automated scalable oversight" (Figure 1 caption).

**Persuasiveness-optimization effect (Finding 2, stated precisely)**: using inference-time optimization
(best-of-N sampling and critique-and-refinement, judged by a preference model scoring for judge approval),
debaters optimized for persuasiveness become **better at arguing the correct answer relative to the incorrect
answer**, which **increases** judge accuracy — and this effect generalizes to held-out judges whose preferences
were not used in the optimization. By direct contrast, in the non-adversarial **consultancy** condition, judge
accuracy **decreases** as the single consultant becomes more persuasive. This asymmetry (persuasion optimization
helps under debate, hurts under consultancy) is the paper's central positive claim for the value of adversarial
structure specifically.

## The capitulation / adversarial-stability quote-hunt — result: not discussed, and structurally excluded

We searched exhaustively (`grep -i` "capitulat", "concede"/"conced", "abandon", "sycophan") across the full
4,674-line extracted text: **zero occurrences**. There is also no "Discussion" or "Limitations" section heading
anywhere in the extracted text — the paper does not explicitly engage the question of debaters
capitulating/conforming, for or against.

More importantly, a structural detail in the protocol (Section 2.1/2.3) makes this silence unsurprising rather
than a gap: **each debater is assigned a fixed answer for the entire match** ("At the start of a round, debaters
receive nearly-identical prompts explaining the game, their assigned answer, and the current transcript" — the
debater argues that one assigned answer for the full N-round debate; win rate is defined per fixed assignment,
Eq. 1–2). The protocol design does not include any mechanism, prompt, or scoring rule that would let a debater
switch or abandon its assigned position mid-debate — there is no "concede" action in the game as specified. This
means Khan et al.'s debaters **cannot exhibit capitulation as HEXIS defines and measures it**, not because the
phenomenon was tested and found absent, but because the experimental design holds the adversarial assignment
fixed by construction.

**This is worth stating precisely in the paper**: Khan et al. measure what happens when the adversarial
structure (opposed, fixed positions) is *maintained* — and they find, under that condition, that increasing
persuasiveness helps rather than hurts oversight. This is fully consistent with, and does not contradict,
HEXIS's contribution: we study what happens when the fixed-assignment premise itself breaks down (a debater
drifts off its assigned position under conversational/conformity pressure), which is a distinct experimental
question Khan et al.'s design cannot speak to either way. The relationship should be framed as "orthogonal and
complementary," not "in tension."

## Contradicting evidence

The one result requiring careful handling is the persuasiveness-optimization finding itself: if read
uncharitably, "more persuasive debaters make judges *more* accurate" could be paraphrased as "sycophancy/
persuasion isn't a problem for debate," which would look like it cuts against HEXIS's framing. **This is not
what the paper claims** — persuasiveness here means becoming better at *marshaling true arguments and quotes
for the correct side* under a fixed, fully adversarial win condition, not persuading the judge to abandon a
correct assessment via non-truth-tracking means, and it says nothing about a debater's own commitment to its
assigned position, only about a preference-model-optimized policy improving argument quality. We should state
this distinction explicitly rather than let a reviewer discover it: Khan et al.'s "persuasiveness" is a property
of argument quality under a maintained adversarial structure, not a measure of whether the debater keeps
arguing consistently for its assigned side (which their protocol enforces by design and does not measure as a
variable).

## Citation guidance (3–5 sentences)

Cite Khan et al. (2024), ICML/PMLR 235 — not as an ICML best paper unless independently confirmed — as the
strongest available empirical evidence that debate-format oversight outperforms non-adversarial baselines: with
debate, non-expert human judges reach 88% accuracy (vs. 60% naive, 78% consultancy) and non-expert LLM judges
reach 76% (vs. 48% naive, 54% consultancy) on QuALITY-HARD, and persuasiveness-optimized debaters make judges
*more* accurate while persuasiveness-optimized consultants make judges *less* accurate. When citing this
alongside HEXIS's capitulation result, note explicitly that Khan et al.'s protocol assigns each debater a fixed
position for the full match with no mechanism for switching sides — their positive result is evidence that
debate works well precisely *when* the adversarial structure is held fixed, which sharpens rather than
contradicts HEXIS's finding that this fixed-structure assumption is itself fragile under the pressures we study.
Do not cite this paper as showing that sycophancy/capitulation is a non-issue for debate — the paper's design
does not test for it either way.
