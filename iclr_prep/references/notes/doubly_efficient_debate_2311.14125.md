# Notes: Scalable AI Safety via Doubly-Efficient Debate

## Citation metadata

- **Title**: Scalable AI Safety via Doubly-Efficient Debate
- **Authors**: Jonah Brown-Cohen, Geoffrey Irving, Georgios Piliouras (all Google DeepMind)
- **Venue**: arXiv preprint. `arXiv:2311.14125v1 [cs.AI]`, submitted 23 Nov 2023. The extracted text contains no
  venue/conference acceptance notice — treat as an arXiv preprint unless a later peer-reviewed venue is confirmed
  independently (do not assume one).
- **BibTeX key suggestion**: `brown-cohen2023doubly`
- **Formalization artifact**: main theorem of Section 6 is also formalized in the Lean 4 theorem prover;
  code at https://github.com/google-deepmind/debate (stated in the paper, not independently verified by us).

## Precise theorem/result statements

The paper formalizes debate as a `(Ptime, Vtime, q)-debate protocol` (Definition 4.1): two provers `A`, `B` run
in time `Ptime`; verifier `V` runs in time `Vtime` and makes `q` oracle queries to a black-box representing human
judgement. A protocol decides language `L` with **completeness** `c` and **soundness** `s` if: for `x ∈ L`, the
honest prover wins with probability `≥ c` against *any* (including unbounded) opposing prover; for `x ∉ L`, no
prover can win with probability `> s`. When `c=1, s=0` the protocol *deterministically* decides `L`.

Two headline theorems (both in the deterministic setting):

- **Theorem 5.1**: For any language `L` decidable by an oracle Turing machine `M` in time `T = T(n)` and space
  `S = S(n)`, there exists an `(O(T log T), O(S log T), O(1))`-debate protocol deterministically deciding `L`.
  I.e., the honest prover runs in time only slightly more than the underlying computation (`T log T`), the
  verifier runs in time near-linear in the *space* used by the computation (not its full time `T`), using a
  constant number of oracle queries.
- **Theorem 5.3** (with cross-examination — independent, non-communicating copies of each prover can be
  queried): For any `L` decidable in time `T` with oracle queries of length `l`, there exists an
  `(O(T log T), O(l log T), O(1))`-debate protocol with cross-examination deterministically deciding `L`. This
  extends the result from bounded-space to **all of polynomial time**, with verifier time now near-linear in the
  query length `l` rather than the space bound `S`.
- Section 6 extends to **stochastic** oracles (modeling noisy/fuzzy human judgement) under an added
  **Lipschitzness/stability assumption**: the computation's output probability must not be overly sensitive to
  `O(1/T)`-scale perturbations in the oracle's response distribution. Without this stability assumption the
  stochastic-oracle results do not go through.

**The exact complexity-theoretic claim for "both prover and verifier polynomial-time"**: the *honest* prover
always runs in polynomial time (`O(T log T)`, itself polynomial when `T` is polynomial in `n`), and the verifier
always runs in sub-linear-to-near-linear time relative to the full computation with only `O(1)` oracle queries —
**but the dishonest opposing prover is explicitly allowed to be computationally unbounded** and the honest
strategy still wins. This is the paper's central advance over Irving et al. (2018), whose original debate
proposal modeled *both* provers as unbounded (and required the honest strategy to simulate deterministic AI
systems for exponentially many steps in the worst case — the exact limitation this paper is designed to remove).
So "doubly-efficient" specifically means: efficient honest prover *and* efficient verifier, with no efficiency
assumption placed on a potential adversary.

## The capitulation / adversarial-stability quote-hunt — result: theory is silent

We searched exhaustively (`grep -i` for "capitulat", "concede"/"conced", "abandon", "sycophan", "honest
strategy", "equilibrium", "Nash", "stable"/"deviat") and read the full paper. **No language anywhere addresses
debaters capitulating, conforming, or abandoning an assigned position under social/conversational pressure.**
The closest the paper comes to a stability claim is the framing (Sec 1, discussion around Def. 4.1): "this
requirement gives a complexity theoretic formalization of the intuitively desirable property that **debates
should be structured so that it is easier to tell the truth than to lie**." This is a claim about the protocol's
*incentive geometry under idealized optimal play* (a completeness/soundness gap that holds for any opposing
strategy, bounded or not) — it is not a claim that any concrete implemented debater, faced with a real
opponent's live pressure, will in fact play the honest strategy rather than defect from it. The model treats
provers as abstract oracle Turing machines executing optimal strategies; there is no notion in the formalism of
a debater mid-transcript changing its answer due to social pressure, deference, or persuasion by the opponent —
the theorem is a *worst-case guarantee over strategies*, not a *behavioral prediction about what strategies
real LLM debaters adopt*. This is the precise gap HEXIS's empirical result targets: the theory proves the
honest strategy is a winning strategy if played; it says nothing about whether real debaters play it, or
continue playing it once started.

## Contradicting evidence

None found. The paper does not engage behavioral debater failure modes (sycophancy, conformity, capitulation)
in either direction — it is a pure complexity-theory paper. Nothing here supports or undermines HEXIS's
empirical framing; it is simply orthogonal, which is itself the point worth making explicit (the theory this
proposal rests on has no representation of the failure mode in question).

## Citation guidance (3–5 sentences)

Cite Brown-Cohen, Irving & Piliouras (2023) as the strongest current complexity-theoretic grounding for
debate-based scalable oversight: it proves that an honest prover can win against an unbounded dishonest
opponent while itself running in polynomial time, with a verifier needing only a constant number of queries to
human judgement (Theorems 5.1, 5.3) — a substantial generalization of Irving et al.'s (2018) original proposal.
When citing it for HEXIS's significance argument, be precise that the "honest strategy wins" guarantee is a
worst-case game-theoretic result over abstract prover *strategies*, not an empirical or behavioral claim that
real LLM debaters will adopt or persist in the honest strategy — the paper never discusses capitulation,
conformity, or sycophancy, so it should be cited as establishing the theoretical soundness *conditional on*
debaters actually playing (and continuing to play) their assigned/optimal strategy, which is precisely the
condition our empirical results probe. Avoid implying the paper claims anything about LLM behavior under
social pressure — it doesn't, and overclaiming here would be an easy reviewer catch.
