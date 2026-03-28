import { useState } from "react";

const P = {
  bg: "#ffffff", text: "#0f172a", textMid: "#475569", textLight: "#94a3b8",
  line: "#334155", lineLight: "#cbd5e1",
  blue: "#1d4ed8", blueLight: "#dbeafe", blueBg: "#eff6ff",
};
const s = "'Helvetica Neue', Helvetica, Arial, sans-serif";
const m = "'Courier New', monospace";

export default function Fig() {
  const W = 780, H = 440;
  return <div style={{background:P.bg,padding:0,lineHeight:0}}>
    <svg width="100%" viewBox={`0 0 ${W} ${H}`} style={{display:"block"}}>
      <defs>
        <marker id="ab" markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto"><polygon points="0 0, 8 3, 0 6" fill={P.blue}/></marker>
        <marker id="ad" markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto"><polygon points="0 0, 8 3, 0 6" fill={P.line}/></marker>
        <marker id="al" markerWidth="7" markerHeight="5" refX="7" refY="2.5" orient="auto"><polygon points="0 0, 7 2.5, 0 5" fill={P.textLight}/></marker>
      </defs>

      {/* ═══ COMPILATION LOOP (top band) ═══ */}
      <rect x={8} y={8} width={570} height={148} rx={8} fill={P.blueBg} stroke={P.blue} strokeWidth={1.2} strokeDasharray="8,4"/>
      <text x={22} y={28} fontSize={13} fontFamily={s} fill={P.blue} fontWeight="700">Compilation loop</text>
      <text x={160} y={28} fontSize={10} fontFamily={s} fill={P.textLight}>(once per Mind Tree update, cached until beliefs change)</text>

      {/* Mind Tree */}
      <rect x={22} y={42} width={96} height={64} rx={5} fill={P.blueLight} stroke={P.blue} strokeWidth={1.5}/>
      <text x={70} y={60} textAnchor="middle" fontSize={12} fontFamily={s} fill={P.blue} fontWeight="700">Mind Tree</text>
      <text x={70} y={76} textAnchor="middle" fontSize={9} fontFamily={s} fill={P.blue}>beliefs · identity</text>
      <text x={70} y={88} textAnchor="middle" fontSize={9} fontFamily={s} fill={P.blue}>strategies · models</text>

      {/* Arrow → Host */}
      <line x1={118} y1={74} x2={140} y2={74} stroke={P.blue} strokeWidth={1.5} markerEnd="url(#ab)"/>

      {/* Frozen Host (parallel pass) */}
      <rect x={146} y={42} width={118} height={64} rx={5} fill={P.blueBg} stroke={P.blue} strokeWidth={1} strokeDasharray="5,3"/>
      <text x={205} y={60} textAnchor="middle" fontSize={11} fontFamily={s} fill={P.blue} fontWeight="600">Frozen Host</text>
      <text x={205} y={76} textAnchor="middle" fontSize={10} fontFamily={s} fill={P.textMid}>(parallel pass)</text>
      <text x={205} y={90} textAnchor="middle" fontSize={9} fontFamily={m} fill={P.textLight}>h_ℓ per layer</text>

      {/* Arrow → φ */}
      <line x1={264} y1={74} x2={294} y2={74} stroke={P.blue} strokeWidth={1.5} markerEnd="url(#ab)"/>

      {/* φ */}
      <circle cx={322} cy={74} r={24} fill={P.blue+"15"} stroke={P.blue} strokeWidth={2}/>
      <text x={322} y={78} textAnchor="middle" fontSize={19} fontFamily={m} fill={P.blue} fontWeight="700">φ</text>

      {/* Arrow → M/E tensors */}
      <line x1={346} y1={74} x2={376} y2={74} stroke={P.blue} strokeWidth={1.5} markerEnd="url(#ab)"/>

      {/* M/E Tensors */}
      <rect x={382} y={42} width={108} height={64} rx={5} fill={P.blue+"12"} stroke={P.blue} strokeWidth={1.5}/>
      <text x={436} y={60} textAnchor="middle" fontSize={11} fontFamily={m} fill={P.blue} fontWeight="700">M_A, M_B</text>
      <text x={436} y={78} textAnchor="middle" fontSize={11} fontFamily={m} fill={P.blue} fontWeight="700">E_A, E_B</text>
      <text x={436} y={94} textAnchor="middle" fontSize={9} fontFamily={s} fill={P.textMid}>per patched layer</text>

      {/* ═══ CURATION ARROW — left side, below compilation band ═══ */}
      <path d="M 400,106 C 400,130 260,130 120,170" fill="none" stroke={P.blue} strokeWidth={1.2} strokeDasharray="5,3" markerEnd="url(#ab)"/>
      <rect x={178} y={122} width={200} height={16} rx={3} fill={P.bg} opacity={0.9}/>
      <text x={278} y={134} textAnchor="middle" fontSize={10} fontFamily={s} fill={P.blue} fontWeight="500">M scores → select novel content for slot</text>

      {/* ═══ MODULATION ARROW — right side, below compilation band ═══ */}
      <line x1={460} y1={106} x2={460} y2={194} stroke={P.blue} strokeWidth={2} markerEnd="url(#ab)"/>
      <rect x={468} y={136} width={60} height={30} rx={3} fill={P.bg}/>
      <text x={498} y={150} textAnchor="middle" fontSize={11} fontFamily={s} fill={P.blue} fontWeight="600">modulate</text>
      <text x={498} y={164} textAnchor="middle" fontSize={11} fontFamily={s} fill={P.blue} fontWeight="600">Q / V</text>

      {/* ═══ REFLECTION LOOP — right side ═══ */}
      <rect x={545} y={8} width={82} height={148} rx={5} fill={P.bg} stroke={P.blue} strokeWidth={1} strokeDasharray="5,3"/>
      <text x={586} y={44} textAnchor="middle" fontSize={10} fontFamily={s} fill={P.blue} fontWeight="700">Reflection</text>
      <text x={586} y={58} textAnchor="middle" fontSize={10} fontFamily={s} fill={P.blue} fontWeight="700">loop</text>
      {/* Arrow from output up into reflection box */}
      <path d="M 548,290 C 586,290 586,160 586,156" fill="none" stroke={P.blue} strokeWidth={1.2} strokeDasharray="5,3" markerEnd="url(#ab)"/>
      {/* Arrow from reflection box back to Mind Tree */}
      <line x1={545} y1={80} x2={496} y2={80} stroke={P.blue} strokeWidth={1.2} strokeDasharray="5,3"/>
      <path d="M 496,80 C 496,130 70,130 70,106" fill="none" stroke={P.blue} strokeWidth={1.2} strokeDasharray="5,3" markerEnd="url(#ab)"/>
      {/* Reflection steps */}
      <text x={586} y={80} textAnchor="middle" fontSize={8} fontFamily={s} fill={P.textMid}>1. generate</text>
      <text x={586} y={94} textAnchor="middle" fontSize={8} fontFamily={s} fill={P.textMid}>2. reflect on</text>
      <text x={586} y={106} textAnchor="middle" fontSize={8} fontFamily={s} fill={P.textMid}>   output</text>
      <text x={586} y={120} textAnchor="middle" fontSize={8} fontFamily={s} fill={P.textMid}>3. update tree</text>
      <text x={586} y={134} textAnchor="middle" fontSize={8} fontFamily={s} fill={P.textMid}>4. recompile</text>

      {/* ═══ PRIMARY CHANNEL (bottom band) ═══ */}
      <rect x={8} y={178} width={530} height={130} rx={8} fill="#f8fafc" stroke={P.line} strokeWidth={1}/>
      <text x={22} y={198} fontSize={13} fontFamily={s} fill={P.text} fontWeight="700">Primary context</text>
      <text x={146} y={198} fontSize={10} fontFamily={s} fill={P.textLight}>(generation forward pass)</text>

      {/* Curated Slot */}
      <rect x={22} y={210} width={106} height={56} rx={5} fill={P.blueLight} stroke={P.blue} strokeWidth={1.2}/>
      <text x={75} y={228} textAnchor="middle" fontSize={11} fontFamily={s} fill={P.text} fontWeight="600">Curated Slot</text>
      <text x={75} y={244} textAnchor="middle" fontSize={10} fontFamily={s} fill={P.textMid}>40–80 tokens</text>
      <text x={75} y={258} textAnchor="middle" fontSize={9} fontFamily={s} fill={P.textLight}>novel evidence</text>

      {/* + */}
      <text x={142} y={242} textAnchor="middle" fontSize={20} fontFamily={s} fill={P.textLight}>+</text>

      {/* Query */}
      <rect x={156} y={210} width={106} height={56} rx={5} fill="white" stroke={P.line} strokeWidth={1}/>
      <text x={209} y={228} textAnchor="middle" fontSize={11} fontFamily={s} fill={P.text} fontWeight="600">Query</text>
      <text x={209} y={244} textAnchor="middle" fontSize={10} fontFamily={s} fill={P.textMid}>conversation</text>
      <text x={209} y={258} textAnchor="middle" fontSize={9} fontFamily={s} fill={P.textLight}>user input</text>

      {/* Arrow → Host */}
      <line x1={262} y1={238} x2={296} y2={238} stroke={P.line} strokeWidth={1.2} markerEnd="url(#ad)"/>

      {/* Frozen Host (primary) */}
      <rect x={302} y={206} width={168} height={66} rx={5} fill="white" stroke={P.line} strokeWidth={1.5}/>
      <text x={386} y={226} textAnchor="middle" fontSize={12} fontFamily={s} fill={P.text} fontWeight="700">Frozen Host</text>
      <text x={386} y={242} textAnchor="middle" fontSize={10} fontFamily={s} fill={P.textMid}>(primary pass)</text>
      <text x={386} y={258} textAnchor="middle" fontSize={10} fontFamily={m} fill={P.blue}>x′ = x + s·(x M_A) M_Bᵀ</text>

      {/* Arrow → Output */}
      <line x1={470} y1={238} x2={492} y2={238} stroke={P.line} strokeWidth={1.2} markerEnd="url(#ad)"/>

      {/* Output */}
      <rect x={498} y={216} width={62} height={44} rx={5} fill="#f1f5f9" stroke={P.line} strokeWidth={1}/>
      <text x={529} y={242} textAnchor="middle" fontSize={13} fontFamily={s} fill={P.text} fontWeight="600">Output</text>

      {/* expand_belief loop */}
      <path d={`M 529,260 L 529,328 L 75,328 L 75,270`} fill="none" stroke={P.textLight} strokeWidth={0.8} strokeDasharray="5,3" markerEnd="url(#al)"/>
      <text x={300} y={324} textAnchor="middle" fontSize={10} fontFamily={m} fill={P.textLight}>expand_belief(id) → deeper evidence on demand (Layer 3)</text>

      {/* ═══ COST BOX (far right) ═══ */}
      <rect x={642} y={178} width={130} height={130} rx={5} fill="#fafafa" stroke={P.lineLight} strokeWidth={0.6}/>
      <text x={707} y={198} textAnchor="middle" fontSize={11} fontFamily={s} fill={P.textMid} fontWeight="700">Per-token cost</text>
      <line x1={652} y1={206} x2={762} y2={206} stroke={P.lineLight} strokeWidth={0.5}/>
      <text x={707} y={224} textAnchor="middle" fontSize={10} fontFamily={s} fill={P.textMid}>4 rank-r matmuls</text>
      <text x={707} y={240} textAnchor="middle" fontSize={10} fontFamily={s} fill={P.textMid}>per patched layer</text>
      <text x={707} y={256} textAnchor="middle" fontSize={10} fontFamily={s} fill={P.textLight}>(2 for Q, 2 for V)</text>
      <line x1={652} y1={266} x2={762} y2={266} stroke={P.lineLight} strokeWidth={0.5}/>
      <text x={707} y={290} textAnchor="middle" fontSize={24} fontFamily={s} fill={P.blue} fontWeight="700">82%</text>
      <text x={707} y={306} textAnchor="middle" fontSize={10} fontFamily={s} fill={P.blue}>token savings</text>

      {/* ═══ CHANNELS BOX (far right, top) ═══ */}
      <rect x={642} y={8} width={130} height={148} rx={5} fill="#fafafa" stroke={P.lineLight} strokeWidth={0.6}/>
      <text x={707} y={28} textAnchor="middle" fontSize={11} fontFamily={s} fill={P.textMid} fontWeight="700">Three channels</text>
      <line x1={652} y1={36} x2={762} y2={36} stroke={P.lineLight} strokeWidth={0.5}/>
      <text x={707} y={56} textAnchor="middle" fontSize={10} fontFamily={m} fill={P.blue} fontWeight="600">d*</text>
      <text x={707} y={70} textAnchor="middle" fontSize={10} fontFamily={s} fill={P.textMid}>stance direction</text>
      <line x1={662} y1={78} x2={752} y2={78} stroke={P.lineLight} strokeWidth={0.3}/>
      <text x={707} y={94} textAnchor="middle" fontSize={10} fontFamily={m} fill={P.blue} fontWeight="600">M / E</text>
      <text x={707} y={108} textAnchor="middle" fontSize={10} fontFamily={s} fill={P.textMid}>disposition</text>
      <line x1={662} y1={116} x2={752} y2={116} stroke={P.lineLight} strokeWidth={0.3}/>
      <text x={707} y={132} textAnchor="middle" fontSize={10} fontFamily={m} fill={P.blue} fontWeight="600">slot</text>
      <text x={707} y={146} textAnchor="middle" fontSize={10} fontFamily={s} fill={P.textMid}>novel content</text>

      {/* ═══ KEY ═══ */}
      <text x={14} y={360} fontSize={10} fontFamily={s} fill={P.textMid} fontWeight="600">Key:</text>
      <line x1={36} y1={357} x2={60} y2={357} stroke={P.blue} strokeWidth={1.5}/>
      <text x={66} y={360} fontSize={10} fontFamily={s} fill={P.textMid}>data flow</text>
      <line x1={120} y1={357} x2={144} y2={357} stroke={P.blue} strokeWidth={1.2} strokeDasharray="5,3"/>
      <text x={150} y={360} fontSize={10} fontFamily={s} fill={P.textMid}>curation / reflection</text>
      <rect x={256} y={351} width={22} height={12} rx={2} fill={P.blueBg} stroke={P.blue} strokeWidth={0.6} strokeDasharray="3,2"/>
      <text x={284} y={360} fontSize={10} fontFamily={s} fill={P.textMid}>parallel ctx</text>
      <rect x={340} y={351} width={22} height={12} rx={2} fill="white" stroke={P.line} strokeWidth={0.8}/>
      <text x={368} y={360} fontSize={10} fontFamily={s} fill={P.textMid}>primary ctx</text>

      {/* Bottom annotation */}
      <text x={14} y={384} fontSize={10} fontFamily={s} fill={P.textLight}>Compilation produces modulation tensors (Layer 1: 0 tokens, dilution-immune) and curated slot content (Layer 2: 40–80 tokens of novel evidence).</text>
      <text x={14} y={398} fontSize={10} fontFamily={s} fill={P.textLight}>The reflection loop optionally updates the Mind Tree from output, triggering recompilation. Cost: one forward pass (~50ms on GPU).</text>

    </svg>
  </div>;
}
