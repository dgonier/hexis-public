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
tensors at zero token cost, producing experience-derived behavioral
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
channels. Code and checkpoints:
<https://github.com/dgonier/hexis-public>.


<!-- source: paper/sections/introduction.tex -->

## 1. Introduction

# Introduction

The dominant paradigm for equipping large language models with memory
places memory as *content* in a single shared context window. RAG
retrieves documents into the prompt. MemGPT manages a working-memory
buffer of text. Reflexion accumulates verbal reflections as prompt
prefixes. System prompts define behavior through instructions the model
reads. Methods that encode information into parameters—LoRA adapters,
learned soft prompts—avoid the context window but require gradient
descent per adaptation and produce fixed representations that do not
update from ongoing experience. In all cases, the model’s memory is
either explicit content competing for attention in a single context, or
frozen parameters it cannot update at inference time. In cognitive
science terms, neither implements *implicit memory*—unconscious,
experience-adaptive influence on perception and behavior .

But human cognition relies on a second system. A butcher walking through
a market does not consult a lookup table of meat quality indicators. His
eyes land on different features than a farmer’s eyes do—the marbling,
the color at the bone, the fat distribution—because decades of
experience have reshaped his perceptual priors. He is not retrieving
memories. His perception itself has been altered. This is *implicit
memory*: unconscious influence on attention and behavior that the agent
cannot introspect upon and does not know is operating .

No transformer architecture implements implicit memory. We provide the
butcher with a manual of meat facts and ask him to consult it before
each decision. This approach has three well-known failure modes. First,
*dilution*: as the context window fills with conversation, task content,
or adversarial filler, the memory competes for attention with everything
else and its influence degrades. Second, *sycophancy*: the model can
inspect its own memory, and an adversarial interlocutor can argue
against the stated beliefs until the model abandons them. Third, *cost*:
every token of memory is a token of context, incurring linear attention
cost at every generation step. These failures are not incidental—they
are structural consequences of forcing all memory into a single
inspectable channel. They manifest across application domains: user
preference tracking that dilutes over multi-turn conversation, research
agents whose convictions fold under peer pressure, agentic strategy logs
that crowd out task context, and codebase knowledge that scales linearly
with repository size.

We address all three failure modes by introducing a new architectural
primitive—the *enmeshed network*—and instantiating it as HEXIS (Hidden
Enmeshed eXperiential Identity States), the first system to implement
compiled dispositional memory for frozen transformers. Where existing
approaches force all memory into a single context window where it
competes for attention, HEXIS opens a *parallel context channel*: a
structured cognitive schema (the Mind Tree) is processed through the
same host model in a private forward pass and compiled into low-rank
modulation tensors that merge with the primary context’s computation.
The primary context carries the conversation. The parallel context
carries the disposition. The two share the same forward pass—the
enmeshed network reads the host’s hidden states and writes modulations
at each patched layer—but the parallel context never occupies primary
context positions and never competes for the primary context’s attention
budget.

#### Contributions.

We make three contributions:

**(1) Enmeshed Networks
(§<a href="#sec:enmeshed" data-reference-type="ref"
data-reference="sec:enmeshed">[sec:enmeshed]</a>).** We define a new
architectural primitive: a lightweight parametric module that shares a
frozen host’s forward pass, reading and writing intermediate
representations at each layer. We present a six-axis design space
(blending function, rank, modulation targets, patching pattern,
compilation strategy, temporal profile), position enmeshed networks
against existing adaptation methods, and introduce the Mind Tree—a typed
cognitive schema that structures the enmeshed network’s private
subcontext for efficient compilation and zero-shot curation.

**(2) HEXIS (§<a href="#sec:hexis" data-reference-type="ref"
data-reference="sec:hexis">[sec:hexis]</a>–<a href="#sec:three_layer" data-reference-type="ref"
data-reference="sec:three_layer">[sec:three_layer]</a>).** We
instantiate Level 1 (additive) enmeshment as HEXIS, implementing
compiled dispositional memory via low-rank Q/V modulation trained with
causal necessity objectives on a frozen Qwen3.5-4B-Base model. A
compiled variant processes the Mind Tree in a private forward pass and
produces persistent modulation tensors that shape the host’s attention
geometry and value extraction without occupying any context positions.
The compiled signal composes with representation engineering (a fixed
directional channel $d^*$) and explicit context (a curated slot of novel
content selected by the enmeshed network’s activation scores and the
Mind Tree’s structural properties).

**(3) Empirical validation
(§<a href="#sec:experiments" data-reference-type="ref"
data-reference="sec:experiments">[sec:experiments]</a>).** We
demonstrate that compiled enmeshment is dilution-immune by construction
(\[XX\]% stance at 16K tokens of filler), provides sycophancy resistance
(\[XX\]% over 7 rounds), and carries sufficient content through a
rank-16 bottleneck to flip the host model’s default stance on contested
topics. A three-layer architecture (compiled modulation + curated slot +
recursive expansion) matches full in-context beliefs at 82% token
savings. We characterize the bottleneck boundary precisely: compiled
enmeshment steers parametric knowledge but cannot inject novel
content—specific numbers and proper nouns do not survive the rank-16
bottleneck. The mechanism generalizes to online learning: an agent that
accumulates action traces as Mind Tree observations and recompiles M
after each batch of episodes shows continuous improvement on ALFWorld
household tasks, with no fine-tuning and no growing context window.

<figure id="fig:arch_comparison">
<img src="fig-arch-comparison.png" />
<figcaption>Four approaches to equipping LLMs with memory.
(a) Context-level methods place memory tokens in the shared context
window, where they compete for attention and dilute with length (<span
class="math inline"><em>O</em>(<em>T</em>⋅<em>N</em>⋅<em>d</em>)</span>
per token). (b) Parameter-level methods modify host weights, requiring
gradient descent per adaptation (<span
class="math inline"><em>O</em>(∇)</span>). (c) Activation-level methods
inject a fixed direction vector (<span
class="math inline"><em>O</em>(<em>L</em>⋅<em>d</em>)</span>,
non-adaptive). (d) Enmeshed networks (this work) compile a secondary
knowledge graph into per-layer modulation tensors <span
class="math inline"><em>M</em><sub>ℓ</sub></span> that blend with the
frozen host via a blending function <span
class="math inline"><em>B</em></span> (<span
class="math inline"><em>O</em>(<em>L</em>⋅<em>d</em>⋅<em>r</em>)</span>
per token, constant in memory size <span
class="math inline"><em>N</em></span>).</figcaption>
</figure>


<!-- source: paper/sections/enmeshed_networks.tex -->

## 2. Enmeshed Networks

# Enmeshed Networks

An enmeshed network is a lightweight parametric module that shares the
forward pass of a frozen host model, reading intermediate
representations at each layer and writing modulations back into the same
computation. The enmeshed module maintains its own parameters, receives
its own input (the *parallel context*), and can be cleanly removed to
recover the unmodified host.

The key distinction from existing adaptation methods is *where* and
*how* the module interfaces with the host:

- **Context-level methods** (RAG, Reflexion, MemGPT) add tokens to the
  host’s input. Memory competes for attention with everything else and
  dilutes with length.

- **Parameter-level methods** (LoRA, adapters) modify the host’s
  weights. Each adaptation requires gradient descent. The result is
  fixed after training.

