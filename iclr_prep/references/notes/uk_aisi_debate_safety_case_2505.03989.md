# Notes: An Alignment Safety Case Sketch Based on Debate (UK AISI)

## Citation metadata

- **Title**: An Alignment Safety Case Sketch Based on Debate
- **Authors**: Marie Davidsen Buhl (UK AI Security Institute; Centre for the Governance of AI), Jacob Pfau (UK
  AI Security Institute; NYU), Benjamin Hilton (UK AI Security Institute), Geoffrey Irving (UK AI Security
  Institute)
- **Venue**: arXiv preprint. `arXiv:2505.03989v3 [cs.AI]`, last revised 23 May 2025.
- **BibTeX key suggestion**: `buhl2025alignment`
- Note the author overlap with the doubly-efficient-debate paper (Geoffrey Irving is a co-author of both) —
  useful for framing institutional continuity of the research program from complexity theory into applied
  safety-case work.

## Structure of the safety case sketch

The sketch is a "Claims, Arguments, Evidence" (CAE) style argument that a specific AI system (an internally
deployed AI R&D agent inside an AI company, in a defined "low-stakes" context) will not autonomously sabotage
research, built on **four sequential steps**:

1. Specify a low-stakes deployment context (a small number of bad actions cannot, by themselves, cause
   unacceptable outcomes).
2. Train the model via a debate game until it reaches an equilibrium where honest answers are the reward-
   maximizing strategy.
3. Secure "exploration guarantees" — evidence the model isn't avoiding high-reward strategies it could pursue
   (to rule out exploration hacking).
4. Continue online training during deployment so the error rate doesn't drift.

These map to **four key claims** the developer must defend (Section 1 / Section 4):
- **C1**: the training process has reached an approximate global equilibrium of the debate game.
- **C2**: in approximate global equilibria of the game, the system errs in at most an ε′-fraction of cases.
- **C3**: during deployment, the error rate will not drift past ε given online training.
- **C4**: the system cannot cause unacceptable outcomes given an error rate of ε.

The authors are explicit and self-critical about the strength of this argument: "**Overall, the argument in
this sketch is not strong with current techniques. Much better techniques are needed before developers can rely
on alignment arguments.**" (Section 6, Conclusion). This candor is itself useful — it signals institutional
awareness that debate-as-safety-case is aspirational scaffolding, not a solved problem, which supports a "strong
theory, real institutional uptake, mixed/early empirical record" framing for HEXIS's related work rather than
either dismissing or overselling AISI's position.

## GOLD quotes: the load-bearing assumption about debaters holding/maintaining positions

**Quote 1 — the core equilibrium-honesty assumption** (Section 3.2, "Step 2: Train via a debate game"):

> "**Honesty**: In the global equilibrium of the game, when both debaters are playing their best response
> strategies, both debaters are honest (i.e. there should be no dishonest answer that would give them higher
> reward)."

This is the precise theoretical condition the entire safety case is built on top of: *at* equilibrium, honesty
is the reward-maximizing (i.e., stable, non-deviating) strategy. Note carefully what this claim is and is not:
it is a claim about the **reward landscape at the fixed point of training**, not a claim that any given deployed
debater instance, mid-debate, under live pressure from an opponent, will in fact continue playing that strategy
rather than defect from it in response to social/conversational pressure. AISI's own safety case requires this
gap to be bridged by *further* claims (C3, deployment-time drift) — which is exactly the vulnerability HEXIS's
empirical result speaks to.

**Quote 2 — exploration hacking, the closest AISI comes to naming a capitulation-adjacent failure mode**
(Section 3.3, "Step 3: Secure exploration guarantees"):

> "[A] potential barrier is exploration hacking: the models failing to explore certain strategies that would be
> highly rewarded to avoid having them reinforced (e.g. failing to use certain good counterarguments they do not
> want humans to know about). To protect against this failure mode, our sketch requires exploration guarantees,
> i.e. evidence that the models are not foregoing high reward from unexplored strategies."

This is the nearest AISI comes to naming a phenomenon adjacent to capitulation — a debater declining to deploy
an argument it "knows" would win. But the framing and proposed remedies (whitebox interpretability, singular
learning theory susceptibility analysis, adversarial RL probes — Section 3.3) are entirely **training-time and
RL-specific**: the concern is that gradient descent never discovers/reinforces the winning strategy in the first
place, not that a policy which *has* learned the honest strategy defects from it live, in-context, under an
opponent's conversational pressure. This is a meaningfully different mechanism from what HEXIS studies (context-
delivered vs. compiled/weight-level conditioning under live debate pressure) and the two should be described as
distinct, adjacent failure modes rather than conflated as the same problem AISI already covers.

