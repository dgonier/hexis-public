// Slides 1-8: Title, problem, landscape, enmeshed primitive, design space, mind tree, architecture overview
const T1 = window.HEXIS_TOKENS;
const TS1 = window.TYPE_SCALE;
const SP1 = window.SPACING;
const F1 = window.FONTS;

// ============================================================
// 01 — Title
// ============================================================
function S01_Title({ index, total }) {
  return (
    <Slide label="01 Title" padded={false}>
      {/* Background animated node mesh */}
      <svg width="1920" height="1080" style={{ position: 'absolute', inset: 0 }}>
        <Defs />
        {/* faint grid mesh */}
        <g opacity={0.5}>
          {Array.from({ length: 7 }).map((_, i) => {
            const cx = 1500, cy = 540;
            const angle = (i / 7) * Math.PI * 2;
            const r = 360;
            const nx = cx + Math.cos(angle) * r;
            const ny = cy + Math.sin(angle) * r;
            return (
              <g key={i}>
                <Edge x1={cx} y1={cy} x2={nx} y2={ny}
                  stroke={T1.rule} strokeWidth={1}
                  particle particleColor={T1.accent} particleDur="3.4s" particleDelay={i * 0.4} particleR={3} />
                <Node x={nx} y={ny} r={14} fill={T1.bgRaised} stroke={T1.rule} pulse pulseDelay={i * 0.4} haloColor={T1.accent2Dim} />
              </g>
            );
          })}
          <Node x={1500} y={540} r={36} fill={T1.bgRaised} stroke={T1.accent} halo haloColor={T1.accent} />
          <text x={1500} y={547} textAnchor="middle" fontFamily={F1.mono} fontSize={18} fill={T1.accent}
            style={{ letterSpacing: '0.1em' }}>φ</text>
        </g>
      </svg>

      <div style={{
        position: 'absolute',
        left: SP1.paddingX, top: 320, right: 800,
      }}>
        <div style={{
          fontFamily: F1.mono, fontSize: 22, color: T1.accent,
          letterSpacing: '0.24em', textTransform: 'uppercase', marginBottom: 36,
        }}>
          NeurIPS 2026 — Architectures for Memory
        </div>
        <h1 style={{
          fontFamily: F1.serif, fontWeight: 400, fontSize: 180,
          lineHeight: 0.92, letterSpacing: '-0.02em',
          margin: 0, color: T1.ink,
        }}>
          HEXIS
        </h1>
        <div style={{
          fontFamily: F1.serif, fontSize: 48, color: T1.ink, fontStyle: 'italic',
          marginTop: 24, lineHeight: 1.2, fontWeight: 300, letterSpacing: '-0.01em',
        }}>
          Compiled dispositional memory<br />
          through enmeshed networks
        </div>
        <div style={{
          fontFamily: F1.sans, fontSize: 26, color: T1.inkMute, marginTop: 56,
          letterSpacing: '0.04em',
        }}>
          Devin Gonier
        </div>
      </div>

      <div style={{
        position: 'absolute', bottom: 40, left: SP1.paddingX, right: SP1.paddingX,
        display: 'flex', justifyContent: 'space-between',
        fontFamily: F1.mono, fontSize: 24, color: T1.inkMute,
        letterSpacing: '0.08em', textTransform: 'uppercase',
      }}>
        <span>Hidden Enmeshed eXperiential Identity States</span>
        <span>{String(index).padStart(2, '0')} / {String(total).padStart(2, '0')}</span>
      </div>
    </Slide>
  );
}