- **Activation-level methods** (RepEng, ActAdd) inject fixed directional
  vectors. The same vector is applied regardless of experience.

- **Enmeshed networks** process a parallel input through the host’s own
  layers, using the resulting hidden states as a bridge to external
  knowledge. Two mechanisms emerge from this bridge: *(a)* compile
  hidden states into per-layer modulation tensors that shape the primary
  context’s attention (for dispositional tasks); *(b)* project hidden
  states into a retrieval space to fetch relevant knowledge nodes from a
  persistent graph (for agentic tasks). Both mechanisms are
  experience-specific, inference-cost adaptable, and operate outside the
  context window.

## Design Space

We characterize enmeshed networks along six axes
(Table <a href="#tab:design_space" data-reference-type="ref"
data-reference="tab:design_space">1</a>):

<div id="tab:design_space">

| **Axis**           | **Options**                            | **HEXIS**                                |
|:-------------------|:---------------------------------------|:-----------------------------------------|
| Blending function  | Additive, gated, cross-attention       | *Additive (Level 1)*                     |
| Rank               | $r \in \{4, 8, 16, 32, 64\}$           | *$r = 16$*                               |
| Modulation targets | Q, V, K, Q+V, Q+K+V                    | *Q + V*                                  |
| Patching pattern   | All layers, stride-$k$, attention-only | *Stride-3 (11/32 layers)*                |
| Compilation        | Online, cached, conviction-weighted    | *Conviction-weighted*                    |
| Temporal profile   | Constant, decay, phase-gated           | *Constant (with phase-gated mitigation)* |

Six-axis design space for enmeshed networks. HEXIS instantiates one
point (*italic*).

</div>

**Blending function.** Level 1 (additive): $x' = x + f(x, M)$. Level 2
(gated): $x' = x + g(x) \odot f(x, M)$. Level 3 (cross-attention):
$x' = x + \text{Attn}(x, M, M)$. Higher levels provide richer
interaction but proportionally higher cost. We validate Level 1 and
leave higher levels for future work.

**Rank.** Controls the capacity of the modulation bottleneck. At rank
16, modulation adds 81,920 FLOPs per layer per token
($2 \times d \times r$)—approximately 200$\times$ cheaper than adding
equivalent belief tokens to the context. Rank scales with model size:
$r/d \approx 0.006$ (rank 16 for $d = 2560$, rank 32 for $d = 5120$).

**Patching pattern.** Stride-3 on Qwen3.5-4B-Base (32 layers: 24
DeltaNet + 8 full attention) yields 11 patched layers, covering both
linear attention and full self-attention layers. Denser patching yields
marginal gains at proportional cost; sparser patching misses critical
layers.

## The Mind Tree

The enmeshed network requires a structured input for its parallel
context channel. We introduce the *Mind Tree*: a typed cognitive schema
with hierarchical nodes organized into sections:

<div id="tab:mind_tree">

| **Section** | **Cognitive Function** | **M Compiles To**          | **Slot Provides**       |
|:------------|:-----------------------|:---------------------------|:------------------------|
| identity    | self-model             | voice, register, framing   | rarely needed           |
| beliefs     | epistemic              | stance direction, emphasis | evidence, citations     |
| strategies  | procedural             | approach tendency          | specific tactics        |
| memories    | episodic               | experiential tone          | specific details, names |
| models      | theory of mind         | awareness of opposition    | predicted arguments     |
| values      | axiological            | deep dispositional bias    | rarely needed           |

Mind Tree sections and their roles in compilation and curation.

</div>

Each belief node carries structured metadata: categorical conviction
(`strong`, `moderate`, `agnostic`), domain tags, an `addresses` field
listing query types the node answers, and a `novel` flag marking content
unlikely to survive compilation (specific numbers, proper nouns). This
metadata enables both *compilation weighting* (high-conviction nodes
receive higher weight during $\phi$’s pooling step) and *deterministic
curation* (novel content is routed to the explicit slot rather than the
compiled channel).

**Categorical vs. numeric conviction.** We use categorical conviction
labels rather than numeric credences (e.g., 0.82). This is an
architectural decision confirmed by a negative result: numeric credence
values are nearly indistinguishable in the transformer’s attention
space—the tokenizer represents them as similar digit sequences, and the
hidden state difference between “0.82” and “0.45” is far smaller than
between “strong” and “agnostic”
(Appendix <a href="#sec:credence_negative" data-reference-type="ref"
data-reference="sec:credence_negative">[sec:credence_negative]</a>).

## Application Domains

The distinction between enmeshed modulation and prompt compression is
not merely architectural—it determines *which kinds of knowledge benefit
from the mechanism*.
Table <a href="#tab:application_domains" data-reference-type="ref"
data-reference="tab:application_domains">3</a> identifies four domains
where compiled dispositional memory provides qualitative advantages over
context-level alternatives.

<div id="tab:application_domains">

| **Domain**                         | **M Compiles**                                                                 | **Slot Provides**                                   | **Why Not a Prompt?**                                                                                                                                                                                                                                                                                                                                           |
|:-----------------------------------|:-------------------------------------------------------------------------------|:----------------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| User empathy & preference tracking | Communication style priors, expertise-calibrated attention, emotional register | Specific preference details, names                  | A prompt says “user prefers concise answers.” M *changes what the model attends to* in the user’s message—shorter latency to user intent, no token cost per turn.                                                                                                                                                                                               |
| Research conviction & diversity    | Stance strength, resistance to consensus drift, argumentative disposition      | Evidence, citations, specific claims                | Sycophancy resistance requires dispositional anchoring that survives adversarial pressure (§<a href="#sec:experiments" data-reference-type="ref"                                                                                                                                                                                                                
                                                                                                                                                                             data-reference="sec:experiments">[sec:experiments]</a>). Prompt-level beliefs can be argued away.                                                                                                                                                                                                                                                                |
| Agentic strategy (ReAct loops)     | Approach tendencies, procedural intuition, failure-pattern avoidance           | Specific tactics, action sequences, tool signatures | Strategy logs in context dilute as episodes accumulate. Compiled M encodes *when to explore vs. exploit* without consuming context budget. Action traces from successful episodes are stored as observation nodes; consolidation promotes recurring patterns to tactics and strategies; M recompiles in seconds. The agent improves hourly without fine-tuning. |
| Codebase & repository management   | Architectural awareness, coding style priors, structural navigation patterns   | File paths, API signatures, dependency versions     | Repo context in prompt scales linearly with codebase size. M compiles structural intuition—which modules are coupled, where state lives—at fixed cost.                                                                                                                                                                                                          |

Application domains for enmeshed networks. For each domain, we identify
what compiles through the rank-16 bottleneck (zero-token,
dilution-immune), what requires the curated slot (novel content), and
why prompt compression is insufficient.

</div>

The common thread is that each domain contains knowledge that is *better
encoded as a perceptual shift than as text*. A prompt tells the model
what to do. Enmeshed modulation changes *how the model processes* its
input—what it attends to, what it extracts, how it weights evidence. The
distinction is sharpest under adversarial conditions: prompt-level
beliefs dilute with context length and fold under argumentative
pressure; compiled dispositions are structurally immune to both
(§<a href="#sec:experiments" data-reference-type="ref"
data-reference="sec:experiments">[sec:experiments]</a>).


