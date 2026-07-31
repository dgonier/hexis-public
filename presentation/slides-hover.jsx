// Hover-triggered animations replacing tooltip-only versions.
// Each slide: a "focus" state lights/moves elements based on what's hovered.
const HT = window.HEXIS_TOKENS;
const HSP = window.SPACING;
const HF = window.FONTS;

// ============================================================
// 05 — Architecture comparison · hover (d) reveals parallel column
// ============================================================
function S05_HoverReveal({ index, total }) {
  const [hover, setHover] = React.useState(null);
  const cols = [
    { tag: '(a)', name: 'Context-level', sub: 'RAG · Reflexion · MemGPT', line: '#7c5d3a',
      facts: ['Memory in context', 'Competes for attention', 'Dilutes with length'], complexity: 'O(T·N·d)' },
    { tag: '(b)', name: 'Parameter-level', sub: 'LoRA · Adapters', line: HT.accent3,
      facts: ['Weights modified', '∇ per adaptation', 'Fixed after training'], complexity: 'O(∇)' },
    { tag: '(c)', name: 'Activation-level', sub: 'RepEng · ActAdd', line: '#5d9b78',
      facts: ['Fixed direction', 'Same ∀ experience', 'Non-adaptive'], complexity: 'O(L·d)' },
    { tag: '(d)', name: 'Enmeshed (HEXIS)', sub: 'this work', line: HT.accent,
      facts: ['Parallel channel', 'Adapts at inference', 'Dilution-immune'], complexity: 'O(L·d·r)', highlight: true },
  ];

  const dimmed = (i) => hover !== null && hover !== i;

  return (
    <Slide label="05 Enmeshed">
      <TitleBlock
        eyebrow="The new primitive · paper Fig. 1"
        title="Where does the new information fuse?"
        sub="Hover (d) — watch the host stack split open and the parallel channel slide in."
      />

      <div style={{
        position: 'absolute', left: HSP.paddingX, right: HSP.paddingX, top: 360,
        display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 24,
      }}>
        {cols.map((c, i) => {
          const focused = hover === i;
          return (
            <div key={i}
              onMouseEnter={() => setHover(i)}
              onMouseLeave={() => setHover(null)}
              style={{
                border: `1px solid ${focused ? c.line : (c.highlight ? c.line : HT.rule)}`,
                borderRadius: 12, padding: '24px 24px 28px',
                background: focused ? `${c.line}11` : (c.highlight ? 'rgba(212,138,73,0.06)' : HT.bgPanel),
                minHeight: 560, position: 'relative', cursor: 'pointer',
                opacity: dimmed(i) ? 0.35 : 1,
                transform: focused ? 'translateY(-6px)' : 'translateY(0)',
                transition: 'all 380ms cubic-bezier(.2,.7,.3,1)',
                boxShadow: focused ? `0 24px 60px ${c.line}44` : 'none',
              }}>
              <div style={{ fontFamily: HF.mono, fontSize: 14, color: c.line,
                letterSpacing: '0.14em', textTransform: 'uppercase', marginBottom: 8 }}>
                {c.tag} {c.sub}
              </div>
              <div style={{ fontFamily: HF.serif, fontSize: 32, color: HT.ink,
                lineHeight: 1.05, marginBottom: 24 }}>
                {c.name}
              </div>

              {/* Diagram — animates per panel */}
              <svg width="100%" height="220" viewBox="0 0 240 220">
                {i === 0 && <PanelA c={c} focused={focused} />}
                {i === 1 && <PanelB c={c} focused={focused} />}
                {i === 2 && <PanelC c={c} focused={focused} />}
                {i === 3 && <PanelD c={c} focused={focused} />}
              </svg>

              <div style={{ marginTop: 12 }}>
                {c.facts.map((f, j) => (
                  <div key={j} style={{ fontFamily: HF.sans, fontSize: 17,
                    color: focused ? HT.ink : HT.inkDim, marginBottom: 4 }}>
                    {c.highlight ? '✓' : '✗'} {f}
                  </div>
                ))}
              </div>
              <div style={{ marginTop: 12, fontFamily: HF.mono, fontSize: 13,
                color: c.line, letterSpacing: '0.08em' }}>
                {c.complexity}
              </div>

              {c.highlight && (
                <div style={{ position: 'absolute', top: -1, right: -1,
                  background: c.line, color: HT.bg,
                  fontFamily: HF.mono, fontSize: 11, letterSpacing: '0.12em',
                  padding: '5px 10px', borderRadius: '0 12px 0 12px',
                  textTransform: 'uppercase', fontWeight: 700,
                }}>this paper</div>
              )}
            </div>
          );
        })}
      </div>

      <Chrome index={index} total={total} chapter="enmeshed networks" />
    </Slide>
  );
}

