// Slides 5-8: Enmeshed Network primitive, design space, Mind Tree, system overview
const T2 = window.HEXIS_TOKENS;
const TS2 = window.TYPE_SCALE;
const SP2 = window.SPACING;
const F2 = window.FONTS;

// ============================================================
// 05 — The Enmeshed Network — centerpiece animation
// ============================================================
function S05_Enmeshed({ index, total }) {
  // Two parallel host columns sharing layers, with bridges fusing
  // hidden states from the parallel pass into modulations on the primary pass.
  return (
    <Slide label="05 Enmeshed">
      <TitleBlock
        eyebrow="The new primitive"
        title="An enmeshed network."
        sub="A lightweight module shares the forward pass of a frozen host. It reads hidden states at each layer and writes modulations back into the same computation — without occupying primary-context positions."
      />

      <svg width="1700" height="540" style={{ position: 'absolute', left: SP2.paddingX, bottom: 90 }}>
        <Defs />

        {/* Parallel context (left) */}
        <g>
          <text x={140} y={50} textAnchor="middle"
            fontFamily={F2.mono} fontSize={16} fill={T2.accent}
            style={{ letterSpacing: '0.18em', textTransform: 'uppercase' }}>
            parallel context
          </text>
          <text x={140} y={75} textAnchor="middle"
            fontFamily={F2.sans} fontSize={20} fill={T2.inkDim} fontStyle="italic">
            Mind Tree (private)
          </text>
          <HostColumn x={50} y={110} layers={8} layerW={180} layerH={36} gap={10}
            patched={[]}
            label=""
            patchedColor={T2.accent} />
        </g>

        {/* Primary context (right) */}
        <g>
          <text x={950} y={50} textAnchor="middle"
            fontFamily={F2.mono} fontSize={16} fill={T2.accent2}
            style={{ letterSpacing: '0.18em', textTransform: 'uppercase' }}>
            primary context
          </text>
          <text x={950} y={75} textAnchor="middle"
            fontFamily={F2.sans} fontSize={20} fill={T2.inkDim} fontStyle="italic">
            user query / conversation
          </text>
          <HostColumn x={860} y={110} layers={8} layerW={180} layerH={36} gap={10}
            patched={[1, 4, 7]}
            label=""
            patchedColor={T2.accent} />
        </g>

        {/* phi compiler block in middle */}
        <g>
          <rect x={400} y={200} width={460} height={140} rx={12}
            fill={T2.bgPanel} stroke={T2.accent} strokeWidth={1.5} />
          <text x={630} y={232} textAnchor="middle"
            fontFamily={F2.mono} fontSize={14} fill={T2.accent}
            style={{ letterSpacing: '0.18em', textTransform: 'uppercase' }}>
            write function φ
          </text>
          <text x={630} y={278} textAnchor="middle"
            fontFamily={F2.serif} fontSize={28} fill={T2.ink}>
            compile to modulation
          </text>
          <text x={630} y={310} textAnchor="middle"
            fontFamily={F2.mono} fontSize={16} fill={T2.inkMute}>
            (M_A, M_B, E_A, E_B) per layer
          </text>
        </g>

        {/* Arrows from parallel layers into phi */}
        {[0, 2, 4, 6].map((li, i) => {
          const y = 110 + li * 46 + 18;
          return (
            <Edge key={i}
              x1={230} y1={y} x2={400} y2={250 + i * 25}
              stroke={T2.accentDim} strokeWidth={1.2}
              particle particleColor={T2.accent} particleDur="3s"
              particleDelay={i * 0.25} particleR={3} curve={-15}
            />
          );
        })}
        {/* Arrows from phi into primary patched layers */}
        {[1, 4, 7].map((li, i) => {
          const y = 110 + li * 46 + 18;
          return (
            <Edge key={i}
              x1={860} y1={y} x2={860} y2={y}
              stroke={T2.accent} strokeWidth={0} />
          );
        })}
        {[1, 4, 7].map((li, i) => {
          const y = 110 + li * 46 + 18;
          return (
            <Edge key={i}
              x1={860} y1={y} x2={860 - 0} y2={y}
              stroke={T2.accent} strokeWidth={0} />
          );
        })}
        {/* phi -> primary host */}
        {[1, 4, 7].map((li, i) => {
          const y = 110 + li * 46 + 18;
          return (
            <Edge key={`p${i}`}
              x1={860} y1={295} x2={860} y2={y}
              stroke={T2.accent} strokeWidth={1.2}
              dash="4 4" />
          );
        })}
        {[1, 4, 7].map((li, i) => {
          const y = 110 + li * 46 + 18;
          return (
            <Edge key={`pp${i}`}
              x1={860} y1={270 + i * 10} x2={870} y2={y}
              stroke={T2.accent} strokeWidth={1.5}
              particle particleColor={T2.accent} particleDur="2.4s"
              particleDelay={i * 0.4} particleR={3} arrow />
          );
        })}

        {/* Output bottom of right column */}
        <g>
          <line x1={950} y1={490} x2={950} y2={510} stroke={T2.inkDim} strokeWidth={1.5} markerEnd="url(#arrowhead)" />
          <text x={950} y={530} textAnchor="middle" fontFamily={F2.mono} fontSize={14} fill={T2.inkMute}
            style={{ letterSpacing: '0.12em', textTransform: 'uppercase' }}>
            shaped output
          </text>
        </g>

        {/* Annotations on right side */}
        <g transform="translate(1140, 120)">
          <rect x={0} y={0} width={500} height={360} rx={10}
            fill="none" stroke={T2.rule} strokeDasharray="2 4" />
          <text x={28} y={42} fontFamily={F2.mono} fontSize={14} fill={T2.accent}
            style={{ letterSpacing: '0.18em', textTransform: 'uppercase' }}>
            three properties
          </text>
          {[
            ['private', 'parallel context never occupies primary positions'],
            ['shared', 'same frozen host layers process both passes'],
            ['compiled', 'experience → low-rank modulation tensors'],
            ['removable', 'detach φ to recover the unmodified host'],
          ].map(([k, v], i) => (
            <g key={i} transform={`translate(28, ${80 + i * 64})`}>
              <text x={0} y={0} fontFamily={F2.mono} fontSize={18} fill={T2.ink} fontWeight={600}
                style={{ letterSpacing: '0.06em', textTransform: 'uppercase' }}>
                {k}
              </text>
              <text x={0} y={28} fontFamily={F2.sans} fontSize={20} fill={T2.inkDim}>
                {v}
              </text>
            </g>
          ))}
        </g>
      </svg>

      <Chrome index={index} total={total} chapter="enmeshed networks" />
    </Slide>
  );
}