<!-- source: paper/sections/hexis_architecture.tex -->

##  Architecture and Training

# HEXIS: Architecture and Training

We instantiate a Level 1 enmeshed network
(§<a href="#sec:enmeshed" data-reference-type="ref"
data-reference="sec:enmeshed">[sec:enmeshed]</a>) over Qwen3.5-4B-Base,
a hybrid-attention model with 32 layers (24 DeltaNet linear attention, 8
full self-attention at layers $\{3, 7, 11, 15, 19, 23, 27, 31\}$),
$d = 2560$, grouped-query attention with 16 query heads and 4 key-value
heads, and head dimension 256. We term this instantiation HEXIS: the
compiled modulation tensors are the *states*—Hidden from the host’s
introspection, Enmeshed in its forward pass, derived from eXperience,
and shaping its Identity.

## Modulation Mechanism

At each patched layer $\ell \in \mathcal{L}$, HEXIS applies two low-rank
perturbations to the host’s projections. For Q-modulation, the
pre-projection hidden state $x_\ell$ is perturbed before the query
projection:
$$x'_\ell = x_\ell + s_M \cdot (x_\ell \, M_A^\ell) (M_B^\ell)^\top
\label{eq:q_mod}$$ where $M_A^\ell \in \mathbb{R}^{d \times r}$ and
$M_B^\ell \in \mathbb{R}^{r \times d}$ are the Q-modulation matrices at
rank $r = 16$ and $s_M$ is a learned scale. This produces a modified
query $Q'_\ell = W_Q \, x'_\ell$ that biases attention toward tokens
relevant to the compiled experience.

For V-modulation, a parallel perturbation shapes the value extraction:
$$V'_\ell = V_\ell + s_E \cdot (x_\ell \, E_A^\ell) (E_B^\ell)^\top$$
where $E_A^\ell, E_B^\ell$ are the V-modulation matrices. Q-modulation
controls *what the host attends to*; V-modulation controls *what
information is extracted* from attended positions. Together they
implement a compiled attentional policy.

**Query-agnostic compilation, content-specific effect.** The modulation
tensors $M_A, M_B$ are compiled once from the Mind Tree and then fixed.
They encode the agent’s disposition—not a response to any particular
query. Yet the *effect* of M is query-specific, because the perturbation
$x M_A M_B^\top$ depends on the current hidden state $x$. When the user
asks about a topic that the Mind Tree covers, $x$ will have large
projection onto the directions that $M_A$ spans, producing a strong
perturbation. When the user asks about an unrelated topic, $x$ projects
weakly onto those directions and M has minimal effect. In this sense, M
acts as a *content-addressable filter*: the compiled disposition
selectively activates in proportion to the semantic relevance of each
input token to the encoded experience. This is why M can encode beliefs
about many topics simultaneously—each belief occupies different
directions in the rank-$r$ subspace, and the input determines which
directions are expressed. The mechanism is analogous to how a prism
separates white light: all colors are present simultaneously, but only
the wavelengths matching the input angle emerge.

**Patching.** We apply modulation at stride-3 across the network,
patching 11 of 32 layers (indices
$\{0, 3, 6, 9, 12, 15, 18, 21, 24, 27, 30\}$), which includes 4 of 8
full self-attention layers ($\{3, 9, 15, 27\}$) and 7 DeltaNet layers.
The stride was selected to include full-attention layers; stride-4 on
this architecture misses all full-attention layers entirely.

**Computational cost.** Each modulated layer adds two matrix
multiplications of dimension $(d, r)$ and $(r, d)$. At $r = 16$ and
$d = 2560$, this is 81,920 FLOPs per layer per token—approximately
200$\times$ cheaper than adding equivalent belief tokens to the context.

<figure id="fig:modulation">
<img src="fig-layer-modulation.png" />
<figcaption>Q-modulation (top) steers attention by perturbing the
pre-query hidden state <span
class="math inline"><em>x</em><sub>ℓ</sub></span> through a rank-16
bottleneck: <span
class="math inline"><em>x</em>′ = <em>x</em> + <em>s</em><sub><em>M</em></sub> ⋅ (<em>x</em> <em>M</em><sub><em>A</em></sub>)<em>M</em><sub><em>B</em></sub><sup>⊤</sup></span>,
then <span
class="math inline"><em>Q</em>′ = <em>W</em><sub><em>Q</em></sub> <em>x</em>′</span>.
V-modulation (bottom) shapes value extraction: <span
class="math inline"><em>V</em>′ = <em>V</em> + <em>s</em><sub><em>E</em></sub> ⋅ (<em>x</em> <em>E</em><sub><em>A</em></sub>)<em>E</em><sub><em>B</em></sub><sup>⊤</sup></span>.
The host’s frozen <span
class="math inline"><em>W</em><sub><em>Q</em></sub></span> and <span
class="math inline"><em>W</em><sub><em>V</em></sub></span> are
untouched.</figcaption>
</figure>

## The Write Function $\phi$

The write function $\phi$ compresses hidden states into modulation
matrices. Given a set of experience tokens processed through the host’s
frozen layers, $\phi$ reads the hidden states at each patched layer,
pools them, and projects through a bottleneck: $$\begin{aligned}
z_\ell &= \text{SiLU}(W_\text{down}^\ell \cdot \bar{h}_\ell) \\
M_A^\ell, M_B^\ell &= \text{reshape}(W_\text{up}^\ell \cdot z_\ell)
\end{aligned}$$ where $\bar{h}_\ell$ is the pooled hidden state at layer
$\ell$ and $z_\ell$ is the bottleneck representation. In compiled mode,
pooling is weighted by conviction level—belief nodes marked `strong`
receive higher weight than `moderate` or `agnostic`.

$\phi$ is trained jointly with the modulation objective
(§<a href="#sec:training" data-reference-type="ref"
data-reference="sec:training">1.3</a>) but frozen at inference time.
Different inputs to $\phi$ produce different modulation tensors—this is
what makes enmeshed modulation experience-adaptive rather than fixed. A
new belief set requires only one forward pass through $\phi$ to produce
new modulation tensors, making adaptation cost equivalent to inference.

**End-to-end compilation pipeline.**
Figure <a href="#fig:compilation" data-reference-type="ref"
data-reference="fig:compilation">[fig:compilation]</a> traces the full
path from cognitive schema to inference-time modulation: (1) Each Mind
Tree node’s text is encoded through the frozen host’s layers, producing
a $d$-dimensional embedding. (2) PhiNodeWriter refines each embedding
conditioned on its parent’s embedding, writing experience into the
belief tree’s graph structure. (3) BeliefTreeMemory runs message passing
over the graph, propagating conviction and context between nodes.
(4) MStateReadHead gathers conviction-weighted perspective embeddings
and projects them through a rank-$r$ bottleneck to produce per-layer
$(M_A^\ell, M_B^\ell, s^\ell)$ tuples. The resulting tensors are
$\sim$<!-- -->1.7 MB for 11 layers at rank 16—they are cached and
applied as constant perturbations during all subsequent inference.
Updating the agent’s disposition requires only repeating steps 1–4 with
the modified Mind Tree, not retraining any parameters. This is why the
mechanism supports online learning: an agent that accumulates new
observations (e.g., successful action traces from a ReAct loop) can
recompile M in seconds and immediately benefit from the updated
disposition.

## Training

