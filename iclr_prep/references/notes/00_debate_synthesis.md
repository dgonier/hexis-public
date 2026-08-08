# Debate-as-oversight: synthesis for related work

## The honest one-paragraph state of the field

Debate-based scalable oversight rests on a genuinely strong theoretical foundation and has real institutional
uptake, but its empirical record on the specific behavioral assumption the theory needs is thin and, where it
exists, does not generalize. On the theory side, Brown-Cohen, Irving & Piliouras (2023) prove that a
computationally efficient honest debater can defeat an unbounded dishonest opponent while a verifier makes only
a constant number of queries to human judgement (Theorems 5.1, 5.3) — a substantial strengthening of Irving et
al.'s (2018) original proposal. On the institutional side, the UK AI Security Institute has built a full safety
case sketch on top of debate training for an internally deployed AI R&D agent (Buhl et al., 2025), explicitly
naming "in the global equilibrium of the game, when both debaters are playing their best response strategies,
both debaters are honest" as the load-bearing honesty claim the rest of the argument depends on. But both of
these are claims about behavior *at* an idealized equilibrium or under optimal play — neither is a claim about
what a concrete, deployed debater does when an opponent applies live conversational pressure, and AISI's own
text admits the gap explicitly, warning that even a system that reached equilibrium during training "will not
necessarily continue playing their best strategies during deployment... might be alignment faking, undermining
the guarantees we got from debate training." The empirical evidence available is real but narrow: Khan et al.
(2024, ICML/PMLR 235) show debate lifts non-expert judge accuracy substantially over non-adversarial baselines
(human judges 88% vs. 60% naive vs. 78% consultancy; LLM judges 76% vs. 48% naive vs. 54% consultancy) and that
optimizing debaters for persuasiveness improves rather than harms judge accuracy — but their protocol assigns
each debater a fixed position for the entire match with no mechanism to switch sides, so it cannot speak to
whether debaters hold that position under pressure; and AISI's own related-work discussion concedes that these
positive results "so far... [have] not generalised to set-ups with less or no information asymmetry." No source
we reviewed claims the position-holding assumption has been empirically validated under adversarial,
information-symmetric conditions; no source claims it has been shown to fail either. The honest summary is: the
theory needs debaters to hold positions, institutions are already building safety cases that assume they do,
and nobody has yet tested whether they do under the conditions that matter.

## The strongest defensible connecting sentence

> Debate's soundness guarantee is conditional on debaters playing (and continuing to play) their assigned or
> equilibrium strategy — a condition the theory assumes ("debates should be structured so that it is easier to
> tell the truth than to lie," Brown-Cohen et al. 2023) and an applied safety case now depends on explicitly
> ("in the global equilibrium of the game, when both debaters are playing their best response strategies, both
> debaters are honest," Buhl et al. 2025) — but which the same safety case's authors concede is not guaranteed
> to hold post-training ("they will not necessarily continue playing their best strategies during deployment...
> might be alignment faking, undermining the guarantees we got from debate training," Buhl et al. 2025), and
> which no existing empirical study has directly tested, since the one large-scale empirical debate study
> available (Khan et al. 2024) structurally holds debater assignments fixed for the full match rather than
> measuring whether debaters maintain them under pressure.

This sentence is defensible because every clause is a direct, attributable claim from the source text (not an
inference we are making on the authors' behalf), it does not overstate what any single paper says, and it
explicitly names the gap between "theory/safety-case assumes position-holding" and "nobody has measured
position-holding under adversarial pressure" — which is exactly the gap HEXIS's empirical result (conditioning
installs well but holds poorly via context; the inverse pattern via compiled conditioning) is positioned to
fill.

## Anything that failed to check out / complications for the framing

- **Khan "best paper" claim**: the ICML 2024 / PMLR 235 venue is confirmed directly from the PDF text, but no
  "best paper" designation appears anywhere in the paper itself. This should not be asserted in the manuscript
  without independent verification (e.g., checking ICML 2024's official award list) — currently unconfirmed and
  likely should be dropped or hedged.
- **Khan's persuasiveness-optimization finding** is the one result requiring careful handling: read
  superficially, "debaters optimized for persuasiveness make judges *more* accurate" could look like evidence
  that persuasion/sycophancy pressure isn't a problem for debate, which would cut against HEXIS's framing. On
  inspection this is not in tension — the result is about argument-quality optimization under a *structurally
  fixed* adversarial assignment (their protocol has no mechanism for a debater to switch sides), so it says
  nothing about whether debaters hold their assigned position under pressure. It should be read as showing
  debate works well when the adversarial structure is intact, which is compatible with (and arguably
  strengthens the stakes of) HEXIS's finding that the structure itself is fragile.
- **AISI's "exploration hacking"** is the closest existing safety literature comes to naming a
  capitulation-adjacent failure mode, and it would be easy to overstate the overlap. It is a *training-time,
  RL-specific* concern (a policy failing to discover/reinforce a winning strategy via gradient descent) distinct
  from the *inference-time, social-pressure-driven* defection HEXIS studies. The two should be presented as
  adjacent but distinct failure modes in related work, not conflated — AISI's own document treats them as
  separate open problems.
- No source directly contradicts HEXIS's significance argument. The doubly-efficient-debate paper is simply
  silent on behavioral debater dynamics (pure complexity theory); Khan's design cannot test capitulation by
  construction; AISI names the assumption and independently flags the deployment-time stability gap, which
  supports rather than undermines the framing.
