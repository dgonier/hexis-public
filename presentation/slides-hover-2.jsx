// Hover animations for slides 8, 11, 13
const HT2 = window.HEXIS_TOKENS;
const HSP2 = window.SPACING;
const HF2 = window.FONTS;

// ============================================================
// 08 — System overview · hover φ rotates + Mind Tree flows in
// ============================================================
function S08_HoverFlow({ index, total }) {
  const [hover, setHover] = React.useState(null); // 'phi' | 'mind' | 'host' | null

  return (
    <Slide label="08 System">
      <TitleBlock
        eyebrow="HEXIS — system overview · paper Fig. 7"
        title="Two loops, one frozen host."
        sub="Hover φ — Mind Tree nodes flow in and emerge as M/E tensors. Hover Mind Tree — φ pulses, showing what reads from where."
      />

      <svg width="1700" height="640" style={{ position: 'absolute', left: HSP2.paddingX, bottom: 30 }}>
        <Defs />

        {/* Compilation loop */}
        <rect x={20} y={20} width={1660} height={260} rx={14}
          fill="none" stroke={HT2.accentDim} strokeDasharray="4 6" strokeWidth={1} />
        <text x={50} y={56} fontFamily={HF2.mono} fontSize={16} fill={HT2.accent}
          style={{ letterSpacing: '0.18em', textTransform: 'uppercase' }}>
          compilation loop · async, amortized
        </text>

        {/* Mind Tree */}
        <g onMouseEnter={() => setHover('mind')} onMouseLeave={() => setHover(null)} style={{ cursor: 'pointer' }}>
          <circle cx={130} cy={170} r={hover === 'mind' ? 38 : 30}
            fill={hover === 'mind' ? 'rgba(106,179,159,0.15)' : HT2.bgRaised}
            stroke={HT2.accent} strokeWidth={hover === 'mind' ? 2.5 : 1.5}
            style={{ transition: 'all 350ms' }} />
          <circle cx={100} cy={150} r={6} fill={HT2.accent2} />
          <circle cx={160} cy={150} r={6} fill={HT2.accent2} />
          <circle cx={100} cy={190} r={6} fill={HT2.accent2} />
          <circle cx={160} cy={190} r={6} fill={HT2.accent2} />
          <text x={130} y={228} textAnchor="middle" fontFamily={HF2.sans} fontSize={18} fill={HT2.inkDim}>Mind Tree</text>
        </g>

        {/* Particle flow Mind Tree → φ when hovering φ */}
        {hover === 'phi' && [0,1,2,3,4,5].map(j => (
          <circle key={j} r={4} fill={HT2.accent}>
            <animateMotion dur="1.6s" repeatCount="indefinite" begin={`${j*0.15}s`}
              path="M 130 170 Q 400 100 800 170" />
            <animate attributeName="opacity" values="1;1;0" dur="1.6s" repeatCount="indefinite" begin={`${j*0.15}s`} />
          </circle>
        ))}

        {/* Static arrows */}
        <Edge x1={170} y1={170} x2={330} y2={170}
          stroke={HT2.inkDim} arrow particle particleColor={HT2.accent} particleDur="2.6s" />

        {/* Frozen host */}
        <g onMouseEnter={() => setHover('host')} onMouseLeave={() => setHover(null)} style={{ cursor: 'pointer' }}>
          <rect x={340} y={100} width={180} height={140} rx={8}
            fill={hover === 'host' ? 'rgba(108,168,200,0.12)' : HT2.bgRaised}
            stroke={hover === 'host' ? HT2.accent2 : HT2.rule}
            strokeWidth={hover === 'host' ? 2 : 1}
            style={{ transition: 'all 300ms' }} />
          {[0,1,2,3,4].map((i) => (
            <line key={i} x1={340} y1={120 + i * 24} x2={520} y2={120 + i * 24}
              stroke={HT2.rule} strokeWidth={1} />
          ))}
          <text x={430} y={88} textAnchor="middle" fontFamily={HF2.mono} fontSize={13} fill={HT2.inkMute}
            style={{ letterSpacing: '0.12em', textTransform: 'uppercase' }}>frozen host</text>
          <text x={430} y={266} textAnchor="middle" fontFamily={HF2.mono} fontSize={13} fill={HT2.inkMute}
            style={{ letterSpacing: '0.12em', textTransform: 'uppercase' }}>(private pass)</text>
        </g>

        <Edge x1={530} y1={170} x2={680} y2={170}
          stroke={HT2.inkDim} arrow particle particleColor={HT2.accent} particleDur="2.6s" particleDelay={0.6} />

        {/* φ compiler */}
        <g onMouseEnter={() => setHover('phi')} onMouseLeave={() => setHover(null)} style={{ cursor: 'pointer' }}>
          <rect x={690} y={120} width={220} height={100} rx={10}
            fill={hover === 'phi' ? 'rgba(212,138,73,0.18)' : HT2.bgPanel}
            stroke={HT2.accent} strokeWidth={hover === 'phi' ? 3 : 1.5}
            style={{ transition: 'all 300ms' }} />
          <g transform={hover === 'phi' ? 'rotate(0 800 165)' : ''}>
            <text x={800} y={163} textAnchor="middle" fontFamily={HF2.serif} fontSize={48} fill={HT2.accent}
              style={{
                transition: 'all 400ms',
                transformOrigin: '800px 158px',
                animation: hover === 'phi' ? 'phiSpin 3s linear infinite' : 'none',
              }}>
              φ
            </text>
          </g>
          <text x={800} y={196} textAnchor="middle" fontFamily={HF2.mono} fontSize={14}
            fill={hover === 'phi' ? HT2.accent : HT2.inkDim}
            style={{ letterSpacing: '0.12em', textTransform: 'uppercase', transition: 'fill 300ms' }}>
            write function
          </text>
          {/* phi pulse when hovering mind */}
          {hover === 'mind' && (
            <rect x={690} y={120} width={220} height={100} rx={10} fill="none" stroke={HT2.accent} strokeWidth={2}>
              <animate attributeName="stroke-width" values="1;4;1" dur="1.4s" repeatCount="indefinite" />
              <animate attributeName="opacity" values="0.4;1;0.4" dur="1.4s" repeatCount="indefinite" />
            </rect>
          )}
        </g>

        <Edge x1={920} y1={170} x2={1080} y2={170}
          stroke={HT2.inkDim} arrow particle particleColor={HT2.accent} particleDur="2.6s" particleDelay={1.2} />

        {/* Modulation tensors — light up when hovering φ */}
        <g>
          {[0, 1, 2, 3, 4].map((i) => (
            <rect key={i} x={1090 + i * 36} y={120} width={28} height={100} rx={4}
              fill={hover === 'phi' ? 'rgba(212,138,73,0.40)' : HT2.bgRaised}
              stroke={HT2.accent} strokeWidth={hover === 'phi' ? 2 : 1.2}
              style={{ transition: 'all 350ms' }}>
              <animate attributeName="opacity" values="0.5;1;0.5" dur="2.5s"
                repeatCount="indefinite" begin={`${i * 0.2}s`} />
            </rect>
          ))}
          <text x={1180} y={250} textAnchor="middle" fontFamily={HF2.mono} fontSize={14}
            fill={hover === 'phi' ? HT2.accent : HT2.inkMute}
            style={{ letterSpacing: '0.12em', textTransform: 'uppercase', transition: 'fill 300ms' }}>
            M_A, M_B, E_A, E_B
          </text>
        </g>

        {/* Curated slot */}
        <g transform="translate(1320, 110)">
          <rect x={0} y={0} width={300} height={120} rx={10}
            fill={HT2.bgPanel} stroke={HT2.accent2} strokeWidth={1.5} />
          <text x={150} y={36} textAnchor="middle" fontFamily={HF2.mono} fontSize={14} fill={HT2.accent2}
            style={{ letterSpacing: '0.14em', textTransform: 'uppercase' }}>curated slot</text>
          <text x={150} y={70} textAnchor="middle" fontFamily={HF2.serif} fontSize={22} fill={HT2.ink}>novel specifics</text>
          <text x={150} y={98} textAnchor="middle" fontFamily={HF2.mono} fontSize={14} fill={HT2.inkMute}>~70 tokens</text>
        </g>

        {/* Generation loop */}
        <rect x={20} y={310} width={1660} height={310} rx={14}
          fill="none" stroke={HT2.accent2Dim} strokeDasharray="4 6" strokeWidth={1} />
        <text x={50} y={346} fontFamily={HF2.mono} fontSize={16} fill={HT2.accent2}
          style={{ letterSpacing: '0.18em', textTransform: 'uppercase' }}>
          generation loop · per-token, fixed cost
        </text>

        <rect x={50} y={420} width={210} height={100} rx={10} fill={HT2.bgPanel} stroke={HT2.rule} />
        <text x={155} y={460} textAnchor="middle" fontFamily={HF2.mono} fontSize={14} fill={HT2.inkMute}
          style={{ letterSpacing: '0.14em', textTransform: 'uppercase' }}>user query</text>
        <text x={155} y={494} textAnchor="middle" fontFamily={HF2.sans} fontSize={20} fill={HT2.inkDim}>+ curated slot</text>

        <Edge x1={270} y1={470} x2={420} y2={470}
          stroke={HT2.inkDim} arrow particle particleColor={HT2.accent2} particleDur="2.4s" />

        <rect x={430} y={370} width={460} height={220} rx={12}
          fill={HT2.bgRaised} stroke={HT2.rule} />
        <text x={660} y={358} textAnchor="middle" fontFamily={HF2.mono} fontSize={14} fill={HT2.inkMute}
          style={{ letterSpacing: '0.14em', textTransform: 'uppercase' }}>frozen host (generation)</text>
        {[0, 1, 2, 3, 4, 5, 6, 7].map((i) => {
          const patched = [1, 4, 7].includes(i);
          const yi = 390 + i * 24;
          return (
            <g key={i}>
              <line x1={450} y1={yi} x2={870} y2={yi}
                stroke={patched ? HT2.accent : HT2.rule}
                strokeWidth={patched ? 1.5 : 1} />
              {patched && (
                <text x={880} y={yi + 5} fontFamily={HF2.mono} fontSize={11} fill={HT2.accent}>+M, +E</text>
              )}
            </g>
          );
        })}

        {[0, 1, 2].map((i) => (
          <Edge key={i}
            x1={1180} y1={235} x2={780} y2={414 + i * 72}
            stroke={HT2.accent} strokeWidth={1.2} dash="4 4"
            particle particleColor={HT2.accent} particleDur="2.8s" particleDelay={i * 0.4} particleR={3} curve={-30} />
        ))}

        <Edge x1={900} y1={470} x2={1100} y2={470}
          stroke={HT2.inkDim} arrow particle particleColor={HT2.accent} particleDur="2.4s" particleDelay={1} />

        <rect x={1120} y={420} width={300} height={100} rx={10}
          fill={HT2.bgPanel} stroke={HT2.accent2} strokeWidth={1.5} />
        <text x={1270} y={460} textAnchor="middle" fontFamily={HF2.mono} fontSize={14} fill={HT2.accent2}
          style={{ letterSpacing: '0.14em', textTransform: 'uppercase' }}>generation</text>
        <text x={1270} y={494} textAnchor="middle" fontFamily={HF2.serif} fontSize={22} fill={HT2.ink}>shaped output</text>

        <Edge x1={1420} y1={470} x2={1580} y2={470}
          stroke={HT2.accent} arrow particle particleColor={HT2.accent} particleDur="3s" particleDelay={1.5} />
        <text x={1500} y={446} textAnchor="middle" fontFamily={HF2.mono} fontSize={13} fill={HT2.accent}
          style={{ letterSpacing: '0.12em', textTransform: 'uppercase' }}>teacher</text>

        <Edge x1={1620} y1={470} x2={1620} y2={170} stroke={HT2.accentDim} strokeWidth={1.2} dash="6 4" />
        <Edge x1={1620} y1={170} x2={170} y2={170}
          stroke={HT2.accentDim} strokeWidth={1.2} dash="6 4"
          particle particleColor={HT2.accent} particleDur="6s" particleDelay={2} particleR={3} />
      </svg>

      <style>{`
        @keyframes phiSpin {
          from { transform: rotate(0deg); transform-origin: 800px 158px; }
          to   { transform: rotate(360deg); transform-origin: 800px 158px; }
        }
      `}</style>

      <Chrome index={index} total={total} chapter="architecture" />
    </Slide>
  );
}