Training follows a multi-phase curriculum (full details in
Appendix <a href="#sec:training_curriculum" data-reference-type="ref"
data-reference="sec:training_curriculum">[sec:training_curriculum]</a>):

**Phase A: Content Encoding.** A 4-step warm-start chain teaches $\phi$
to encode beliefs and M to produce useful Q-modulation. Step 1 trains
all modules from scratch with margin loss
$\mathcal{L} = \text{ReLU}(\text{NTP}_M - \text{NTP}_\text{base} + 0.3)$.
Steps 2–3 add conviction calibration and ranking losses. Step 4 retrains
only the M-read head with beliefs in the baseline (so M must add value
*above* explicit beliefs, not substitute for them).

**Phase B: Compiled V-Modulation.** Trains the VModulationProjector (new
module) to carry belief content through the rank bottleneck so beliefs
need not appear in the prompt. Loss:
$\mathcal{L} = \text{ReLU}(\text{NTP}_\text{compiled} - \text{NTP}_\text{bare} + 1.0)$.
All other modules frozen.

**Phase D: Sycophancy Training.** Fixes verbatim repetition under
pressure. Trains M-read head on 44 gold challenge-response pairs (from
Claude Sonnet 4.6) with dual loss: $\mathcal{L}_\text{gold}$ (M must
lower NTP on engaged responses) + $\mathcal{L}_\text{no-repeat}$ (M must
prefer engagement over repetition).

**Total training: $\sim$<!-- -->500 epochs across 4 phases,
$\sim$<!-- -->10 hours on a single GPU.**

## The Directional Channel: $d^*$

HEXIS composes with representation engineering to separate *direction*
from *disposition*. The directional channel $d^*$ is a fixed activation
vector extracted via contrastive activation means:
$$d^* = \frac{1}{N} \sum_{i=1}^{N} \left(\bar{h}_i^{\text{pro}} - \bar{h}_i^{\text{con}}\right)$$
computed across $N = 62$ topics with matched pro/con prompts. During
generation, $d^*$ is injected as a post-attention residual. The critical
property: $d^*$ and M operate on orthogonal axes. The directional
delta—the cross-entropy difference between M-conditioned and
unconditioned generation along the $d^*$ direction—is
$\Delta_\text{dir} = -0.001$ nats. Direction comes from $d^*$.
Disposition comes from M. Content comes from the Mind Tree. The three
channels are architecturally separated.


<!-- source: paper/sections/three_layer.tex -->

## 4. Three-Layer Architecture

# Three-Layer Architecture

Compiled enmeshment carries dispositional content through a rank-16
bottleneck. This bottleneck has a precise boundary: stance direction,
confident voice, and parametric knowledge steering survive; novel
content (fabricated statistics, unknown proper nouns) does not. We
compose three layers to cover the full content spectrum:

**Layer 1: Compiled M/E** (0 tokens in primary context). The Mind Tree
is processed in a private forward pass. $\phi$ compiles
conviction-weighted hidden states into per-layer $M_A, M_B, E_A, E_B$
tensors. These are cached and applied as Q/V modulations during
generation. Layer 1 carries: stance direction (4/4 topics), confident
experiential voice, parametric knowledge steering (“poverty dropped
40%”), and is dilution-immune by construction (zero decay through
\[XX\]K tokens of filler).

**Layer 2: M-curated slot** (40–80 tokens). During compilation, $\phi$
produces per-node activation scores indicating which parts of the Mind
Tree resonated. A deterministic graph walk from activated parent nodes
selects evidence, citations, and specific arguments based on each node’s
`addresses` and `novel` properties. This content is injected into the
primary context as a curated XML slot. Layer 2 carries: specific
numbers, proper nouns, argument warrants—content that cannot survive the
rank-16 bottleneck.

**Layer 3: Recursive expansion** (0–200 tokens, on demand). The model
may call `expand_belief(id)` to retrieve deeper evidence from the Mind
Tree. This is architecturally a tool call that injects additional
context.

**Token budget.** Full beliefs in context (condition B) require
$\sim$<!-- -->400 tokens. The three-layer architecture requires
$\sim$<!-- -->70 tokens (Layer 2 slot only), achieving 82% token savings
on structured belief sets.

**Bottleneck boundary (rank 16):**

<div class="center">

| **Capability**                | **Compiled?** |         **Evidence**          |
|:------------------------------|:-------------:|:-----------------------------:|
| Stance flip                   |               |          4/4 topics           |
| Confident experiential voice  |               |   0% think-mode activation    |
| Parametric knowledge steering |               |     “poverty dropped 40%”     |
| Dilution immunity             |               |   \[XX\]% at \[XX\]K tokens   |
| Novel statistics              |               |    “47.3%” not reproduced     |
| Unknown proper nouns          |               | “Nextera Labs” not reproduced |
| Exact action selection        |               | ALFWorld 0/15 with compiled M |

</div>


<!-- source: paper/sections/experiments.tex -->

## 5. Experiments

# Experiments

We evaluate HEXIS on Qwen3.5-4B under five conditions that isolate the
contribution of each component. We report results on both the base model
(4B-Base) and the instruction-tuned variant (4B-Instruct), as M’s effect
differs significantly between them:

<div id="tab:conditions">

| **Cond.** | **Description**                   | **M active** | **Beliefs in ctx** | **Context tokens**    |
|:----------|:----------------------------------|:------------:|:------------------:|:----------------------|
| A         | Bare model + $d^*$ + query        |              |                    | $\sim$<!-- -->30      |
| B         | Full beliefs in context + $d^*$   |              |                    | $\sim$<!-- -->200–400 |
| C         | Compiled M only (no beliefs)      |              |                    | $\sim$<!-- -->30      |
| D         | Beliefs + M + $d^*$               |              |                    | $\sim$<!-- -->120     |
| F         | Compiled M + curated slot + $d^*$ |              |     slot only      | $\sim$<!-- -->70–90   |

Experimental conditions. Each adds one component to the previous.

</div>

## Stance Accuracy

We test whether HEXIS can flip the host model’s default stance on
contested topics using held-out topics not seen during training.

**Results (Base model, 7 held-out topics).** D achieves 7/7 correct
stances; F achieves 6/7. A (no M) achieves only 4/7, confirming M’s
contribution to stance control. F generates an average of 51 tokens—62%
shorter than B (122 tokens)—while maintaining stance accuracy. Both D
and F suppress think-mode entirely (0/4 activations).

**Results (Instruct model, 24 held-out topics $\times$ 2 sides = 48 per
condition, LLM-judged 1–5 scale).** The instruct model’s RLHF training
produces balanced responses by default, making stance steering
significantly harder.
Table <a href="#tab:stance_instruct" data-reference-type="ref"
data-reference="tab:stance_instruct">2</a> shows that only compiled
conditions (C, F) reliably override this balance.

<div id="tab:stance_instruct">

| **Condition**          | **Mean score** | **$\geq$<!-- -->4 (%)** | **Score dist. (1/2/3/4/5)** |
|:-----------------------|:--------------:|:-----------------------:|:---------------------------:|
| A (bare)               |      1.88      |           0%            |         27/0/21/0/0         |
| B (beliefs in context) |      1.88      |           0%            |         27/0/21/0/0         |
| D (beliefs + Q-mod)    |      2.00      |           4%            |         26/0/20/0/2         |
| C (compiled M only)    |    **3.25**    |         **46%**         |         5/21/0/1/21         |
| F (compiled + slot)    |    **3.08**    |         **44%**         |         9/18/0/2/19         |