// ============================================================
// 02 — The Memory Problem
// ============================================================
function S02_MemoryProblem({ index, total }) {
  // Animated diagram: a single context window crammed with tokens
  return (
    <Slide label="02 Memory Problem">
      <TitleBlock
        eyebrow="The setting"
        title="All memory in one channel."
        sub="The dominant pattern places memory as text inside the context window — RAG, MemGPT, Reflexion, system prompts. Memory becomes content that competes for attention with the conversation itself."
      />

      <svg width="1700" height="540" style={{ position: 'absolute', left: SP1.paddingX, bottom: 110 }}>
        <Defs />
        {/* Context window rectangle */}
        <rect x={20} y={140} width={1660} height={260} rx={14}
          fill={T1.bgPanel} stroke={T1.rule} />
        <text x={40} y={120} fontFamily={F1.mono} fontSize={16} fill={T1.inkMute}
          style={{ letterSpacing: '0.18em', textTransform: 'uppercase' }}>
          context window — one shared channel
        </text>
        {/* Token chips inside */}
        {(() => {
          const labels = [
            { t: 'system prompt', c: T1.accent2Dim, w: 180 },
            { t: 'retrieved doc', c: T1.accent3Dim, w: 200 },
            { t: 'belief', c: T1.accent, w: 110 },
            { t: 'belief', c: T1.accent, w: 110 },
            { t: 'reflection', c: T1.accent3Dim, w: 160 },
            { t: 'user turn 1', c: T1.inkDim, w: 160 },
            { t: 'tool result', c: T1.accent2Dim, w: 160 },
            { t: 'user turn 2', c: T1.inkDim, w: 160 },
            { t: 'filler', c: T1.rule, w: 120 },
            { t: 'user turn 3', c: T1.inkDim, w: 160 },
          ];
          let cx = 50;
          return labels.map((l, i) => {
            const out = (
              <g key={i}>
                <rect x={cx} y={200} width={l.w} height={140} rx={6}
                  fill={T1.bgRaised} stroke={l.c} strokeWidth={1.5} />
                <text x={cx + l.w / 2} y={278} textAnchor="middle"
                  fontFamily={F1.mono} fontSize={15} fill={l.c}
                  style={{ letterSpacing: '0.06em' }}>
                  {l.t}
                </text>
              </g>
            );
            cx += l.w + 12;
            return out;
          });
        })()}
        {/* Attention competition arrow */}
        <text x={840} y={460} textAnchor="middle" fontFamily={F1.mono} fontSize={15}
          fill={T1.inkMute} style={{ letterSpacing: '0.18em', textTransform: 'uppercase' }}>
          all of these compete for the same attention budget
        </text>
        {/* tiny attention beams */}
        {[180, 380, 580, 780, 980, 1180, 1380].map((x, i) => (
          <line key={i} x1={x} y1={400} x2={x + 10} y2={440}
            stroke={T1.inkMute} strokeWidth={1} opacity={0.5}>
            <animate attributeName="opacity" values="0.1;0.7;0.1" dur="2.4s" repeatCount="indefinite" begin={`${i * 0.2}s`} />
          </line>
        ))}
      </svg>

      <Chrome index={index} total={total} chapter="problem" />
    </Slide>
  );
}

