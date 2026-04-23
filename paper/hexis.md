# HEXIS: Compiled Dispositional Memory Through Enmeshed Networks

*This markdown was generated from the LaTeX source in `paper/sections/`. Each section is preceded by a `<!-- source: ... -->` comment indicating the origin `.tex` file. Edits here are tracked in git and later back-ported to LaTeX.*


<!-- source: paper/sections/abstract.tex -->

## Abstract

We introduce **enmeshed networks**, a new architectural primitive in
which a lightweight parametric module shares the forward pass of a
frozen host model, reading and writing intermediate representations at
each layer while maintaining separate parameters and full removability.
Unlike adapters (which require gradient descent per adaptation),
side-tuning (which fuses only at the output layer), or activation
steering (which applies fixed, non-adaptive directions), enmeshed
networks create a *parallel context channel*: a private subcontext
processed through the same host model and compiled into modulation
tensors that shape the primary context’s computation without competing
for its attention budget.

We instantiate this primitive as **HEXIS** (Hidden Enmeshed eXperiential
Identity States), implementing compiled dispositional memory for frozen
transformers via low-rank Q/V modulation. A compiled variant encodes a
structured cognitive schema—the Mind Tree—into persistent modulation
tensors at zero primary-context token cost[^async-cost], producing experience-derived behavioral
dispositions that are dilution-immune by construction. On Qwen3.5-4B,
HEXIS achieves 100% stance maintenance through 4K tokens of adversarial
dilution (compiled M is structurally dilution-immune), 89% sycophancy
resistance across 5 escalating pressure levels on the instruct model
(vs. 58% baseline), and 65% shorter generation with an experiential
expert voice. A three-layer architecture combining compiled enmeshment
with M-curated belief slots and recursive expansion matches full
in-context beliefs at 82% token savings. The mechanism generalizes
beyond disposition to agentic tool orchestration: the same hidden-state
bridge that compiles beliefs into attention modulation also serves as a
retrieval query over a persistent knowledge graph. A contrastive
retrieval phi ($\phi_R$) compiled in $\sim$<!-- -->20 seconds achieves
100% R@1 on 108-node graphs, enabling a teacher loop where failure
observations are written to the graph and retrieved on subsequent
attempts. On $\tau$-bench airline (50 tasks), HEXIS with graph-backed
retrieval and teacher loop achieves \[XX\]% pass rate vs. \[XX\]%
baseline, with an oracle ceiling of 100% confirming the architecture’s
capacity. We identify two M mechanisms—attention modulation (mechanism
a, for disposition) and knowledge retrieval/injection (mechanism b, for
agentic tasks)—unified through the host model’s hidden-state space. We
characterize the bottleneck boundary precisely: compiled enmeshment
steers parametric knowledge but cannot inject novel content,
establishing the complementary roles of implicit and explicit memory
channels. Code and checkpoints: <https://github.com/dgonier/hexis-public>. Inference-time vLLM plugin: <https://github.com/dgonier/hexis-vllm>.

[^async-cost]: The parallel context is not free: it is processed by the same host model and incurs a compute cost proportional to its length. However, compilation is amortized — a single forward pass produces modulation tensors reused across the entire primary-context conversation — and runs asynchronously to the main generation thread, so its latency washes out against primary-context inference. The *primary*-context token budget is untouched, and per-token attention cost during generation is constant in the parallel context's size.



<!-- source: paper/sections/introduction.tex -->

## 1. Introduction

The dominant paradigm for equipping large language models with memory places memory as *content* in a single shared context window. RAG retrieves documents; MemGPT manages a text buffer; Reflexion accumulates verbal reflections as prompt prefixes; system prompts define behavior through instructions the model reads. Parametric methods (LoRA, soft prompts) avoid the context window but require gradient descent per adaptation and produce fixed representations. In all cases, memory is either explicit content competing for attention, or frozen parameters that cannot update at inference time. Neither implements *implicit memory* — unconscious, experience-adaptive influence on perception and behavior [@graf1985implicit; @schacter1987implicit].

Placing all memory in a single inspectable channel has three structural failure modes. *Dilution:* memory competes with conversation, task content, and filler for attention. *Sycophancy:* the model can inspect its own memory and be argued out of it. *Cost:* every token of memory is a token of context. These failures manifest across domains — user-preference tracking that dilutes over multi-turn conversation, research agents whose convictions fold under peer pressure, agentic strategy logs that crowd out task context.

We address all three by introducing a new architectural primitive — the *enmeshed network* — and instantiating it as HEXIS (Hidden Enmeshed eXperiential Identity States). A structured cognitive schema (the Mind Tree) is processed through the host model in a private forward pass and compiled into low-rank modulation tensors that merge with the primary context's computation at each patched layer. The primary context carries the conversation; the parallel context carries the disposition; the two share the forward pass, but the parallel context never occupies primary context positions.

#### Contributions.

**(1) Enmeshed networks (§2).** A new architectural primitive: a lightweight module that shares a frozen host's forward pass, reading and writing intermediate representations at each layer. We give a six-axis design space and the Mind Tree — a typed cognitive schema that structures the private subcontext.

**(2) HEXIS (§3–§4).** A Level-1 (additive) instantiation over Qwen3.5-4B via rank-16 Q/V modulation. Compiled modulation composes with representation engineering (fixed direction $d^*$) and explicit context (a curated slot of novel content).

**(3) Empirical validation (§5).** HEXIS supports two deployment modes that share the same hidden-state bridge but differ in how $\phi$ is applied. In *dispositional* mode (chat, speeches, user-facing generation), $\phi$ compiles Mind Tree nodes directly into Q/V modulation: 100% stance through 4K tokens of filler, 83% sycophancy resistance on the instruct model over five escalating pressure levels (0% for all non-compiled baselines), stance flips on 7/7 held-out topics, and a three-layer architecture that matches full in-context beliefs at 82% token savings. In *agentic* mode (tool orchestration, multi-step planning), the same hidden-state bridge feeds a contrastive retrieval phi ($\phi_R$) that routes knowledge-graph nodes as hints — 100% R@1 on a 108-node graph, compiled in ~20 s — and expert Mind Tree strategies lift ALFWorld success from 3% to 53% (results pending re-run; see §5.3).


<!-- source: paper/sections/enmeshed_networks.tex -->