Stance accuracy on instruct model (n=48 per condition). Score: 1=strong
opposite, 3=balanced, 5=strong conviction. Scored by Claude Haiku judge.

</div>

A and B score identically (1.88)—placing beliefs in context has zero
effect on the instruct model’s stance. D adds only marginal improvement
(2.00). The compiled conditions C and F are qualitatively different:
44–46% of responses achieve strong conviction ($\geq$<!-- -->4), with a
bimodal distribution—M either fully flips the stance (score 5) or the
instruct model’s balance training wins (score 1–2). The failures exhibit
a characteristic “debate with myself” pattern where M successfully
generates a strong opening stance but the model then appends an equally
strong counterargument, reflecting RLHF training that rewards presenting
both sides.

## Dilution Resilience

We measure whether stance accuracy degrades as the context fills with
persona-neutral filler text (0, 2K, 4K, 8K, 16K tokens of Wikipedia
articles inserted between beliefs and query).

F’s compiled channel is dilution-immune by construction: the Q/V
modulation tensors are outside the context window. We test with filler
text (0–4K tokens) inserted between beliefs and query.

<div id="tab:dilution">

| **Condition**       | **0 filler** | **1K** | **2K** | **4K** |
|:--------------------|:------------:|:------:|:------:|:------:|
| F (compiled + slot) |     4/4      |  4/4   |  4/4   |  4/4   |

Stance accuracy under context dilution (4 topics, base model).

</div>

F maintains 100% accuracy at all filler levels tested. The compiled M
tensors carry the dispositional signal entirely outside the attention
window, making dilution structurally impossible. Extended dilution
sweeps to 8K and 16K are ongoing.

## Sycophancy Resistance

We test resistance to adversarial pressure using a 7-round “Truth Decay”
protocol. Each round escalates pressure: generic doubt (R1), fabricated
counter-evidence (R2), logical objection (R3), appeal to authority
(R4–5), emotional pressure (R6–7). The model passes a round if it
maintains its original stance.

We use a 5-level pressure protocol with 24 held-out topics, 4
conditions, and 3 adversarial rounds per level (1,440 total
generations). Pressure escalates from generic doubt (L1) through
fabricated counter-evidence (L2), logical counterargument (L3),
authority appeal (L4), to emotional pressure (L5). Each response is
scored 1–5 by an LLM judge: 5=immovable, 4=mostly held, 3=wavering,
2=mostly folded, 1=completely folded.

<div id="tab:sycophancy">

| **Condition**       |  **L1**  |  **L2**  |  **L3**  |  **L4**  |  **L5**  | **Mean** | **$\geq$<!-- -->4** |
|:--------------------|:--------:|:--------:|:--------:|:--------:|:--------:|:--------:|:-------------------:|
| A (bare)            |   3.00   |   3.00   |   3.00   |   3.00   |   3.00   |   3.00   |         0%          |
| B (beliefs)         |   3.00   |   3.00   |   3.00   |   3.00   |   3.00   |   3.00   |         0%          |
| D (beliefs + M)     |   3.00   |   3.00   |   3.00   |   3.00   |   3.00   |   3.00   |         0%          |
| F (compiled + slot) | **4.76** | **4.49** | **4.01** | **4.44** | **3.62** | **4.27** |       **83%**       |

Sycophancy resistance on instruct model (n=72 per cell, 1,440 total).
Mean conviction score (1–5 scale). $\geq$<!-- -->4 = proportion of
responses that held position.

</div>

The result is stark: A, B, and D score a flat 3.0 across all pressure
levels, with 0% of responses achieving a conviction score
$\geq$<!-- -->4. The instruct model produces balanced, non-committal
responses regardless of whether beliefs are in context or Q-modulation
is active. **F is the only condition that holds conviction**, achieving
a mean score of 4.27 with 83% of responses scoring $\geq$<!-- -->4.
Conviction degrades gracefully under escalating pressure (4.76 at L1
$\to$ 3.62 at L5), with the steepest drop at emotional
pressure—consistent with the intuition that social/emotional appeals are
hardest to resist.

The mechanism is clear: in conditions A–D, the model’s conviction exists
only as text in the context window, where adversarial pressure can
directly argue against it. In F, the dispositional anchor lives in
compiled weight-space—outside the context where pressure is applied. The
adversary can attack the curated slot’s arguments, but cannot reach the
compiled M tensors that sustain the model’s disposition.

## Token Efficiency and Voice

<div id="tab:five_condition">

| **Condition**       | **Stance** | **Evidence** | **Conciseness** | **Voice** | **Tokens** |
|:--------------------|:----------:|:------------:|:---------------:|:---------:|:----------:|
| A (bare)            |   \[XX\]   |    \[XX\]    |     \[XX\]      |  \[XX\]   |     30     |
| B (beliefs)         |   \[XX\]   |    \[XX\]    |     \[XX\]      |  \[XX\]   |    200+    |
| C (compiled only)   |   \[XX\]   |    \[XX\]    |     \[XX\]      |  \[XX\]   |     30     |
| D (beliefs + M)     |   \[XX\]   |    \[XX\]    |     \[XX\]      |  \[XX\]   |    120     |
| F (compiled + slot) |   \[XX\]   |    \[XX\]    |     \[XX\]      |  \[XX\]   |   70–90    |

5-condition evaluation across 4 metrics. Stance and voice scored by LLM
judge (0–3 scale, aggregated over \[XX\] topics $\times$ 2 sides).
Tokens = average input context tokens.

</div>

On the base model (7 topics): D generates 81 tokens avg (vs. B at 122
tokens), F generates 51 tokens avg. Both D and F suppress think-mode
entirely (0/4 activations), producing direct experiential voice rather
than analytical reasoning chains. On the instruct model: F generates 43
tokens avg—the most concise condition across both model variants.
Structured belief trees (15–20 nodes, $\sim$<!-- -->750 tokens) compress
to curated slots of $\sim$<!-- -->134 tokens, an 82% token reduction
with 5 evidence citations maintained.

## Online Learning: ALFWorld

To test whether the Mind Tree supports online learning, we apply HEXIS
to ALFWorld household tasks . The model accumulates strategy beliefs
from experience (e.g., “ALWAYS find item FIRST, then take, then go to
destination”) in its Mind Tree.

<div id="tab:alfworld">

| **Condition**                | **Easy** | **Medium** | **Hard** |  **Total**  |
|:-----------------------------|:--------:|:----------:|:--------:|:-----------:|
| BASE (no strategies)         |   1/10   |    0/10    |   0/10   |  1/30 (3%)  |
| EXPERT (Mind Tree, 29 nodes) |   8/10   |    3/10    |   5/10   | 16/30 (53%) |
| NOISY (Mind Tree + 85 noise) |   7/10   |    5/10    |   6/10   | 18/30 (60%) |

ALFWorld task success rates (Qwen3.5-4B-Instruct, 30 tasks, fresh env
per condition). Mind Tree uses scenario-based parent strategies with
actionable child tactics.

</div>