// ============================================================
// 06 — Six-axis design space
// ============================================================
function S06_DesignSpace({ index, total }) {
  const axes = [
    { name: 'Blending', vals: ['additive', 'gated', 'cross-attn'], pick: 0 },
    { name: 'Rank', vals: ['r=4', 'r=16', 'r=64'], pick: 1 },
    { name: 'Targets', vals: ['Q only', 'Q + V', 'Q + K + V'], pick: 1 },
    { name: 'Patching', vals: ['all layers', 'stride-3', 'attn only'], pick: 1 },
    { name: 'Compilation', vals: ['online', 'cached', 'conviction'], pick: 2 },
    { name: 'Temporal', vals: ['constant', 'decay', 'phase-gated'], pick: 0 },
  ];

  return (
    <Slide label="06 Design Space">
      <TitleBlock
        eyebrow="Six-axis design space"
        title="HEXIS picks one point. The rest is open."
        sub="Each axis is a knob. We validate Level 1 — the simplest setting at every axis. The space behind it is unexplored."
      />

      <div style={{
        position: 'absolute', left: SP2.paddingX, right: SP2.paddingX, top: 380,
        display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 36,
      }}>
        {axes.map((a, i) => (
          <div key={a.name} style={{
            background: T2.bgPanel, border: `1px solid ${T2.rule}`,
            borderRadius: 12, padding: '28px 32px 32px',
          }}>
            <div style={{
              fontFamily: F2.mono, fontSize: 16, color: T2.inkMute,
              letterSpacing: '0.14em', textTransform: 'uppercase', marginBottom: 22,
            }}>
              axis {String(i + 1).padStart(2, '0')} — {a.name}
            </div>
            <div style={{ display: 'flex', gap: 12, alignItems: 'center' }}>
              {a.vals.map((v, j) => {
                const sel = j === a.pick;
                return (
                  <div key={j} style={{
                    flex: 1,
                    padding: '14px 8px',
                    border: `1.5px solid ${sel ? T2.accent : T2.rule}`,
                    background: sel ? 'rgba(212,138,73,0.08)' : 'transparent',
                    borderRadius: 8, textAlign: 'center',
                    fontFamily: F2.mono, fontSize: 18,
                    color: sel ? T2.accent : T2.inkDim,
                    fontWeight: sel ? 600 : 400,
                    position: 'relative',
                  }}>
                    {v}
                    {sel && (
                      <div style={{
                        position: 'absolute', top: -10, right: -10,
                        background: T2.accent, color: T2.bg,
                        width: 22, height: 22, borderRadius: 11,
                        fontFamily: F2.mono, fontSize: 12, lineHeight: '22px',
                        fontWeight: 700,
                      }}>✓</div>
                    )}
                  </div>
                );
              })}
            </div>
          </div>
        ))}
      </div>

      <div style={{
        position: 'absolute', left: SP2.paddingX, bottom: 90,
        fontFamily: F2.serif, fontStyle: 'italic',
        fontSize: 28, color: T2.inkDim, maxWidth: 1300,
      }}>
        HEXIS = additive · r=16 · Q+V · stride-3 · conviction-weighted · constant.
      </div>

      <Chrome index={index} total={total} chapter="design space" />
    </Slide>
  );
}

