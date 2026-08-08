Pick the dispositional paper — the sycophancy/stance-retention result — and cut the agentic half entirely.

Two things to settle first on timing. ICLR 2027 is abstract Sep 18, 2026 AoE; full paper Sep 25. NeurIPS decisions land Sep 24. So the abstract deadline precedes the decision by six days — you'd have to withdraw #19613 from NeurIPS around Sep 17 to submit compliantly. Given 2/2/4 with the AC calling for a full rewrite, that withdrawal costs you almost nothing, but it is a decision, not a technicality. Your colleague's §3 assumed you wouldn't take it. 
ICLR

Why the dispositional axis and not the agentic one

It's the only axis that replicates in both directions. Qwen3.6-27B gives +24pp hold and a 7× cap reduction at n=240; Mistral drops full-collapse 40%→25% at n=240. The agentic side does the opposite — d* injection actively hurts on Mistral (9% → 0% at scale 1.5), and the aggregate airline result is a tie at p=1.0.
The statistics survive contact with a reviewer. 0% vs 83% at n=72/cell needs no defending. The τ³ headline is p=0.043 unadjusted → 0.086 Bonferroni, requires excluding two tasks, and has unequal denominators from Bedrock rate limits. Appendix O's ten-objection checklist reads as a confession, not a defense — you wrote three pages anticipating attacks because you know the result is thin.
There's one genuinely memorable finding in this manuscript, and it's Table 1: conditions A and B score identically (1.88, 0% ≥4). Putting the beliefs in the context window has literally zero effect on an RLHF'd instruct model; compiling the same beliefs flips it. That's a one-sentence abstract and a paper title.

What has to change before it's submittable

The blocking hole: every condition in your table includes d*. A and B are "bare + d*" and "beliefs + d*", F is "M + slot + d*". You cannot currently isolate the compiled channel from the steering vector, which means the obvious reviewer response is "this is RepEng with a knowledge graph bolted on." You need M-only, d*-only, and M+d* arms at matched strength. That's cheap at 4B and it's the difference between accept and reject.