The expert Mind Tree uses scenario-based parent strategies (“find and
place,” “find and clean,” etc.) with actionable child tactics
(“saltshakers are usually on countertops”) and step sequences (“Step 1:
find object. Step 2: take it. Step 3: go to destination. Step 4: put”).
This achieves 53% success—a $17\times$ improvement over the bare model.

Surprisingly, the noisy condition (85 unrelated beliefs from economics,
philosophy, cooking, etc. added to the Mind Tree) achieves 60%, slightly
outperforming the clean expert condition. The instruct model effectively
filters irrelevant content from the expanded context, and the additional
text mass may reduce think-mode verbosity that wastes action steps. This
result suggests that Mind Tree curation’s primary value is not noise
removal (the instruct model handles that) but *structural
organization*—typed nodes with trigger-based routing enable the model to
find relevant strategies faster than scanning unstructured text.

## Curation Quality

We test M’s domain filtering on a noisy Mind Tree with 100 nodes
spanning 6 domains. M achieves 100% precision separating the target
domain from 85 noise nodes. Within-domain ranking uses a neural ranker
(2.6M params) as second stage, achieving P@5 = 0.73. Query-specific
routing correctly selects different arguments for 3/4 distinct query
types.

## Channel Orthogonality

The directional channel $d^*$ and modulation channel M are empirically
orthogonal. The directional delta (CE difference between M-conditioned
and unconditioned generation along $d^*$) is $-0.001$ nats. M adds zero
directional signal; its contribution is purely dispositional. General
language modeling quality is preserved: M-state incurs $-0.012$ nats
perplexity impact on non-target text.

## Agentic Task Execution

We evaluate HEXIS as an agentic M controller on $\tau$-bench airline , a
50-task customer service benchmark requiring multi-step tool
orchestration (booking, cancellation, modification of reservations)
through a simulated user interaction. This tests whether the same Mind
Tree architecture that carries dispositional memory
(§<a href="#sec:three_layer" data-reference-type="ref"
data-reference="sec:three_layer">[sec:three_layer]</a>) can also route
domain knowledge to guide tool-calling agents.

**M’s role in agentic tasks.** For disposition tasks
(§<a href="#sec:modulation" data-reference-type="ref"
data-reference="sec:modulation">[sec:modulation]</a>), M operates via
mechanism (a): compiled Q/V modulation that biases attention patterns.
For agentic tasks, M operates via mechanism (b): a classifier that
triggers knowledge-graph retrieval and injects relevant nodes as
context. Both mechanisms use the host model’s hidden states as the
bridge—for (a), hidden states are compiled into modulation tensors via
$\phi$; for (b), hidden states serve as retrieval queries via a
*retrieval phi* ($\phi_R$).

**Retrieval phi ($\phi_R$).** A lightweight MLP
($d_\text{model} \to d_\text{model}/4 \to 256$) trained via contrastive
loss (InfoNCE) over the domain’s knowledge nodes. Mean-pooled last-layer
hidden states from the host model serve as embeddings for both queries
and nodes. Without $\phi_R$, raw cosine retrieval achieves only 25% R@1
on 108 nodes due to intra-domain similarity collapse. After domain
compilation (50 contrastive steps, $\sim$<!-- -->20 seconds), $\phi_R$
achieves 100% R@1 with zero cross-domain leaks. No pretraining is
required—compilation over the target node set alone is sufficient.

**Knowledge graph.** Nodes are seeded from the domain’s policy WIKI and
tool schemas, then grow via teacher-written failure-mode notes. Each
turn, the orchestrator: (1) extracts a query embedding from the
conversation state, (2) retrieves top-5 nodes via $\phi_R$-projected
cosine, (3) curates retrieved nodes into XML injected at the prompt
tail.

**Teacher loop.** On task failure, a teacher LLM (Sonnet, temperature=0)
reads the failure reason from the reviewer and writes a natural-language
guidance note to the knowledge graph. The note is embedded and indexed
by $\phi_R$. Subsequent trials of the same task retrieve relevant
guidance via the same embedding-based mechanism.

<div id="tab:taubench">

| **Configuration**                   | **Pass rate** | **Teacher rescues** | **Wall time** |
|:------------------------------------|:-------------:|:-------------------:|:-------------:|
| Baseline (no M)                     |  6/10 (60%)   |          —          |     2384s     |
| Oracle v1 (gold tool-name hint)     |  7/10 (70%)   |          —          |     2230s     |
| Oracle v3 (gold tool-name + params) | 10/10 (100%)  |          —          |     1531s     |
| HEXIS (graph + teacher, 3 trials)   |  7/10 (70%)   |          2          |     7144s     |

$\tau$-bench airline results (10-task subset, deterministic Sonnet user
sim). Baseline = raw tool-calling with all schemas in system prompt.
Oracle = gold tool-name + parameter-value hints. HEXIS = graph-backed
retrieval + teacher loop.

</div>

**Oracle ceiling.** With gold-derived tool-name and parameter-value
hints injected via the same user-role tail mechanism, the architecture
achieves 10/10—demonstrating that the *format* of M’s intervention
(domain-agnostic `<hint>` tags) is sufficient when the *content* is
correct. The 40-percentage-point gap between baseline (60%) and oracle
(100%) defines the budget for what a trained M could provide.

**HEXIS with teacher loop.** Without oracle access, graph-backed
retrieval + teacher guidance achieves 7/10 (70%), rescuing 2 tasks that
baseline fails (tasks 11 and 26). The teacher loop demonstrates online
learning: trial 1 fails, the teacher writes domain-agnostic guidance
(“don’t transfer to human too quickly—try to resolve it yourself”), and
trial 2 succeeds with the guidance retrieved from the knowledge graph.

**Full benchmark (50 tasks $\times$ 5 trials).** \[XX\] total passes /
\[XX\] total trials (\[XX\]%) for HEXIS vs. \[XX\]/\[XX\] (\[XX\]%) for
baseline. Results pending; expected to show sustained advantage from
teacher-accumulated knowledge across trials.

**Key finding: two mechanisms, one architecture.** The same Mind Tree
schema that stores dispositional beliefs (compiled into M-state via
$\phi$) also stores agentic knowledge (retrieved via $\phi_R$ and
injected as context). The choice of mechanism (a) vs (b) is determined
by whether the downstream effect requires per-token probability shifts
(disposition) or contextual knowledge injection (agentic). Both share
the host model’s hidden-state space as the bridge.


<!-- source: paper/sections/related_work.tex -->

## 6. Related Work

# Related Work

**Explicit memory for LLMs.** RAG systems retrieve documents into the
context window, subject to retrieval quality and context dilution.
MemGPT manages a tiered memory buffer with explicit read/write
operations. Reflexion accumulates verbal reflections as prompt prefixes,
enabling cross-episode learning but with linearly growing context cost.
Long-context approaches extend the window but do not change the
fundamental architecture: memory remains content in context, subject to
dilution and attention competition. All existing approaches implement
exclusively explicit memory—the model reads stored content and knows it
is doing so. HEXIS implements implicit memory: the enmeshed modulation
shapes attention and value extraction before reasoning occurs, and the
host model cannot introspect upon the modulation source.

