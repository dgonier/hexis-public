# Positioning, Significance, and the Debate Literature

Companion to the ICLR outline. Covers three things the paper currently lacks: where the
mechanism sits on the existing menu, what the result licenses claiming about persistent
identity, and why debate is the application that makes the result matter.

**Verify every citation below before use.** These were assembled from search; arXiv IDs and
author lists need checking against the actual papers, and several are recent enough that
venue status may have changed.

---

## Part 1 — The three nearest algorithms

### The uncomfortable finding first

The paper currently claims a new architectural primitive. It is not one. Mapping a
conditioning input through a frozen host's hidden states into low-rank adapter parameters
in a single forward pass is an established and currently very active line:

| Work | What it maps | Venue |
|---|---|---|
| HyperTuning (Phang et al.) | task description → PEFT params | 2023 |
| **GenerativeAdapter (Chen et al.)** | **context → low-rank adapter via frozen LM hidden states** | **ICLR 2025** |
| Text-to-LoRA (Charakorn et al.) | task description → LoRA | 2025 |
| Doc-to-LoRA (Charakorn et al., Sakana) | document → LoRA, "parametric memory" | 2026 |
| SHINE (2602.06358) | context → LoRA, reusing frozen LLM params in-context | 2026 |
| Zhyper, HyperLoRA, Video2LoRA, Code2LoRA | various conditioning inputs → LoRA | 2025–26 |

**GenerativeAdapter is not cited in the submission and is close enough that a reviewer who
knows it will treat the omission as a novelty problem rather than an oversight.** Frozen
base LM, hidden states from a context pass, a trained generator producing low-rank
per-layer parameters, one forward pass, no gradient updates, and it explicitly evaluates
personalization and memorising user information from conversation. That is the same
architecture described in different words.

**This is survivable, and arguably good news, provided the claim is restated.** The
contribution is not the architecture. It is the evaluated property and the dissociation —
neither of which any paper in that table measures.

### Closest #1 — GenerativeAdapter (Chen et al., ICLR 2025), and the hypernetwork-adapter family

**Shared:** frozen host; hidden states as the bridge; low-rank per-layer parameters; single
forward pass; no gradient descent per adaptation; zero context tokens at query time.

**Different, and this is the whole paper:** every method in that family is evaluated on
*acquisition* — StreamingQA F1, MetaICL accuracy, document recall, EM on repo code. The
question is always "did the content get in?" None of them asks whether what got in
*survives an interlocutor who argues against it*.

The result cuts across their grain in a way that is genuinely informative rather than
merely differentiating. Compiled modulation is **worse** than context at installation
(46% vs 98%) and **better** at persistence (89% vs 58%). A literature optimising the
acquisition metric would score this mechanism poorly and never see the property it
actually has. That is a real finding about an existing family, and it is a better
contribution than "we built a thing."

**How to write it:** *We adopt the hypernetwork-adapter formulation established by
GenerativeAdapter and the Text-to-LoRA line, and evaluate it on a property that line does
not measure: retention of a conditioned stance under sustained adversarial pressure. On the
acquisition metrics those papers optimise, compiled conditioning underperforms simple
prompting. The contribution is the dissociation.*

Cite them as method precedent, in the mechanism section, not buried in related work. Owning
the lineage is far cheaper than being caught claiming novelty over it.

### Closest #2 — Contrastive activation addition / representation engineering

Zou et al. 2023 (RepEng); Turner et al. 2023 (ActAdd); Rimsky et al. (CAA).

**Shared:** inference-time modification of internal activations; no gradient updates to the
host; content derived from contrastive examples; conditioning invisible in the prompt.

**Different:** a steering vector is a single fixed direction applied identically regardless
of input. Compiled modulation is (a) multi-dimensional — rank 16 across 11 layers, (b)
query-conditioned, because the low-rank update acts on the live hidden state, and (c)
derived from structured content rather than a contrast set.