function PanelA({ c, focused }) {
  // RAG: memory chip flows into context window
  return (
    <g>
      {/* host */}
      {[0,1,2,3].map(j => (
        <rect key={j} x={130} y={20 + j*38} width={80} height={30} rx={3}
          fill={HT.bgRaised} stroke={HT.rule} strokeWidth={1} />
      ))}
      {/* memory chip */}
      <rect x={focused ? 60 : 20} y={focused ? 20 : 100}
        width={60} height={30} rx={3}
        fill={`${c.line}33`} stroke={c.line} strokeWidth={1.5}
        style={{ transition: 'all 600ms cubic-bezier(.2,.7,.3,1)' }}>
      </rect>
      <text x={focused ? 90 : 50} y={focused ? 39 : 119} textAnchor="middle"
        fontFamily={HF.mono} fontSize={11} fill={c.line}
        style={{ transition: 'all 600ms cubic-bezier(.2,.7,.3,1)' }}>memory</text>
      {focused && (
        <line x1={120} y1={35} x2={130} y2={35} stroke={c.line} strokeWidth={1.5} markerEnd="url(#arrowhead-accent2)" />
      )}
      <text x={120} y={200} textAnchor="middle" fontFamily={HF.sans} fontSize={11} fill={HT.inkMute} fontStyle="italic">
        memory becomes input tokens
      </text>
    </g>
  );
}

function PanelB({ c, focused }) {
  // LoRA: ΔW chips fade into weights when focused
  return (
    <g>
      {[0,1,2,3].map(j => (
        <g key={j}>
          <rect x={70} y={20 + j*38} width={100} height={30} rx={3}
            fill={focused ? `${c.line}22` : HT.bgRaised} stroke={c.line}
            strokeWidth={1.2} style={{ transition: 'fill 500ms' }} />
          {/* ΔW chips slide in */}
          <rect x={focused ? 130 : 200} y={24 + j*38}
            width={32} height={22} rx={3}
            fill={`${c.line}55`} stroke={c.line} strokeWidth={0.8}
            opacity={focused ? 1 : 0.4}
            style={{ transition: 'all 500ms cubic-bezier(.2,.7,.3,1)', transitionDelay: `${j*60}ms` }} />
          <text x={focused ? 146 : 216} y={40 + j*38} textAnchor="middle"
            fontFamily={HF.mono} fontSize={9} fill={c.line}
            style={{ transition: 'all 500ms', transitionDelay: `${j*60}ms` }}>ΔW</text>
        </g>
      ))}
      <text x={120} y={200} textAnchor="middle" fontFamily={HF.sans} fontSize={11} fill={HT.inkMute} fontStyle="italic">
        weights changed permanently
      </text>
    </g>
  );
}

function PanelC({ c, focused }) {
  // ActAdd: fixed direction stays fixed (intentionally rigid)
  return (
    <g>
      {[0,1,2,3].map(j => (
        <rect key={j} x={70} y={20 + j*38} width={80} height={30} rx={3}
          fill={HT.bgRaised} stroke={c.line} strokeWidth={1} />
      ))}
      <rect x={170} y={focused ? 50 : 56} width={36} height={70} rx={3}
        fill={`${c.line}33`} stroke={c.line} strokeWidth={1.5}
        style={{ transition: 'all 500ms' }} />
      <text x={188} y={focused ? 92 : 95} textAnchor="middle"
        fontFamily={HF.mono} fontSize={14} fill={c.line} fontWeight={700}
        style={{ transition: 'all 500ms' }}>d*</text>
      {[1,2].map(j => (
        <line key={j} x1={170} y1={35 + j*38} x2={155} y2={35 + j*38}
          stroke={c.line} strokeWidth={1.2} markerEnd="url(#arrowhead-accent2)">
          {focused && <animate attributeName="opacity" values="0.3;1;0.3" dur="1.4s" repeatCount="indefinite" begin={`${j*0.2}s`} />}
        </line>
      ))}
      <text x={120} y={200} textAnchor="middle" fontFamily={HF.sans} fontSize={11} fill={HT.inkMute} fontStyle="italic">
        same direction every input
      </text>
    </g>
  );
}