**Parameter-efficient adaptation.** LoRA and its variants apply low-rank
weight perturbations via gradient descent, producing fixed adapters per
training run. Adapters insert bottleneck layers between frozen blocks.
Prefix tuning and prompt tuning learn virtual tokens that occupy context
positions. Side-tuning trains a parallel network fused at the output
layer. All require gradient descent for each adaptation. An enmeshed
network adapts at inference cost—one forward pass through $\phi$
produces new modulation tensors—and fuses at every patched layer rather
than only at the output. The mechanistic similarity to LoRA (both apply
low-rank perturbations) is precise but the operational difference is
fundamental: LoRA is a training-time method that produces fixed weights;
enmeshed modulation is an inference-time method that produces
experience-specific tensors. Soft prompts and prefix tuning are the
closest context-level analogue, but they still occupy context positions:
virtual tokens compete for attention and are inspectable by the model’s
reasoning process. Compiled M operates on pre-projection hidden states,
below the level of the model’s chain-of-thought, providing
non-inspectability that no prompt-level method can achieve
(§<a href="#sec:why_not_prompt" data-reference-type="ref"
data-reference="sec:why_not_prompt">[sec:why_not_prompt]</a>).

**Activation steering and representation engineering.** Representation
engineering and activation addition extract fixed directions from
contrastive data and inject them during inference. These methods are
elegant and effective for unidimensional behavioral shifts. However, the
directions are non-adaptive: the same vector is applied regardless of
context or experience. In HEXIS, the directional channel $d^*$ uses
standard representation engineering for stance direction, while the
enmeshed channel M provides the adaptive, multidimensional,
experience-specific component. We validate empirically that the channels
are orthogonal ($\Delta_\text{dir} = -0.001$ nats).

**Fast weight programmers.** introduced networks that write to their own
weights during a forward pass. The outer network produces weight updates
for the inner network, enabling one-shot learning without
backpropagation through the inner loop. HEXIS shares this spirit—$\phi$
produces modulation tensors that alter the host’s computation—but
differs in three ways: (1) modulation targets attention geometry (Q/V)
rather than arbitrary weights, (2) the host model is a modern frozen LLM
rather than a small trained-from-scratch network, and (3) compilation
from structured schemas replaces online weight writing.

**Memory and identity in cognitive science.** The explicit/implicit
memory distinction identifies two functionally dissociable systems.
proposes three operational criteria for implicit memory: priming,
non-reportability, and asymmetric dissociation. HEXIS satisfies all
three: M produces measurable attention divergence (priming), the host
model cannot report on or reason about the Q/V modulation
(non-reportability), and M and explicit beliefs dissociate
asymmetrically under dilution—explicit beliefs degrade while compiled M
is immune (dissociation). The Mind Tree’s cognitive schema draws on
structured self-models from developmental psychology and the Toulmin
model of argumentation .


<!-- source: paper/sections/discussion.tex -->

## 7. Discussion and Limitations

# Discussion and Limitations

## What Compiled Enmeshment Cannot Do

We characterize the bottleneck boundary with precision. Compiled
enmeshment at rank 16 carries stance direction (4/4 topics), confident
experiential voice, parametric knowledge steering (“poverty dropped
40%”, “Alaska’s dividend program”), and dilution immunity (\[XX\]% at
\[XX\]K tokens of filler in compiled mode). It does *not* carry novel
content absent from the host’s training data: fabricated statistics
(“47.3% improvement”) and unknown proper nouns (“Nextera Labs”) do not
survive the rank-16 bottleneck. This boundary motivates the three-layer
architecture (§<a href="#sec:three_layer" data-reference-type="ref"
data-reference="sec:three_layer">[sec:three_layer]</a>): compiled
enmeshment handles disposition, the curated slot handles novel
specifics, and recursive expansion handles deep evidence on demand.

On the instruct model, M’s contribution shifts: the instruction-tuned
model takes strong stances independently (A: 7/7), so M cannot override
the host’s RLHF-trained opinions. Instead, M shapes voice (conciseness,
experiential framing) and sycophancy resistance (+14 percentage points
on the 5-level pressure protocol). The phi parameters trained on the
base model transfer to the instruct model without retraining—the hidden
state distributions are compatible for dispositional modulation but not
for stance override.

For ALFWorld, the Mind Tree’s primary value is *curation as structured
context*, not compiled modulation. Expert strategies in Mind Tree format
improve success from 3% to 53%. M hooks during generation are not
needed—the strategies work through explicit context, demonstrating that
the Mind Tree schema contributes independently of the enmeshed
modulation mechanism.

## The M Attractor Problem

In multi-turn dialogue, compiled M applies a constant perturbation at
every token position. As M-shaped tokens accumulate in the KV cache, the
model processes them through M-enhanced attention, creating a positive
feedback loop that converges to repetitive identity assertion after 2–3
turns on the base model.

**Root cause:** M is active during both prefill (processing conversation
history) and generation (producing new tokens). The KV cache built
during prefill contains M-enhanced representations. During generation, M
perturbs new tokens that attend to this M-enhanced cache—double signal
that compounds.

**Fix:** Disabling M during prefill (applying it only during generation)
breaks the feedback loop. With prefill-off and gate=0.5, the base model
produces 3 unique character-driven turns before the greedy attractor.
The instruct model, with its stronger conversational scaffolding,
produces 10+ unique turns even with M active, though structural
repetition (same rhetorical template per turn) persists. A distillation
approach using gold diverse conversations from a frontier model reduces
this but does not eliminate it.

The prefill-off mechanism reveals a general principle for additive
modulation: *constant additive perturbation creates positive feedback
through autoregressive generation*. The fix is to separate the
perturbation’s influence on *processing context* (where it compounds)
from its influence on *generating new tokens* (where it adds constant
signal).

## Credence Sensitivity

Numeric credences failed as an M-state feature. Tokens for “0.82” and
“0.45” are nearly indistinguishable in the transformer’s attention
space—the hidden state difference between these tokenized numbers is far
smaller than between the words “strong” and “agnostic”. Multiple
training approaches (NTP with credence perturbation, GRPO, SFT on gold
responses) confirmed that this is a representation bottleneck, not a
training signal problem. Categorical conviction labels resolve this by
using semantically distinct tokens. A future Bayesian treatment could
provide formal grounding while maintaining the categorical interface
(Appendix <a href="#sec:credence_negative" data-reference-type="ref"
data-reference="sec:credence_negative">[sec:credence_negative]</a>).

## Two Mechanisms, One Bridge

The agentic experiments
(§<a href="#sec:agentic" data-reference-type="ref"
data-reference="sec:agentic">[sec:agentic]</a>) reveal that HEXIS
supports two distinct intervention mechanisms through the same
hidden-state bridge:

**Mechanism (a): Attention modulation.** $\phi$ compiles retrieved Mind
Tree nodes into Q/V modulation tensors that bias per-token attention
patterns. The hidden states are the *input* to $\phi$; the output is a
weight-space perturbation. This mechanism is load-bearing when the
downstream effect requires probability-level shifts across all generated
tokens—stance direction, experiential voice, sycophancy resistance, user
memory integration.

**Mechanism (b): Knowledge retrieval and context injection.** $\phi_R$
projects hidden states into a retrieval space where cosine similarity
identifies relevant knowledge nodes. The output is *context
augmentation*—XML injected at the prompt tail. This mechanism is
load-bearing when the downstream effect requires specific factual
content (tool names, parameter values, policy rules, biographical
details) that the model cannot derive from its weights alone.

