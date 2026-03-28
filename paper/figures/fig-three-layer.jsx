import { useState } from "react";

const P = {
  bg: "#ffffff", text: "#0f172a", textMid: "#475569", textLight: "#94a3b8",
  line: "#334155", lineLight: "#cbd5e1",
  blue: "#1d4ed8", blueLight: "#dbeafe", blueBg: "#eff6ff",
  green: "#15803d", red: "#b91c1c",
};
const s = "'Helvetica Neue', Helvetica, Arial, sans-serif";
const m = "'Courier New', monospace";

export default function Fig() {
  const W = 780, H = 440;
  return <div style={{background:P.bg,padding:0,lineHeight:0}}>
    <svg width="100%" viewBox={`0 0 ${W} ${H}`} style={{display:"block"}}>

      {/* ═══ LAYER 1 ═══ */}
      <rect x={8} y={8} width={480} height={82} rx={6} fill={P.blueBg} stroke={P.blue} strokeWidth={1.8}/>
      <text x={24} y={32} fontSize={16} fontFamily={s} fill={P.blue} fontWeight="700">Layer 1: Compiled M/E</text>
      <text x={24} y={52} fontSize={12} fontFamily={s} fill={P.textMid}>Disposition compiled from Mind Tree via φ</text>
      <text x={24} y={74} fontSize={12} fontFamily={m} fill={P.blue}>x′ = x + s_M · (x M_A) M_Bᵀ     V′ = V + s_E · (x E_A) E_Bᵀ</text>

      {/* Token count */}
      <rect x={500} y={8} width={88} height={82} rx={6} fill={P.blue+"08"} stroke={P.blue} strokeWidth={1}/>
      <text x={544} y={36} textAnchor="middle" fontSize={24} fontFamily={m} fill={P.blue} fontWeight="700">0</text>
      <text x={544} y={56} textAnchor="middle" fontSize={12} fontFamily={s} fill={P.blue}>tokens</text>
      <text x={544} y={74} textAnchor="middle" fontSize={10} fontFamily={s} fill={P.textLight}>always active</text>

      {/* Carries */}
      <rect x={600} y={8} width={112} height={82} rx={6} fill="#f0fdf4" stroke={P.green} strokeWidth={0.6}/>
      <text x={612} y={28} fontSize={11} fontFamily={s} fill={P.green}>✓ stance (4/4)</text>
      <text x={612} y={44} fontSize={11} fontFamily={s} fill={P.green}>✓ confident voice</text>
      <text x={612} y={60} fontSize={11} fontFamily={s} fill={P.green}>✓ parametric steering</text>
      <text x={612} y={76} fontSize={11} fontFamily={s} fill={P.green}>✓ dilution-immune</text>

      {/* ═══ LAYER 2 ═══ */}
      <rect x={8} y={104} width={480} height={82} rx={6} fill="#f8fafc" stroke={P.line} strokeWidth={1.5}/>
      <text x={24} y={128} fontSize={16} fontFamily={s} fill={P.text} fontWeight="700">Layer 2: M-curated slot</text>
      <text x={24} y={148} fontSize={12} fontFamily={s} fill={P.textMid}>Arguments + novel evidence selected by M activation scores</text>
      <text x={24} y={168} fontSize={12} fontFamily={s} fill={P.textMid}>+ structural routing via Mind Tree node properties</text>

      <rect x={500} y={104} width={88} height={82} rx={6} fill="#f8fafc" stroke={P.line} strokeWidth={1}/>
      <text x={544} y={132} textAnchor="middle" fontSize={20} fontFamily={m} fill={P.text} fontWeight="700">40–80</text>
      <text x={544} y={152} textAnchor="middle" fontSize={12} fontFamily={s} fill={P.textMid}>tokens</text>
      <text x={544} y={170} textAnchor="middle" fontSize={10} fontFamily={s} fill={P.textLight}>in primary context</text>

      <rect x={600} y={104} width={112} height={82} rx={6} fill="#fafafa" stroke={P.lineLight} strokeWidth={0.5}/>
      <text x={612} y={126} fontSize={11} fontFamily={s} fill={P.text}>specific numbers</text>
      <text x={612} y={142} fontSize={11} fontFamily={s} fill={P.text}>proper nouns, citations</text>
      <text x={612} y={158} fontSize={11} fontFamily={s} fill={P.text}>argument warrants</text>
      <text x={612} y={174} fontSize={10} fontFamily={s} fill={P.textLight}>content M can't compress</text>

      {/* ═══ LAYER 3 ═══ */}
      <rect x={8} y={200} width={480} height={70} rx={6} fill="none" stroke={P.lineLight} strokeWidth={1.2} strokeDasharray="6,4"/>
      <text x={24} y={226} fontSize={16} fontFamily={s} fill={P.textMid} fontWeight="700">Layer 3: Recursive expansion</text>
      <text x={24} y={248} fontSize={12} fontFamily={s} fill={P.textLight}>Model calls expand_belief(id) when deeper evidence needed</text>

      <rect x={500} y={200} width={88} height={70} rx={6} fill="none" stroke={P.lineLight} strokeWidth={0.6} strokeDasharray="4,3"/>
      <text x={544} y={226} textAnchor="middle" fontSize={18} fontFamily={m} fill={P.textLight} fontWeight="600">0–200</text>
      <text x={544} y={246} textAnchor="middle" fontSize={12} fontFamily={s} fill={P.textLight}>tokens</text>
      <text x={544} y={262} textAnchor="middle" fontSize={10} fontFamily={s} fill={P.textLight}>on demand</text>

      <rect x={600} y={200} width={112} height={70} rx={6} fill="none" stroke={P.lineLight} strokeWidth={0.3}/>
      <text x={612} y={224} fontSize={11} fontFamily={s} fill={P.textLight}>full methodology</text>
      <text x={612} y={240} fontSize={11} fontFamily={s} fill={P.textLight}>extended evidence</text>
      <text x={612} y={256} fontSize={11} fontFamily={s} fill={P.textLight}>deep backing</text>

      {/* ═══ TOKEN BAR CHART ═══ */}
      <line x1={8} y1={290} x2={W-8} y2={290} stroke={P.lineLight} strokeWidth={0.5}/>
      <text x={14} y={316} fontSize={15} fontFamily={s} fill={P.text} fontWeight="700">Token budget comparison</text>

      {[
        { label: "B  (full beliefs in context)", tokens: 400, color: P.textMid },
        { label: "D  (beliefs + M)", tokens: 120, color: P.textMid },
        { label: "F  (compiled M + curated slot)", tokens: 70, color: P.blue },
      ].map((item, i) => {
        const by = 332 + i * 30;
        const maxW = 280;
        const bw = (item.tokens / 400) * maxW;
        const lx = 220;
        return <g key={i}>
          <text x={14} y={by+14} fontSize={12} fontFamily={m} fill={P.textMid}>{item.label}</text>
          <rect x={lx} y={by} width={bw} height={22} rx={3}
            fill={item.color + (item.color===P.blue?"25":"15")}
            stroke={item.color} strokeWidth={item.color===P.blue?1.2:0.7}/>
          <text x={lx+bw+8} y={by+15} fontSize={13} fontFamily={m} fill={item.color} fontWeight="600">{item.tokens}t</text>
        </g>;
      })}

      {/* Savings bracket */}
      <line x1={560} y1={336} x2={560} y2={396} stroke={P.blue} strokeWidth={1}/>
      <line x1={555} y1={336} x2={565} y2={336} stroke={P.blue} strokeWidth={1}/>
      <line x1={555} y1={396} x2={565} y2={396} stroke={P.blue} strokeWidth={1}/>
      <text x={580} y={360} fontSize={20} fontFamily={s} fill={P.blue} fontWeight="700">82%</text>
      <text x={580} y={380} fontSize={12} fontFamily={s} fill={P.blue}>token savings</text>
      <text x={580} y={396} fontSize={10} fontFamily={s} fill={P.textLight}>(structured belief sets)</text>

      {/* Bottleneck boundary */}
      <line x1={8} y1={420} x2={W-8} y2={420} stroke={P.lineLight} strokeWidth={0.5}/>
      <text x={14} y={438} fontSize={11} fontFamily={s} fill={P.textMid} fontWeight="600">Bottleneck boundary (rank 16):</text>
      <text x={260} y={438} fontSize={11} fontFamily={s} fill={P.green}>✓ stance  ✓ voice  ✓ parametric  ✓ dilution-immune</text>
      <text x={592} y={438} fontSize={11} fontFamily={s} fill={P.red}>✗ novel content  ✗ exact actions</text>

    </svg>
  </div>;
}