function PanelD({ c, focused }) {
  // The big reveal: host stack splits, parallel column slides in
  // When focused: hostX shifts right, parallel column appears at left
  const hostX = focused ? 150 : 90;
  const parallelX = focused ? 30 : 90;
  const parallelOp = focused ? 1 : 0;
  const bridgeOp = focused ? 1 : 0;

  return (
    <g>
      {/* host stack */}
      {[0,1,2,3].map(j => (
        <rect key={j} x={hostX} y={20 + j*38} width={70} height={30} rx={3}
          fill={HT.bgRaised} stroke={c.line} strokeWidth={1.2}
          style={{ transition: 'x 500ms cubic-bezier(.2,.7,.3,1)', transitionDelay: `${j*40}ms` }} />
      ))}
      {/* parallel column */}
      {[0,1,2,3].map(j => (
        <g key={j} style={{ transition: 'all 500ms', transitionDelay: `${j*60 + 200}ms`, opacity: parallelOp }}>
          <rect x={parallelX} y={20 + j*38} width={60} height={30} rx={3}
            fill={`${c.line}22`} stroke={c.line} strokeWidth={1.2} strokeDasharray="3 2"
            style={{ transition: 'x 500ms cubic-bezier(.2,.7,.3,1)' }} />
          <text x={parallelX + 30} y={39 + j*38} textAnchor="middle"
            fontFamily={HF.mono} fontSize={10} fill={c.line} fontWeight={600}>
            M_{j}
          </text>
        </g>
      ))}
      {/* bridges (B circles) */}
      {focused && [0,1,2,3].map(j => (
        <g key={j} style={{ opacity: bridgeOp, transition: `opacity 400ms ${j*80 + 400}ms` }}>
          <line x1={parallelX + 60} y1={35 + j*38} x2={hostX} y2={35 + j*38}
            stroke={c.line} strokeWidth={1} />
          <circle cx={(parallelX + 60 + hostX)/2} cy={35 + j*38} r={6}
            fill={HT.bg} stroke={c.line} strokeWidth={1.5}>
            <animate attributeName="r" values="5;8;5" dur="1.6s" repeatCount="indefinite" begin={`${j*0.15}s`} />
          </circle>
          <text x={(parallelX + 60 + hostX)/2} y={38 + j*38} textAnchor="middle"
            fontFamily={HF.mono} fontSize={8} fill={c.line} fontWeight={700}>B</text>
        </g>
      ))}
      <text x={120} y={200} textAnchor="middle" fontFamily={HF.sans} fontSize={11}
        fill={focused ? c.line : HT.inkMute} fontStyle="italic"
        style={{ transition: 'fill 400ms' }}>
        {focused ? 'parallel pass · same frozen weights' : 'hover to reveal →'}
      </text>
    </g>
  );
}