// ============================================================
// 07 — Mind Tree
// ============================================================
function S07_MindTree({ index, total }) {
  // Hierarchical node graph with section headers, conviction colors, novel flag
  return (
    <Slide label="07 Mind Tree">
      <TitleBlock
        eyebrow="Structured private subcontext"
        title="The Mind Tree."
        sub="A typed cognitive schema — identity, beliefs, strategies, memories, models, values. Each node carries conviction, domain tags, and an addresses field. φ pools by conviction; novel content routes to the curated slot."
      />

      <svg width="1700" height="540" style={{ position: 'absolute', left: SP2.paddingX, bottom: 90 }}>
        <Defs />

        {/* Root */}
        <Node x={140} y={270} r={28} fill={T2.bgRaised} stroke={T2.accent}
          label="self" labelPos="left" fontSize={20} color={T2.ink} halo haloColor={T2.accent} />
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
              stroke={T2.rule} strokeWidth={1}
              particle particleColor={T2.accent2Dim} particleDur="3s" particleDelay={i * 0.3} particleR={2.5} curve={5} />
            <Node x={380} y={s.y} r={20} fill={T2.bgRaised} stroke={T2.accent2}
              label={s.label} labelPos="right" fontSize={18} color={T2.ink} />
          </g>
        ))}

        {/* Belief children with conviction */}
        {(() => {
          const beliefs = [
            { x: 740, y: 130, label: 'b1', conv: 'strong', color: T2.accent, novel: false },
            { x: 740, y: 200, label: 'b2', conv: 'strong', color: T2.accent, novel: false },
            { x: 740, y: 270, label: 'b3', conv: 'moderate', color: T2.accent2, novel: false },
            { x: 740, y: 340, label: 'b4', conv: 'moderate', color: T2.accent2, novel: true },
            { x: 740, y: 410, label: 'b5', conv: 'agnostic', color: T2.inkMute, novel: false },
          ];
          return beliefs.map((b, i) => (
            <g key={i}>
              <Edge x1={400} y1={180} x2={720} y2={b.y}
                stroke={T2.rule} strokeWidth={1} curve={i % 2 ? 8 : -8} />
              <Node x={b.x} y={b.y} r={14} fill={T2.bgRaised} stroke={b.color}
                label={`${b.label} · ${b.conv}${b.novel ? ' · novel' : ''}`} labelPos="right" fontSize={16}
                color={b.novel ? T2.accent : T2.inkDim} />
            </g>
          ));
        })()}

        {/* Right side: how the schema flows */}
        <g transform="translate(1180, 60)">
          <rect x={0} y={0} width={500} height={460} rx={10}
            fill={T2.bgPanel} stroke={T2.rule} />
          <text x={28} y={48} fontFamily={F2.mono} fontSize={14} fill={T2.accent}
            style={{ letterSpacing: '0.18em', textTransform: 'uppercase' }}>
            routing
          </text>

          <text x={28} y={100} fontFamily={F2.serif} fontSize={28} fill={T2.ink}>
            conviction → φ pooling
          </text>
          <text x={28} y={134} fontFamily={F2.sans} fontSize={20} fill={T2.inkDim}>
            strong &gt; moderate &gt; agnostic
          </text>

          <text x={28} y={210} fontFamily={F2.serif} fontSize={28} fill={T2.ink}>
            novel = true → curated slot
          </text>
          <text x={28} y={244} fontFamily={F2.sans} fontSize={20} fill={T2.inkDim}>
            specifics that can&rsquo;t survive r=16
          </text>

          <text x={28} y={320} fontFamily={F2.serif} fontSize={28} fill={T2.ink}>
            addresses → query match
          </text>
          <text x={28} y={354} fontFamily={F2.sans} fontSize={20} fill={T2.inkDim}>
            which nodes resonate per turn
          </text>

          <line x1={28} y1={400} x2={472} y2={400} stroke={T2.rule} />
          <text x={28} y={432} fontFamily={F2.mono} fontSize={16} fill={T2.inkMute}
            style={{ letterSpacing: '0.06em' }}>
            categorical, not numeric — the mechanism
          </text>
          <text x={28} y={452} fontFamily={F2.mono} fontSize={16} fill={T2.inkMute}
            style={{ letterSpacing: '0.06em' }}>
            can read &ldquo;strong&rdquo; vs &ldquo;agnostic&rdquo;.
          </text>
        </g>
      </svg>

      <Chrome index={index} total={total} chapter="mind tree" />
    </Slide>
  );
}