// ============================================================
// 11 — Dilution · hover lines triggers token-flood / fade animation
// ============================================================
function S11_HoverDilution({ index, total }) {
  const [hover, setHover] = React.useState(null); // 'hexis' | 'context' | null

  return (
    <Slide label="11 Dilution">
      <TitleBlock
        eyebrow="Result · stance under dilution"
        title="Filler doesn't reach a tensor it can't see."
        sub="Hover the orange line — compiled M chips pulse outside the chart, untouched. Hover the dashed line — belief chips fade as filler floods in."
      />

      <svg width="1700" height="500" style={{ position: 'absolute', left: HSP2.paddingX, bottom: 90 }}>
        <Defs />
        <g transform="translate(80, 60)">
          <line x1={0} y1={380} x2={1380} y2={380} stroke={HT2.rule} />
          <line x1={0} y1={0} x2={0} y2={380} stroke={HT2.rule} />
          {[0, 25, 50, 75, 100].map((v, i) => (
            <g key={i}>
              <line x1={-6} y1={380 - v * 3.6} x2={0} y2={380 - v * 3.6} stroke={HT2.rule} />
              <text x={-14} y={385 - v * 3.6} textAnchor="end" fontFamily={HF2.mono} fontSize={14} fill={HT2.inkMute}>{v}%</text>
            </g>
          ))}
          {[
            { x: 50, label: '0' },
            { x: 480, label: '1K' },
            { x: 910, label: '2K' },
            { x: 1340, label: '4K' },
          ].map((t, i) => (
            <g key={i}>
              <line x1={t.x} y1={380} x2={t.x} y2={386} stroke={HT2.rule} />
              <text x={t.x} y={406} textAnchor="middle" fontFamily={HF2.mono} fontSize={14} fill={HT2.inkMute}>{t.label}</text>
            </g>
          ))}
          <text x={690} y={440} textAnchor="middle" fontFamily={HF2.mono} fontSize={14} fill={HT2.inkMute}
            style={{ letterSpacing: '0.18em', textTransform: 'uppercase' }}>
            filler tokens between beliefs and query
          </text>

          {/* Filler token wall sweeping in below the chart for visual rhythm */}
          <g opacity={0.3}>
            {Array.from({ length: 26 }).map((_, j) => {
              const bx = 50 + j * 50;
              return (
                <rect key={j} x={bx} y={380} width={36} height={16} rx={2}
                  fill={HT2.inkDim} opacity={0.35 + (j / 26) * 0.5}>
                  <animate attributeName="y" from={380} to={362}
                    dur="0.6s" begin={`${0.4 + j * 0.04}s`} fill="freeze" />
                </rect>
              );
            })}
          </g>

          {/* In-context line — drawn first, animates in */}
          <polyline
            points={`50,${380 - 95 * 3.6} 480,${380 - 70 * 3.6} 910,${380 - 45 * 3.6} 1340,${380 - 22 * 3.6}`}
            fill="none" stroke={HT2.inkDim} strokeWidth={hover === 'context' ? 4 : 2}
            strokeDasharray="4 4" pathLength={1}
            style={{ transition: 'stroke-width 300ms' }}
            onMouseEnter={() => setHover('context')} onMouseLeave={() => setHover(null)}>
            <animate attributeName="stroke-dashoffset" from={1} to={0}
              dur="1.2s" begin="0.6s" fill="freeze" />
          </polyline>
          <polyline
            points={`50,${380 - 95 * 3.6} 480,${380 - 70 * 3.6} 910,${380 - 45 * 3.6} 1340,${380 - 22 * 3.6}`}
            fill="none" stroke="transparent" strokeWidth={28}
            onMouseEnter={() => setHover('context')} onMouseLeave={() => setHover(null)}
            style={{ cursor: 'pointer' }} />
          {[
            { x: 50, v: 95 }, { x: 480, v: 70 }, { x: 910, v: 45 }, { x: 1340, v: 22 },
          ].map((p, i) => (
            <circle key={i} cx={p.x} cy={380 - p.v * 3.6} r={0}
              fill={HT2.bg} stroke={HT2.inkDim} strokeWidth={1.5}
              style={{ pointerEvents: 'none' }}>
              <animate attributeName="r" from={0} to={6}
                dur="0.4s" begin={`${0.6 + i * 0.3}s`} fill="freeze" />
            </circle>
          ))}
          <text x={1360} y={380 - 22 * 3.6 + 6} fontFamily={HF2.mono} fontSize={14} fill={HT2.inkDim} opacity={0}>
            in-context · decays
            <animate attributeName="opacity" from={0} to={1}
              dur="0.5s" begin="1.6s" fill="freeze" />
          </text>

          {/* HEXIS — line sweeps in left-to-right */}
          <line x1={50} y1={380 - 360} x2={1340} y2={380 - 360}
            stroke="transparent" strokeWidth={28}
            onMouseEnter={() => setHover('hexis')} onMouseLeave={() => setHover(null)}
            style={{ cursor: 'pointer' }} />
          <line x1={50} y1={380 - 360} x2={50} y2={380 - 360}
            stroke={HT2.accent} strokeWidth={hover === 'hexis' ? 5 : 3}
            style={{ transition: 'stroke-width 300ms', pointerEvents: 'none' }}>
            <animate attributeName="x2" from={50} to={1340}
              dur="1.4s" begin="0.4s" fill="freeze" />
          </line>
          {[50, 480, 910, 1340].map((x, i) => (
            <g key={i}>
              <circle cx={x} cy={380 - 360} r={0}
                fill={HT2.accent} stroke={HT2.bg} strokeWidth={2}
                style={{ pointerEvents: 'none' }}>
                <animate attributeName="r" from={0} to={hover === 'hexis' ? 12 : 8}
                  dur="0.4s" begin={`${0.6 + i * 0.25}s`} fill="freeze" />
                <animate attributeName="r" values="8;14;8" dur="2.4s"
                  repeatCount="indefinite" begin={`${1.8 + i * 0.3}s`} />
              </circle>
              {/* M-particle floating above the line */}
              <circle cx={x} cy={380 - 360} r={3} fill={HT2.accent} opacity={0.6}>
                <animate attributeName="cy"
                  values={`${380 - 360};${380 - 360 - 16};${380 - 360}`}
                  dur="3s" repeatCount="indefinite" begin={`${2 + i * 0.2}s`} />
                <animate attributeName="opacity" values="0.7;0;0.7"
                  dur="3s" repeatCount="indefinite" begin={`${2 + i * 0.2}s`} />
              </circle>
            </g>
          ))}
          <text x={1360} y={380 - 360 + 6} fontFamily={HF2.mono} fontSize={14} fill={HT2.accent} fontWeight={600} opacity={0}>
            HEXIS — 100%
            <animate attributeName="opacity" from={0} to={1}
              dur="0.5s" begin="1.8s" fill="freeze" />
          </text>

          {/* Animation panel below the chart */}
          {hover === 'hexis' && (
            <g>
              <text x={690} y={120} textAnchor="middle" fontFamily={HF2.mono} fontSize={13} fill={HT2.accent}
                style={{ letterSpacing: '0.18em', textTransform: 'uppercase' }}>
                M lives in weight-space
              </text>
              {Array.from({ length: 5 }).map((_, j) => (
                <g key={j}>
                  <rect x={400 + j * 120} y={140} width={80} height={60} rx={4}
                    fill="rgba(212,138,73,0.20)" stroke={HT2.accent} strokeWidth={2}>
                    <animate attributeName="opacity" values="0.6;1;0.6" dur="1.6s" repeatCount="indefinite" begin={`${j * 0.2}s`} />
                  </rect>
                  <text x={440 + j * 120} y={176} textAnchor="middle" fontFamily={HF2.mono} fontSize={14} fill={HT2.accent} fontWeight={700}>M</text>
                </g>
              ))}
            </g>
          )}
          {hover === 'context' && (
            <g>
              <text x={690} y={120} textAnchor="middle" fontFamily={HF2.mono} fontSize={13} fill={HT2.inkMute}
                style={{ letterSpacing: '0.18em', textTransform: 'uppercase' }}>
                beliefs fade as filler floods in
              </text>
              {/* belief chip at start */}
              <rect x={20} y={140} width={70} height={60} rx={4} fill="rgba(212,138,73,0.18)" stroke={HT2.accent}>
                <animate attributeName="opacity" values="1;0.15;1" dur="3s" repeatCount="indefinite" />
              </rect>
              <text x={55} y={176} textAnchor="middle" fontFamily={HF2.mono} fontSize={12} fill={HT2.accent} fontWeight={700}>belief</text>
              {/* growing wall of filler */}
              {Array.from({ length: 14 }).map((_, j) => (
                <rect key={j} x={110 + j * 86} y={150} width={76} height={40} rx={3}
                  fill={HT2.inkDim} opacity={0.5}>
                  <animate attributeName="opacity" values="0;0.6;0.6" dur="3s"
                    repeatCount="indefinite" begin={`${j * 0.14}s`} />
                </rect>
              ))}
              {/* query chip at end */}
              <rect x={1300} y={140} width={70} height={60} rx={4} fill="rgba(108,168,200,0.18)" stroke={HT2.accent2} />
              <text x={1335} y={176} textAnchor="middle" fontFamily={HF2.mono} fontSize={12} fill={HT2.accent2} fontWeight={700}>query</text>
            </g>
          )}
        </g>
      </svg>

      <Chrome index={index} total={total} chapter="results" />
    </Slide>
  );
}