// ============================================================
// 07 — Mind Tree · hover by conviction lights up siblings
// ============================================================
function S07_HoverPool({ index, total }) {
  const [hover, setHover] = React.useState(null); // 'strong' | 'moderate' | 'agnostic' | 'novel' | null
  const beliefs = [
    { x: 740, y: 130, lab: 'b1', conv: 'strong',    novel: false },
    { x: 740, y: 200, lab: 'b2', conv: 'strong',    novel: false },
    { x: 740, y: 270, lab: 'b3', conv: 'moderate',  novel: false },
    { x: 740, y: 340, lab: 'b4', conv: 'moderate',  novel: true  },
    { x: 740, y: 410, lab: 'b5', conv: 'agnostic',  novel: false },
  ];
  const matches = (b) =>
    hover === null ? false :
    hover === 'novel' ? b.novel :
    b.conv === hover;
  const colorFor = (conv) =>
    conv === 'strong' ? HT.accent :
    conv === 'moderate' ? HT.accent2 :
    HT.inkMute;

  return (
    <Slide label="07 Mind Tree">
      <TitleBlock
        eyebrow="Structured private subcontext"
        title="The Mind Tree."
        sub="Hover a tag on the right — every belief that matches lights up, and a flow traces from those nodes through φ to the modulation tensor."
      />

      <svg width="1700" height="540" style={{ position: 'absolute', left: HSP.paddingX, bottom: 90 }}>
        <Defs />
        {/* Root */}
        <Node x={140} y={270} r={28} fill={HT.bgRaised} stroke={HT.accent}
          label="self" labelPos="left" fontSize={20} color={HT.ink} halo haloColor={HT.accent} />
        {/* Sections */}
        {[
          { x: 380, y: 80, label: 'identity' },
          { x: 380, y: 180, label: 'beliefs' },
          { x: 380, y: 280, label: 'strategies' },
          { x: 380, y: 380, label: 'memories' },
          { x: 380, y: 480, label: 'models' },
        ].map((s, i) => (
          <g key={i}>
            <Edge x1={168} y1={270} x2={350} y2={s.y}
              stroke={HT.rule} strokeWidth={1} curve={5} />
            <Node x={380} y={s.y} r={20} fill={HT.bgRaised}
              stroke={i === 1 ? HT.accent2 : HT.rule}
              label={s.label} labelPos="right" fontSize={18} color={HT.ink} />
          </g>
        ))}

        {/* Beliefs */}
        {beliefs.map((b, i) => {
          const lit = matches(b);
          const c = colorFor(b.conv);
          return (
            <g key={i}>
              <line x1={400} y1={180} x2={720} y2={b.y}
                stroke={lit ? c : HT.rule} strokeWidth={lit ? 2 : 1}
                style={{ transition: 'all 350ms' }} />
              <circle cx={b.x} cy={b.y} r={lit ? 22 : 14}
                fill={HT.bgRaised} stroke={c} strokeWidth={lit ? 2.5 : 1.5}
                opacity={hover && !lit ? 0.25 : 1}
                style={{ transition: 'all 350ms' }}>
                {lit && <animate attributeName="r" values="20;26;20" dur="1.4s" repeatCount="indefinite" />}
              </circle>
              {lit && (
                <circle cx={b.x} cy={b.y} r={28} fill="none" stroke={c} strokeWidth={1} opacity={0.5}>
                  <animate attributeName="r" values="18;40;18" dur="1.6s" repeatCount="indefinite" />
                  <animate attributeName="opacity" values="0.6;0;0.6" dur="1.6s" repeatCount="indefinite" />
                </circle>
              )}
              <text x={b.x + 30} y={b.y + 5}
                fontFamily={HF.sans} fontSize={16}
                fill={lit ? HT.ink : (hover ? HT.inkDim : HT.inkDim)}
                opacity={hover && !lit ? 0.3 : 1}
                style={{ transition: 'all 350ms' }}>
                {b.lab} · {b.conv}{b.novel ? ' · novel' : ''}
              </text>
              {/* Flow particle from belief to phi */}
              {lit && (
                <Edge x1={b.x + 30} y1={b.y} x2={1240} y2={270}
                  stroke="none" particle particleColor={c}
                  particleDur="1.6s" particleDelay={i * 0.12} particleR={4} curve={-50} />
              )}
            </g>
          );
        })}

        {/* φ on the right */}
        <g>
          <circle cx={1240} cy={270} r={hover ? 56 : 46}
            fill={hover ? 'rgba(212,138,73,0.14)' : HT.bgRaised}
            stroke={HT.accent} strokeWidth={hover ? 2.5 : 1.5}
            style={{ transition: 'all 380ms' }}>
            {hover && <animate attributeName="stroke-width" values="2;4;2" dur="1.4s" repeatCount="indefinite" />}
          </circle>
          <text x={1240} y={284} textAnchor="middle"
            fontFamily={HF.mono} fontSize={48} fill={HT.accent} fontWeight={700}>φ</text>
        </g>

        {/* Modulation tensor */}
        <g>
          {[0,1,2,3].map(j => (
            <rect key={j} x={1380 + j*32} y={230} width={24} height={80} rx={3}
              fill={hover ? 'rgba(212,138,73,0.30)' : HT.bgRaised}
              stroke={HT.accent} strokeWidth={hover ? 1.8 : 1}
              style={{ transition: 'all 400ms' }}>
              {hover && <animate attributeName="opacity" values="0.5;1;0.5" dur="1.2s" repeatCount="indefinite" begin={`${j*0.2}s`} />}
            </rect>
          ))}
          <text x={1444} y={340} textAnchor="middle"
            fontFamily={HF.mono} fontSize={14} fill={HT.inkMute}
            style={{ letterSpacing: '0.06em' }}>M_A · M_B · E_A · E_B</text>
          {hover && (
            <Edge x1={1296} y1={270} x2={1380} y2={270}
              stroke="none" particle particleColor={HT.accent}
              particleDur="1.2s" particleR={4} />
          )}
        </g>
      </svg>

      {/* Hover tag panel */}
      <div style={{
        position: 'absolute', right: HSP.paddingX, top: 360,
        display: 'flex', flexDirection: 'column', gap: 14, width: 360,
      }}>
        <div style={{ fontFamily: HF.mono, fontSize: 14, color: HT.accent,
          letterSpacing: '0.18em', textTransform: 'uppercase', marginBottom: 6 }}>
          hover to pool
        </div>
        {[
          { k: 'strong',    label: 'strong conviction',    desc: 'highest weight in φ', color: HT.accent },
          { k: 'moderate',  label: 'moderate conviction',  desc: 'medium weight',       color: HT.accent2 },
          { k: 'agnostic',  label: 'agnostic',             desc: 'low weight',          color: HT.inkMute },
          { k: 'novel',     label: 'novel · curated slot', desc: 'routes to slot, not M', color: HT.accent3 },
        ].map(t => (
          <div key={t.k}
            onMouseEnter={() => setHover(t.k)}
            onMouseLeave={() => setHover(null)}
            style={{
              border: `1.5px solid ${hover === t.k ? t.color : HT.rule}`,
              background: hover === t.k ? `${t.color}18` : HT.bgPanel,
              borderRadius: 10, padding: '14px 18px', cursor: 'pointer',
              transition: 'all 250ms',
            }}>
            <div style={{ fontFamily: HF.serif, fontSize: 22, color: HT.ink, marginBottom: 4 }}>
              {t.label}
            </div>
            <div style={{ fontFamily: HF.sans, fontSize: 14, color: HT.inkDim }}>
              {t.desc}
            </div>
          </div>
        ))}
      </div>

      <Chrome index={index} total={total} chapter="mind tree" />
    </Slide>
  );
}

