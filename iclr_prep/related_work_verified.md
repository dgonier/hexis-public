# Related Work: verified outline (Devin, 2026-08-19 — canonical for §10 drafting)

Organising axis: (1) where does the conditioning live — context tokens, activations,
weights; (2) what property was measured — acquisition, or retention under pressure.
Every prior line measures acquisition.

Six paragraphs in order: (1) context-delivered conditioning + decay (Choi 2412.00804 —
larger models drift more; personas don't prevent drift; no mitigation proposed);
(2) hypernetwork adapters — LEAD WITH THE CONCESSION (GenerativeAdapter ICLR25 2411.05877:
attn-OUT projection rank 128, self-supervised on SlimPajama, StreamingQA/MetaICL/MSC — all
acquisition; Text-to-LoRA 2506.06105; SHINE 2602.06358 63.6 SQuAD, meta-LoRA accumulation;
Doc-to-LoRA; lineage to fast-weight programmers); measurement difference carries the paper;
(3) the override gap (Cheng 2604.23750) — competing explanation for the 46% install figure
(adapter margin constant vs prior margin grows; 68%->16% by prior strength; SLB/CAI fixes
46.4->71.0 Gemma-2B); differentiator: their pressure is the model's own prior, static;
ours is an adversarial interlocutor, escalating; ALSO their retrieval-in-context scores
63.8 vs 71.0 parametric on deep conflicts — never imply context always wins install;
(4) activation steering (Turner/Zou/ITI/Rimsky CAA + Le&Le 2606.07696: robustness drops
up to 64 points, layer shifts up to 17, confidence <=0.25 — CAA collapse is structural,
not a strawman); differentiate on FORM: fixed offset vs low-rank map on live hidden state;
(5) PEFT/modulated-LoRA (LoRA targets Q/V by default — placement is NOT a contribution,
say so; prefix tuning = not-readable-but-in-context; FiLM/AdaLN = one-sentence framing of
the write function); (6) sycophancy/debate/oversight arc (Irving 2018, Brown-Cohen
2311.14125, UK AISI 2505.03989, Khan 2402.06782 vs Parrish — report the disagreement;
Bertalanic&Fortuna 2605.00914: 85.5% modal sycophancy, 90.1% consensus, 32.3% oracle gap,
2.1-3.4x tokens; temperature ablation — debate absorbs diversity without converting it);
close with the rigidity bridge immediately.

Table A (by axis) goes in the paper. Table B (by paper: same/different/significance for
GenerativeAdapter, Text-to-LoRA, SHINE, Override Gap, CAA/RepEng, Le&Le, PEFT line,
Choi, Bertalanic, debate line) is the rebuttal-writing reference — keep in iclr_prep.

## CORRECTIONS (propagate everywhere)
1. The MSC 40.2-vs-66.0 F1 claim in the first positioning memo is WRONG — no such
   comparison exists in GenerativeAdapter; use their StreamingQA framing or Text-to-LoRA's
   zero-shot-below-task-specific-LoRA admission for the "parametric underperforms prompting
   on acquisition" citation. (NOTE: earlier mining-agent verification "CONFIRMED exactly"
   was itself wrong — treat that verification pass as unreliable on this point.)
2. GenerativeAdapter modulates attention OUTPUT projection at rank 128 (not Q/V low-rank) —
   smaller differentiator than earlier memos claimed; checkable.
3. Le&Le: abstract says "up to 64%", conclusion "64 percentage points" — match phrasing to
   sentence, never convert.
## STILL UNVERIFIED (pull-and-check or cut): Assistant Axis (Lu 2026), Baltaji 2024,
CONSENSAGENT, Huang martingale, the 0.88 opposing-persona convergence figure.