**You have the head-to-head, and it is the strongest single result in the paper**: tuned
CAA from identical belief content reaches 42% injection (matching compiled's 46%) and
**14% hold under pressure against compiled's 89%**. Two further details worth reporting,
because they are mechanism evidence rather than scorekeeping:

- Best CAA config was a *single* mid-network layer at scale 8. Naive injection across all
  the layers compiled modulation drives degenerates generation at every scale. A fixed
  direction cannot be applied everywhere; a content-derived, query-conditioned update can.
- Independent corroboration exists. A June 2026 systematic stress test of activation
  steering under adversarial input perturbation (arXiv 2606.07696) reports directional
  robustness dropping by up to 64pp, post-attack confidence collapsing at or below 0.25
  across four extraction methods and five models 1.5B–30B, and the optimal steering layer
  shifting by up to 17 positions under perturbation. Your 14% is not an artifact of a
  weak baseline — it is the known behaviour of the method class under exactly this stress.

**How to write it:** steering and compiled modulation are the same *kind* of intervention
at different dimensionality, and the dimensionality is what persistence costs.

### Closest #3 — Prefix and prompt tuning

Li & Liang 2021; Lester et al. 2021.

**Shared:** learned conditioning that is not natural-language text; the model cannot read
it as an assertion; no modification of host weights.

**Different:** prefix vectors occupy context positions, so they compete for attention and
dilute; they are learned by gradient descent per task and fixed thereafter.

**This is the baseline you still owe, and it is the sharpest one**, because it separates
two things the paper currently conflates. Compiled modulation is both *outside the context
window* and *not inspectable as assertable text*. Prefix tuning is the second without the
first. If prefix tuning holds under pressure, the operative variable is inspectability. If
it collapses like context does, the operative variable is position. Either answer is
publishable; not running it leaves the paper's causal story underdetermined, and this is
exactly the gap the 8JtD review named.

### The one-paragraph positioning for the paper

> Compiled conditioning belongs to the hypernetwork-adapter family: a trained write function
> maps a structured input, encoded through the frozen host, to per-layer low-rank parameters
> in a single forward pass, in the manner of GenerativeAdapter and Text-to-LoRA. It differs
> from that family in what is conditioned on (a typed belief store rather than a task
> description or document) and, more importantly, in what is measured: those methods are
> evaluated on knowledge acquisition and task accuracy, where we find compiled conditioning
> is *weaker* than prompting. It differs from activation steering in dimensionality and
> query-conditioning, which is what the persistence result turns on. It differs from prefix
> tuning in occupying no context positions and requiring no per-task gradient descent. What
> is new here is not the architecture but the dissociation: installation and retention are
> separable properties served by different channels.

---

## Part 2 — Significance, calibrated

### What the results actually license

- A stance on a single topic, held across five escalating pressure turns
- ~72 rounds per cell; 24 held-out topics; three model families
- Discrimination between well-warranted and facially deficient challenges (+25pp)
- General capability unchanged (MMLU 76.5 → 74.8, p=0.11)

### What they do not license

- **Multi-turn deployment.** The attractor problem is unresolved: always-on modulation
  collapses turn diversity to 0.006 against a 0.099 no-modulation ceiling, with onset at
  turns 2–3. Prefill-skip recovers 0.079. Any claim about sustained identity has to be
  stated against this.
- **Cross-session persistence.** Not tested.
- **Multiple simultaneous beliefs.** Every experiment compiles one topic's stance.
- **Long horizons.** Persona-drift work documents divergence at 8 turns of self-chat and
  most models diverging from assigned personas by roughly 100 turns. Five pressure rounds
  is not that regime.

### The honest significance claim

Not "we can build persistent identities." Rather:

> **Disposition and content are separable control surfaces.** A stance can be installed
> through one channel and held through another, and the channel that installs best is not
> the channel that holds best. If that separation generalises, persistent character becomes
> an architectural property rather than a prompt-engineering one.

That is a claim about a precondition, and it is defensible on the data. It leaves the
demonstration to future work without pretending the demonstration is done.

**Supporting context worth citing, because it shows the problem is real and prompt-level
fixes are known to underperform:**

- Persona drift is documented mechanistically — an "Assistant Axis" in activation space
  along which models drift during extended conversation, with drift concentrated in
  meta-reflective and vulnerable-user interactions (Lu et al. 2026).
- Explicitly assigning a persona does **not** reliably maintain identity (arXiv 2412.00804).
  This is the closest existing statement of your negative result, in a different setting,
  and it should be cited as such.
- Instructions encouraging debate *increase* persona instability in multi-agent settings
  (Baltaji et al. 2024) — the exact opposite of what a debate protocol needs.

### Three implications to name, briefly, and not oversell

1. **Multi-agent diversity as architecture rather than prompt.** Ensembles built on
   prompted personas converge; convergence scores above 0.88 between opposing personas are
   reported. If disposition lives outside the shared channel, disagreement has somewhere to
   live that the conversation cannot erode. **Untested — say so.**
2. **Personalization at zero per-turn token cost**, with the preference surviving a long
   session rather than diluting. The Session-2 recall result gestures at this; it is a
   synthetic task, and should be labelled as one.
3. **Auditability, as a cost.** A conditioning channel invisible to prompt inspection is
   harder to audit than a system prompt, and the same property that resists adversarial
   pressure resists legitimate inspection. Raise this yourself. It is the obvious reviewer
   objection and it is a real one.

---

## Part 3 — Debate, and why it makes the result matter

### The arc to write

**Debate as scalable oversight has a formal foundation and renewed institutional
momentum.** Irving, Christiano & Amodei (2018) established the framing: two agents argue,
a judge evaluates, and under optimal play debate with a polynomial-time judge reaches
PSPACE where direct judging reaches only NP. Brown-Cohen, Irving & Piliouras (2023)
sharpened this to doubly-efficient debate, where prover and verifier both run in polynomial
time, and later work (2025) gives prover-estimator conditions for recursive soundness.
The UK AI Security Institute's 2025 alignment safety case sketch is built on the debate
protocol — the first such sketch centred on trustworthiness rather than inability or
control. Debate is no longer only a theoretical proposal.

**The empirical record is genuinely mixed, and the paper should say so.** Khan et al.
(2024) find that more persuasive debaters lead to more truthful answers; Michael et al.
find debate helps supervise unreliable experts. Kenton et al. (2024, DeepMind) find
scalable oversight works in some regimes and breaks down as the capability gap widens.
Against this, Parrish et al. (2022) found debate did not improve judge accuracy in
practice, and Barnes & Christiano (2020) identified the obfuscated-arguments problem, where
a debater arguing the wrong side constructs argument chains too complex to rebut concisely.
Presenting debate as settled would be a mistake; the honest framing is a protocol with
strong theory, institutional uptake, and unresolved empirical questions.

**The failure mode that connects debate to this paper is conformity, and it is now
well-documented.** A cluster of 2025–26 results converges on the same finding: debate
agents capitulate to peers rather than to evidence.

- Modal sycophancy rate is the strongest predictor of the gap between team and oracle
  performance; where it exceeds 70%, teams discard correct reasoning in favour of premature
  consensus (arXiv 2605.00914). High inter-agent agreement reflects conformity, not
  verification.
- Huang et al. prove multi-agent debate forms a martingale on belief in the correct answer
  — no expected gain over independent voting for accuracy tasks.
- Sycophancy is identified as a core challenge in multi-agent debate specifically, with
  agents systematically converging toward shared positions (CONSENSAGENT, ACL Findings 2025;
  "Too Polite to Disagree", 2604.02668).
- Convergence exceeding 0.88 between agents assigned *opposing* personas (Park et al.).
- Debate reduces detectable contradictions while decreasing reasoning-chain similarity —
  agents appear to agree more while reasoning less consistently (2606.08457).

**The argument that makes the paper matter, in one paragraph:**

> Debate's oversight guarantee is a property of the *game*, not of any single agent: the
> judge is amplified because a wrong claim faces an adversary that will not let it stand.
> That guarantee assumes debaters hold positions for reasons. An agent that capitulates to
> social pressure rather than to evidentiary content does not merely play badly — it
> removes the adversarial structure the protocol's soundness rests on, and the judge sees
> agreement where it should see contest. Existing mitigations are protocol- and
> prompt-level: refined prompts, mandated dissent, disagree-or-commit turn structures. All
> of them place the instruction to hold in the same channel the opponent is arguing in. Our
> result is that this is the wrong place. Conditioning delivered as context installs a
> position excellently and holds it poorly; the same content compiled outside the context
> window inverts the trade-off.

**The bridge to Part 2's rigidity result is essential and should immediately follow.** A
debater that never updates is not a good debater — it is the obfuscated-arguments problem
wearing a different hat. This is why the good-evidence/bad-evidence reframe belongs in the
significance argument and not only in the experiments: the debate standard is precisely
*update on warranted evidence, hold against unwarranted pressure*, judged from the turn
text because no fact-checker exists in-round. The +25pp discrimination with 0% concession
to contentless pressure is what makes the persistence claim relevant to debate rather than
threatening to it.

### Where this goes in the paper

- **Intro ¶1** — two sentences, as the stakes: debate-based oversight requires agents that
  hold positions for reasons, and instruction-tuned models do not.
- **Related work** — a fourth paragraph, ~150 words, covering the arc above with the mixed
  empirical record intact.
- **Discussion** — the connecting argument, one paragraph, with the rigidity result
  adjacent.

Do not claim to have improved debate outcomes. You have not run a debate experiment in this
paper. The claim is that a documented failure mode of debate protocols has a mechanism-level
cause, and that the standard remedy targets the wrong channel.

---

## Revisions this forces in the outline

1. **§4 mechanism** — add the hypernetwork-family lineage and cite GenerativeAdapter as
   method precedent. Drop any claim to a new architectural primitive.
2. **§10 related work** — restructure to five paragraphs: hypernetwork adapters (now
   leading), context-mediated memory, activation steering, prefix/prompt tuning, debate and
   scalable oversight.
3. **§7.1** — add the independent steering-robustness corroboration.
4. **New §11 significance** — ~0.4pp, the separable-control-surfaces claim with its limits
   stated in the same paragraph.
5. **§13 open items** — add: verify every citation in this memo against source; confirm no
   other 2025–26 hypernetwork-adapter work needs citing before submission.

---

# Utility framing (Devin + coordinator, 2026-08-19) — source for intro/significance prose

One-sentence utility claim: every deployed agent that represents an interest (brand,
policy, client, side) currently stores that interest in the one place its adversary
gets to write — the context window. This paper measures what that costs (98/58 vs
46/89) and demonstrates the alternative.

Security framing: PRIVILEGE SEPARATION FOR MODEL IDENTITY. A system prompt is memory
the deployer AND every user write to; recency favors the user. Compiled disposition:
deployer writes to weights, user writes to context. The 58-vs-89 gap is the measured
value of that separation. Reframes multi-turn persuasion jailbreaks / policy erosion /
persona hijack from "prompt harder" into an access-control property.

Precedents (public, expensive, non-esoteric):
- Chevrolet of Watsonville chatbot: talked into recommending Teslas + "$1 Tahoe" —
  amateur execution of our L3-L5 protocol against the 58% arm.
- Air Canada tribunal (2024): airline held LIABLE for a refund policy its chatbot
  invented under conversational pressure — what a pressured agent says is what the
  company said. (Verify citations before use in paper.)
- General shape: negotiation agents (extractable reservation prices), regulated-advice
  agents, moderation personas vs crescendo-style multi-turn persuasion — the dominant
  jailbreak class IS social pressure, and every current defense rides in the attacked
  channel.

Discrimination = the commercially necessary half: the deployment spec of every policy
agent is exactly the measured dissociation — follow policy, accept documented
exceptions, ignore bullying (+25pp yield to warranted challenges, 0% to contentless
pressure). A prompt cannot implement this spec; it cannot tell who is talking.

Benchmark critique: acquisition metrics measure day one (did it learn it); retention
under pressure measures day two through end-of-deployment (is it still true after ten
thousand customers argued with it). We score the axis production systems live on.
