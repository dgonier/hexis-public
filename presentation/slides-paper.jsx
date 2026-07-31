// Paper-faithful interactive figures + replacement slides
const PT = window.HEXIS_TOKENS;
const PSP = window.SPACING;
const PF = window.FONTS;

// =============================================================
// Replacement Slide 05 — Architecture comparison (paper Fig 1)
// Hover any panel for definition; the four-column comparison.
// =============================================================
function S05_Enmeshed_v2({ index, total }) {
  const tt = useTooltip();
  const cols = [
    { tag: '(a)', name: 'Context-level', sub: 'RAG · Reflexion · MemGPT', color: PT.inkDim, line: '#7c5d3a',
      facts: ['Memory in context', 'Competes for attention', 'Dilutes with length'],
      ok: false, complexity: 'O(T·N·d) per token' },
    { tag: '(b)', name: 'Parameter-level', sub: 'LoRA · Adapters', color: PT.accent3, line: PT.accent3,
      facts: ['Weights modified', '∇ per adaptation', 'Fixed after training'],
      ok: false, complexity: 'O(∇) per adaptation' },
    { tag: '(c)', name: 'Activation-level', sub: 'RepEng · ActAdd', color: '#5d9b78', line: '#5d9b78',
      facts: ['Fixed direction', 'Same ∀ experience', 'Non-adaptive'],
      ok: false, complexity: 'O(L·d) per token' },
    { tag: '(d)', name: 'Enmeshed (HEXIS)', sub: 'this work', color: PT.accent, line: PT.accent,
      facts: ['Parallel channel', 'Adapts at inference cost', 'Dilution-immune'],
      ok: true, complexity: 'O(L·d·r) — fixed in N', highlight: true },
  ];

  return (
    <Slide label="05 Enmeshed">
      <TitleBlock
        eyebrow="The new primitive · paper Fig. 1"
        title="Where does the new information fuse?"
        sub="Four families of adaptation, distinguished by where new information meets the host computation. Hover any panel."
      />

      <div style={{
        position: 'absolute', left: PSP.paddingX, right: PSP.paddingX, top: 360,
        display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 24,
      }}>
        {cols.map((c, i) => (
          <div key={i}
            onMouseEnter={tt.onEnter(c.highlight ? 'parallel' : 'host')}
            onMouseLeave={tt.onLeave}
            style={{
              border: `1px solid ${c.highlight ? c.line : PT.rule}`,
              borderRadius: 12, padding: '24px 24px 28px',
              background: c.highlight ? 'rgba(212,138,73,0.06)' : PT.bgPanel,
              minHeight: 540, position: 'relative', cursor: 'help',
            }}>
            <div style={{
              fontFamily: PF.mono, fontSize: 14, color: c.color,
              letterSpacing: '0.14em', textTransform: 'uppercase', marginBottom: 8,
            }}>{c.tag} {c.sub}</div>
            <div style={{
              fontFamily: PF.serif, fontSize: 32, color: PT.ink, lineHeight: 1.05,
              marginBottom: 24, fontWeight: 400,
            }}>{c.name}</div>

            {/* Diagram */}
            <svg width="100%" height="200" viewBox="0 0 240 200">
              {/* host stack */}
              <g>
                {[0,1,2,3].map(j => (
                  <rect key={j} x={i === 3 ? 130 : 90} y={20 + j*36} width={70} height={28} rx={3}
                    fill={i === 1 ? `${c.line}22` : PT.bgRaised}
                    stroke={i === 1 || i === 3 ? c.line : (i === 2 && j > 0 ? c.line : PT.rule)}
                    strokeWidth={i === 1 || i === 3 || (i === 2 && j > 0) ? 1.5 : 1} />
                ))}
                {i === 1 && [0,1,2,3].map(j => (
                  <g key={j}>
                    <rect x={170} y={22 + j*36} width={28} height={24} rx={2}
                      fill={`${c.line}22`} stroke={c.line} strokeWidth={0.8} />
                    <text x={184} y={38 + j*36} textAnchor="middle" fontFamily={PF.mono} fontSize={10} fill={c.line}>ΔW</text>
                  </g>
                ))}
                {i === 2 && (
                  <g>
                    <rect x={170} y={56} width={32} height={56} rx={3} fill={`${c.line}22`} stroke={c.line} strokeWidth={1.2} />
                    <text x={186} y={88} textAnchor="middle" fontFamily={PF.mono} fontSize={13} fill={c.line} fontWeight={700}>d*</text>
                    {[1,2,3].map(j => (
                      <line key={j} x1={170} y1={34 + j*36} x2={160} y2={34 + j*36} stroke={c.line} strokeWidth={1.2}
                        markerEnd="url(#arrowhead-accent2)" />
                    ))}
                  </g>
                )}
                {i === 3 && (
                  <g>
                    {/* parallel column */}
                    {[0,1,2,3].map(j => (
                      <rect key={j} x={20} y={20 + j*36} width={50} height={28} rx={3}
                        fill="rgba(212,138,73,0.10)" stroke={c.line} strokeWidth={1} strokeDasharray="3 2" />
                    ))}
                    {[0,1,2,3].map(j => (
                      <text key={j} x={45} y={38 + j*36} textAnchor="middle" fontFamily={PF.mono} fontSize={11} fill={c.line}>M_{3-j}</text>
                    ))}
                    {/* B blending circles */}
                    {[0,1,2,3].map(j => (
                      <g key={j}>
                        <line x1={70} y1={34 + j*36} x2={120} y2={34 + j*36} stroke={c.line} strokeWidth={0.8} />
                        <circle cx={100} cy={34 + j*36} r={7} fill={PT.bg} stroke={c.line} strokeWidth={1.2}>
                          <animate attributeName="r" values="6;8;6" dur="2.4s" repeatCount="indefinite" begin={`${j*0.2}s`} />
                        </circle>
                        <text x={100} y={37 + j*36} textAnchor="middle" fontFamily={PF.mono} fontSize={9} fill={c.line} fontWeight={700}>B</text>
                      </g>
                    ))}
                  </g>
                )}
                {i === 0 && (
                  <g>
                    <rect x={10} y={170} width={50} height={20} rx={3} fill="none" stroke={c.line} strokeDasharray="3 2" />
                    <text x={35} y={184} textAnchor="middle" fontFamily={PF.mono} fontSize={9} fill={c.line}>memory</text>
                    <rect x={70} y={170} width={50} height={20} rx={3} fill="none" stroke={PT.inkDim} strokeDasharray="3 2" />
                    <text x={95} y={184} textAnchor="middle" fontFamily={PF.mono} fontSize={9} fill={PT.inkDim}>query</text>
                    <path d="M 30 168 Q 70 158 110 168" fill="none" stroke={c.line} strokeWidth={1} />
                  </g>
                )}
              </g>
              <text x={120} y={196} textAnchor="middle" fontFamily={PF.mono} fontSize={10}
                fill={c.highlight ? c.line : PT.inkMute}>{c.complexity}</text>
            </svg>

            {/* Facts */}
            <div style={{ marginTop: 20 }}>
              {c.facts.map((f, j) => (
                <div key={j} style={{
                  fontFamily: PF.sans, fontSize: 18, color: c.color, marginBottom: 6,
                }}>{c.ok ? '✓' : '✗'} {f}</div>
              ))}
            </div>

            {c.highlight && (
              <div style={{
                position: 'absolute', top: -1, right: -1,
                background: c.line, color: PT.bg,
                fontFamily: PF.mono, fontSize: 12, letterSpacing: '0.12em',
                padding: '6px 12px', borderRadius: '0 12px 0 12px',
                textTransform: 'uppercase', fontWeight: 700,
              }}>this paper</div>
            )}
          </div>
        ))}
      </div>

      <Tooltip tip={tt.tip} />
      <Chrome index={index} total={total} chapter="enmeshed networks" />
    </Slide>
  );
}