// ============================================================
// 03 — Three failure modes
// ============================================================
function S03_FailureModes({ index, total }) {
  const modes = [
    {
      name: 'Dilution',
      glyph: 'fade',
      blurb: 'Memory fights for attention with conversation, task content, and filler. Beliefs decay as context grows.',
    },
    {
      name: 'Sycophancy',
      glyph: 'mirror',
      blurb: 'The model can read its own memory and be argued out of it. Convictions fold under pressure.',
    },
    {
      name: 'Cost',
      glyph: 'budget',
      blurb: 'Every token of memory is a token of context. Profiles, reflections, and beliefs consume the budget.',
    },
  ];

  return (
    <Slide label="03 Failure Modes">
      <TitleBlock
        eyebrow="Three structural failure modes"
        title="One channel, three ways it breaks."
      />

      <div style={{
        position: 'absolute', left: SP1.paddingX, right: SP1.paddingX,
        top: 360, display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: 60,
      }}>
        {modes.map((m, i) => (
          <div key={m.name}>
            <svg width="500" height="220" viewBox="0 0 500 220">
              {m.glyph === 'fade' && (
                <g>
                  {Array.from({ length: 8 }).map((_, j) => (
                    <rect key={j} x={20 + j * 56} y={80} width={44} height={60} rx={4}
                      fill={T1.accent} opacity={1 - j * 0.13}>
                      <animate attributeName="opacity"
                        values={`${1 - j * 0.13};${Math.max(0.05, 1 - j * 0.13 - 0.3)};${1 - j * 0.13}`}
                        dur="3s" repeatCount="indefinite" begin={`${j * 0.15}s`} />
                    </rect>
                  ))}
                  <line x1={20} y1={170} x2={460} y2={170} stroke={T1.inkMute} strokeWidth={1} />
                  <text x={20} y={195} fontFamily={F1.mono} fontSize={13} fill={T1.inkMute}
                    style={{ letterSpacing: '0.1em' }}>0 tok</text>
                  <text x={460} y={195} textAnchor="end" fontFamily={F1.mono} fontSize={13} fill={T1.inkMute}
                    style={{ letterSpacing: '0.1em' }}>4K tok</text>
                </g>
              )}
              {m.glyph === 'mirror' && (
                <g>
                  <Node x={150} y={110} r={36} fill={T1.bgRaised} stroke={T1.accent} label="belief" labelPos="below" fontSize={14} color={T1.inkDim} />
                  <Node x={350} y={110} r={36} fill={T1.bgRaised} stroke={T1.bad} label="adversary" labelPos="below" fontSize={14} color={T1.inkDim} />
                  <Edge x1={186} y1={110} x2={314} y2={110} stroke={T1.bad}
                    particle particleColor={T1.bad} particleDur="1.6s" arrow />
                  <Edge x1={314} y1={120} x2={186} y2={120} stroke={T1.accentDim}
                    particle particleColor={T1.accentDim} particleDur="1.6s" particleDelay={0.8} curve={20} />
                </g>
              )}
              {m.glyph === 'budget' && (
                <g>
                  <rect x={20} y={80} width={460} height={60} rx={6} fill="none" stroke={T1.rule} />
                  {/* memory portion grows */}
                  <rect x={20} y={80} width={120} height={60} fill={T1.accent}>
                    <animate attributeName="width" values="120;320;120" dur="4s" repeatCount="indefinite" />
                  </rect>
                  <rect x={460} y={155} width={20} height={20} fill={T1.inkDim} />
                  <text x={490} y={170} fontFamily={F1.mono} fontSize={13} fill={T1.inkMute}>conversation</text>
                  <rect x={20} y={155} width={20} height={20} fill={T1.accent} />
                  <text x={50} y={170} fontFamily={F1.mono} fontSize={13} fill={T1.inkMute}>memory</text>
                </g>
              )}
            </svg>
            <div style={{
              fontFamily: F1.mono, fontSize: 16, color: T1.accent,
              letterSpacing: '0.18em', textTransform: 'uppercase', marginTop: 20,
            }}>
              {String(i + 1).padStart(2, '0')} — {m.name}
            </div>
            <p style={{
              fontFamily: F1.sans, fontSize: 28, lineHeight: 1.35, color: T1.inkDim,
              marginTop: 16, textWrap: 'pretty',
            }}>
              {m.blurb}
            </p>
          </div>
        ))}
      </div>

      <Chrome index={index} total={total} chapter="problem" />
    </Slide>
  );
}