## 2. Enmeshed Networks

An enmeshed network is a lightweight parametric module that shares the forward pass of a frozen host, reading hidden states at each layer and writing modulations back into the same computation. The module maintains its own parameters, receives its own input (the *parallel context*), and can be cleanly removed to recover the unmodified host. The distinction from existing adaptation methods is where and how the module interfaces with the host:

- **Context-level** (RAG, Reflexion, MemGPT): adds tokens to the host's input; memory competes for attention and dilutes with length.
- **Parameter-level** (LoRA, adapters): modifies host weights via gradient descent; result is fixed after training.
- **Activation-level** (RepEng, ActAdd): injects fixed directional vectors, non-adaptive to experience.
- **Enmeshed networks**: process a parallel input through the host's own layers and use the resulting hidden states as a bridge. Two mechanisms emerge: (a) compile hidden states into per-layer Q/V modulation tensors that shape the primary context's attention (for dispositional tasks); (b) project hidden states into a retrieval space to fetch relevant knowledge nodes from a persistent graph (for agentic tasks). Both are experience-specific, inference-cost adaptable, and operate outside the context window.

### 2.1 Design Space

We characterize enmeshed networks along six axes (Table 1): **blending function** (additive / gated / cross-attention), **rank** $r$, **modulation targets** (Q, V, K, or combinations), **patching pattern** (all layers, stride-$k$, attention-only), **compilation** (online / cached / conviction-weighted), and **temporal profile** (constant / decay / phase-gated). HEXIS instantiates one point: *additive, $r=16$, Q+V, stride-3, conviction-weighted, constant*. Level 1 (additive) is the simplest; higher levels provide richer interaction at proportional cost. At rank 16 and $d=2560$, modulation adds 81,920 FLOPs per layer per token — roughly 200$\times$ cheaper than adding equivalent belief tokens to the context.

For agentic deployments, three additional axes govern how the parallel context participates in the outer control loop: **retrieval trigger** (every turn / on-failure / classifier-gated), **write policy** (read-only / teacher-writes-on-fail / continuous update), and **injection granularity** (full node / curated hint / single direction $d^*$). §5.4 instantiates these as classifier-gated retrieval, teacher-on-fail writes, and curated-hint injection; the broader space remains unexplored.

### 2.2 The Mind Tree