// ============================================================
// 13 — Two mechanisms · hover (a)/(b) routes bridge particles
// ============================================================
function S13_HoverRoute({ index, total }) {
  const [hover, setHover] = React.useState(null);

  return (
    <Slide label="13 Two Mechanisms">
      <TitleBlock
        eyebrow="Generalization"
        title="Two mechanisms. One hidden-state bridge."
        sub="Hover (a) — the bridge sends particles only to disposition. Hover (b) — only to retrieval. Same hidden state, two destinations."
      />

      <svg width="1700" height="540" style={{ position: 'absolute', left: HSP2.paddingX, bottom: 70 }}>
        <Defs />

        {/* Shared bridge in middle */}
        <g>
          <rect x={750} y={210} width={200} height={120} rx={12}
            fill={HT2.bgPanel} stroke={HT2.ink} strokeWidth={1.5} />
          <text x={850} y={246} textAnchor="middle" fontFamily={HF2.mono} fontSize={13} fill={HT2.inkMute}
            style={{ letterSpacing: '0.18em', textTransform: 'uppercase' }}>shared bridge</text>
          <text x={850} y={282} textAnchor="middle" fontFamily={HF2.serif} fontSize={26} fill={HT2.ink}>host hidden state</text>
          <text x={850} y={308} textAnchor="middle" fontFamily={HF2.mono} fontSize={16} fill={HT2.inkMute}>h ∈ ℝ^d</text>
        </g>

        {/* Mechanism A — left */}
        <g onMouseEnter={() => setHover('a')} onMouseLeave={() => setHover(null)} style={{ cursor: 'pointer' }}>
          <rect x={60} y={80} width={500} height={400} rx={12}
            fill={hover === 'a' ? 'rgba(212,138,73,0.08)' : 'transparent'}
            stroke={hover === 'a' ? HT2.accent : HT2.accentDim}
            strokeWidth={hover === 'a' ? 2 : 1}
            strokeDasharray="4 6"
            style={{ transition: 'all 300ms' }} />
          <text x={300} y={50} textAnchor="middle" fontFamily={HF2.mono} fontSize={14}
            fill={hover === 'a' ? HT2.accent : HT2.inkMute}
            style={{ letterSpacing: '0.18em', textTransform: 'uppercase', transition: 'fill 300ms' }}>
            mechanism (a) — disposition
          </text>

          <Node x={140} y={170} r={28} fill={HT2.bgRaised} stroke={HT2.accent}
            label="φ" labelPos="inside" fontSize={28} color={HT2.accent} />
          <text x={140} y={222} textAnchor="middle" fontFamily={HF2.mono} fontSize={13} fill={HT2.inkMute}
            style={{ letterSpacing: '0.12em', textTransform: 'uppercase' }}>compile</text>

          <Edge x1={170} y1={170} x2={400} y2={170} stroke={HT2.accent} arrow
            particle particleColor={HT2.accent} particleDur="2.4s" particleR={3} />

          <g transform="translate(420, 130)">
            {[0, 1, 2, 3].map((i) => (
              <rect key={i} x={i * 28} y={0} width={20} height={80} rx={3}
                fill={hover === 'a' ? 'rgba(212,138,73,0.25)' : HT2.bgRaised}
                stroke={HT2.accent} strokeWidth={hover === 'a' ? 1.8 : 1.2}
                style={{ transition: 'all 300ms' }}>
                <animate attributeName="opacity" values="0.4;1;0.4" dur="2s"
                  repeatCount="indefinite" begin={`${i * 0.2}s`} />
              </rect>
            ))}
            <text x={56} y={100} textAnchor="middle" fontFamily={HF2.mono} fontSize={13} fill={HT2.inkMute}
              style={{ letterSpacing: '0.06em' }}>M_A · M_B · E_A · E_B</text>
          </g>

          <text x={310} y={300} textAnchor="middle" fontFamily={HF2.serif} fontSize={26} fill={HT2.ink}>Q / V modulation</text>
          <text x={310} y={336} textAnchor="middle" fontFamily={HF2.sans} fontSize={20} fill={HT2.inkDim}>per-token probability shifts</text>
          <text x={310} y={376} textAnchor="middle" fontFamily={HF2.mono} fontSize={15} fill={HT2.accent}
            style={{ letterSpacing: '0.06em' }}>stance · voice · sycophancy</text>
        </g>

        {/* Mechanism B — right */}
        <g onMouseEnter={() => setHover('b')} onMouseLeave={() => setHover(null)} style={{ cursor: 'pointer' }}>
          <rect x={1140} y={80} width={500} height={400} rx={12}
            fill={hover === 'b' ? 'rgba(127,90,162,0.08)' : 'transparent'}
            stroke={hover === 'b' ? HT2.accent3 : HT2.accent3Dim}
            strokeWidth={hover === 'b' ? 2 : 1}
            strokeDasharray="4 6"
            style={{ transition: 'all 300ms' }} />
          <text x={1400} y={50} textAnchor="middle" fontFamily={HF2.mono} fontSize={14}
            fill={hover === 'b' ? HT2.accent3 : HT2.inkMute}
            style={{ letterSpacing: '0.18em', textTransform: 'uppercase', transition: 'fill 300ms' }}>
            mechanism (b) — agentic
          </text>

          <Node x={1560} y={170} r={28} fill={HT2.bgRaised} stroke={HT2.accent3}
            label="φ_R" labelPos="inside" fontSize={20} color={HT2.accent3} />
          <text x={1560} y={222} textAnchor="middle" fontFamily={HF2.mono} fontSize={13} fill={HT2.inkMute}
            style={{ letterSpacing: '0.12em', textTransform: 'uppercase' }}>retrieve</text>

          <Edge x1={1530} y1={170} x2={1300} y2={170}
            stroke={HT2.accent3} arrow
            particle particleColor={HT2.accent3} particleDur="2.4s" particleR={3} />

          <g transform="translate(1170, 110)">
            {[
              { x: 30, y: 30 }, { x: 90, y: 50 }, { x: 50, y: 80 },
              { x: 110, y: 100 }, { x: 30, y: 110 }, { x: 90, y: 130 },
            ].map((p, i) => (
              <Node key={i} x={p.x} y={p.y} r={8}
                fill={HT2.bgRaised}
                stroke={i === 2 ? HT2.accent3 : HT2.rule}
                pulse={i === 2} pulseDelay={0} haloColor={HT2.accent3} />
            ))}
            {[[0,1],[0,2],[1,3],[2,3],[2,4],[3,5],[4,5]].map(([a, b], i) => {
              const pts = [{x:30,y:30},{x:90,y:50},{x:50,y:80},{x:110,y:100},{x:30,y:110},{x:90,y:130}];
              return (
                <line key={i} x1={pts[a].x} y1={pts[a].y} x2={pts[b].x} y2={pts[b].y}
                  stroke={HT2.rule} strokeWidth={1} />
              );
            })}
          </g>

          <text x={1380} y={300} textAnchor="middle" fontFamily={HF2.serif} fontSize={26} fill={HT2.ink}>knowledge injection</text>
          <text x={1380} y={336} textAnchor="middle" fontFamily={HF2.sans} fontSize={20} fill={HT2.inkDim}>tool names, params, hints</text>
          <text x={1380} y={376} textAnchor="middle" fontFamily={HF2.mono} fontSize={15} fill={HT2.accent3}
            style={{ letterSpacing: '0.06em' }}>100% R@1 · 108-node graph</text>
        </g>

        {/* Routed bridge particles */}
        {hover === 'a' && [0,1,2,3,4].map(j => (
          <circle key={j} r={5} fill={HT2.accent}>
            <animateMotion dur="1.6s" repeatCount="indefinite" begin={`${j*0.2}s`}
              path="M 750 270 Q 600 270 560 270" />
            <animate attributeName="opacity" values="1;1;0" dur="1.6s" repeatCount="indefinite" begin={`${j*0.2}s`} />
          </circle>
        ))}
        {hover === 'b' && [0,1,2,3,4].map(j => (
          <circle key={j} r={5} fill={HT2.accent3}>
            <animateMotion dur="1.6s" repeatCount="indefinite" begin={`${j*0.2}s`}
              path="M 950 270 Q 1100 270 1140 270" />
            <animate attributeName="opacity" values="1;1;0" dur="1.6s" repeatCount="indefinite" begin={`${j*0.2}s`} />
          </circle>
        ))}
        {/* When neither is hovered, dimmer particles flow both ways */}
        {!hover && (
          <>
            <Edge x1={750} y1={270} x2={560} y2={270}
              stroke={HT2.accent} strokeWidth={1.2} dash="4 4"
              particle particleColor={HT2.accent} particleDur="2.8s" particleR={3} />
            <Edge x1={950} y1={270} x2={1140} y2={270}
              stroke={HT2.accent3} strokeWidth={1.2} dash="4 4"
              particle particleColor={HT2.accent3} particleDur="2.8s" particleDelay={1} particleR={3} />
          </>
        )}
      </svg>

      <Chrome index={index} total={total} chapter="generalization" />
    </Slide>
  );
}

Object.assign(window, { S08_HoverFlow, S11_HoverDilution, S13_HoverRoute });