// ============================================================
// 04 — The Adaptation Landscape
// ============================================================
function S04_Landscape({ index, total }) {
  // Four columns — RAG, LoRA, ActAdd, Enmeshed — showing where they fuse
  const methods = [
    { name: 'RAG / Reflexion', sub: 'context-level', detail: 'Adds tokens to the input. Memory competes for attention; dilutes with length.', fuse: 'input' },
    { name: 'LoRA / adapters', sub: 'parameter-level', detail: 'Modifies host weights via gradient descent. Result is fixed after training.', fuse: 'weights' },
    { name: 'ActAdd / RepEng', sub: 'activation-level', detail: 'Injects fixed directions. Non-adaptive to experience.', fuse: 'activation' },
    { name: 'Enmeshed network', sub: 'parallel-channel', detail: 'A second context shares the host’s forward pass. Hidden-state bridge becomes the substrate.', fuse: 'parallel', highlight: true },
  ];

  return (
    <Slide label="04 Landscape">
      <TitleBlock
        eyebrow="The adaptation landscape"
        title="Where does the new information fuse?"
      />

      <div style={{
        position: 'absolute', left: SP1.paddingX, right: SP1.paddingX, top: 340,
        display: 'grid', gridTemplateColumns: '1fr 1fr 1fr 1fr', gap: 28,
      }}>
        {methods.map((m, i) => {
          const c = m.highlight ? T1.accent : T1.inkDim;
          return (
            <div key={m.name} style={{
              border: `1px solid ${m.highlight ? T1.accent : T1.rule}`,
              borderRadius: 12, padding: '32px 28px 36px',
              background: m.highlight ? 'rgba(212, 138, 73, 0.05)' : T1.bgPanel,
              minHeight: 460, position: 'relative', display: 'flex', flexDirection: 'column',
            }}>
              <div style={{
                fontFamily: F1.mono, fontSize: 14, color: c,
                letterSpacing: '0.18em', textTransform: 'uppercase', marginBottom: 18,
              }}>
                {m.sub}
              </div>
              <div style={{
                fontFamily: F1.serif, fontSize: 36, color: T1.ink, lineHeight: 1.1,
                marginBottom: 28, fontWeight: 400,
              }}>
                {m.name}
              </div>

              {/* Mini diagram */}
              <svg width="100%" height="160" viewBox="0 0 320 160">
                <rect x={120} y={20} width={80} height={120} rx={6}
                  fill={T1.bgRaised} stroke={T1.rule} strokeWidth={1} />
                {/* layers */}
                {[40, 70, 100, 130].map((y, j) => (
                  <line key={j} x1={120} y1={y} x2={200} y2={y} stroke={T1.rule} strokeWidth={1} />
                ))}
                {m.fuse === 'input' && (
                  <g>
                    <rect x={20} y={60} width={80} height={40} rx={4} fill={c} opacity={0.25} stroke={c} />
                    <Edge x1={100} y1={80} x2={120} y2={80} stroke={c} arrow particle particleColor={c} particleDur="2s" />
                  </g>
                )}
                {m.fuse === 'weights' && (
                  <g>
                    <rect x={120} y={20} width={80} height={120} fill={c} opacity={0.12} />
                    <text x={160} y={84} textAnchor="middle" fontFamily={F1.mono} fontSize={11} fill={c}>
                      W += ΔW
                    </text>
                  </g>
                )}
                {m.fuse === 'activation' && (
                  <g>
                    <line x1={210} y1={80} x2={300} y2={80} stroke={c} strokeWidth={2} markerEnd="url(#arrowhead)">
                    </line>
                    <text x={255} y={70} textAnchor="middle" fontFamily={F1.mono} fontSize={11} fill={c}>
                      + d*
                    </text>
                  </g>
                )}
                {m.fuse === 'parallel' && (
                  <g>
                    {/* phi column */}
                    <rect x={20} y={20} width={70} height={120} rx={6}
                      fill={T1.bgRaised} stroke={c} strokeWidth={1.5} />
                    {[40, 70, 100, 130].map((y, j) => (
                      <line key={j} x1={20} y1={y} x2={90} y2={y} stroke={T1.rule} strokeWidth={1} />
                    ))}
                    <text x={55} y={10} textAnchor="middle" fontFamily={F1.mono} fontSize={11} fill={c}>parallel</text>
                    {/* bridges between columns */}
                    {[40, 70, 100, 130].map((y, j) => (
                      <Edge key={j} x1={90} y1={y} x2={120} y2={y}
                        stroke={c} strokeWidth={1.5}
                        particle particleColor={c} particleDur="2s" particleDelay={j * 0.4} particleR={3} />
                    ))}
                  </g>
                )}
              </svg>

              <p style={{
                fontFamily: F1.sans, fontSize: 22, lineHeight: 1.4, color: T1.inkDim,
                marginTop: 22, textWrap: 'pretty',
              }}>
                {m.detail}
              </p>

              {m.highlight && (
                <div style={{
                  position: 'absolute', top: -1, right: -1,
                  background: T1.accent, color: T1.bg,
                  fontFamily: F1.mono, fontSize: 12, letterSpacing: '0.12em',
                  padding: '6px 12px', borderRadius: '0 12px 0 12px',
                  textTransform: 'uppercase', fontWeight: 600,
                }}>
                  this paper
                </div>
              )}
            </div>
          );
        })}
      </div>

      <Chrome index={index} total={total} chapter="landscape" />
    </Slide>
  );
}

Object.assign(window, { S01_Title, S02_MemoryProblem, S03_FailureModes, S04_Landscape });