// =============================================================
// Replacement Slide 08 — System overview (paper Fig 7)
// Click "step" to advance compilation flow.
// =============================================================
function S08_System_v2({ index, total }) {
  const tt = useTooltip();
  const [step, setStep] = React.useState(0);
  const STEPS = ['idle', 'mindtree', 'host', 'phi', 'tensors', 'modulate', 'output'];

  const isActive = (k) => STEPS.indexOf(k) <= step;
  const isCurrent = (k) => STEPS[step] === k;

  return (
    <Slide label="08 System">
      <TitleBlock
        eyebrow="HEXIS · system overview"
        title="Two loops, one frozen host."
        sub="Click the diagram or use the stepper. Hover any node for definition."
      />

      <svg width="1700" height="540" style={{ position: 'absolute', left: PSP.paddingX, top: 320, cursor: 'pointer' }}
        onClick={() => setStep((step + 1) % STEPS.length)}>
        <Defs />

        {/* Compilation band */}
        <g>
          <rect x={20} y={20} width={1340} height={220} rx={12}
            fill="rgba(212,138,73,0.04)" stroke={PT.accent} strokeWidth={1} strokeDasharray="6 4" />
          <text x={50} y={48} fontFamily={PF.mono} fontSize={16} fill={PT.accent}
            style={{ letterSpacing: '0.18em', textTransform: 'uppercase' }}>
            compilation loop · cached until beliefs change
          </text>

          {/* Mind Tree */}
          <g onMouseEnter={tt.onEnter('mindtree')} onMouseLeave={tt.onLeave} style={{ cursor: 'help' }}>
            <rect x={50} y={80} width={170} height={120} rx={10}
              fill={isActive('mindtree') ? 'rgba(212,138,73,0.20)' : PT.bgPanel}
              stroke={isCurrent('mindtree') ? PT.accent : (isActive('mindtree') ? PT.accent : PT.rule)}
              strokeWidth={isCurrent('mindtree') ? 3 : 1.5} />
            <text x={135} y={120} textAnchor="middle" fontFamily={PF.serif} fontSize={24} fill={PT.ink}>Mind Tree</text>
            <text x={135} y={148} textAnchor="middle" fontFamily={PF.sans} fontSize={16} fill={PT.inkDim}>identity · beliefs</text>
            <text x={135} y={170} textAnchor="middle" fontFamily={PF.sans} fontSize={16} fill={PT.inkDim}>strategies · models</text>
          </g>

          <Edge x1={220} y1={140} x2={300} y2={140} stroke={isActive('host') ? PT.accent : PT.inkMute} arrow
            particle={isCurrent('host')} particleColor={PT.accent} particleDur="1.4s" />

          {/* Frozen host (parallel) */}
          <g onMouseEnter={tt.onEnter('parallel')} onMouseLeave={tt.onLeave} style={{ cursor: 'help' }}>
            <rect x={310} y={80} width={210} height={120} rx={10}
              fill={isActive('host') ? PT.bgPanel : PT.bgRaised}
              stroke={isCurrent('host') ? PT.accent : (isActive('host') ? PT.accent : PT.rule)}
              strokeWidth={isCurrent('host') ? 3 : 1} strokeDasharray="6 4" />
            <text x={415} y={114} textAnchor="middle" fontFamily={PF.serif} fontSize={22} fill={PT.ink}>Frozen Host</text>
            <text x={415} y={140} textAnchor="middle" fontFamily={PF.mono} fontSize={14} fill={PT.inkDim}>(parallel pass)</text>
            <text x={415} y={172} textAnchor="middle" fontFamily={PF.mono} fontSize={14} fill={PT.inkMute}>h_ℓ per layer</text>
          </g>

          <Edge x1={520} y1={140} x2={620} y2={140} stroke={isActive('phi') ? PT.accent : PT.inkMute} arrow
            particle={isCurrent('phi')} particleColor={PT.accent} particleDur="1.4s" />

          {/* phi */}
          <g onMouseEnter={tt.onEnter('phi')} onMouseLeave={tt.onLeave} style={{ cursor: 'help' }}>
            <circle cx={680} cy={140} r={50}
              fill={isActive('phi') ? 'rgba(212,138,73,0.20)' : PT.bgRaised}
              stroke={isCurrent('phi') ? PT.accent : (isActive('phi') ? PT.accent : PT.rule)}
              strokeWidth={isCurrent('phi') ? 3 : 2} />
            <text x={680} y={156} textAnchor="middle" fontFamily={PF.mono} fontSize={42} fill={PT.accent} fontWeight={700}>φ</text>
          </g>

          <Edge x1={730} y1={140} x2={820} y2={140} stroke={isActive('tensors') ? PT.accent : PT.inkMute} arrow
            particle={isCurrent('tensors')} particleColor={PT.accent} particleDur="1.4s" />

          {/* Tensors */}
          <g onMouseEnter={tt.onEnter('M_A')} onMouseLeave={tt.onLeave} style={{ cursor: 'help' }}>
            <rect x={830} y={80} width={210} height={120} rx={10}
              fill={isActive('tensors') ? 'rgba(212,138,73,0.20)' : PT.bgPanel}
              stroke={isCurrent('tensors') ? PT.accent : (isActive('tensors') ? PT.accent : PT.rule)}
              strokeWidth={isCurrent('tensors') ? 3 : 1.5} />
            <text x={935} y={118} textAnchor="middle" fontFamily={PF.mono} fontSize={20} fill={PT.accent} fontWeight={700}>M_A · M_B</text>
            <text x={935} y={148} textAnchor="middle" fontFamily={PF.mono} fontSize={20} fill={PT.accent2} fontWeight={700}>E_A · E_B</text>
            <text x={935} y={176} textAnchor="middle" fontFamily={PF.sans} fontSize={14} fill={PT.inkMute}>per patched layer</text>
          </g>

          {/* Curated slot — branched from tensors */}
          <g onMouseEnter={tt.onEnter('curated')} onMouseLeave={tt.onLeave} style={{ cursor: 'help' }}>
            <rect x={1100} y={80} width={240} height={120} rx={10}
              fill={isActive('tensors') ? PT.bgPanel : PT.bgRaised}
              stroke={isActive('tensors') ? PT.accent2 : PT.rule}
              strokeWidth={1.5} />
            <text x={1220} y={118} textAnchor="middle" fontFamily={PF.serif} fontSize={22} fill={PT.ink}>Curated slot</text>
            <text x={1220} y={146} textAnchor="middle" fontFamily={PF.mono} fontSize={14} fill={PT.accent2}>40–80 tokens</text>
            <text x={1220} y={172} textAnchor="middle" fontFamily={PF.sans} fontSize={14} fill={PT.inkMute}>novel evidence</text>
          </g>
          <Edge x1={1040} y1={140} x2={1100} y2={140} stroke={isActive('tensors') ? PT.accent2 : PT.inkMute} arrow />
        </g>

        {/* Generation band */}
        <g>
          <rect x={20} y={270} width={1340} height={220} rx={12}
            fill="rgba(74,144,184,0.04)" stroke={PT.accent2} strokeWidth={1} strokeDasharray="6 4" />
          <text x={50} y={298} fontFamily={PF.mono} fontSize={16} fill={PT.accent2}
            style={{ letterSpacing: '0.18em', textTransform: 'uppercase' }}>
            generation loop · per token · fixed cost
          </text>

          {/* Query */}
          <rect x={50} y={330} width={170} height={120} rx={10} fill={PT.bgPanel} stroke={PT.rule} />
          <text x={135} y={372} textAnchor="middle" fontFamily={PF.serif} fontSize={22} fill={PT.ink}>Query</text>
          <text x={135} y={400} textAnchor="middle" fontFamily={PF.sans} fontSize={16} fill={PT.inkDim}>conversation</text>
          <text x={135} y={426} textAnchor="middle" fontFamily={PF.sans} fontSize={16} fill={PT.accent2}>+ curated slot</text>

          <Edge x1={220} y1={390} x2={300} y2={390} stroke={isActive('modulate') ? PT.accent2 : PT.inkMute} arrow
            particle={isCurrent('modulate')} particleColor={PT.accent2} particleDur="1.4s" />

          {/* Frozen host (primary) — modulated */}
          <rect x={310} y={320} width={420} height={140} rx={10}
            fill={isActive('modulate') ? 'rgba(74,144,184,0.10)' : PT.bgRaised}
            stroke={isCurrent('modulate') ? PT.accent : (isActive('modulate') ? PT.accent : PT.rule)}
            strokeWidth={isCurrent('modulate') ? 3 : 1.5} />
          <text x={520} y={356} textAnchor="middle" fontFamily={PF.serif} fontSize={22} fill={PT.ink}>Frozen Host (primary)</text>
          <text x={520} y={388} textAnchor="middle" fontFamily={PF.mono} fontSize={18} fill={PT.accent}>x′ = x + s · (x M_A) M_Bᵀ</text>
          <text x={520} y={418} textAnchor="middle" fontFamily={PF.mono} fontSize={18} fill={PT.accent2}>V′ = V + s · (x E_A) E_Bᵀ</text>
          <text x={520} y={446} textAnchor="middle" fontFamily={PF.mono} fontSize={13} fill={PT.inkMute}
            style={{ letterSpacing: '0.12em', textTransform: 'uppercase' }}>same weights · shaped activations</text>

          {/* Modulation feed-down */}
          {isActive('modulate') && (
            <Edge x1={935} y1={200} x2={520} y2={320} stroke={PT.accent} strokeWidth={1.5} dash="6 4"
              particle particleColor={PT.accent} particleDur="2s" particleR={4} curve={-30} />
          )}

          <Edge x1={730} y1={390} x2={830} y2={390} stroke={isActive('output') ? PT.accent : PT.inkMute} arrow
            particle={isCurrent('output')} particleColor={PT.accent} particleDur="1.4s" />

          {/* Output */}
          <rect x={840} y={340} width={200} height={100} rx={10}
            fill={isActive('output') ? PT.bgPanel : PT.bgRaised}
            stroke={isCurrent('output') ? PT.accent2 : (isActive('output') ? PT.accent2 : PT.rule)}
            strokeWidth={isCurrent('output') ? 3 : 1.5} />
          <text x={940} y={380} textAnchor="middle" fontFamily={PF.serif} fontSize={24} fill={PT.ink}>Output</text>
          <text x={940} y={410} textAnchor="middle" fontFamily={PF.sans} fontSize={16} fill={PT.inkDim}>shaped generation</text>

          {/* Reflection loop */}
          <g>
            <text x={1220} y={356} textAnchor="middle" fontFamily={PF.mono} fontSize={13} fill={PT.accent}
              style={{ letterSpacing: '0.16em', textTransform: 'uppercase' }}>reflection loop</text>
            <path d="M 1040 390 Q 1220 390 1220 320 Q 1220 240 1100 200" fill="none"
              stroke={PT.accent} strokeWidth={1.5} strokeDasharray="6 4" markerEnd="url(#arrowhead-accent)" />
            <text x={1300} y={398} fontFamily={PF.sans} fontSize={16} fill={PT.inkDim}>generate</text>
            <text x={1300} y={420} fontFamily={PF.sans} fontSize={16} fill={PT.inkDim}>→ reflect</text>
            <text x={1300} y={442} fontFamily={PF.sans} fontSize={16} fill={PT.inkDim}>→ recompile</text>
          </g>
        </g>

        {/* Cost callout */}
        <g transform="translate(1400, 20)">
          <rect x={0} y={0} width={260} height={470} rx={12} fill={PT.bgPanel} stroke={PT.rule} />
          <text x={130} y={42} textAnchor="middle" fontFamily={PF.mono} fontSize={14} fill={PT.inkMute}
            style={{ letterSpacing: '0.16em', textTransform: 'uppercase' }}>per-token cost</text>
          <text x={130} y={104} textAnchor="middle" fontFamily={PF.sans} fontSize={18} fill={PT.inkDim}>4 rank-r matmuls</text>
          <text x={130} y={132} textAnchor="middle" fontFamily={PF.sans} fontSize={18} fill={PT.inkDim}>per patched layer</text>
          <text x={130} y={160} textAnchor="middle" fontFamily={PF.mono} fontSize={14} fill={PT.inkMute}>(2 for Q · 2 for V)</text>
          <line x1={30} y1={196} x2={230} y2={196} stroke={PT.rule} />
          <text x={130} y={270} textAnchor="middle" fontFamily={PF.serif} fontSize={88} fill={PT.accent}>82%</text>
          <text x={130} y={300} textAnchor="middle" fontFamily={PF.sans} fontSize={18} fill={PT.accent}>token savings</text>
          <line x1={30} y1={336} x2={230} y2={336} stroke={PT.rule} />
          <text x={130} y={368} textAnchor="middle" fontFamily={PF.mono} fontSize={13} fill={PT.inkMute}
            style={{ letterSpacing: '0.14em', textTransform: 'uppercase' }}>three channels</text>
          <text x={130} y={396} textAnchor="middle" fontFamily={PF.mono} fontSize={16} fill={PT.accent}>M / E · 0 tokens</text>
          <text x={130} y={420} textAnchor="middle" fontFamily={PF.mono} fontSize={16} fill={PT.accent2}>slot · 40–80</text>
          <text x={130} y={444} textAnchor="middle" fontFamily={PF.mono} fontSize={16} fill={PT.accent3}>expand · 0–200</text>
        </g>
      </svg>

      {/* Stepper UI */}
      <div style={{
        position: 'absolute', left: PSP.paddingX, bottom: 90,
        display: 'flex', alignItems: 'center', gap: 16,
      }}>
        <div style={{
          fontFamily: PF.mono, fontSize: 14, color: PT.inkMute,
          letterSpacing: '0.14em', textTransform: 'uppercase',
        }}>step {step} / {STEPS.length - 1}</div>
        <button onClick={() => setStep((step + 1) % STEPS.length)} style={{
          background: PT.accent, color: PT.bg, border: 'none', borderRadius: 6,
          fontFamily: PF.mono, fontSize: 14, letterSpacing: '0.14em',
          padding: '10px 20px', cursor: 'pointer', textTransform: 'uppercase', fontWeight: 600,
        }}>advance ▸</button>
        <button onClick={() => setStep(0)} style={{
          background: 'transparent', color: PT.inkDim, border: `1px solid ${PT.rule}`,
          borderRadius: 6, fontFamily: PF.mono, fontSize: 14, letterSpacing: '0.14em',
          padding: '10px 20px', cursor: 'pointer', textTransform: 'uppercase',
        }}>reset</button>
        <div style={{
          fontFamily: PF.serif, fontSize: 22, color: PT.ink, fontStyle: 'italic',
          marginLeft: 24,
        }}>{['ready', 'reads Mind Tree', 'parallel forward pass', 'φ compiles', 'M / E tensors written', 'modulates primary host', 'shaped output'][step]}</div>
      </div>

      <Tooltip tip={tt.tip} />
      <Chrome index={index} total={total} chapter="architecture" />
    </Slide>
  );
}

