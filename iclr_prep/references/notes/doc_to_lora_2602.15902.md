# Doc-to-LoRA: Learning to Instantly Internalize Contexts

## Citation
Rujikorn Charakorn, Edoardo Cetin, Shinnosuke Uesaka, Robert T. Lange. *Doc-to-LoRA: Learning to
Instantly Internalize Contexts.* Sakana AI, Tokyo / Minerva University, California.
arXiv:2602.15902 (v1, 13 Feb 2026). Preprint, dated Feb 19, 2026 on the manuscript itself; no
venue/proceedings listed at time of writing (later cited by SHINE and the override-gap paper as
"CoRR, abs/2602.15902, 2026," i.e., still unpublished/preprint status as of those citations).
Code: `github.com/SakanaAI/doc-to-lora`.

## Architecture (HEXIS vocabulary)
- **Conditions on**: raw context strings (documents/prompts); one ablation also demonstrates
  conditioning on a VLM's activations for cross-modal (image→text) internalization. Not
  structured/typed input in either case — dense, unstructured signal.
- **Encoding mechanism**: the context is fed through the frozen target LLM to obtain per-layer
  token activations `Z ∈ R^{L×N×D}`. A shared (across layers) Perceiver-style cross-attention
  hypernetwork maps each layer's variable-length activations to a fixed number of learnable
  latent queries (equal to the LoRA rank), which are then linearly projected into rows/columns
  of the LoRA `A`/`B` matrices for that layer.
- **Outputs**: rank-`r` LoRA adapters (`r=8` in main experiments) applied specifically to the
  **MLP down-projection** layer of each transformer block. Long contexts are handled via
  chunking: the context is split into `K` chunks, each processed independently through the
  hypernetwork, and the resulting per-chunk adapters are concatenated along the rank dimension
  (giving effective rank `r·K`) — this is how D2L generalizes far beyond its training-time
  context length (trained on 32–256 tokens, evaluated successfully to 40K tokens on NIAH).
- **Pass structure**: one forward pass (batched mode processes all layers' activations at once;
  iterative mode trades speed for lower memory by generating one layer's adapter at a time — the
  two are mathematically equivalent).
- **Host**: frozen gemma-2-2b-it (main experiments); also validated on Mistral-7B-Instruct-v0.2
  and Qwen3-4B-Instruct-2507 (Appendix E). 309M trainable hypernetwork parameters.
- **Training objective — the key methodological difference from GenerativeAdapter**: meta-learned
  **query-independent context distillation (CD)**, i.e., minimizing KL divergence between a
  teacher (the same LLM, with the context in-context) and a student (the hypernetwork-adapted LLM,
  without the context) across a small set of generated queries/responses per context — not a
  next-token-prediction SFT loss on ground-truth completions. The paper explicitly contrasts this
  against GenerativeAdapter's SFT-style objective and attributes D2L's stronger ROUGE-L *recall*
  (vs. GenerativeAdapter's shorter, higher-F1-but-lower-recall outputs) to this choice (§7 Related
  Work).

## Evaluation metrics and headline numbers (every metric reported)

### 1. Synthetic Needle-in-a-Haystack (§4) — gemma-2-2b-it, 8K native context
ROUGE-L F1 retrieval accuracy vs. haystack length (2^10–2^17 tokens ≈ 1K–128K). D2L "maintains
high retrieval accuracy" past the base model's 8K limit, "remains close to perfect up to 40
chunks (40K tokens)... quintuple the number of chunks the model has been exposed to during
training," degrading gracefully beyond that. Additional-memory-for-inference comparison: base
model uses >12GB extra at 128K tokens; D2L uses <50MB regardless of haystack length.

### 2. Reading comprehension (§5.1.1) — SQuAD, DROP, ROPES, relative ROUGE-L F1 vs. ICL upper bound
D2L "outperforms all the in-parameter baselines," reaching **82.5% relative performance** vs. the
ICL upper bound on SQuAD. Update latency: D2L <1s (batched or iterative) vs. CD (oracle) ~40s vs.
CD (generated queries) >100s. Memory: D2L and CD (oracle) both <2GB; CD (generated queries) >40GB.

### 3. Long-context QA (§5.1.2, Table 1) — 2WikiMultihopQA, MultiFieldQA, QASPER (LongBench), up to 32K tokens, never seen in training (longest training sample: 2,344 tokens):

| Method | Normalized Performance (↑) | Additional Update Memory (GB, ↓) | Mean Update Latency (s, ↓) |
|---|---|---|---|
| CD (oracle query) | 0.901 | 7.820 | 40.171 ± 0.351 |
| D2L (batched) | 0.857 | 11.522 | 0.209 ± 0.123 |
| D2L (iterative) | 0.844 | 3.791 | 0.551 ± 0.101 |
| CD (25 generated queries) | 0.745 | 59.925 | 465.454 ± 67.868 |
| CD (5 generated queries) | 0.704 | 79.371 | 72.537 ± 7.821 |

### 4. Zero-shot visual internalization (§5.2, Table 2) — VLM (gemma-3-4b-it) → text LLM (gemma-2-2b-it), Imagenette (10-class, random baseline 10%):

