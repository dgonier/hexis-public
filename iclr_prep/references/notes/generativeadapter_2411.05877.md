# GenerativeAdapter: Contextualizing Language Models in Parameters with a Single Forward Pass

## Citation
Tong Chen, Hao Fang, Patrick Xia, Xiaodong Liu, Benjamin Van Durme, Luke Zettlemoyer, Jianfeng
Gao, Hao Cheng. *GenerativeAdapter: Contextualizing Language Models in Parameters with a Single
Forward Pass.* University of Washington / Microsoft / Microsoft Research. arXiv:2411.05877
(v1, 8 Nov 2024). Published at ICLR 2025 (OpenReview id `bc3sUsS6ck`) — confirmed via the
Doc-to-LoRA and SHINE reference lists, which both cite it as "The Thirteenth International
Conference on Learning Representations, ICLR 2025."

## Architecture (HEXIS vocabulary)
- **Conditions on**: streaming raw-text context chunks — documents, dialogue/conversation
  history, or in-context-learning demonstrations. Not structured/typed input; plain token
  sequences, encoded by the frozen base LM's own hidden states (no separate encoder).
- **Outputs**: additive low-rank delta weights (`W = W_base + W_∆`) for a single target module
  per experiment — the attention **output-projection** layer in the main results (a feedforward
  down-projection ablation is tested separately, at 3x the parameter cost, and improves
  perplexity slightly but was not adopted as the default). The delta is computed as a bilinear
  function of accumulated context hidden states, `W_∆ = G(H) = (A1A2) H^T H (B1B2)`, then
  SVD-normalized to a rank-`r` (r=128) LoRA-equivalent decomposition. Intermediate rank
  `d_r=1024`. ~500M generator parameters, ~32M generated-adapter parameters.
- **Pass structure**: one forward pass per context chunk; supports incremental/streaming
  accumulation without re-processing prior chunks, via a running outer-product state
  `S_t ← S_{t-1} + A2 H_t^T H_t B1` (Eq. 3). Not iterative/gradient-based — pure feedforward
  generation.
- **Host**: frozen, off-the-shelf Mistral-7B-Instruct-v0.2 or Llama2-7B-Chat.
- **Training**: self-supervised pretraining (reconstruction + completion losses, 1B tokens from
  SlimPajama, chunked at 8,192 tokens) followed by instruction tuning (QA, ICL, instruction-
  following mixtures, chunked at 1,024 tokens for the streaming mechanism).

## Evaluation metrics and headline numbers (every metric reported)

### 1. Document-based QA across context length (§4.1) — SQuAD and StreamingQA
- F1 score, varying context length k ∈ {512, 1K, 2K, 4K, 8K, 16K, 32K tokens}, both
  Mistral-7B-Instruct and Llama2-7B-Chat.
- Baselines: closed-book SFT, continual pretraining (CPT), in-context (full-context) prompting.
- Result pattern: GenerativeAdapter and prompting both beat closed-book SFT; GenerativeAdapter
  is "highly effective when the context is relatively short (< 1K tokens)" and generally beats
  CPT below 8K tokens, while avoiding prompting's attention-computation overhead. No single
  headline F1 number is given in the abstract for this section (numbers are read off Figure 2);
  the abstract's only quoted number for StreamingQA is the 32K-token comparison below.
- Abstract's own headline: "In StreamingQA, our approach is effective in injecting knowledge
  into the LM's parameters, achieving a 63.5% improvement in F1 score over the model with
  supervised fine-tuning (from 19.5 to 31.5) for contexts as long as 32K tokens."

### 2. In-context learning (§4.2) — MetaICL, 26 held-out tasks
- Accuracy at K-shot ∈ {1, 2, 4, 8, 16}, separately for classification and non-classification
  tasks, both backbones. Baselines: zero-shot prompting, few-shot fine-tuning (on max 16
  input-output pairs), standard few-shot in-context prompting.
- Abstract's headline: "average accuracy of 44.9 across 26 tasks, outperforming the base model."
  GenerativeAdapter "outperforms few-shot prompting in most cases, with more significant
  improvements... in the more challenging non-classification tasks."

### 3. Personalization (§4.3) — Multi-Session Conversation (MSC) dataset, Mistral-7B-Instruct only
Table 1 (the load-bearing table for memo assertion (a)), reproduced exactly:

| Model | F1 | Inference Computation (TFLOPS) | Extra Storage (M floats) |
|---|---|---|---|
| Closed-book | 8.1 | 0.505 | 0 |
| **Full-conversation Prompting** | **66.0** | 2.059 | 128+ |
| Ultragist (64 Tokens) | 26.5 | 0.514 | 4 |
| Ultragist (128 Tokens) | 32.2 | 0.552 | 8 |
| Ultragist (256 Tokens) | 38.3 | 0.627 | 16 |
| Ultragist (512 Tokens) | 40.8 | 0.772 | 32 |
| Ultragist (1K Tokens) | 44.4 | 1.067 | 64 |
| Ultragist (2K Tokens) | 42.4 | 1.658 | 128 |
| **GenerativeAdapter** | **40.2** | 0.505 | 32 |

### 4. Ablations (§5.1, Table 2) — validation-set perplexity (reconstruction + completion), Mistral only
| Factor | Setting | Reconstruction PPL | Completion PPL |
|---|---|---|---|
| — | Default | 1.75 | 7.40 |
| Pretraining task | Reconstruction only | 1.75 | 34.34 |
| Pretraining task | Completion only | 6.38 | 6.71 |
| Normalization | Frobenius | 7.72 | 7.32 |
| Module | Feedforward (vs. attn out-proj) | 1.68 | 7.26 |

**No persistence, multi-turn, robustness, or adversarial-pressure metric appears anywhere in the
paper.** Every evaluation is a single-shot readout (F1, accuracy, or perplexity) computed once,
immediately after context is mapped to an adapter, against a static gold answer or reference
text.

## Memo assertion verification (this paper)

**(a) GenerativeAdapter 40.2 F1 vs. 66.0 F1 for full-conversation prompting, framed as a compute
saving: CONFIRMED, numbers exact** (Table 1 above, p.8 of the PDF). The paper's own framing,
verbatim: "Although using the entire conversation leads to better accuracy, full conversation
prompting incurs significant computation and storage costs, i.e., 4x those of
GenerativeAdapter. Such costs are highly undesirable for personalizing LMs for individual users,
especially since most computations occur on edge devices without power[ful] GPUs." The 25.8-point
F1 gap is explicitly rationalized as an acceptable cost trade-off, never flagged as a capability
or robustness shortfall. No persistence/contradiction/multi-turn framing appears near this
result or anywhere else in the paper — the MSC evaluation itself is single-shot F1 against a
gold answer from a static multi-session conversation transcript, not a live dialogue with
adversarial follow-up.

**(b) Acquisition-only evaluation: CONFIRMED for this paper.** All three evaluation scenarios
(StreamingQA/SQuAD F1, MetaICL accuracy, MSC F1) are single-shot recall/accuracy metrics on
static test sets, computed once per adapted model. No streaming/multi-turn degradation curve,
no conflict-resolution test, no adversarial evaluation of any kind.

**(c) No structured/typed input: CONFIRMED.** Context is always raw text — documents, ICL
demonstration pairs, or conversation transcripts — encoded via the base LM's own token
embeddings and hidden states. Nothing resembling a typed graph, schema, or symbolic
representation is used anywhere.

## Threats to novelty
**None found.** This paper contains no experiment, ablation, or framing that overlaps with or
undercuts the installation-vs-persistence dissociation. Its entire contribution is an efficiency
story (F1-per-FLOP, F1-per-byte-of-storage), and the MSC personalization result is the paper's
own best illustration of treating an accuracy gap purely as a cost trade-off — which is exactly
the framing our positioning memo attributes to the family.

One point worth noting for completeness, not as a threat: the paper is explicit that it only
adapts a single module (attention output-projection) in its main experiments, with a feedforward
ablation left as "future work" (§5.1, §7 Conclusion: "it would be interesting to further explore
scaling up the adapter generator, such as by integrating adapters into additional layers"). This
underscores that even the *architectural* scope of the family's most-cited paper is narrower
than what later work (SHINE, HEXIS) attempts — useful lineage context, not a threat.

## Citation guidance
Cite GenerativeAdapter as the foundational paper in the compiled-modulation lineage — the first
to train a hypernetwork end-to-end (via self-supervised reconstruction + completion losses) to
map streaming natural-language context into additive low-rank weight updates on a frozen host
LM, establishing the "fast weights via a slow network" framing HEXIS inherits. Its MSC
personalization result (Table 1: 40.2 vs. 66.0 F1, framed as a 4x compute/storage saving) is the
cleanest single citation for the claim that the family treats the installation gap as an
efficiency trade rather than a robustness finding — quote this table directly in the positioning
paragraph. Do not cite it as evidence of anything about persistence or multi-turn behavior; it
contains no such measurement. When contrasting architectures, note it modulates a single module
type (attention output-projection, or feedforward down-projection in an ablation) rather than
the full per-layer Q/V/K/output/FFN coverage SHINE and HEXIS pursue.