// =============================================================
// Replacement Slide 09 — Q/V modulation (paper Fig 3) with hover hotspots
// =============================================================
function S09_QVMod_v2({ index, total }) {
  const tt = useTooltip();
  return (
    <Slide label="09 QV Modulation">
      <TitleBlock
        eyebrow="The mechanism · paper Fig. 3"
        title="Q-modulation, V-modulation."
        sub="Hover any term to see what it does."
      />

      <svg width="1700" height="560" style={{ position: 'absolute', left: PSP.paddingX, top: 320 }}>
        <Defs />

        {/* Q-mod panel */}
        <g>
          <rect x={20} y={20} width={1640} height={250} rx={12} fill={PT.bgPanel} stroke={PT.rule} />
          <text x={50} y={56} fontFamily={PF.mono} fontSize={14} fill={PT.accent}
            style={{ letterSpacing: '0.18em', textTransform: 'uppercase' }}>Q-modulation</text>
          <text x={220} y={56} fontFamily={PF.sans} fontStyle="italic" fontSize={20} fill={PT.inkDim}>attention steering — what to attend to</text>

          {/* x_ℓ */}
          <rect x={50} y={140} width={90} height={56} rx={6} fill={PT.bgRaised} stroke={PT.ink} strokeWidth={1.2} />
          <text x={95} y={174} textAnchor="middle" fontFamily={PF.mono} fontSize={22} fill={PT.ink}>x_ℓ</text>

          {/* split */}
          <line x1={140} y1={168} x2={200} y2={168} stroke={PT.inkDim} />
          <circle cx={200} cy={168} r={4} fill={PT.inkDim} />
          <line x1={200} y1={168} x2={200} y2={130} stroke={PT.inkDim} />
          <line x1={200} y1={168} x2={200} y2={222} stroke={PT.inkDim} />

          <line x1={200} y1={130} x2={240} y2={130} stroke={PT.accent} markerEnd="url(#arrowhead-accent)" />

          {/* M_A box */}
          <g onMouseEnter={tt.onEnter('M_A')} onMouseLeave={tt.onLeave} style={{ cursor: 'help' }}>
            <rect x={250} y={106} width={170} height={50} rx={6} fill="rgba(212,138,73,0.10)" stroke={PT.accent} strokeWidth={1.5} />
            <text x={335} y={132} textAnchor="middle" fontFamily={PF.mono} fontSize={20} fill={PT.accent} fontWeight={600}>x · M_A</text>
            <text x={335} y={150} textAnchor="middle" fontFamily={PF.mono} fontSize={11} fill={PT.inkDim}>d → r (2560 → 16)</text>
          </g>

          <line x1={420} y1={130} x2={460} y2={130} stroke={PT.accent} markerEnd="url(#arrowhead-accent)" />

          {/* M_B box */}
          <g onMouseEnter={tt.onEnter('M_B')} onMouseLeave={tt.onLeave} style={{ cursor: 'help' }}>
            <rect x={470} y={106} width={170} height={50} rx={6} fill="rgba(212,138,73,0.10)" stroke={PT.accent} strokeWidth={1.5} />
            <text x={555} y={132} textAnchor="middle" fontFamily={PF.mono} fontSize={20} fill={PT.accent} fontWeight={600}>· M_Bᵀ</text>
            <text x={555} y={150} textAnchor="middle" fontFamily={PF.mono} fontSize={11} fill={PT.inkDim}>r → d (16 → 2560)</text>
          </g>

          <line x1={640} y1={130} x2={680} y2={130} stroke={PT.accent} markerEnd="url(#arrowhead-accent)" />

          {/* s_M */}
          <g onMouseEnter={tt.onEnter('sM')} onMouseLeave={tt.onLeave} style={{ cursor: 'help' }}>
            <rect x={690} y={108} width={80} height={46} rx={6} fill={PT.bgRaised} stroke={PT.accent} />
            <text x={730} y={138} textAnchor="middle" fontFamily={PF.mono} fontSize={20} fill={PT.accent} fontWeight={600}>× s_M</text>
          </g>

          <line x1={770} y1={130} x2={830} y2={130} stroke={PT.accent} />
          <line x1={830} y1={130} x2={870} y2={158} stroke={PT.accent} />

          {/* identity bottom path */}
          <line x1={200} y1={222} x2={830} y2={222} stroke={PT.inkMute} strokeDasharray="3 3" />
          <line x1={830} y1={222} x2={870} y2={180} stroke={PT.inkMute} strokeDasharray="3 3" />
          <text x={500} y={240} textAnchor="middle" fontFamily={PF.sans} fontSize={14} fontStyle="italic" fill={PT.inkMute}>identity path (unmodified x_ℓ)</text>

          {/* Plus */}
          <circle cx={888} cy={170} r={20} fill={PT.bgRaised} stroke={PT.ink} strokeWidth={1.5} />
          <text x={888} y={178} textAnchor="middle" fontFamily={PF.serif} fontSize={28} fill={PT.ink}>+</text>

          <line x1={908} y1={170} x2={970} y2={170} stroke={PT.inkDim} markerEnd="url(#arrowhead)" />

          {/* W_Q */}
          <rect x={980} y={142} width={120} height={56} rx={6} fill={PT.bgRaised} stroke={PT.inkDim} />
          <text x={1040} y={170} textAnchor="middle" fontFamily={PF.mono} fontSize={20} fill={PT.ink}>W_Q</text>
          <text x={1040} y={188} textAnchor="middle" fontFamily={PF.sans} fontSize={11} fill={PT.inkMute}>frozen</text>

          <line x1={1100} y1={170} x2={1160} y2={170} stroke={PT.inkDim} markerEnd="url(#arrowhead)" />

          {/* Q' */}
          <rect x={1170} y={140} width={100} height={60} rx={6} fill="rgba(212,138,73,0.18)" stroke={PT.accent} strokeWidth={2} />
          <text x={1220} y={180} textAnchor="middle" fontFamily={PF.mono} fontSize={28} fill={PT.accent} fontWeight={700}>Q′</text>

          {/* Annotation */}
          <g transform="translate(1320, 60)">
            <rect x={0} y={0} width={310} height={170} rx={8} fill={PT.bgRaised} stroke={PT.rule} />
            <text x={20} y={36} fontFamily={PF.mono} fontSize={14} fill={PT.accent} fontWeight={700}
              style={{ letterSpacing: '0.14em', textTransform: 'uppercase' }}>Q′ steers attention</text>
            <text x={20} y={60} fontFamily={PF.sans} fontSize={16} fill={PT.inkDim}>what to attend to</text>
            <line x1={20} y1={80} x2={290} y2={80} stroke={PT.rule} />
            <text x={20} y={106} fontFamily={PF.mono} fontSize={14} fill={PT.accent2} fontWeight={700}
              style={{ letterSpacing: '0.14em', textTransform: 'uppercase' }}>V′ injects content</text>
            <text x={20} y={130} fontFamily={PF.sans} fontSize={16} fill={PT.inkDim}>what to extract</text>
            <line x1={20} y1={146} x2={290} y2={146} stroke={PT.rule} />
            <text x={20} y={166} fontFamily={PF.sans} fontSize={13} fontStyle="italic" fill={PT.inkMute}>host W_Q, W_V untouched</text>
          </g>
        </g>

        {/* V-mod panel */}
        <g>
          <rect x={20} y={290} width={1640} height={250} rx={12} fill={PT.bgPanel} stroke={PT.rule} />
          <text x={50} y={326} fontFamily={PF.mono} fontSize={14} fill={PT.accent2}
            style={{ letterSpacing: '0.18em', textTransform: 'uppercase' }}>V-modulation</text>
          <text x={220} y={326} fontFamily={PF.sans} fontStyle="italic" fontSize={20} fill={PT.inkDim}>content injection — what to extract</text>

          {/* V_ℓ */}
          <rect x={50} y={400} width={90} height={56} rx={6} fill={PT.bgRaised} stroke={PT.ink} strokeWidth={1.2} />
          <text x={95} y={434} textAnchor="middle" fontFamily={PF.mono} fontSize={22} fill={PT.ink}>V_ℓ</text>

          <line x1={140} y1={428} x2={680} y2={428} stroke={PT.inkDim} />

          {/* x_ℓ feed */}
          <text x={170} y={490} fontFamily={PF.mono} fontSize={16} fill={PT.inkMute}>x_ℓ</text>
          <line x1={205} y1={485} x2={250} y2={485} stroke={PT.inkMute} strokeWidth={1} markerEnd="url(#arrowhead)" />

          {/* E perturbation */}
          <g onMouseEnter={tt.onEnter('E_A')} onMouseLeave={tt.onLeave} style={{ cursor: 'help' }}>
            <rect x={260} y={462} width={290} height={50} rx={6} fill="rgba(74,144,184,0.10)" stroke={PT.accent2} strokeWidth={1.5} />
            <text x={405} y={488} textAnchor="middle" fontFamily={PF.mono} fontSize={22} fill={PT.accent2} fontWeight={600}>(x_ℓ · E_A) E_Bᵀ</text>
            <text x={405} y={506} textAnchor="middle" fontFamily={PF.mono} fontSize={11} fill={PT.inkDim}>rank-16 value perturbation</text>
          </g>

          <g onMouseEnter={tt.onEnter('sE')} onMouseLeave={tt.onLeave} style={{ cursor: 'help' }}>
            <rect x={570} y={464} width={80} height={46} rx={6} fill={PT.bgRaised} stroke={PT.accent2} />
            <text x={610} y={494} textAnchor="middle" fontFamily={PF.mono} fontSize={20} fill={PT.accent2} fontWeight={600}>× s_E</text>
          </g>

          <line x1={650} y1={487} x2={700} y2={487} stroke={PT.accent2} />
          <line x1={700} y1={487} x2={730} y2={444} stroke={PT.accent2} markerEnd="url(#arrowhead-accent2)" />

          {/* Plus */}
          <circle cx={748} cy={428} r={20} fill={PT.bgRaised} stroke={PT.ink} strokeWidth={1.5} />
          <text x={748} y={436} textAnchor="middle" fontFamily={PF.serif} fontSize={28} fill={PT.ink}>+</text>

          <line x1={768} y1={428} x2={830} y2={428} stroke={PT.inkDim} markerEnd="url(#arrowhead)" />

          {/* V' */}
          <rect x={840} y={398} width={100} height={60} rx={6} fill="rgba(74,144,184,0.18)" stroke={PT.accent2} strokeWidth={2} />
          <text x={890} y={438} textAnchor="middle" fontFamily={PF.mono} fontSize={28} fill={PT.accent2} fontWeight={700}>V′</text>

          {/* equation */}
          <rect x={1000} y={398} width={620} height={60} rx={6} fill={PT.bgRaised} stroke={PT.rule} />
          <text x={1310} y={428} textAnchor="middle" fontFamily={PF.mono} fontSize={18} fill={PT.accent}>x′_ℓ = x_ℓ + s_M · (x_ℓ M_A) M_Bᵀ</text>
          <text x={1310} y={450} textAnchor="middle" fontFamily={PF.mono} fontSize={18} fill={PT.accent2}>V′_ℓ = V_ℓ + s_E · (x_ℓ E_A) E_Bᵀ</text>
        </g>
      </svg>

      <Tooltip tip={tt.tip} />
      <Chrome index={index} total={total} chapter="mechanism" />
    </Slide>
  );
}

Object.assign(window, { S05_Enmeshed_v2, S08_System_v2, S09_QVMod_v2 });