// ============================================================
// 08 — HEXIS in One Picture (system overview)
// ============================================================
function S08_System({ index, total }) {
  return (
    <Slide label="08 System">
      <TitleBlock
        eyebrow="HEXIS — system overview"
        title="Two loops, one frozen host."
      />

      <svg width="1700" height="640" style={{ position: 'absolute', left: SP2.paddingX, bottom: 30 }}>
        <Defs />

        {/* Compilation loop (top) */}
        <g>
          <rect x={20} y={20} width={1660} height={260} rx={14}
            fill="none" stroke={T2.accentDim} strokeDasharray="4 6" strokeWidth={1} />
          <text x={50} y={56} fontFamily={F2.mono} fontSize={16} fill={T2.accent}
            style={{ letterSpacing: '0.18em', textTransform: 'uppercase' }}>
            compilation loop · async, amortized
          </text>

          {/* Mind tree icon */}
          <Node x={130} y={170} r={30} fill={T2.bgRaised} stroke={T2.accent}
            label="Mind Tree" labelPos="below" fontSize={18} color={T2.inkDim} />
          <circle cx={100} cy={150} r={6} fill={T2.accent2} />
          <circle cx={160} cy={150} r={6} fill={T2.accent2} />
          <circle cx={100} cy={190} r={6} fill={T2.accent2} />
          <circle cx={160} cy={190} r={6} fill={T2.accent2} />

          {/* arrow */}
          <Edge x1={170} y1={170} x2={330} y2={170}
            stroke={T2.inkDim} arrow particle particleColor={T2.accent} particleDur="2.6s" />

          {/* Frozen host (small) */}
          <rect x={340} y={100} width={180} height={140} rx={8}
            fill={T2.bgRaised} stroke={T2.rule} />
          {[0, 1, 2, 3, 4].map((i) => (
            <line key={i} x1={340} y1={120 + i * 24} x2={520} y2={120 + i * 24}
              stroke={T2.rule} strokeWidth={1} />
          ))}
          <text x={430} y={88} textAnchor="middle" fontFamily={F2.mono} fontSize={13} fill={T2.inkMute}
            style={{ letterSpacing: '0.12em', textTransform: 'uppercase' }}>
            frozen host
          </text>
          <text x={430} y={266} textAnchor="middle" fontFamily={F2.mono} fontSize={13} fill={T2.inkMute}
            style={{ letterSpacing: '0.12em', textTransform: 'uppercase' }}>
            (private pass)
          </text>

          {/* arrow */}
          <Edge x1={530} y1={170} x2={680} y2={170}
            stroke={T2.inkDim} arrow particle particleColor={T2.accent} particleDur="2.6s" particleDelay={0.6} />

          {/* phi compiler */}
          <rect x={690} y={120} width={220} height={100} rx={10}
            fill={T2.bgPanel} stroke={T2.accent} strokeWidth={1.5} />
          <text x={800} y={158} textAnchor="middle" fontFamily={F2.serif} fontSize={32} fill={T2.accent}>
            φ
          </text>
          <text x={800} y={188} textAnchor="middle" fontFamily={F2.mono} fontSize={14} fill={T2.inkDim}
            style={{ letterSpacing: '0.12em', textTransform: 'uppercase' }}>
            write function
          </text>

          {/* arrow */}
          <Edge x1={920} y1={170} x2={1080} y2={170}
            stroke={T2.inkDim} arrow particle particleColor={T2.accent} particleDur="2.6s" particleDelay={1.2} />

          {/* Modulation tensors */}
          <g>
            {[0, 1, 2, 3, 4].map((i) => (
              <rect key={i} x={1090 + i * 36} y={120} width={28} height={100} rx={4}
                fill={T2.bgRaised} stroke={T2.accent} strokeWidth={1.2}>
                <animate attributeName="opacity" values="0.5;1;0.5" dur="2.5s"
                  repeatCount="indefinite" begin={`${i * 0.2}s`} />
              </rect>
            ))}
            <text x={1180} y={250} textAnchor="middle" fontFamily={F2.mono} fontSize={14} fill={T2.inkMute}
              style={{ letterSpacing: '0.12em', textTransform: 'uppercase' }}>
              M_A, M_B, E_A, E_B
            </text>
          </g>

          {/* Curated slot */}
          <g transform="translate(1320, 110)">
            <rect x={0} y={0} width={300} height={120} rx={10}
              fill={T2.bgPanel} stroke={T2.accent2} strokeWidth={1.5} />
            <text x={150} y={36} textAnchor="middle" fontFamily={F2.mono} fontSize={14} fill={T2.accent2}
              style={{ letterSpacing: '0.14em', textTransform: 'uppercase' }}>
              curated slot
            </text>
            <text x={150} y={70} textAnchor="middle" fontFamily={F2.serif} fontSize={22} fill={T2.ink}>
              novel specifics
            </text>
            <text x={150} y={98} textAnchor="middle" fontFamily={F2.mono} fontSize={14} fill={T2.inkMute}>
              ~70 tokens
            </text>
          </g>
        </g>

        {/* Generation loop (bottom) */}
        <g>
          <rect x={20} y={310} width={1660} height={310} rx={14}
            fill="none" stroke={T2.accent2Dim} strokeDasharray="4 6" strokeWidth={1} />
          <text x={50} y={346} fontFamily={F2.mono} fontSize={16} fill={T2.accent2}
            style={{ letterSpacing: '0.18em', textTransform: 'uppercase' }}>
            generation loop · per-token, fixed cost
          </text>

          {/* User query */}
          <rect x={50} y={420} width={210} height={100} rx={10}
            fill={T2.bgPanel} stroke={T2.rule} />
          <text x={155} y={460} textAnchor="middle" fontFamily={F2.mono} fontSize={14} fill={T2.inkMute}
            style={{ letterSpacing: '0.14em', textTransform: 'uppercase' }}>
            user query
          </text>
          <text x={155} y={494} textAnchor="middle" fontFamily={F2.sans} fontSize={20} fill={T2.inkDim}>
            + curated slot
          </text>

          <Edge x1={270} y1={470} x2={420} y2={470}
            stroke={T2.inkDim} arrow particle particleColor={T2.accent2} particleDur="2.4s" />

          {/* Frozen host (large, with patches) */}
          <rect x={430} y={370} width={460} height={220} rx={12}
            fill={T2.bgRaised} stroke={T2.rule} />
          <text x={660} y={358} textAnchor="middle" fontFamily={F2.mono} fontSize={14} fill={T2.inkMute}
            style={{ letterSpacing: '0.14em', textTransform: 'uppercase' }}>
            frozen host (generation)
          </text>
          {[0, 1, 2, 3, 4, 5, 6, 7].map((i) => {
            const patched = [1, 4, 7].includes(i);
            const yi = 390 + i * 24;
            return (
              <g key={i}>
                <line x1={450} y1={yi} x2={870} y2={yi}
                  stroke={patched ? T2.accent : T2.rule}
                  strokeWidth={patched ? 1.5 : 1} />
                {patched && (
                  <text x={880} y={yi + 5} fontFamily={F2.mono} fontSize={11} fill={T2.accent}>
                    +M, +E
                  </text>
                )}
              </g>
            );
          })}

          {/* Modulation feed-in arrows from above */}
          {[0, 1, 2].map((i) => (
            <Edge key={i}
              x1={1180} y1={235} x2={780} y2={414 + i * 72}
              stroke={T2.accent} strokeWidth={1.2} dash="4 4"
              particle particleColor={T2.accent} particleDur="2.8s" particleDelay={i * 0.4} particleR={3} curve={-30} />
          ))}

          <Edge x1={900} y1={470} x2={1100} y2={470}
            stroke={T2.inkDim} arrow particle particleColor={T2.accent} particleDur="2.4s" particleDelay={1} />

          {/* Output */}
          <rect x={1120} y={420} width={300} height={100} rx={10}
            fill={T2.bgPanel} stroke={T2.accent2} strokeWidth={1.5} />
          <text x={1270} y={460} textAnchor="middle" fontFamily={F2.mono} fontSize={14} fill={T2.accent2}
            style={{ letterSpacing: '0.14em', textTransform: 'uppercase' }}>
            generation
          </text>
          <text x={1270} y={494} textAnchor="middle" fontFamily={F2.serif} fontSize={22} fill={T2.ink}>
            shaped output
          </text>

          {/* Reflection / write back */}
          <Edge x1={1420} y1={470} x2={1580} y2={470}
            stroke={T2.accent} arrow particle particleColor={T2.accent} particleDur="3s" particleDelay={1.5} />
          <text x={1500} y={446} textAnchor="middle" fontFamily={F2.mono} fontSize={13} fill={T2.accent}
            style={{ letterSpacing: '0.12em', textTransform: 'uppercase' }}>
            teacher
          </text>

          {/* loop back to mind tree */}
          <Edge x1={1620} y1={470} x2={1620} y2={170}
            stroke={T2.accentDim} strokeWidth={1.2} dash="6 4" />
          <Edge x1={1620} y1={170} x2={170} y2={170}
            stroke={T2.accentDim} strokeWidth={1.2} dash="6 4"
            particle particleColor={T2.accent} particleDur="6s" particleDelay={2} particleR={3} />
        </g>
      </svg>

      <Chrome index={index} total={total} chapter="architecture" />
    </Slide>
  );
}

Object.assign(window, { S05_Enmeshed, S06_DesignSpace, S07_MindTree, S08_System });