// ============================================================
// 09 — Q/V modulation · hover M_A/M_B animates data-flow chips
// ============================================================
function S09_HoverFlow({ index, total }) {
  const [hover, setHover] = React.useState(null); // 'M_A' | 'M_B' | 'sM' | 'E_A' | null
  const isHovered = (k) => hover === k;
  const dim = (k) => hover && hover !== k;

  return (
    <Slide label="09 QV Modulation">
      <TitleBlock
        eyebrow="The mechanism · paper Fig. 3"
        title="Q-modulation, V-modulation."
        sub="Hover M_A — watch x_ℓ split into 16 chips squeezed through the bottleneck. Hover M_B — they expand back to model dimension."
      />

      <svg width="1700" height="560" style={{ position: 'absolute', left: HSP.paddingX, top: 320 }}>
        <Defs />

        {/* Q-modulation panel */}
        <g>
          <rect x={20} y={20} width={1640} height={250} rx={12} fill={HT.bgPanel} stroke={HT.rule} />
          <text x={50} y={56} fontFamily={HF.mono} fontSize={14} fill={HT.accent}
            style={{ letterSpacing: '0.18em', textTransform: 'uppercase' }}>Q-modulation</text>

          {/* x_ℓ source */}
          <rect x={50} y={140} width={90} height={56} rx={6}
            fill={HT.bgRaised} stroke={HT.ink} strokeWidth={1.2} />
          <text x={95} y={174} textAnchor="middle" fontFamily={HF.mono} fontSize={22} fill={HT.ink}>x_ℓ</text>

          {/* Wide chips approaching M_A — 16 narrow chips when hovered */}
          {Array.from({ length: 8 }).map((_, j) => {
            const hov = isHovered('M_A');
            return (
              <rect key={j}
                x={hov ? 160 + j*8 : 142}
                y={hov ? 152 : 152}
                width={hov ? 6 : 14}
                height={hov ? 32 : 32}
                rx={2}
                fill={hov ? HT.accent : HT.inkDim}
                opacity={hov ? 1 : (dim('M_A') ? 0.2 : 0.6)}
                style={{ transition: 'all 500ms cubic-bezier(.2,.7,.3,1)', transitionDelay: `${j*30}ms` }} />
            );
          })}

          {/* M_A box */}
          <g onMouseEnter={() => setHover('M_A')} onMouseLeave={() => setHover(null)} style={{ cursor: 'pointer' }}>
            <rect x={250} y={106} width={170} height={92} rx={6}
              fill={isHovered('M_A') ? 'rgba(212,138,73,0.20)' : 'rgba(212,138,73,0.06)'}
              stroke={HT.accent} strokeWidth={isHovered('M_A') ? 2.5 : 1.5}
              opacity={dim('M_A') ? 0.4 : 1}
              style={{ transition: 'all 350ms' }} />
            <text x={335} y={144} textAnchor="middle" fontFamily={HF.mono} fontSize={20} fill={HT.accent} fontWeight={700}>M_A</text>
            <text x={335} y={166} textAnchor="middle" fontFamily={HF.mono} fontSize={12} fill={HT.inkDim}>d → r (2560 → 16)</text>
            <text x={335} y={186} textAnchor="middle" fontFamily={HF.sans} fontSize={11} fill={HT.inkMute} fontStyle="italic">down-projection</text>
          </g>

          {/* Bottleneck chips between M_A and M_B */}
          {Array.from({ length: 16 }).map((_, j) => {
            const hov = isHovered('M_A') || isHovered('M_B');
            return (
              <rect key={j}
                x={425 + (j % 4) * 8}
                y={130 + Math.floor(j/4) * 12}
                width={6} height={8} rx={1}
                fill={hov ? HT.accent : HT.inkDim}
                opacity={hov ? 1 : 0.3}
                style={{ transition: 'opacity 300ms', transitionDelay: `${j*15}ms` }}>
                {hov && <animate attributeName="opacity" values="0.5;1;0.5" dur="1s" repeatCount="indefinite" begin={`${j*0.04}s`} />}
              </rect>
            );
          })}
          <text x={460} y={210} textAnchor="middle" fontFamily={HF.mono} fontSize={11}
            fill={(isHovered('M_A') || isHovered('M_B')) ? HT.accent : HT.inkMute}
            style={{ transition: 'fill 300ms' }}>r=16 bottleneck</text>

          {/* M_B box */}
          <g onMouseEnter={() => setHover('M_B')} onMouseLeave={() => setHover(null)} style={{ cursor: 'pointer' }}>
            <rect x={500} y={106} width={170} height={92} rx={6}
              fill={isHovered('M_B') ? 'rgba(212,138,73,0.20)' : 'rgba(212,138,73,0.06)'}
              stroke={HT.accent} strokeWidth={isHovered('M_B') ? 2.5 : 1.5}
              opacity={dim('M_B') ? 0.4 : 1}
              style={{ transition: 'all 350ms' }} />
            <text x={585} y={144} textAnchor="middle" fontFamily={HF.mono} fontSize={20} fill={HT.accent} fontWeight={700}>M_Bᵀ</text>
            <text x={585} y={166} textAnchor="middle" fontFamily={HF.mono} fontSize={12} fill={HT.inkDim}>r → d (16 → 2560)</text>
            <text x={585} y={186} textAnchor="middle" fontFamily={HF.sans} fontSize={11} fill={HT.inkMute} fontStyle="italic">up-projection</text>
          </g>

          {/* Wide chips after M_B */}
          {Array.from({ length: 8 }).map((_, j) => {
            const hov = isHovered('M_B');
            return (
              <rect key={j}
                x={hov ? 680 + j*9 : 690}
                y={152}
                width={hov ? 7 : 14} height={32} rx={2}
                fill={hov ? HT.accent : HT.inkDim}
                opacity={hov ? 1 : (dim('M_B') ? 0.2 : 0.6)}
                style={{ transition: 'all 500ms cubic-bezier(.2,.7,.3,1)', transitionDelay: `${j*30 + 200}ms` }} />
            );
          })}

          {/* × s_M */}
          <g onMouseEnter={() => setHover('sM')} onMouseLeave={() => setHover(null)} style={{ cursor: 'pointer' }}>
            <rect x={770} y={140} width={70} height={56} rx={6}
              fill={isHovered('sM') ? 'rgba(212,138,73,0.20)' : HT.bgRaised}
              stroke={HT.accent} strokeWidth={isHovered('sM') ? 2.5 : 1.2}
              opacity={dim('sM') ? 0.4 : 1}
              style={{ transition: 'all 300ms' }} />
            <text x={805} y={174} textAnchor="middle" fontFamily={HF.mono} fontSize={20} fill={HT.accent} fontWeight={700}>× s_M</text>
          </g>

          {/* + */}
          <circle cx={870} cy={168} r={20} fill={HT.bgRaised} stroke={HT.ink} strokeWidth={1.5} />
          <text x={870} y={176} textAnchor="middle" fontFamily={HF.serif} fontSize={28} fill={HT.ink}>+</text>

          {/* identity skip */}
          <line x1={140} y1={222} x2={870} y2={222} stroke={HT.inkMute} strokeDasharray="3 3" />
          <line x1={870} y1={222} x2={870} y2={188} stroke={HT.inkMute} strokeDasharray="3 3" />
          <text x={500} y={240} textAnchor="middle" fontFamily={HF.sans} fontSize={13} fontStyle="italic" fill={HT.inkMute}>
            identity path (unmodified x_ℓ)
          </text>

          <line x1={890} y1={168} x2={950} y2={168} stroke={HT.inkDim} markerEnd="url(#arrowhead)" />
          <rect x={960} y={140} width={120} height={56} rx={6} fill={HT.bgRaised} stroke={HT.inkDim} />
          <text x={1020} y={168} textAnchor="middle" fontFamily={HF.mono} fontSize={20} fill={HT.ink}>W_Q</text>
          <text x={1020} y={186} textAnchor="middle" fontFamily={HF.sans} fontSize={11} fill={HT.inkMute}>frozen</text>
          <line x1={1080} y1={168} x2={1140} y2={168} stroke={HT.inkDim} markerEnd="url(#arrowhead)" />
          <rect x={1150} y={138} width={100} height={60} rx={6}
            fill="rgba(212,138,73,0.18)" stroke={HT.accent} strokeWidth={2} />
          <text x={1200} y={178} textAnchor="middle" fontFamily={HF.mono} fontSize={28} fill={HT.accent} fontWeight={700}>Q′</text>

          {/* explainer panel */}
          <g transform="translate(1300, 60)">
            <rect x={0} y={0} width={330} height={180} rx={8} fill={HT.bgRaised} stroke={HT.rule} />
            {hover === 'M_A' && (
              <>
                <text x={20} y={40} fontFamily={HF.mono} fontSize={13} fill={HT.accent} fontWeight={700}
                  style={{ letterSpacing: '0.14em', textTransform: 'uppercase' }}>M_A · down-project</text>
                <text x={20} y={72} fontFamily={HF.sans} fontSize={16} fill={HT.ink}>Compresses x_ℓ from 2560-d</text>
                <text x={20} y={94} fontFamily={HF.sans} fontSize={16} fill={HT.ink}>to a 16-d bottleneck.</text>
                <text x={20} y={130} fontFamily={HF.sans} fontSize={14} fill={HT.inkDim} fontStyle="italic">160× compression — only the</text>
                <text x={20} y={150} fontFamily={HF.sans} fontSize={14} fill={HT.inkDim} fontStyle="italic">most stance-relevant directions survive.</text>
              </>
            )}
            {hover === 'M_B' && (
              <>
                <text x={20} y={40} fontFamily={HF.mono} fontSize={13} fill={HT.accent} fontWeight={700}
                  style={{ letterSpacing: '0.14em', textTransform: 'uppercase' }}>M_Bᵀ · up-project</text>
                <text x={20} y={72} fontFamily={HF.sans} fontSize={16} fill={HT.ink}>Lifts the 16-d signal back to</text>
                <text x={20} y={94} fontFamily={HF.sans} fontSize={16} fill={HT.ink}>full model dimension.</text>
                <text x={20} y={130} fontFamily={HF.sans} fontSize={14} fill={HT.inkDim} fontStyle="italic">The pair (M_A, M_B) is the</text>
                <text x={20} y={150} fontFamily={HF.sans} fontSize={14} fill={HT.inkDim} fontStyle="italic">low-rank perturbation to x_ℓ.</text>
              </>
            )}
            {hover === 'sM' && (
              <>
                <text x={20} y={40} fontFamily={HF.mono} fontSize={13} fill={HT.accent} fontWeight={700}
                  style={{ letterSpacing: '0.14em', textTransform: 'uppercase' }}>s_M · strength</text>
                <text x={20} y={72} fontFamily={HF.sans} fontSize={16} fill={HT.ink}>Per-layer scalar.</text>
                <text x={20} y={94} fontFamily={HF.sans} fontSize={16} fill={HT.ink}>Stride-3: every third layer.</text>
                <text x={20} y={130} fontFamily={HF.sans} fontSize={14} fill={HT.inkDim} fontStyle="italic">Tunes how much the modulation</text>
                <text x={20} y={150} fontFamily={HF.sans} fontSize={14} fill={HT.inkDim} fontStyle="italic">influences the host computation.</text>
              </>
            )}
            {!hover && (
              <>
                <text x={20} y={40} fontFamily={HF.mono} fontSize={13} fill={HT.inkMute}
                  style={{ letterSpacing: '0.14em', textTransform: 'uppercase' }}>hover any term</text>
                <text x={20} y={72} fontFamily={HF.sans} fontSize={16} fill={HT.inkDim}>Each animates the data-flow:</text>
                <text x={20} y={100} fontFamily={HF.sans} fontSize={14} fill={HT.inkDim}>· M_A: 8-chip → 16 narrow chips</text>
                <text x={20} y={120} fontFamily={HF.sans} fontSize={14} fill={HT.inkDim}>· M_B: 16 chips expand back</text>
                <text x={20} y={140} fontFamily={HF.sans} fontSize={14} fill={HT.inkDim}>· s_M: scales the perturbation</text>
              </>
            )}
          </g>
        </g>

        {/* Equation strip */}
        <g>
          <rect x={20} y={300} width={1640} height={240} rx={12} fill={HT.bgPanel} stroke={HT.rule} />
          <text x={50} y={336} fontFamily={HF.mono} fontSize={14} fill={HT.accent2}
            style={{ letterSpacing: '0.18em', textTransform: 'uppercase' }}>V-modulation · same shape, different role</text>

          <text x={840} y={400} textAnchor="middle" fontFamily={HF.mono} fontSize={26} fill={HT.accent}>
            x′_ℓ = x_ℓ + s_M · (x_ℓ M_A) M_Bᵀ
          </text>
          <text x={840} y={448} textAnchor="middle" fontFamily={HF.mono} fontSize={26} fill={HT.accent2}>
            V′_ℓ = V_ℓ + s_E · (x_ℓ E_A) E_Bᵀ
          </text>
          <text x={840} y={500} textAnchor="middle" fontFamily={HF.sans} fontSize={18} fill={HT.inkDim} fontStyle="italic">
            Q steers what to attend to · V steers what to extract
          </text>
        </g>
      </svg>

      <Chrome index={index} total={total} chapter="mechanism" />
    </Slide>
  );
}

Object.assign(window, { S05_HoverReveal, S07_HoverPool, S09_HoverFlow });
