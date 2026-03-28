import { useState } from "react";

const P = {
  bg: "#ffffff", text: "#0f172a", textMid: "#475569", textLight: "#94a3b8",
  line: "#334155", lineLight: "#cbd5e1",
  blue: "#1d4ed8", blueLight: "#dbeafe", blueBg: "#eff6ff",
};
const s = "'Helvetica Neue', Helvetica, Arial, sans-serif";
const m = "'Courier New', monospace";

export default function Fig() {
  const W = 680, H = 380;

  // Q-mod: title row, then subtitle, then diagram
  const qTitle = 20;    // "Q-modulation"
  const qSub = 38;      // "(attention steering...)"
  const qBoxY = 54;     // x_ℓ box top — well below subtitle
  const qMid = qBoxY + 22; // vertical center of x_ℓ box (height=44)
  const qPertY = qBoxY - 6; // M_A/M_B boxes top — just above x_ℓ but below subtitle

  // Divider
  const divY = qBoxY + 108;

  // V-mod
  const vTitle = divY + 18;
  const vSub = divY + 36;
  const vBoxY = divY + 50;
  const vMid = vBoxY + 22;

  return <div style={{background:P.bg,padding:0,lineHeight:0}}>
    <svg width="100%" viewBox={`0 0 ${W} ${H}`} style={{display:"block"}}>
      <defs>
        <marker id="ab" markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto"><polygon points="0 0, 8 3, 0 6" fill={P.blue}/></marker>
        <marker id="ad" markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto"><polygon points="0 0, 8 3, 0 6" fill={P.line}/></marker>
      </defs>

      {/* ═══ Q-MODULATION ═══ */}
      <text x={14} y={qTitle} fontSize={16} fontFamily={s} fill={P.text} fontWeight="700">Q-modulation</text>
      <text x={150} y={qTitle} fontSize={12} fontFamily={s} fill={P.textLight}>(attention steering — what to attend to)</text>

      {/* x_ℓ */}
      <rect x={14} y={qBoxY} width={66} height={44} rx={4} fill="#f8fafc" stroke={P.line} strokeWidth={1.2}/>
      <text x={47} y={qMid+4} textAnchor="middle" fontSize={16} fontFamily={m} fill={P.text}>x_ℓ</text>

      {/* Split point */}
      <line x1={80} y1={qMid} x2={108} y2={qMid} stroke={P.line} strokeWidth={1}/>
      <circle cx={108} cy={qMid} r={3} fill={P.line}/>
      <line x1={108} y1={qMid} x2={108} y2={qPertY+19} stroke={P.line} strokeWidth={1}/>
      <line x1={108} y1={qMid} x2={108} y2={qMid+32} stroke={P.line} strokeWidth={1}/>

      {/* Top path: M perturbation — boxes aligned at qPertY */}
      <line x1={108} y1={qPertY+19} x2={130} y2={qPertY+19} stroke={P.blue} strokeWidth={1.2} markerEnd="url(#ab)"/>

      <rect x={136} y={qPertY} width={86} height={38} rx={4} fill={P.blueBg} stroke={P.blue} strokeWidth={1.2}/>
      <text x={179} y={qPertY+15} textAnchor="middle" fontSize={13} fontFamily={m} fill={P.blue} fontWeight="600">x · M_A</text>
      <text x={179} y={qPertY+30} textAnchor="middle" fontSize={10} fontFamily={s} fill={P.textMid}>d → r (2560→16)</text>

      <line x1={222} y1={qPertY+19} x2={244} y2={qPertY+19} stroke={P.blue} strokeWidth={1.2} markerEnd="url(#ab)"/>

      <rect x={250} y={qPertY} width={86} height={38} rx={4} fill={P.blueBg} stroke={P.blue} strokeWidth={1.2}/>
      <text x={293} y={qPertY+15} textAnchor="middle" fontSize={13} fontFamily={m} fill={P.blue} fontWeight="600">· M_Bᵀ</text>
      <text x={293} y={qPertY+30} textAnchor="middle" fontSize={10} fontFamily={s} fill={P.textMid}>r → d (16→2560)</text>

      <line x1={336} y1={qPertY+19} x2={362} y2={qPertY+19} stroke={P.blue} strokeWidth={1.2} markerEnd="url(#ab)"/>

      {/* Scale */}
      <rect x={368} y={qPertY+4} width={50} height={30} rx={4} fill={P.blue+"10"} stroke={P.blue} strokeWidth={1}/>
      <text x={393} y={qPertY+23} textAnchor="middle" fontSize={13} fontFamily={m} fill={P.blue} fontWeight="600">× s_M</text>

      <line x1={418} y1={qPertY+19} x2={440} y2={qPertY+19} stroke={P.blue} strokeWidth={1}/>
      <line x1={440} y1={qPertY+19} x2={460} y2={qMid-8} stroke={P.blue} strokeWidth={1}/>

      {/* Bottom path: identity */}
      <line x1={108} y1={qMid+32} x2={440} y2={qMid+32} stroke={P.line} strokeWidth={0.8}/>
      <line x1={440} y1={qMid+32} x2={460} y2={qMid+12} stroke={P.line} strokeWidth={0.8}/>
      <text x={274} y={qMid+46} textAnchor="middle" fontSize={11} fontFamily={s} fill={P.textLight}>identity path (unmodified x_ℓ)</text>

      {/* Addition */}
      <circle cx={468} cy={qMid} r={16} fill="white" stroke={P.line} strokeWidth={1.5}/>
      <text x={468} y={qMid+4} textAnchor="middle" fontSize={20} fontFamily={s} fill={P.line}>+</text>

      {/* → W_Q → Q' */}
      <line x1={484} y1={qMid} x2={512} y2={qMid} stroke={P.line} strokeWidth={1.2} markerEnd="url(#ad)"/>

      <rect x={518} y={qBoxY} width={62} height={44} rx={4} fill="#f8fafc" stroke={P.line} strokeWidth={1.2}/>
      <text x={549} y={qMid-4} textAnchor="middle" fontSize={13} fontFamily={m} fill={P.text}>W_Q</text>
      <text x={549} y={qMid+12} textAnchor="middle" fontSize={10} fontFamily={s} fill={P.textLight}>frozen</text>

      <line x1={580} y1={qMid} x2={614} y2={qMid} stroke={P.line} strokeWidth={1.2} markerEnd="url(#ad)"/>

      <rect x={620} y={qBoxY} width={52} height={44} rx={4} fill={P.blueLight} stroke={P.blue} strokeWidth={1.8}/>
      <text x={646} y={qMid+4} textAnchor="middle" fontSize={18} fontFamily={m} fill={P.blue} fontWeight="700">Q′</text>

      {/* ═══ DIVIDER ═══ */}
      <line x1={14} y1={divY} x2={W-14} y2={divY} stroke={P.lineLight} strokeWidth={0.5}/>

      {/* ═══ V-MODULATION ═══ */}
      <text x={14} y={vTitle} fontSize={16} fontFamily={s} fill={P.text} fontWeight="700">V-modulation</text>
      <text x={150} y={vTitle} fontSize={12} fontFamily={s} fill={P.textLight}>(content injection — what to extract)</text>

      {/* V_ℓ */}
      <rect x={14} y={vBoxY} width={66} height={44} rx={4} fill="#f8fafc" stroke={P.line} strokeWidth={1.2}/>
      <text x={47} y={vMid+4} textAnchor="middle" fontSize={16} fontFamily={m} fill={P.text}>V_ℓ</text>

      <line x1={80} y1={vMid} x2={170} y2={vMid} stroke={P.line} strokeWidth={1}/>

      {/* E perturbation block */}
      <rect x={120} y={vMid+24} width={150} height={38} rx={4} fill={P.blueBg} stroke={P.blue} strokeWidth={1.2}/>
      <text x={195} y={vMid+39} textAnchor="middle" fontSize={13} fontFamily={m} fill={P.blue} fontWeight="600">(x_ℓ · E_A) E_Bᵀ</text>
      <text x={195} y={vMid+55} textAnchor="middle" fontSize={10} fontFamily={s} fill={P.textMid}>rank-16 value perturbation</text>

      {/* Scale */}
      <rect x={284} y={vMid+24} width={50} height={38} rx={4} fill={P.blue+"10"} stroke={P.blue} strokeWidth={1}/>
      <text x={309} y={vMid+47} textAnchor="middle" fontSize={13} fontFamily={m} fill={P.blue} fontWeight="600">× s_E</text>

      {/* x_ℓ input label */}
      <text x={82} y={vMid+46} fontSize={11} fontFamily={m} fill={P.textLight}>x_ℓ</text>
      <line x1={100} y1={vMid+43} x2={120} y2={vMid+43} stroke={P.textLight} strokeWidth={0.8} markerEnd="url(#ab)"/>

      <line x1={334} y1={vMid+43} x2={360} y2={vMid+43} stroke={P.blue} strokeWidth={1}/>
      <line x1={360} y1={vMid+43} x2={380} y2={vMid+14} stroke={P.blue} strokeWidth={1}/>

      {/* Addition */}
      <circle cx={388} cy={vMid} r={16} fill="white" stroke={P.line} strokeWidth={1.5}/>
      <text x={388} y={vMid+4} textAnchor="middle" fontSize={20} fontFamily={s} fill={P.line}>+</text>
      <line x1={170} y1={vMid} x2={372} y2={vMid} stroke={P.line} strokeWidth={0.8}/>

      {/* → V' */}
      <line x1={404} y1={vMid} x2={460} y2={vMid} stroke={P.line} strokeWidth={1.2} markerEnd="url(#ad)"/>

      <rect x={466} y={vBoxY} width={52} height={44} rx={4} fill={P.blueLight} stroke={P.blue} strokeWidth={1.8}/>
      <text x={492} y={vMid+4} textAnchor="middle" fontSize={18} fontFamily={m} fill={P.blue} fontWeight="700">V′</text>

      {/* Annotation box */}
      <rect x={536} y={vBoxY-10} width={136} height={100} rx={5} fill="#fafafa" stroke={P.lineLight} strokeWidth={0.5}/>
      <text x={548} y={vBoxY+10} fontSize={12} fontFamily={s} fill={P.blue} fontWeight="700">Q′ steers attention</text>
      <text x={548} y={vBoxY+26} fontSize={11} fontFamily={s} fill={P.textMid}>what to attend to</text>
      <line x1={548} y1={vBoxY+34} x2={660} y2={vBoxY+34} stroke={P.lineLight} strokeWidth={0.5}/>
      <text x={548} y={vBoxY+50} fontSize={12} fontFamily={s} fill={P.blue} fontWeight="700">V′ injects content</text>
      <text x={548} y={vBoxY+66} fontSize={11} fontFamily={s} fill={P.textMid}>what to extract</text>
      <line x1={548} y1={vBoxY+74} x2={660} y2={vBoxY+74} stroke={P.lineLight} strokeWidth={0.5}/>
      <text x={548} y={vBoxY+88} fontSize={10} fontFamily={s} fill={P.textLight}>Host W_Q, W_V untouched</text>

      {/* Equation bar */}
      <rect x={14} y={H-38} width={W-28} height={30} rx={4} fill="#f8fafc" stroke={P.lineLight} strokeWidth={0.5}/>
      <text x={W/2} y={H-18} textAnchor="middle" fontSize={13} fontFamily={m} fill={P.text}>
        x′_ℓ = x_ℓ + s_M · (x_ℓ M_A) M_Bᵀ          V′_ℓ = V_ℓ + s_E · (x_ℓ E_A) E_Bᵀ
      </text>
    </svg>
  </div>;
}
