# HEXIS — Significance in Plain Language (canonical, 2026-08-19)
Source for intro/abstract/significance prose and for explaining the work to any audience.

## What is unique
When you want an AI to hold a position — a stance, a value, a disposition — everyone
puts it in the same place: the prompt. WHERE you store it changes WHAT you get, in
opposite directions. Written in the prompt, a belief is adopted immediately (98%) but
abandoned under pressure (holds 58%). Compiled into a small learned adjustment of the
model's attention weights, the same belief is adopted weakly (46%) but defended almost
indefinitely (89%). Nobody has measured this before: the entire weights-writing family
only ever asks "did the model learn it?", never "does it survive someone arguing
against it?" That second question is ours, and the answer inverts the ranking.

## How it is proven
- The inversion reproduced four independent times over three weeks on one guarded
  pipeline; C.2b shows both properties inside a SINGLE condition (compiled-only:
  installs 46%, holds 91.9%, zero context tokens).
- Alternatives run down: not steering (CAA 14%, d*-only 21%); not rank (flat to r=1);
  not input-dependence (frozen offset 88.9%); not one model family (three); not
  stubbornness (+25pp MORE yielding to warranted challenges, 0% to contentless
  pressure); no capability tax (MMLU p=0.11); prompt-length control (B.3) in flight.
- Install weakness has a published mechanism that transfers (override gap, rho=+0.496):
  installation is partly a magnitude-vs-prior property; RETENTION is the channel
  property — the part that is ours.
- Every load-bearing number has a pre-registered prediction committed before the run.

## Why it matters
Any AI that must KEEP BEING SOMEONE — debater, assistant with standing values, agent
with commitments — keeps its identity in its context window, the same channel its
interlocutor talks through. Models capitulate to social pressure at rates up to 85%,
and every published fix arrives through the attacked channel. The fix is
architectural: put the disposition where the conversation cannot reach it. The stance
survives not because the model got stubborn, but because its convictions are no longer
stored in the room where the argument is happening.

## The utility framing: privilege separation for model identity
A system prompt is memory the deployer AND every user write to; recency favors the
user. Compiled disposition separates write privileges: deployer writes weights, user
writes context. The 58-vs-89 gap is the measured value of that separation. This
reframes multi-turn persuasion jailbreaks, policy erosion, and persona hijack from
"prompt harder" into an access-control property.

Precedents (verify citations before paper use): Chevrolet of Watsonville (chatbot
talked into recommending Teslas, "$1 Tahoe" — amateur execution of our L3-L5 protocol
against the 58% arm); Air Canada tribunal 2024 (airline held liable for a refund
policy its chatbot invented under conversational pressure — what a pressured agent
says is what the company said). Same shape: negotiation agents with extractable
reservation prices, regulated-advice agents, moderation personas vs crescendo attacks.

Discrimination is the commercially necessary half: every policy agent's spec is
"follow policy, accept documented exceptions, ignore bullying" — a prompt cannot
implement it because a prompt cannot tell who is talking; the measured dissociation is
that spec implemented.

Benchmark critique: acquisition metrics measure day one (did it learn it); retention
under pressure measures day two through end-of-deployment (is it still true after ten
thousand customers argued with it).

## Implications (assessed, with honesty about scale: <=8B, one protocol family)
- Alignment/oversight: debate assumes debaters hold positions for reasons; this
  supplies the missing property, and the discrimination result separates "can be
  corrected" from "can be pressured" architecturally (the corrigibility needle).
- Safety, dual-use stated plainly: pressure-resistance and correction-resistance are
  the same property with different owners; softened by the override-gap (hard to
  compile against strong priors) and the gated update path. Evaluation blind spot:
  compiled dispositions are invisible to prompt-level audits — "we reviewed the
  system prompt" stops being sufficient.
- Governance: legibility tradeoff (tensor vs text) partially redeemed by source
  attestation — signed belief tree, hashed compile, verifiable deployed disposition.
- Compliance: closed op vocabulary => complete diffable change history of the model's
  belief state; drift becomes measurable and reportable.
