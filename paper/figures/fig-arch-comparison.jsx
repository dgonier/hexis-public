import { useState } from "react";

const P = {
  bg: "#ffffff", text: "#0f172a", textMid: "#475569", textLight: "#94a3b8",
  line: "#334155", lineLight: "#cbd5e1",
  blue: "#1d4ed8", blueLight: "#dbeafe", blueBg: "#eff6ff",
  purple: "#7c3aed", purpleLight: "#ede9fe",
  amber: "#b45309", amberLight: "#fef3c7",
  green: "#15803d", greenLight: "#dcfce7",
  red: "#b91c1c",
};
const s = "'Helvetica Neue', Helvetica, Arial, sans-serif";
const m = "'Courier New', monospace";

function Stack({ x, y, layers = 4, w = 110, color = P.line, hl = [] }) {
  const lh = 36, gap = 4;
  return <g>{Array.from({ length: layers }, (_, i) => {
    const li = layers - 1 - i, ly = y + i * (lh + gap), h = hl.includes(li);
    return <g key={i}>
      <rect x={x} y={ly} width={w} height={lh} rx={4} fill={h ? color+"12" : "#f8fafc"} stroke={h ? color : P.lineLight} strokeWidth={h ? 1.5 : 0.7}/>
      <text x={x+w/2} y={ly+lh/2+1} textAnchor="middle" dominantBaseline="middle" fontSize={11} fontFamily={s} fill={h ? color : P.textLight}>Layer {li}</text>
    </g>;
  })}</g>;
}