| Method | SQuAD | DROP | ROPES | Imagenette |
|---|---|---|---|---|
| D2L (LLM ⇒ LLM) | 0.814 | 0.655 | 0.906 | N/A |
| D2L (VLM ⇒ LLM) | 0.705 | 0.568 | 0.772 | **75.03%** |

### 5. Zero-shot query internalization (§6, Table 3) — extreme generalization test: internalizing
the *query* instead of the document, document given in-context instead:

| Method | Recall | Precision |
|---|---|---|
| Base model w/ context | 0.886 | 0.876 |
| D2L | 0.740 | 0.720 |
| D2L (swapped: query internalized) | 0.587 | 0.044 |
| Base model w/o context | 0.185 | 0.205 |

### 6. D2L vs. many-query CD (§6, Table 4) — SQuAD, 100 samples: CD improves from 0.506 (20
queries) to 0.650 (100 queries, >10 min/sample); D2L reaches **0.866** in 0.086s.

### 7. **Appendix C.4, "Knowledge Interference" (Table 8) — the closest thing to a robustness test in this paper.**
Tests whether D2L over-applies internalized knowledge to unrelated queries, by replacing SQuAD
contexts with either an irrelevant "assistant" system prompt or a distracting ~4K-token book
chapter:

| Method | SQuAD (assistant-prompt context) | SQuAD (distracting context) |
|---|---|---|
| Base model w/ replaced context | 0.201 | 0.175 |
| **D2L** | **0.096** | **0.126** |
| CD (10 generated queries) | 0.211 | 0.203 |

D2L performs *worse* than both the base model and CD when the internalized content is unrelated
to the query — the paper's own hypothesis, verbatim: *"D2L might acquire a strong prior, assuming
that the subsequent queries will always be related to the internalized knowledge. This might be
caused by the bias in the data generation pipeline that only considers queries related to the
input context."* This is a genuine failure-mode/robustness experiment, but it tests
**over-application to unrelated queries** (an interference/false-positive problem), not
**failure to hold under contest of the same fact** (our persistence axis) — opposite direction of
failure from ours.

**No multi-turn dialogue, no adversarial contradiction of an already-installed fact, and no
repeated-query-under-pressure evaluation appears anywhere in this paper.**

## Memo assertion verification (this paper)

**(a)** Not applicable — D2L does not run the GenerativeAdapter MSC personalization experiment.

**(b) Acquisition-only evaluation: MOSTLY CONFIRMED, with the knowledge-interference exception.**
NIAH retrieval accuracy, ROUGE-L F1 on six QA benchmarks, and VLM→LLM zero-shot classification
accuracy are all single-shot recall metrics. The one exception, App. C.4 Knowledge Interference
(Table 8), is a genuine robustness-adjacent ablation but tests over-application/interference, not
persistence-under-pressure — must be disclosed, not silently omitted, when asserting the family
is uniformly acquisition-focused.

**(c) No structured/typed input: CONFIRMED.** Context is raw text throughout; the VLM ablation
conditions on dense visual activations, which is richer/cross-modal but still unstructured, not
typed/symbolic.

## Threats to novelty

1. **Appendix C.4 "Knowledge Interference" (p.23, Table 8)** — quoted above. Genuine
   failure-mode finding, but orthogonal to our axis: theirs is "adapter fires when it shouldn't
   (on unrelated queries)"; ours is "adapter/context fails to hold when it's directly contested
   (on the same topic, under pressure)." Cite as adjacent-but-distinct — useful evidence that
   the family is aware compiled modulation has failure modes, but has not identified or measured
   the specific one we report.

2. **App. F framing line (p.24)**: *"D2L differs [from prompt compression] by operating in
   parameter space via a hypernetwork that predicts weight deltas, which yields persistent,
   re-usable adaptations."* Uses the word "persistent" but means "does not need to be
   re-supplied on every query" (reusability across queries without recomputation), not "robust
   to contradiction or adversarial pressure." Low risk, but a reviewer skimming both papers
   could conflate this usage with ours — worth a one-line disambiguating footnote in our related
   work if we use the word "persistence" near a citation of this paper.

3. **§2, "Defining Internalization"** mentions persistent instructions as a motivating use case
   without testing them: *"persistent instructions like safety and alignment prompts are prime
   candidates for internalization. These prompts are often tailored for different use cases and
   must remain in the context window throughout deployment."* This is a motivating example, not
   an evaluation — D2L never tests whether an internalized safety/alignment instruction survives
   subsequent adversarial pressure. Worth noting as a missed-opportunity citation (they gesture
   at exactly our use case without measuring it), not a threat.

## Citation guidance
Cite Doc-to-LoRA as the Sakana AI entry in the compiled-modulation lineage and the architecture
whose CD-based (query-independent context-distillation) training objective is the clearest
methodological alternative to GenerativeAdapter's SFT-style approach — useful for establishing
that the family has already explored multiple training objectives without any of them
addressing persistence. Its Appendix C.4 Knowledge Interference ablation is worth citing
explicitly as evidence the family has begun probing failure modes beyond raw recall, which
strengthens (rather than undercuts) the case that persistence-under-pressure is the natural next
axis and one the family has not yet reached. Do not describe D2L's "persistent, re-usable
adaptations" language (App. F) as evidence it addresses our claim — clarify in-text that this
refers to query-reusability, not robustness to contest, if both papers are cited near each
other.