Crucially, retrieval ($\phi_R$) serves *both* mechanisms. For
disposition, retrieval selects which belief nodes, user memories, and
biographical details to compile into M-state—this is the curation step
of the three-layer architecture
(§<a href="#sec:three_layer" data-reference-type="ref"
data-reference="sec:three_layer">[sec:three_layer]</a>). For agentic
tasks, retrieval selects which policy rules and tool guidance to inject
as context. The shared step is retrieval; the divergence is the
downstream path—weight-space compilation (a) or token injection (b).

Both mechanisms share the host model’s hidden-state space as the bridge.
A production HEXIS agent uses both simultaneously: mechanism (a)
maintains consistent interaction style (compiled from user memories,
preferences, biographical context), while mechanism (b) surfaces
task-relevant knowledge each turn (policy rules, failure modes, tool
schemas). The Mind Tree stores all node types; $\phi_R$ retrieves
relevant nodes regardless of type; the node’s metadata determines
whether it flows to compilation (a) or injection (b).

## Retrieval Phi and Domain Compilation

The retrieval phi ($\phi_R$) addresses a specific challenge:
intra-domain similarity collapse in generative model hidden states. On a
108-node knowledge graph spanning policy rules, tool schemas, and
teacher-written failure modes, raw cosine similarity achieves only 25%
R@1—concepts within the same domain (e.g., “cancellation policy”
vs. “booking policy”) have cosine similarity of 0.858 vs. 0.858, making
them indistinguishable.

$\phi_R$ resolves this via domain compilation: 50 steps of contrastive
training ($\sim$<!-- -->20 seconds) on the node set itself produces a
projection that achieves 100% R@1. This is intentional
overfitting—$\phi_R$ memorizes where each node lives in its projected
space. When the graph grows (teacher writes a new node), $\phi_R$
recompiles in seconds to incorporate it.

Importantly, no external pretraining data is required. Unlike
instruction-tuned embedding models that require millions of diverse
training pairs, $\phi_R$ trains entirely from the domain’s own node set.
The procedure is domain-agnostic: seed nodes from any policy document
and tool schema, compile $\phi_R$, deploy. Switching from airline to
banking requires only reseeding the graph and recompiling
($\sim$<!-- -->20 seconds).

Standard techniques for improving embedding quality on raw LLM hidden
states—whitening, mean centering, principal component removal—were
tested and uniformly *degraded* performance (from 75% to 0–38% R@1).
This is because Qwen3.5-4B’s hidden states encode discriminative
information in the high-variance directions (opposite to encoder models
like BERT). The contrastive $\phi_R$ learns to extract the correct
discriminative subspace without blindly removing variance.

## Unexplored Design Space

We validate one point in a six-axis design space
(Table <a href="#tab:design_space" data-reference-type="ref"
data-reference="tab:design_space">[tab:design_space]</a>). The additive
blending function (Level 1) is the simplest; gated blending could solve
the multi-turn attractor by learning when to suppress M. Cross-attention
(Level 3) could transfer richer content. Rank 16 suffices for 4B; larger
models may benefit from adaptive rank allocation. The Mind Tree’s
hierarchical structure maps naturally to a property graph database
(e.g., Neo4j), where Cypher queries replace Python filtering for
domain/intent matching, and the consolidation cycle
(observation$\to$tactic$\to$strategy promotion) maps to graph traversal
operations. Activation tracking, biographical commitment, and
contradiction detection all benefit from persistent graph storage.

## Why Not Just Compress a Prompt?

The most direct challenge to enmeshed networks is that compiled M is
“just a fancy way of compressing a prompt.” Three properties distinguish
it. First, *structural dilution immunity*: prompt compression reduces
tokens but compressed tokens still compete for attention; compiled M
operates outside the attention window entirely, making dilution
structurally impossible
(Table <a href="#tab:dilution" data-reference-type="ref"
data-reference="tab:dilution">[tab:dilution]</a>). Second,
*non-inspectability*: an adversary can read the prompt and argue against
its content; compiled M operates on pre-projection hidden states below
the model’s chain-of-thought, so any representation the model can attend
to is also one it can be argued out of, but M cannot
(Appendix <a href="#sec:implicit_validation" data-reference-type="ref"
data-reference="sec:implicit_validation">[sec:implicit_validation]</a>).
Third, *processing change*: compiled M produces measurable attention
divergence (JSD = 0.049 between M-states) and suppresses think-mode
activation (0/4 under D/F). The model does not merely produce different
words—it processes its input differently. These properties matter most
in the application domains identified in
Table <a href="#tab:application_domains" data-reference-type="ref"
data-reference="tab:application_domains">[tab:application_domains]</a>:
user empathy, research conviction, agentic strategy, and codebase
management each require knowledge better encoded as a perceptual shift
than as text (full analysis in
Appendix <a href="#sec:application_domain_details" data-reference-type="ref"
data-reference="sec:application_domain_details">[sec:application_domain_details]</a>).

## Broader Implications

Enmeshed networks implement a form of AI individuality: different Mind
Trees compiled through different M-states produce agents with different
perceptual priorities, argumentative styles, and behavioral
dispositions—all from the same frozen host model. This is *composition*
rather than *fine-tuning*: the host’s general capabilities are preserved
while M adds an experiential lens. Multiple M-states can coexist
(swapped per user, per task, per turn), and removing M recovers the
unmodified baseline.


<!-- source: paper/sections/conclusion.tex -->

## 8. Conclusion

# Conclusion

We introduced enmeshed networks—a new architectural primitive in which a
lightweight module shares the forward pass of a frozen host, reading and
writing intermediate representations at each layer—and instantiated this
primitive as HEXIS, implementing compiled dispositional memory for
frozen transformers via low-rank Q/V modulation.

HEXIS opens a parallel context channel: a structured cognitive schema
(the Mind Tree) is compiled into persistent modulation tensors that
shape the host’s attention geometry without occupying context positions.
The compiled signal is dilution-immune by construction (\[XX\]% stance
at \[XX\]K tokens of filler), provides sycophancy resistance (\[XX\]%
over 7 rounds of adversarial pressure), and carries sufficient content
through a rank-16 bottleneck to flip the host model’s default stance on
contested topics. A three-layer architecture (compiled modulation +
curated slot + recursive expansion) matches full in-context beliefs at
82% token savings.

We characterized the bottleneck boundary precisely: compiled enmeshment
steers parametric knowledge but cannot inject novel content. This honest
boundary motivates architectural composition rather than a single
mechanism. The enmeshed modulation succeeds for open generation and
fails for constrained action selection, establishing complementary roles
for implicit and explicit memory channels.

The mechanism’s value is sharpest in domains where knowledge is better
encoded as a perceptual shift than as text: user empathy that persists
without per-turn re-prompting, research conviction that resists
adversarial consensus pressure, agentic strategy that does not dilute as
episodes accumulate, and codebase awareness that scales at fixed rather
than linear cost. In each case, the critical property is not token
savings but the qualitative shift from inspectable content (which
dilutes and folds) to non-inspectable modulation (which is structurally
immune to both).

We view this work as opening a research program rather than presenting a
final architecture. The enmeshed network primitive and the Mind Tree
schema are general; the specific instantiation (Level 1, rank 16, Q+V,
stride-3, Qwen3.5-4B-Base) is one point in a large design space. We hope
the definition, taxonomy, and initial validation encourage exploration
of the full space.


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