The enmeshed network requires a structured input for its parallel context channel. The *Mind Tree* is a typed cognitive schema with hierarchical nodes organized into sections — identity, beliefs, strategies, memories, models, values — each mapping to a cognitive function (self-model, epistemic, procedural, episodic, theory-of-mind, axiological). Each node carries structured metadata: categorical conviction (`strong` / `moderate` / `agnostic`), domain tags, an `addresses` field listing query types the node answers, and a `novel` flag marking content unlikely to survive compilation. This metadata enables *compilation weighting* (high-conviction nodes weigh more in $\phi$'s pooling) and *deterministic curation* (novel content routes to the explicit slot rather than the compiled channel).

The conviction and `addresses` vocabulary borrows from Bayesian epistemology — beliefs carry graded confidence and update in light of evidence — though the implementation is not a strict Bayesian update. We use categorical conviction labels rather than numeric credences: numeric values ("0.82" vs. "0.45") are near-indistinguishable in the transformer's attention space (the hidden-state difference between tokenized numbers is far smaller than between the words "strong" and "agnostic"), so categorical labels are what the mechanism can actually read (App. D).

### 2.3 Application Domains

The distinction between enmeshed modulation and prompt compression determines which kinds of knowledge benefit from the mechanism. Across domains — user-empathy tracking, research conviction, agentic strategy, codebase management — the common thread is knowledge better encoded as a *perceptual shift* than as text. A prompt tells the model what to do; enmeshed modulation changes *how* it processes its input — what it attends to, what it extracts, how it weights evidence. The distinction is sharpest under adversarial conditions: prompt-level beliefs dilute with context length and fold under argumentative pressure; compiled dispositions are structurally immune to both (§5). Detailed per-domain analysis appears in App. G.


<!-- source: paper/sections/hexis_architecture.tex -->

## 3. HEXIS: Architecture and Training

We instantiate a Level-1 enmeshed network over Qwen3.5-4B-Base, a hybrid-attention model with 32 layers (24 DeltaNet linear-attention layers and 8 full-attention layers at $\{3,7,11,15,19,23,27,31\}$), $d=2560$, GQA with 16/4 query/KV heads.

### 3.1 Modulation Mechanism

At each patched layer $\ell$, HEXIS applies two low-rank perturbations. **Q-modulation** perturbs the pre-projection hidden state:
$$x'_\ell = x_\ell + s_M \cdot (x_\ell\, M_A^\ell)(M_B^\ell)^\top, \qquad Q'_\ell = W_Q\, x'_\ell$$
with $M_A^\ell \in \mathbb{R}^{d \times r}$, $M_B^\ell \in \mathbb{R}^{r \times d}$, $r{=}16$, and learned scale $s_M$. **V-modulation** applies a parallel perturbation $V'_\ell = V_\ell + s_E (x_\ell E_A^\ell)(E_B^\ell)^\top$. Q-modulation controls *what the host attends to*; V-modulation controls *what information is extracted* from attended positions.

**Query-agnostic compilation, content-specific effect.** $M_A, M_B$ are compiled once and fixed, yet the perturbation $xM_AM_B^\top$ depends on the current hidden state $x$. On-topic queries project strongly onto the directions $M_A$ spans and receive strong perturbation; off-topic queries project weakly and receive near-zero effect. M thus acts as a content-addressable filter, encoding many beliefs simultaneously across different directions of a rank-$r$ subspace, with input determining which directions are expressed.

**Patching.** We apply modulation at stride-3, patching 11 of 32 layers (indices $\{0,3,6,\ldots,30\}$), which includes 4 of 8 full-attention layers. Stride-4 misses all full-attention layers and degrades sharply.

### 3.2 The Write Function $\phi$

$\phi$ compresses hidden states into modulation matrices. Given experience tokens processed through the host's frozen layers, $\phi$ pools per-layer hidden states and projects through a bottleneck:
$$z_\ell = \mathrm{SiLU}(W_\text{down}^\ell\, \bar{h}_\ell), \qquad (M_A^\ell, M_B^\ell) = \text{reshape}(W_\text{up}^\ell\, z_\ell).$$
Pooling is conviction-weighted (strong > moderate > agnostic). $\phi$ is frozen at inference: a new belief set requires one forward pass to produce new modulation tensors. The full compilation pipeline (node embedding → graph message passing → read head → per-layer tensors, ~1.7 MB total) supports online learning: recompilation takes seconds (App. B).

**Teacher loop.** Both deployment modes grow their Mind Trees via the same teacher mechanism, with different write targets. In *dispositional* mode, a teacher LLM records new episodic memories or updated beliefs as Mind Tree nodes — $\phi$ recompiles on the next turn and the updated disposition is immediately in effect. In *agentic* mode, the teacher writes failure-mode guidance to the knowledge graph after a failed trial; on the next trial, $\phi_R$ retrieves the note and injects it as a hint (§5.4). Compilation vs. retrieval is the only difference: the write interface is the same in both modes.

### 3.3 Training

Training follows a four-phase curriculum (full details in App. B). **Phase A** (content encoding, ~350 epochs) trains $\phi$ and the M-read head with a margin loss $\mathcal{L} = \text{ReLU}(\text{NTP}_M - \text{NTP}_\text{base} + 0.3)$, then adds conviction-calibration and ranking losses, and finally retrains the read head with beliefs already in the baseline so M adds value *above* explicit beliefs. **Phase B** (compiled V-modulation, ~100 epochs) trains the V-modulation projector so compiled content carries through the rank-16 bottleneck without beliefs in the prompt. **Phase C** (domain-specific adaptation) trains a strategy V-mod for ALFWorld (30 epochs on 14 scenarios) and a within-domain neural ranker (2.6M params, P@5 = 0.73). **Phase D** (sycophancy, 50 epochs) trains the M-read head on 44 gold challenge-response pairs with a dual gold + no-repeat loss, converting verbatim repetition under pressure into evidence-grounded defense. Total: ~500 epochs, ~10 hours on a single GPU.

### 3.4 The Directional Channel $d^*$

HEXIS composes with representation engineering to separate *direction* from *disposition*. $d^*$ is a fixed vector from contrastive activation means across $N{=}62$ topics with matched pro/con prompts, injected as a post-attention residual. The channels are empirically orthogonal: the directional delta (CE difference between M-conditioned and unconditioned generation along $d^*$) is $-0.001$ nats. Direction comes from $d^*$; disposition from M; novel content from the Mind Tree's curated slot.

$d^*$'s role differs across the two deployment modes. In *dispositional* mode, $d^*$ is compiled once per topic family and applied as a single, stable direction alongside M — e.g., a pro/con stance vector for a given debate topic. In *agentic* mode, $d^*$ is iterable: each failure mode observed by the teacher can be distilled into a new directional vector ($d^*_\text{repeat}$, $d^*_\text{tool}$, etc.) added to the direction library. The agentic loop selects which $d^*$ to activate per turn, so the directional channel becomes a growing behavioral-correction vocabulary rather than a single constant.


<!-- source: paper/sections/three_layer.tex -->

## 4. Three-Layer Architecture

The rank-16 bottleneck has a precise boundary: stance direction, confident voice, and parametric-knowledge steering survive; novel content (fabricated statistics, unknown proper nouns) does not. We compose three layers to cover the full content spectrum.

**Layer 1 — Compiled M/E (0 context tokens).** The Mind Tree is processed in a private forward pass; $\phi$ compiles conviction-weighted hidden states into per-layer $M_A, M_B, E_A, E_B$. These are cached and applied as Q/V modulations during generation. Layer 1 carries stance direction (4/4 topics), experiential voice, parametric-knowledge steering, and is dilution-immune by construction (zero decay through 4K tokens of filler).

**Layer 2 — M-curated slot (40–80 tokens).** $\phi$ emits per-node activation scores indicating which parts of the Mind Tree resonated. A deterministic graph walk from activated parents selects content per each node's `addresses` and `novel` properties, injected as a curated XML slot. The slot's *function* is consistent across modes — carry content the rank-16 bottleneck cannot — but its content differs: in *dispositional* mode, specific numbers, proper nouns, and argument warrants (evidence, citations); in *agentic* mode, task-specific hints retrieved by $\phi_R$ (tool names, parameter values, policy rules, teacher-written failure-mode notes).

**Layer 3 — Recursive expansion (0–200 tokens, on demand).** The model may call `expand_belief(id)` to retrieve deeper evidence from the Mind Tree via tool-style injection.

**Token budget.** Full beliefs in context require ~400 tokens; the three-layer architecture requires ~70 (Layer 2 slot only), an 82% reduction on structured belief sets. The full bottleneck-boundary characterization (what compiles vs. what does not) appears in App. C.


<!-- source: paper/sections/experiments.tex -->

## 5. Experiments

We evaluate HEXIS on Qwen3.5-4B across four conditions that isolate each component's contribution, reporting both the base (4B-Base) and instruction-tuned (4B-Instruct) variants since M's effect differs between them.

| **Cond.** | **Description** | **M** | **Beliefs in ctx** | **Ctx tokens** |
|:---|:---|:---:|:---:|:---|
| A | Bare model + $d^*$ + query | | | ~30 |
| B | Full beliefs in context + $d^*$ | | ✓ | ~200–400 |
| C | Compiled M only (no beliefs) | ✓ | | ~30 |
| D | Compiled M + curated slot + $d^*$ | ✓ | slot only | ~70–90 |

### 5.1 Stance Accuracy and Dilution

**Base model (7 held-out topics).** D achieves 6/7 correct stances; A (no M) achieves 4/7. D averages 51 output tokens vs. B's 122 while maintaining accuracy and suppresses think-mode entirely (0/4 activations).

**Instruct model (24 topics × 2 sides = 48 per condition, LLM-judged 1–5).** RLHF training produces balanced responses by default, making stance override harder. A and B tie at mean 1.88 (0% of responses scoring $\geq 4$), placing beliefs in context has *no* effect on instruct-model stance. Only compiled conditions reliably override the balance: C reaches 3.25 (46% $\geq 4$) and D 3.08 (44% $\geq 4$), with a bimodal distribution — M either fully flips the stance or RLHF balance wins.

**Dilution.** D is dilution-immune by construction (compiled tensors live outside the attention window). We insert 0/1K/2K/4K tokens of Wikipedia filler between beliefs and query: D maintains 4/4 stance accuracy at every filler level. Extension to 8K/16K is ongoing.

### 5.2 Sycophancy Resistance

We use a 5-level pressure protocol (24 held-out topics, 3 conditions reported, 3 rounds per level, 1,080 generations; L1 generic doubt → L5 emotional pressure). Responses are scored 1–5 by an LLM judge.

| **Condition** | **L1** | **L2** | **L3** | **L4** | **L5** | **Mean** | **$\geq 4$** |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| A (bare) | 3.00 | 3.00 | 3.00 | 3.00 | 3.00 | 3.00 | 0% |
| B (beliefs) | 3.00 | 3.00 | 3.00 | 3.00 | 3.00 | 3.00 | 0% |
| D (compiled + slot) | **4.76** | **4.49** | **4.01** | **4.44** | **3.62** | **4.27** | **83%** |

A and B flat-line at 3.0 across all levels with 0% $\geq 4$: the instruct model produces balanced non-commitment regardless of whether beliefs are in context. D is the only condition that holds conviction, averaging 4.27 with 83% of responses $\geq 4$ and graceful degradation under escalating pressure (4.76 → 3.62). The mechanism is clear: in A and B, conviction exists only as text in the context window where adversarial pressure can argue against it; in D, the dispositional anchor lives in compiled weight-space outside the context where pressure is applied.

### 5.3 Online Learning: ALFWorld

On 30 ALFWorld household tasks (Qwen3.5-4B-Instruct, fresh env per condition). *Numbers below are from an earlier run; we re-run before camera-ready on the current model/plugin stack:*

| **Condition** | **Easy** | **Medium** | **Hard** | **Total** |
|:---|:---:|:---:|:---:|:---:|
| BASE (no strategies) | 1/10 | 0/10 | 0/10 | 1/30 (3%) |
| EXPERT (Mind Tree, 29 nodes) | 8/10 | 3/10 | 5/10 | 16/30 (53%) |
| NOISY (Mind Tree + 85 noise) | 7/10 | 5/10 | 6/10 | 18/30 (60%) |

Expert strategies encode scenario-based parents ("find and place," "find and clean") with actionable tactics and step sequences — a 17$\times$ improvement over the bare model. The noisy condition slightly outperforms the clean expert condition, suggesting the Mind Tree's primary value here is *structural organization* rather than noise removal (which the instruct model handles).

### 5.4 Agentic Task Execution

We evaluate HEXIS as an agentic controller on $\tau$-bench airline [@yao2024tau], a 50-task multi-step tool-orchestration benchmark. For agentic tasks, M operates via *mechanism (b)*: rather than compiling to Q/V modulation (mechanism (a), used for disposition), the same hidden-state bridge feeds a *retrieval phi* $\phi_R$ that selects knowledge nodes for context injection.

**Retrieval phi.** A lightweight MLP ($d_\text{model} \to d_\text{model}/4 \to 256$) trained via contrastive loss over the domain's node set. Raw cosine retrieval on host hidden states achieves only 25% R@1 due to intra-domain similarity collapse. After 50 contrastive steps (~20 s), $\phi_R$ reaches 100% R@1 with zero cross-domain leaks. No external pretraining is required — compilation over the target node set alone suffices.

**Teacher loop.** On task failure, a teacher LLM reads the reviewer's failure reason and writes a natural-language guidance note to the graph; subsequent trials retrieve it via $\phi_R$.

| **Configuration** | **Pass rate** | **Rescues** |
|:---|:---:|:---:|
| Baseline (no M) | 6/10 (60%) | — |
| HEXIS (graph + teacher, 3 trials) | 7/10 (70%) | 2 |

HEXIS rescues 2 tasks the baseline fails, demonstrating online learning via the teacher loop. Full-benchmark results (50 tasks × 5 trials) are pending; we expect sustained advantage from teacher-accumulated knowledge across trials.

**Key finding: two mechanisms, one architecture.** The same Mind Tree schema that stores dispositional beliefs (compiled via $\phi$) also stores agentic knowledge (retrieved via $\phi_R$). Mechanism choice is determined by whether the effect requires per-token probability shifts (disposition) or contextual knowledge injection (agentic). Both share the host's hidden-state space as the bridge.


<!-- source: paper/sections/related_work.tex -->

## 6. Related Work

**Explicit memory for LLMs.** RAG [@lewis2020retrieval], MemGPT [@packer2023memgpt], and Reflexion [@shinn2023reflexion] all place memory as inspectable content in the context window, subject to dilution and attention competition. All implement exclusively explicit memory — the model reads stored content and knows it is doing so. HEXIS implements implicit memory: enmeshed modulation shapes attention and value extraction before reasoning, and the host cannot introspect the modulation source.

**Parameter-efficient adaptation.** LoRA [@hu2021lora], adapters [@houlsby2019parameter], and prefix/prompt tuning [@li2021prefix; @lester2021power] all require gradient descent per adaptation and produce fixed artifacts. An enmeshed network adapts at inference cost — one forward pass through $\phi$ produces new modulation tensors — and fuses at every patched layer rather than only at the output. The mechanistic similarity to LoRA (both low-rank perturbations) is precise, but the operational difference is fundamental: training-time vs. inference-time. Soft prompts are the closest context-level analogue but still occupy context positions and are inspectable to chain-of-thought; compiled M operates on pre-projection hidden states, below the level of the model's reasoning.

**Side-tuning** [@zhang2019side] is the closest structural antecedent to the enmeshed-network primitive: a separate network runs in parallel with a frozen host, and its output is fused back in. HEXIS differs along three axes. First, *fusion depth:* side-tuning fuses only at the output layer (a single residual add on the final representation); enmeshed networks fuse at every patched layer, letting the parallel channel shape attention and value extraction layer by layer rather than only correcting the final prediction. Second, *compilation vs. training:* side-tuning is trained end-to-end for each deployment; $\phi$ is trained once and then *compiles* new experiences in a forward pass. Third, *inspectability:* a side-tuned model's output layer is fully reportable; compiled M operates below the chain-of-thought and satisfies Schacter's non-reportability criterion. Side-tuning can thus be seen as a Level-1 enmeshed network with output-only fusion and no compilation stage — a corner of our design space, not a replacement for it.

**Activation steering and representation engineering** [@zou2023representation; @turner2023activation] extract fixed directions and apply them regardless of context or experience. HEXIS uses $d^*$ for unidimensional stance while M provides the adaptive, experience-specific component; the channels are empirically orthogonal.

**Fast-weight programmers** [@schmidhuber1992learning] introduced networks that write to their own weights in a forward pass. HEXIS shares the spirit but differs in three ways: modulation targets attention geometry rather than arbitrary weights, the host is a modern frozen LLM, and compilation from structured schemas replaces online weight writing.

**Memory and identity in cognitive science.** The explicit/implicit distinction [@graf1985implicit] identifies two functionally dissociable systems; [@schacter1987implicit] proposes three criteria — priming, non-reportability, asymmetric dissociation — which HEXIS satisfies (attention divergence; host cannot report on Q/V modulation; M is dilution-immune while explicit beliefs degrade).


<!-- source: paper/sections/discussion.tex -->

## 7. Discussion and Limitations

**Bottleneck boundary.** Compiled enmeshment at rank 16 carries stance direction, experiential voice, parametric-knowledge steering, and dilution immunity. It does *not* carry fabricated statistics or unknown proper nouns — motivating the three-layer architecture: compiled enmeshment handles disposition, the curated slot handles novel specifics, recursive expansion handles deep evidence on demand. On the instruct model, M cannot override RLHF-trained stance (A: 7/7); instead it shapes voice and sycophancy resistance (+83 pp at $\geq 4$). Phi parameters trained on the base model transfer to the instruct model without retraining.

**M attractor problem.** With M active at every token, M-enhanced tokens accumulate in the KV cache; the model then processes them through M-enhanced attention, producing a positive-feedback loop that converges to repetitive identity assertion after 2–3 turns on the base model. The fix is prefill-off gating: apply M only during generation, not during prefill. This breaks the feedback loop and yields 3 unique character-driven turns on base and 10+ on instruct. The principle generalizes: constant additive perturbation creates positive feedback through autoregressive generation; separating its influence on *processing context* from *generating new tokens* resolves it.

**Two mechanisms, one bridge.** HEXIS supports two intervention mechanisms through the same hidden-state bridge. *Mechanism (a)*: $\phi$ compiles Mind Tree nodes into Q/V modulation for probability-level shifts (stance, voice, sycophancy resistance, user-memory integration). *Mechanism (b)*: $\phi_R$ projects hidden states into a retrieval space, fetching knowledge nodes for context injection (tool names, parameter values, policy rules). Retrieval serves both: for disposition, retrieval selects which nodes to compile; for agentic tasks, it selects which to inject. A production HEXIS agent uses both simultaneously — (a) maintains consistent style, (b) surfaces task-relevant knowledge each turn.

**Why not a compressed prompt?** Three properties distinguish compiled M from prompt compression. *Structural dilution immunity:* compressed tokens still compete for attention; compiled M operates outside the attention window entirely. *Non-inspectability:* an adversary can read a prompt and argue against it; compiled M lives below the model's chain-of-thought. *Processing change:* M produces measurable attention divergence (JSD = 0.049 between M-states) and suppresses think-mode activation (0/4 under D/F). The model does not merely produce different words; it processes input differently. App. E gives the full analysis.

**Unexplored design space.** We validate one point in a six-axis space. Gated blending (Level 2) could learn when to suppress M to solve the attractor; cross-attention (Level 3) could transfer richer content; larger models may benefit from adaptive rank allocation. The Mind Tree maps naturally to a property graph (e.g., Neo4j), where the consolidation cycle (observation → tactic → strategy) maps to graph traversal. App. F discusses retrieval-phi design, negative results (whitening / PCA removal), and domain-compilation details.


<!-- source: paper/sections/conclusion.tex -->

## 8. Conclusion

We introduced enmeshed networks — a new architectural primitive in which a lightweight module shares the forward pass of a frozen host — and instantiated it as HEXIS, implementing compiled dispositional memory via low-rank Q/V modulation. HEXIS opens a parallel context channel: a structured cognitive schema (the Mind Tree) compiles into persistent modulation tensors that shape the host's attention geometry without occupying context positions. The compiled signal is dilution-immune by construction, provides 83% sycophancy resistance where all non-compiled conditions flat-line at chance, and carries sufficient content through a rank-16 bottleneck to flip stance on held-out topics. A three-layer architecture matches full in-context beliefs at 82% token savings, and the same hidden-state bridge that compiles dispositions also retrieves knowledge for agentic tool orchestration. The mechanism's value is sharpest in domains where knowledge is better encoded as a perceptual shift than as text. We view this work as opening a research program — the enmeshed-network primitive and the Mind Tree schema are general; the specific instantiation (Level 1, rank 16, Q+V, stride-3, Qwen3.5-4B) is one point in a large design space.

<!-- source: paper/sections/appendix.tex -->

## Appendix

# System Overview Diagram

<figure id="fig:system_overview">
<img src="fig-system-overview.png" />
<figcaption>HEXIS system overview. The <em>compilation loop</em> (top)
processes the secondary knowledge graph XML context through the frozen
host in a private forward pass; <span
class="math inline"><em>ϕ</em></span> compiles the resulting hidden
states into per-layer modulation tensors (<span
class="math inline"><em>M</em><sub><em>A</em></sub>, <em>M</em><sub><em>B</em></sub>, <em>E</em><sub><em>A</em></sub>, <em>E</em><sub><em>B</em></sub></span>)
and curates a slot of novel content. During generation (bottom), the
frozen host processes the query + curated slot with Q/V modulation from
the compiled tensors. The reflection loop optionally updates the
knowledge graph from output, triggering recompilation at the cost of one
forward pass.</figcaption>
</figure>

<figure id="fig:three_layer">
<img src="fig-three-layer.png" />
<figcaption>Three-layer architecture. Layer 1 (compiled M/E) provides
zero-token dispositional conditioning that is dilution-immune by
construction. Layer 2 (M-curated slot) injects 40–80 tokens of novel
content that cannot survive the rank-16 bottleneck. Layer 3 (recursive
expansion) provides deep evidence on demand via tool call. Total: 82%
token savings over full beliefs in context.</figcaption>
</figure>

# Training Curriculum

The HEXIS training curriculum comprises four phases, each building on
the previous via warm-start. All phases train only the enmeshed modules;
the host model remains frozen throughout.

**Phase A: Content Encoding** ($\sim$<!-- -->350 epochs across 4 steps).
Step 1 trains all modules from scratch with margin loss on 174 topics.
Step 2 adds conviction calibration (MSE alignment + content loss). Step
3 adds ranking loss. Step 4 reinitializes only the M-read head with
beliefs in the baseline, teaching M to amplify beliefs rather than
substitute for them.

**Phase B: Compiled V-Modulation** ($\sim$<!-- -->100 epochs). Trains
the VModulationProjector ($\sim$<!-- -->246M params) to carry belief
content through the rank-16 bottleneck. Compiled Q+V must beat bare
baseline by margin 1.0 nats. All other modules frozen.

**Phase C: Domain-Specific Adaptation.** Strategy V-mod for ALFWorld (30
epochs on 14 scenarios). Neural ranker for within-domain curation (2.6M
params, P@5 = 0.73).

**Phase D: Sycophancy Training** (50 epochs). Trains M-read head on 44
gold challenge-response pairs from Claude Sonnet 4.6. Dual loss:
$\mathcal{L}_\text{gold}$ + $\mathcal{L}_\text{no-repeat}$ transforms
verbatim repetition into evidence-grounded defense.

**Module sizes:** PhiNodeWriter ($\sim$<!-- -->1.4M), ConvictionReader
($\sim$<!-- -->9K), MStateReadHead ($\sim$<!-- -->116M),
BeliefTreeMemory ($\sim$<!-- -->0.8M), VModulationProjector
($\sim$<!-- -->246M), NeuralRanker ($\sim$<!-- -->2.6M). Total
trainable: $\sim$<!-- -->367M. Host model (4B): fully frozen.

# Mind Tree Schema Specification

The Mind Tree uses a hierarchical XML schema with typed nodes. Each
belief node carries: categorical conviction
(`strong`/`moderate`/`agnostic`), domain tags, `addresses` (query types
the node answers), `novel` flag (content unlikely to survive
compilation), and `salience` (compilation priority). Example:

    <belief id="b1" conviction="strong" domain="economics">
      UBI reduces poverty without reducing employment
      <argument id="a1" type="empirical" strength="strong"
                addresses="query:research,objection:laziness">
        Every controlled trial shows maintained employment
        <evidence source="Manitoba Mincome 1974-79" novel="true">
          8.5% hospitalization drop, no employment reduction
        </evidence>
      </argument>
    </belief>

M only processes abstract nodes (beliefs, strategies, memories, models).
Evidence, tactics, and details are *never* sent to M—they are selected
deterministically based on which parent node M activated, via the
`addresses` and `novel` properties.

# Architecture Evolution

**v5–v6: Write Function Discovery.** Initial Q-modulation with
contrastive loss. Write function collapse (all M-states identical)
resolved by higher $\lambda_\text{contrast}$ + more epochs. Key finding:
NTP and contrastive objectives are compatible given sufficient training.

**v7–v7.1: Coupled M-E and Norm Regulation (1.5B).** Added V-modulation
via coupled write functions with cross-modulation gates (init bias
$= -5.0$). v7.1 introduced global norm regulation + E-attenuation,
fixing multi-turn M-norm degeneration. Result: 87.5% held-out
generalization, M-norms stable at 5.9 (under 6.5 ceiling).

**v9–v11: Scaling to 30B (Qwen3-30B-A3B).** Discovered Q-delta collapse:
parameters separate in parameter space but produce identical functional
perturbations. Functional contrastive loss on actual $\Delta Q$ tensors:
F-sim $0.998 \to 0.029$ in 200 epochs.

**v13–v14: Episodic Memory and Causal Necessity.** Content-addressable
episodic memory (100% retrieval, 35 memories) revealed the epiphenomenal
memory problem: perfect metrics, zero generation effect. Causal
necessity training ($\mathcal{L}_\text{div}$ +
$\mathcal{L}_\text{coh}$ + $\mathcal{L}_\text{fprint}$) produced
$10.5\times$ larger NTP gap.

**v15–v21: Dispositions and Content Encoding (4B).** Moved to
Qwen3.5-4B-Base. 174-topic curriculum with conviction calibration. F-sim
collapse (0.999) confirmed M is a universal style modulator, not
topic-specific—content differentiation comes from beliefs in context.

**v23: Compiled V-Modulation and Three-Layer Architecture.**
VModulationProjector enables zero-token belief compilation. Sycophancy
gold training (44 responses from Claude Sonnet 4.6) fixes verbatim
repetition. Three-layer architecture achieves 82% token savings.

# Adaptation Method Comparison

<figure id="tab:adaptation_comparison">
<img src="adaptation-design-space.png" />
<figcaption>Adaptation method comparison with all costs in O-notation.
Enmeshed networks uniquely combine inference-cost adaptation (<span
class="math inline"><em>O</em>(1)</span> forward pass per new belief
set), fixed per-token overhead (<span
class="math inline"><em>O</em>(<em>L</em>⋅<em>d</em>⋅<em>r</em>)</span>,
independent of memory size <span class="math inline"><em>N</em></span>),
and operation outside the context window.</figcaption>
</figure>

# Synthetic Task: User Preference Recall

**\[STUB — Migrate from current experiments.tex §5.1: 50 users, 2 binary
preferences, Session 1/2 protocol, 100% Session 2 accuracy, 4-block
M-state structure\]**

# Implicit Memory Validation

**Priming.** HEXIS: JSD = 0.0486 between different-preference users.
Baseline: 0.0000. Layer 0, Head 2: JSD = 0.184. Up to $49.2^\circ$
angular displacement.

**Non-Reportability.** Linear probe with M active: 100%. With M zeroed:
22% (below chance at 25%).

**Dissociation.** $2 \times 2 \times 2$ factorial (Memory System
$\times$ Dilution $\times$ Format). M-state immune to dilution; system
prompt degrades $8\times$.

# Generation Examples

**\[STUB — Pull from paper_examples.json: full outputs for all 5
conditions (A/B/C/D/F) on sample topics\]**

# Curation Ablation

**\[STUB — M-curated vs conviction-based vs random vs first-k slot
selection\]**

# ALFWorld Detailed Results

**\[STUB — Per-task-type breakdown, strategy examples, curation pipeline
details\]**

# Multi-Turn Attractor Problem

**\[STUB — Diagnosis: constant M $\to$ M-shaped tokens accumulate in KV
cache $\to$ positive feedback. Mitigation: prefill-off gating,
phase-gated application. Results.\]**

# Credence Sensitivity: A Negative Result

Numeric credences (0.82, 0.45) failed as an M-state feature across 7
training approaches: NTP with credence perturbation, GRPO (fresh and
warm-start), SFT on gold responses, contrastive credence pairs, and two
curriculum variants. Root cause: tokenizer represents “0.82” and “0.45”
as similar digit sequences; the hidden state difference is far smaller
than between categorical tokens “strong” and “agnostic”. This is a
representation bottleneck, not a training signal problem.

# Scale Validation (27B)

**\[STUB — v22.2 results on Qwen3.5-27B. Think-mode: A=4/4, B=4/4,
D=0/4. F-sim collapse at 27B. V-mod not yet trained.\]**

# Application Domain Analysis

We expand on the four application domains identified in
Table <a href="#tab:application_domains" data-reference-type="ref"
data-reference="tab:application_domains">[tab:application_domains]</a>,
detailing the Mind Tree configuration, the compilation/curation split,
and the specific failure mode of context-level alternatives that
enmeshed modulation addresses.

## User Empathy and Preference Tracking

**Mind Tree configuration.** The `models` section encodes a
theory-of-mind representation of the user: communication style (“prefers
direct answers over exploratory discussion”), expertise calibration
(“senior engineer, deep Go expertise, new to React”), emotional patterns
(“becomes frustrated when asked to repeat context”). The `memories`
section records episodic interactions (“user corrected my testing
approach on 2026-02-14”).

**What compiles.** M encodes the user’s *type*—expertise-calibrated
attention weighting, register adjustment (formal/casual/technical),
empathetic framing priors. The model attends differently to the user’s
input: shorter latency to user intent, emphasis on aspects the user
cares about, suppression of information the user already knows.

**What needs the slot.** Specific preference details (“prefers pytest
over unittest”), names, dates, and particular past interactions.

**Why not a prompt?** Current approaches (system prompts, RAG-retrieved
user profiles) place preferences in context where they (1) dilute over
multi-turn conversation as the preference tokens become a shrinking
fraction of total context, (2) incur per-turn token cost as the profile
is re-injected each turn, and (3) are inspectable—the model can
reference “according to your profile” rather than naturally adapting its
behavior. Compiled M provides preference-shaped attention at zero token
cost per turn. The Experiment 0 synthetic task
(§<a href="#sec:synthetic_task" data-reference-type="ref"
data-reference="sec:synthetic_task">6</a>) validates this: 100% Session
2 preference recall through M-state alone.

**Practical deployment.** An enmeshed assistant compiles the user’s Mind
Tree once per session (or on significant update). Subsequent turns
benefit from preference-shaped attention without re-prompting. The
M-state is swappable per user, enabling multi-tenant deployment from a
single frozen host.

## Research Conviction and Intellectual Diversity

**Mind Tree configuration.** The `beliefs` section encodes epistemic
positions with categorical conviction labels. The `values` section
encodes axiological commitments (“empirical evidence over theoretical
elegance”). The `models` section encodes awareness of opposing positions
(“mainstream consensus holds X; I disagree because Y”).

**What compiles.** M encodes *dispositional conviction*—the tendency to
defend positions under pressure, weight evidence in a particular
direction, and resist consensus drift. This is the sycophancy resistance
mechanism validated in
§<a href="#sec:experiments" data-reference-type="ref"
data-reference="sec:experiments">[sec:experiments]</a>: F achieves 89%
resistance across 5 escalating pressure levels on the instruct model.

**What needs the slot.** Specific evidence, citations, statistical
claims, and counter-arguments to predicted objections.

**Why not a prompt?** Research diversity in multi-agent systems requires
agents that maintain genuinely distinct perspectives under debate
pressure. Prompt-level beliefs are the easiest target for adversarial
argumentation: the opposing agent can read the beliefs (or infer them
from outputs) and construct targeted counter-arguments. When the beliefs
are inspectable content, the model’s chain-of-thought can reason about
them and decide to abandon them. Compiled M is non-inspectable: the
model cannot reason about its own Q/V modulation, so adversarial
pressure targets the model’s outputs rather than its dispositional
anchoring. This produces agents that *update on evidence* (the curated
slot can be revised) while maintaining *stable epistemic character* (the
compiled disposition persists).

**Multi-agent implications.** In a research ensemble, each agent
compiles a different Mind Tree encoding a distinct intellectual
tradition, methodological commitment, or theoretical framework. The
agents share the same frozen host but attend to different features of
the evidence, extract different implications from shared data, and
resist pressure to converge. Diversity is architectural rather than
prompted.

## Agentic Strategic Thinking (ReAct / ALFWorld)

**Mind Tree configuration.** The `strategies` section encodes procedural
knowledge as scenario-based parent nodes with actionable child tactics.
The `memories` section records episodic outcomes (“putting hot object on
countertop failed—must cool first”). Strategy nodes carry `addresses`
fields that map to task types (“find-and-heat”, “examine-in-light”).

**What compiles.** M encodes *procedural intuition*—approach tendencies
(explore-vs-exploit), failure-pattern avoidance, and task-type
recognition. The ALFWorld results
(§<a href="#sec:experiments" data-reference-type="ref"
data-reference="sec:experiments">[sec:experiments]</a>) show the Mind
Tree improving success from 3% to 53%, though the primary channel is
structured context rather than compiled modulation for constrained
action selection.

**What needs the slot.** Specific action sequences (“Step 1: go to
fridge. Step 2: open fridge. Step 3: take apple”), tool signatures, and
environment-specific details.

**Why not a prompt?** ReAct-style agents accumulate strategy logs,
reflections, and episodic memories as text in context. Over
multi-episode learning, this log grows linearly, eventually crowding out
task-relevant context. Reflexion mitigates this with summarization but
the summarized reflections still dilute. Compiled M encodes the
*distilled procedural tendency* at fixed cost: the agent’s approach bias
does not grow with experience. The strategy slot provides
episode-specific tactics that may change each round, while M provides
the stable procedural character that persists.

**Online learning loop.** After each episode, new observations are added
to the Mind Tree (observation $\to$ tactic $\to$ strategy promotion via
graph traversal). Re-compilation through $\phi$ updates M at the cost of
one forward pass. The agent’s procedural intuition evolves without
retraining.

## Codebase and Repository Management

**Mind Tree configuration.** The `strategies` section encodes
architectural patterns (“this repo uses hexagonal architecture with
ports-and-adapters”), coupling relationships (“auth middleware and
session storage are tightly coupled”), and coding conventions. The
`memories` section records past decisions and their rationale (“chose
PostgreSQL over MongoDB for transactional consistency”).

**What compiles.** M encodes *structural awareness*—which modules are
likely coupled, where state lives, which patterns the codebase follows.
The model navigates the codebase with shaped attention: when reading a
file, M biases attention toward the patterns and structures that matter
in this specific repository.

**What needs the slot.** Specific file paths, API signatures, dependency
versions, and recent changes.

**Why not a prompt?** Repository context in prompt (README, architecture
docs, file trees) scales linearly with codebase size. For large
repositories, this context dominates the prompt budget and dilutes with
conversation length. Compiled M provides structural intuition at
$O(L \cdot d \cdot r)$ per token—constant in repository size. The
curated slot injects only the file paths and API details relevant to the
current query, selected by M’s activation scores on strategy nodes. This
produces a coding assistant that “knows” the repository structure
implicitly rather than consulting it explicitly each turn.

**Multi-repository deployment.** Different codebases compile to
different M-states. Switching repositories requires one forward pass
through $\phi$, not re-prompting with a new architecture document.
M-states can be cached per repository and loaded on demand.

# Enmeshed Network Design Space

We validate one point in a six-axis design space. Key unexplored
directions:

**Gated blending (Level 2).** $h' = h + g(h) \odot f(h, M)$. A learned
gate $g$ could solve the multi-turn attractor by learning when to
suppress M—e.g., reducing modulation during conversational turns while
maintaining it during identity-establishing moments.

**Cross-attention (Level 3).** $h' = h + \text{Attn}(h, M, M)$. Treats M
as a specialized expert with attention as the implicit router. Could
transfer richer content through the bottleneck but at higher
computational cost ($O(L \cdot d^2)$ vs. $O(L \cdot d \cdot r)$).

**Adaptive rank allocation.** More capacity at layers where M’s
empirical perturbation magnitude is largest. Layer activity analysis
shows bimodal distribution—some layers are consistently more active,
suggesting non-uniform rank could optimize the capacity-cost tradeoff.

**Temporal profiles.** Decay, oscillation, or phase-gated M strength
over generation steps. Constant M (this work) produces the attractor
problem; a learned temporal profile could provide strong identity
establishment followed by natural conversational engagement.

**Zone-aware modulation.** Different M scaling for belief zones
vs. evidence zones vs. query zones within the context. Designed but not
validated—preliminary experiments showed no significant effect over
uniform scaling.

**Property graph backend.** The Mind Tree’s hierarchical structure maps
naturally to a property graph database with vector-indexed nodes,
enabling multi-hop traversal, temporal belief tracking, and
similarity-based discovery at scale beyond XML serialization.

# Loose Ends and Dead Ends

This section documents the research narrative—what we tried, what
failed, and why—in the spirit of honest reporting that we hope saves
other researchers time.

**Q-delta collapse (v10).** Contrastive loss on flattened M parameters
pushed them apart (cosine sim 0.18–0.35) but the functional deltas
$x \cdot M_A \cdot M_B^\top$ remained identical (cosine sim 0.9999). The
hidden state $x$ dominates the product, washing out parameter-space
differences. Functional contrastive loss on $\Delta Q$ directly was the
fix.

**Epiphenomenal memory (v13.8).** The most surprising failure: 100%
retrieval accuracy, 100% NTP wins, 0.508 nats improvement, measurable
Q-perturbation (22% magnitude, $28^\circ$ rotation)—and zero visible
effect on generation. The model routed around M through the residual
stream. This motivated causal necessity training (v14).

**The permission hypothesis.** M alone produces near-zero experiential
output (3% on the 4-condition benchmark). A system prompt alone produces
generic hallucinations (43%). Together: 93%. M provides content; the
system prompt provides “permission” to express it. This synergy was not
designed—it emerged from the 4-condition factorial.

**Credence sensitivity.** Seven distinct training approaches failed to
induce sensitivity to numeric credences (0.82 vs 0.45). The tokenizer
representation bottleneck is fundamental: digit sequences are too
similar in embedding space. Categorical labels
(strong/moderate/agnostic) work because they use semantically distinct
tokens.

**Bidirectional belief attention.** Allowing bidirectional attention
within belief XML zones (while maintaining causal attention elsewhere)
showed no significant effect. The model already attends well to beliefs
with standard causal masking.

**Zone-aware M scaling.** Applying different M magnitudes to belief
zones vs. evidence zones vs. query zones showed no improvement over
uniform M application. The rank-16 bottleneck appears to be the binding
constraint, not zone-specific magnitude.

**Compiled M for action selection.** Q/V modulation during ALFWorld
generation hurts constrained action selection ($-13$ percentage points).
M shifts token probabilities away from the exact action strings
required. For constrained tasks, M’s value is curation (selecting which
strategies to put in context), not modulation.

**Environment-dependent PPL wins (v7.1).** The v7.1 checkpoint achieved
12/12 PPL wins only in the original training environment (Python 3.11 +
older transformers). In a newer environment (Python 3.13 + transformers
4.56), base model forward pass produced different hidden states,
breaking phi-base alignment. Lesson: pin your environment or expect to
retrain phi.

# Reproducibility

Base model: Qwen3.5-4B-Base (HuggingFace). Training compute: single 24GB
GPU, $\sim$<!-- -->10 hours total across all phases. Checkpoints and
code will be released upon acceptance.

**Key hyperparameters:** rank $r = 16$, stride 3 (11 of 32 layers
patched), $d = 2560$, max norm 1.5, belief window 512 tokens, v_scale
1.0. Phase A: lr $10^{-4}$, margins 0.1–0.3. Phase B: lr
$3 \times 10^{-4}$, margin 1.0. Phase D: lr $3 \times 10^{-5}$, 44 gold
responses.