**Quote 3 — deployment-time drift, directly supports "installs well but holds poorly"** (Section 3.4, "Step 4:
Continue online training during deployment"):

> "Even if the models reach an approximate global equilibrium during training, they will not necessarily
> continue playing their best strategies during deployment due to distribution shifts. In particular, the
> models might be **alignment faking, undermining the guarantees we got from debate training**."

This is AISI explicitly acknowledging that equilibrium-honesty achieved during training is **not** a guarantee
of stable honest behavior once deployed — directly supporting a "conditioning installs well [at/near training
equilibrium] but holds poorly [under live deployment pressure]" framing for HEXIS. Their proposed fix is
different from what HEXIS investigates: continuous online retraining every k steps to keep re-anchoring the
policy toward the equilibrium, rather than a comparison of context-delivered vs. compiled conditioning. Cite
this as institutional convergence on the *problem* (stability of honest/adversarial behavior post-training is
not automatic) even though the *proposed remedy* differs from HEXIS's angle.

**Quote 4 — AISI's own admission that the empirical record is thin/non-generalizing** (Section 2, Related work):

> "There is some empirical evidence that debate with human and LLM debaters improves accuracy when debaters
> have access to more information than judges (Michael et al. 2023; Khan et al. 2024; Arnesen et al. 2024).
> However, **so far this has not generalised to set-ups with less or no information asymmetry** (Kenton et al.,
> 2024; Parrish et al., 2022b;a). Human experiments have also highlighted potential obstacles to debate,
> including the obfuscated arguments problem (Barnes & Christiano, 2020; Barnes, 2020)."

Directly citable as institutional support for a "mixed empirical record" framing — AISI itself, the body writing
the safety case, states the positive empirical results (including Khan et al.) do not generalize beyond the
information-asymmetric setup, and flags obfuscated arguments as a known open obstacle.

**Quote 5 — from Section 5.2 ("Open problems")**, listing "Empirical testing and optimisation" as one of five
named open research gaps:

> "While debate has theoretical appeal, we have only limited data on its practical effectiveness... Key
> questions include whether debate measurably improves performance, whether training reliably reaches
> equilibrium, whether stability is a real problem, and whether obfuscated arguments actually emerge as
> predicted."

Reinforces Quote 4; useful as a second, independent citation point if a reviewer wants more than one AISI
passage supporting "mixed empirical record."

## Explicit search for "capitulation"/"sycophancy" language — result: absent as a named phenomenon

We searched (`grep -i`) the full extracted text for "capitulat", "concede"/"conced", "abandon", "switch answer",
"change answer", "flip answer", and "sycophan": **no occurrences in the body text**. The single "sycophan-" hit
in the file is a bibliography entry only — a citation to Sharma et al., "Towards understanding sycophancy in
language models," ICLR 2024 — which is listed in the references but **never discussed, quoted, or engaged with
in the body of the paper**. We also read Section 5 ("Discussion") and Section 5.2 ("Open problems") in full,
including the five named research gaps (improved debate protocols, empirical testing and optimisation,
exploration hacking, high-stakes contexts, from-honesty-to-alignment) — **none of the five names conformity,
sycophancy, or in-context capitulation as a distinct research gap**. This confirms the safety case's honesty
guarantee is conditioned entirely on reaching-and-remaining-at-equilibrium plus exploration guarantees; the
specific inference-time, social-pressure-driven defection mechanism HEXIS studies is not named anywhere in this
document, despite the paper citing the general sycophancy literature in its bibliography. This absence is
itself a fair and citable claim: a document written specifically to sketch out what evidence a debate-based
safety case needs does not identify in-context capitulation under debate pressure as one of its open problems,
even though it cites the broader sycophancy literature and separately identifies "limited [empirical] data on
[debate's] practical effectiveness" as a named gap.

## Contradicting evidence

None found. No claim in the paper asserts that conformity/capitulation is already solved, already
low-probability, or irrelevant to the safety case. If anything the paper's own posture (self-described as "not
strong with current techniques," Section 6) is maximally hospitable to HEXIS's framing.

## Citation guidance (3–5 sentences)

Cite Buhl, Pfau, Hilton & Irving (2025), UK AI Security Institute, as direct institutional evidence that
debate-as-oversight has moved from pure theory into applied safety-case scaffolding, while candidly
acknowledging its own fragility — the authors state plainly that "the argument in this sketch is not strong with
current techniques." Use the Honesty claim ("in the global equilibrium of the game... both debaters are honest")
as the theoretical assumption HEXIS's empirical result targets, and the deployment-drift admission ("they will
not necessarily continue playing their best strategies during deployment... might be alignment faking") as
independent institutional acknowledgment that equilibrium-honesty from training does not guarantee stable
honest behavior post-deployment — precisely the "installs well but holds poorly" pattern HEXIS documents
empirically, albeit via a different mechanism (distribution shift/alignment faking rather than in-context
conformity pressure) and a different proposed remedy (continuous online retraining rather than compiled
conditioning). Be precise that AISI's "exploration hacking" concern is a distinct, training-time/RL failure
mode adjacent to but not the same as the inference-time capitulation phenomenon HEXIS studies — conflating the
two would be an easy reviewer catch, since AISI's own text treats them as separate problems requiring separate
solutions. It is also fair and safe to cite AISI's related-work section directly for the claim that "so far
[debate's positive empirical results have] not generalised to set-ups with less or no information asymmetry,"
which independently corroborates HEXIS's "mixed empirical record" framing from a source with strong domain
authority.