export default function Fig() {
  const W = 920, H = 494, pw = 196, gap = 16, top = 44;
  const px = [10, 10+pw+gap, 10+2*(pw+gap), 10+3*(pw+gap)];
  const stackBot = top + 32 + 4*40;
  const inputY = stackBot + 52; // extra padding for O-notation text
  const sumY = inputY + 48;
  const legendY = sumY + 68;

  // Panel (d) centering — wider spread, shifted 5px right of separator
  const dMid = px[3] + pw/2 + 15;
  const mX = dMid - 100; // M boxes left edge
  const mW = 36;
  const bX = mX + mW + 8; // B circles
  const hostX = bX + 30; // host stack — more gap
  const hostW = 82;

  return <div style={{background:P.bg,padding:0,lineHeight:0}}>
    <svg width="100%" viewBox={`0 0 ${W} ${H}`} style={{display:"block"}}>
      <defs>{[P.amber,P.purple,P.green,P.blue,P.line,P.textLight].map(c=><marker key={c} id={`a${c.replace('#','')}`} markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto"><polygon points="0 0, 8 3, 0 6" fill={c}/></marker>)}</defs>

      {/* Separator */}
      <line x1={px[3]-9} y1={top-10} x2={px[3]-9} y2={sumY-6} stroke={P.blue} strokeWidth={1.2} strokeDasharray="6,4"/>
      <text x={px[3]-9} y={top-18} textAnchor="middle" fontSize={11} fontFamily={s} fill={P.blue} fontWeight="700">this work</text>

      {/* ═══ (a) Context ═══ */}
      <text x={px[0]} y={top} fontSize={15} fontFamily={s} fill={P.text} fontWeight="700">(a) Context-level</text>
      <text x={px[0]} y={top+18} fontSize={12} fontFamily={s} fill={P.textLight}>RAG · Reflexion · MemGPT</text>
      <Stack x={px[0]+32} y={top+32} w={110} layers={4}/>
      <text x={px[0]+87} y={stackBot+10} textAnchor="middle" fontSize={10} fontFamily={s} fill={P.textLight}>Frozen host</text>
      <path d={`M${px[0]+10},${inputY-4} Q${px[0]+77},${inputY-14} ${px[0]+144},${inputY-4}`} fill="none" stroke={P.amber} strokeWidth={1}/>
      <text x={px[0]+77} y={inputY-18} textAnchor="middle" fontSize={10} fontFamily={s} fill={P.amber}>shared context window</text>
      <rect x={px[0]+4} y={inputY} width={68} height={36} rx={4} fill="none" stroke={P.amber} strokeWidth={1} strokeDasharray="4,2"/>
      <text x={px[0]+38} y={inputY+15} textAnchor="middle" fontSize={11} fontFamily={s} fill={P.amber} fontWeight="600">Memory</text>
      <text x={px[0]+38} y={inputY+28} textAnchor="middle" fontSize={10} fontFamily={s} fill={P.amber}>tokens</text>
      <rect x={px[0]+80} y={inputY} width={68} height={36} rx={4} fill="none" stroke={P.textMid} strokeWidth={1} strokeDasharray="4,2"/>
      <text x={px[0]+114} y={inputY+22} textAnchor="middle" fontSize={11} fontFamily={s} fill={P.textMid} fontWeight="500">Query</text>
      {/* O notation */}
      <text x={px[0]+87} y={stackBot+24} textAnchor="middle" fontSize={9} fontFamily={m} fill={P.red}>O(T·N·d) per token</text>

      {/* ═══ (b) Parameter ═══ */}
      <text x={px[1]} y={top} fontSize={15} fontFamily={s} fill={P.text} fontWeight="700">(b) Parameter-level</text>
      <text x={px[1]} y={top+18} fontSize={12} fontFamily={s} fill={P.textLight}>LoRA · Adapters</text>
      <Stack x={px[1]+32} y={top+32} w={110} layers={4} color={P.purple} hl={[0,1,2,3]}/>
      <text x={px[1]+87} y={stackBot+10} textAnchor="middle" fontSize={10} fontFamily={s} fill={P.textLight}>Modified host</text>
      {[0,1,2,3].map(i=>{const ly=top+32+(3-i)*40+18;return <g key={i}><rect x={px[1]+148} y={ly-13} width={34} height={26} rx={3} fill={P.purpleLight} stroke={P.purple} strokeWidth={0.8}/><text x={px[1]+165} y={ly} textAnchor="middle" dominantBaseline="middle" fontSize={11} fontFamily={m} fill={P.purple} fontWeight="600">ΔW</text><line x1={px[1]+142} y1={ly} x2={px[1]+148} y2={ly} stroke={P.purple} strokeWidth={0.8}/></g>})}
      <rect x={px[1]+50} y={inputY} width={76} height={36} rx={4} fill="none" stroke={P.textMid} strokeWidth={1} strokeDasharray="4,2"/>
      <text x={px[1]+88} y={inputY+22} textAnchor="middle" fontSize={11} fontFamily={s} fill={P.textMid} fontWeight="500">Query</text>
      <text x={px[1]+87} y={stackBot+24} textAnchor="middle" fontSize={9} fontFamily={m} fill={P.red}>O(∇) per adaptation</text>

      {/* ═══ (c) Activation ═══ */}
      <text x={px[2]} y={top} fontSize={15} fontFamily={s} fill={P.text} fontWeight="700">(c) Activation-level</text>
      <text x={px[2]} y={top+18} fontSize={12} fontFamily={s} fill={P.textLight}>RepEng · ActAdd</text>
      <Stack x={px[2]+32} y={top+32} w={110} layers={4} color={P.green} hl={[1,2,3]}/>
      <text x={px[2]+87} y={stackBot+10} textAnchor="middle" fontSize={10} fontFamily={s} fill={P.textLight}>Frozen host</text>
      <rect x={px[2]+154} y={top+62} width={36} height={72} rx={4} fill={P.greenLight} stroke={P.green} strokeWidth={1.2}/>
      <text x={px[2]+172} y={top+92} textAnchor="middle" fontSize={15} fontFamily={m} fill={P.green} fontWeight="700">d*</text>
      <text x={px[2]+172} y={top+108} textAnchor="middle" fontSize={9} fontFamily={s} fill={P.green}>fixed</text>
      {[1,2,3].map(i=>{const ly=top+32+(3-i)*40+18;return <line key={i} x1={px[2]+154} y1={ly} x2={px[2]+144} y2={ly} stroke={P.green} strokeWidth={1.2} markerEnd={`url(#a${P.green.replace('#','')})`}/>})}
      <text x={px[2]+172} y={top+150} textAnchor="middle" fontSize={11} fontFamily={m} fill={P.green} fontWeight="600">h + d*</text>
      <rect x={px[2]+50} y={inputY} width={76} height={36} rx={4} fill="none" stroke={P.textMid} strokeWidth={1} strokeDasharray="4,2"/>
      <text x={px[2]+88} y={inputY+22} textAnchor="middle" fontSize={11} fontFamily={s} fill={P.textMid} fontWeight="500">Query</text>
      <text x={px[2]+87} y={stackBot+24} textAnchor="middle" fontSize={9} fontFamily={m} fill={P.green}>O(L·d) per token</text>

      {/* ═══ (d) Enmeshed network — centered ═══ */}
      <text x={dMid} y={top} textAnchor="middle" fontSize={15} fontFamily={s} fill={P.blue} fontWeight="700">(d) Enmeshed network</text>
      <text x={dMid} y={top+18} textAnchor="middle" fontSize={12} fontFamily={s} fill={P.blue}>HEXIS (this work)</text>

      {/* M_ℓ compiled tensor boxes — left parallel column */}
      {[0,1,2,3].map(i=>{const ly=top+32+i*40;const li=3-i;return <g key={i}>
        <rect x={mX} y={ly} width={mW} height={36} rx={4} fill={P.blueBg} stroke={P.blue} strokeWidth={1} strokeDasharray="4,2"/>
        <text x={mX+mW/2} y={ly+21} textAnchor="middle" fontSize={10} fontFamily={m} fill={P.blue} fontWeight="600">M_{li}</text>
      </g>})}

      {/* Blending function B circles — connecting M_ℓ to host layers */}
      {[0,1,2,3].map(i=>{const ly=top+32+i*40+18;return <g key={i}>
        <line x1={mX+mW} y1={ly} x2={bX+2} y2={ly} stroke={P.blue} strokeWidth={0.8}/>
        <circle cx={bX+10} cy={ly} r={8} fill="white" stroke={P.blue} strokeWidth={1.2}/>
        <text x={bX+10} y={ly+3.5} textAnchor="middle" fontSize={9} fontFamily={m} fill={P.blue} fontWeight="700">B</text>
        <line x1={bX+18} y1={ly} x2={hostX} y2={ly} stroke={P.blue} strokeWidth={0.8}/>
      </g>})}

      {/* Host stack — right column */}
      <Stack x={hostX} y={top+32} w={hostW} layers={4} color={P.blue} hl={[0,1,2,3]}/>

      {/* Labels */}
      <text x={mX+mW/2} y={stackBot+10} textAnchor="middle" fontSize={9} fontFamily={s} fill={P.blue}>Compiled M</text>
      <text x={hostX+hostW/2} y={stackBot+10} textAnchor="middle" fontSize={9} fontFamily={s} fill={P.blue}>Frozen host</text>
      <text x={dMid} y={stackBot+24} textAnchor="middle" fontSize={9} fontFamily={m} fill={P.blue}>O(L·d·r) per token, fixed in N</text>

      {/* Inputs — spread horizontally, centered under respective columns */}
      {/* Secondary Knowledge Graph XML Context — under M column */}
      <rect x={mX-10} y={inputY} width={mW+50} height={44} rx={4} fill="none" stroke={P.blue} strokeWidth={1} strokeDasharray="4,2"/>
      <text x={mX-10+(mW+50)/2} y={inputY+12} textAnchor="middle" fontSize={8} fontFamily={s} fill={P.blue} fontWeight="600">Secondary</text>
      <text x={mX-10+(mW+50)/2} y={inputY+23} textAnchor="middle" fontSize={8} fontFamily={s} fill={P.blue} fontWeight="600">Knowledge Graph</text>
      <text x={mX-10+(mW+50)/2} y={inputY+34} textAnchor="middle" fontSize={8} fontFamily={s} fill={P.blue} fontWeight="600">XML Context</text>
      {/* Arrow up: φ compiles */}
      <line x1={mX+15} y1={inputY} x2={mX+15} y2={inputY-14} stroke={P.blue} strokeWidth={0.8} markerEnd={`url(#a${P.blue.replace('#','')})`}/>
      <text x={mX+34} y={inputY-6} fontSize={8} fontFamily={s} fill={P.blue}>φ compiles</text>

      {/* Query + curated slot — under host column */}
      <rect x={hostX+2} y={inputY} width={hostW} height={44} rx={4} fill="none" stroke={P.textMid} strokeWidth={1} strokeDasharray="4,2"/>
      <text x={hostX+hostW/2+2} y={inputY+15} textAnchor="middle" fontSize={9} fontFamily={s} fill={P.textMid} fontWeight="500">Query +</text>
      <text x={hostX+hostW/2+2} y={inputY+29} textAnchor="middle" fontSize={9} fontFamily={s} fill={P.blue} fontWeight="500">curated slot</text>
      <line x1={hostX+hostW/2+2} y1={inputY} x2={hostX+hostW/2+2} y2={inputY-14} stroke={P.textLight} strokeWidth={0.8} markerEnd={`url(#a${P.textLight.replace('#','')})`}/>

      {/* ═══ Summary row ═══ */}
      <line x1={10} y1={sumY} x2={W-10} y2={sumY} stroke={P.lineLight} strokeWidth={0.5}/>
      {[
        {x:px[0]+77, label:"✗", lc:P.red, items:["Memory in context","Competes for attention","Dilutes with length"], color:P.amber},
        {x:px[1]+88, label:"✗", lc:P.red, items:["Weights modified","∇ per adaptation","Fixed after training"], color:P.purple},
        {x:px[2]+88, label:"✗", lc:P.red, items:["Fixed direction","Same ∀ experience","Non-adaptive"], color:P.green},
        {x:dMid, label:"✓", lc:P.blue, items:["Parallel channel","Adapts at inference cost","Dilution-immune"], color:P.blue},
      ].map((col,ci)=><g key={ci}>
        <text x={col.x} y={sumY+16} textAnchor="middle" fontSize={13} fontFamily={s} fill={col.lc} fontWeight="700">{col.label}</text>
        {col.items.map((item,ii)=><text key={ii} x={col.x} y={sumY+32+ii*14} textAnchor="middle" fontSize={11} fontFamily={s} fill={col.color}>{item}</text>)}
      </g>)}

      {/* ═══ Full-width legend ═══ */}
      <line x1={10} y1={legendY} x2={W-10} y2={legendY} stroke={P.lineLight} strokeWidth={0.5}/>

      {/* B legend */}
      <circle cx={20} cy={legendY+16} r={8} fill="white" stroke={P.blue} strokeWidth={1.2}/>
      <text x={20} y={legendY+19} textAnchor="middle" fontSize={9} fontFamily={m} fill={P.blue} fontWeight="700">B</text>
      <text x={34} y={legendY+19} fontSize={10} fontFamily={s} fill={P.text} fontWeight="600">Blending function</text>
      <text x={20} y={legendY+34} fontSize={9} fontFamily={s} fill={P.textMid}>L1 (this work): h′ = h + s·(h·M_A)·M_Bᵀ</text>
      <text x={20} y={legendY+48} fontSize={9} fontFamily={s} fill={P.textMid}>L2: gated — h′ = h + g(h) ⊙ f(h, M)</text>
      <text x={20} y={legendY+62} fontSize={9} fontFamily={s} fill={P.textMid}>L3: cross-attn — h′ = h + Attn(h, M, M)</text>

      {/* Symbols */}
      <text x={310} y={legendY+19} fontSize={10} fontFamily={s} fill={P.text} fontWeight="600">Symbols</text>
      <text x={310} y={legendY+34} fontSize={9} fontFamily={m} fill={P.textMid}>h = hidden state at layer ℓ</text>
      <text x={310} y={legendY+48} fontSize={9} fontFamily={m} fill={P.textMid}>M_ℓ = compiled tensors (M_A, M_B ∈ ℝ^(d×r))</text>
      <text x={310} y={legendY+62} fontSize={9} fontFamily={m} fill={P.textMid}>d* = fixed contrastive direction vector</text>

      {/* Complexity */}
      <text x={610} y={legendY+19} fontSize={10} fontFamily={s} fill={P.text} fontWeight="600">Complexity (per token)</text>
      <text x={610} y={legendY+34} fontSize={9} fontFamily={m} fill={P.amber}>Context:  O(T · N · d)  — grows with N</text>
      <text x={610} y={legendY+48} fontSize={9} fontFamily={m} fill={P.green}>ActSteer: O(L · d)      — fixed</text>
      <text x={610} y={legendY+62} fontSize={9} fontFamily={m} fill={P.blue}>Enmeshed: O(L · d · r)  — fixed in N</text>

    </svg>
  </div>;
}