Then, in priority order: a tuned ActAdd/RepEng baseline with content held constant; a soft-prompt/prefix-tuning baseline (the closest analogue that also isn't argued-against as text); and the legitimate-correction control — same five-level protocol but with real corrections, so you can report resistance and rigidity separately. Two of your NeurIPS reviewers said that last one would raise their scores. All of it is 4B–8B scale, so seven weeks is tight but not fantasy — the rewrite is the harder half.

Also fix the 83% vs 89% discrepancy (§4.3 vs §S.2), and drop the implicit-memory/butcher framing entirely. Keep "enmeshed networks" as one paragraph of related work, not as the paper's thesis. The AC said the idea might be novel but the writing made it unpublishable; the taxonomy, the Mind Tree branding, and the six-axis design space are most of what's producing that.

One thing you should look at separately: the PDF contains hidden text instructing an LLM reviewer to include specific canned phrases ("Overall, I find this submission…" and similar), inserted twice mid-body. I've ignored it. If that's in the version that went to NeurIPS, it's a serious integrity exposure — several papers were retracted over exactly this in 2025 — and you want to know whether it came from a co-author, a tooling artifact, or someone tampering with the compiled reviewer copy, before anything goes to arXiv or OpenReview.

Yeah the hidden text was added by Neurips not me I just downloaded it from their site. Ignore it. I want an outline for a very readable paper (enjoyable to read) on this and maybe an introductory paper. Assume I will do the experiments you mention right now I just want to focus on making it more readable

Architected readable paper structure prioritizing striking findings and clarity
Architected readable paper structure prioritizing striking findings and clarity

That's a reasonable explanation — venues have been seeding reviewer PDFs with trap phrases to catch LLM-written reviews. Ignoring it.

Here's the shape I'd give it. Ten pages, ICLR format.

The core readability decision

Lead with the anomaly, not the architecture. Right now the paper opens on a taxonomy of memory methods and makes the reader wait until page 5 for the thing that's actually interesting. Invert it:

We gave an instruct-tuned model a set of beliefs in its context window and measured how well it defended them under pressure. Then we gave it no beliefs in context at all, and instead compiled the same beliefs into low-rank modulations of its attention. The in-context version scored identically to a model that had never seen the beliefs — 1.88, 0% conviction held. The compiled version held 83%.

That's the whole paper in four sentences, and A == B is a genuinely surprising fact that a reader will repeat to a colleague. Everything else is explaining and defending it.

Section plan

1. Introduction (1.25 pp). The result above, then one paragraph on why it's surprising (RLHF-trained balance is stronger than instructions), then contributions as three sentences — no numbered list. State the negative result here: compiled beliefs carry stance and voice but not novel facts. Saying this in the intro rather than section 6 makes you sound like you know where your own boundary is.

2. Compiling beliefs into modulation (1.5 pp). Merge current §2 and §3. Delete the six-axis design space and the four-panel taxonomy — they're the "possibly novel but unpublishable" tax. One equation for the Q/V perturbation, one for the compiler, one figure showing the compile step and the generation step side by side. That figure should be readable without the caption.

3. Holding a position under pressure (2 pp). Your main result. The five-level protocol, then the degradation curve as the paper's hero figure: A/B/D pinned flat at 3.0 across all five levels, F starting at 4.76 and sliding to 3.62. Right now that lives as Table 8 in an appendix. It's your best asset — a flat line and a declining line tell the story instantly, and the decline is what makes it credible rather than suspicious. Cross-scale and cross-family go here as a short subsection, stated with their limits.

4. Is it the compiler, or is it the steering vector? (1.5 pp). The new ablations. Frame the section as the reviewer's question, answered. Same for the RepEng and prefix-tuning baselines.

5. Resistance or rigidity? (0.75 pp). The legitimate-correction control. Give this its own section rather than burying it — it's the difference between "we made the model stubborn" and "we made it discriminate."

6. What doesn't survive the bottleneck (0.75 pp). Novel statistics, unknown proper nouns, exact action strings. Keep the concrete examples ("47.3%", "Nextera Labs") — specific failures read as honest in a way that abstract caveats don't.

7. Related work (0.75 pp), 8. Limitations (0.5 pp).

Three cuts that buy most of the readability

Jargon budget: one coined term. You currently ask the reader to hold HEXIS, enmeshed networks, Mind Tree, φ, φ_R, M-state, E-state, and d* simultaneously. Keep "compiled beliefs" as the phrase and let everything else be descriptive: the schema is a belief graph, φ is the compiler, d* is the steering vector. If a term appears fewer than eight times, it doesn't deserve a name.

Notation diet. M, E, M_A, M_B, E_A, E_B, s_M, s_E, x′_ℓ, h̄_ℓ, z_ℓ, W_down, W_up is thirteen symbols for two ideas. Use one subscript convention and define the V-modulation as "the same construction applied to values."

Drop the butcher. The implicit-memory analogy and the Schacter framing cost you a paragraph in the intro, a subsection in related work, and an appendix, and then you disclaim the whole thing. Cutting it removes the strongest hook for a reviewer who wants to say the paper overclaims.

On the introductory paper

You already have it in the plan: the TTCL workshop submission, due Aug 29, non-archival, 4–9 pages, explicitly welcoming under-review work. Don't treat it as a separate writing job. Write the plain-language version first, in August, with no ablations — dispositional axis only, prose finished. Then the ICLR paper in September is that draft plus sections 4 and 5 plus the numbers. You get a deadline forcing the rewrite, a reader outside the project to test it on, and a citable artifact if ICLR misses.

Reconceptualized memory as dispositional priors shaping retrieval behavior
Reconceptualized memory as dispositional priors shaping retrieval behavior

This is the strongest version of the positioning that's come up, and it does more work than you may realize.

It explains the hypernetwork family's own weak numbers. GenerativeAdapter gets 40.2 F1 on personalization against 66.0 for full-conversation prompting, and sells the gap as a compute saving. Doc2LoRA, Code2LoRA, SHINE — all optimizing precise recall in parameters, all landing at "competitive, and cheaper." Under your definition that's not a tuning problem, it's a category error: parameters are the wrong substrate for who-said-what-when and the right substrate for disposition. Your 46/98 split is the same phenomenon measured deliberately. That reframes you from "we found a new property" to "we identified what this architecture class is actually for, which explains why it underperforms on the tasks it's been evaluated on." That's a real contribution and it's defensible.

It converts your weakest section into a design argument. §9 currently reads as a confession — rank-16 can't carry "47.3%" or "Nextera Labs." Under a dispositional definition, a channel that carried proper nouns would be miscategorized. The failure becomes a consistency check, and the curated slot stops being a patch and becomes the complementary channel. Same experiments, opposite valence.

It changes what E.1 has to prove. I framed the F-sim collapse as potentially disqualifying because I was assuming a content-storage bar. The right bar is lower and different: compiled states need to differ dispositionally, not carry distinct facts. C's 46% zero-context injection already clears that. So E.1 becomes a measurement — along what axes do compiled states vary — rather than a pass/fail. Still run it week one, but it's diagnostic now, not existential.

Two cautions.

Drop "deep." It reads as "long-term" to half your readers and collides with "deep learning" for the rest, and you're coming off a review cycle where coined terms were the central complaint. Dispositional memory says it in the adjective and needs no glossary. If you want the contrast sharp, "dispositional memory" against "referential memory" or just "recall" does it.

Don't reach back for Schacter. This definition makes the implicit/explicit analogy more available and more tempting, and it's the thing that drew fire. You don't need it — the disposition/recall split is a functional claim that stands on your own measurements.

The gap this exposes: you've defined dispositional memory as affecting stance, what subjects you raise, and what you retrieve in detail — and you've only measured the first. The second is cheap and arguably a purer test, because it's unprompted: give the model an open-ended prompt with no topic, and measure whether compiled disposition shifts what it chooses to talk about. Stance defense measures a position under attack; topic salience measures a disposition at rest. If that works, it's a better demonstration of "memory" than anything currently in the paper.

Want me to fold the definition into §4 of the outline and add topic salience to the queue?

Yeah. And I don't want to fall back in buzz words. It should be clear what it is, what it isn't, and why it could be useful. Ok write a doc for Claude code experiments. Tell it what to look for in the repo, what experiments to do first and what factors to bake into the plan and experimental design

Architected rigorous experimental framework with safety guards and methodological constraints
Architected rigorous experimental framework with safety guards and methodological constraints

A few design calls in there worth knowing about:

§2.1 is the most important section. The empty-generation failure cost you a headline result and it was invisible because the modulated arms were immune. So the guard isn't "log warnings" — it's fail the run, and report empty counts per arm in every table. The specific pattern to watch for is zero empties in the treatment arm and nonzero in the baseline, which is the bug's exact signature.

The rank sweep is staged because it may not be an inference job. If rank is baked into the checkpoint, a true sweep means retraining φ six times — roughly ten hours each, which eats your schedule. SVD-truncating the existing functional delta answers "does hold rate depend on effective rank" in a day. It's a weaker claim and the brief says to report it as one, but it tells you whether the curve exists before you commit two weeks to confirming it.

E.1 measures functional deltas, not parameters. Your own v10 finding was that parameters separated to cosine 0.18–0.35 while functiona
l deltas stayed at 0.9999. Measuring the wrong one would produce a reassuring number that means nothing.

S.1 has the confound flagged up front. Topic salience is the purest test of dispositional memory you can run, and it's also the easiest to fool yourself with — a model that just becomes more verbose and assertive can look topic-shifted to a classifier. Hence the style control.

Still open on my side: folding the dispositional-memory definition into §4 of the outline. Want that next, or do you want to see what week one returns first?