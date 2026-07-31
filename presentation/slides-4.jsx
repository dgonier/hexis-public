// Slides 13-17: Two mechanisms, agentic, bottleneck boundary, future, summary
const T4 = window.HEXIS_TOKENS;
const TS4 = window.TYPE_SCALE;
const SP4 = window.SPACING;
const F4 = window.FONTS;

// ============================================================
// 13 — Two Mechanisms, One Bridge
// ============================================================
function S13_TwoMech({ index, total }) {
  return (
    <Slide label="13 Two Mechanisms">
      <TitleBlock
        eyebrow="Generalization"
        title="Two mechanisms. One hidden-state bridge."
        sub="The same Mind Tree feeds two different φs. (a) compile to Q/V modulation for disposition. (b) project to a retrieval space for agentic knowledge injection."
      />

      <svg width="1700" height="540" style={{ position: 'absolute', left: SP4.paddingX, bottom: 70 }}>
        <Defs />

        {/* Shared hidden state in middle */}
        <g>
          <rect x={750} y={210} width={200} height={120} rx={12}
            fill={T4.bgPanel} stroke={T4.ink} strokeWidth={1.5} />
          <text x={850} y={246} textAnchor="middle"
            fontFamily={F4.mono} fontSize={13} fill={T4.inkMute}
            style={{ letterSpacing: '0.18em', textTransform: 'uppercase' }}>
            shared bridge
          </text>
          <text x={850} y={282} textAnchor="middle"
            fontFamily={F4.serif} fontSize={26} fill={T4.ink}>
            host hidden state
          </text>
          <text x={850} y={308} textAnchor="middle"
            fontFamily={F4.mono} fontSize={16} fill={T4.inkMute}>
            h ∈ ℝ^d
          </text>
        </g>

        {/* Mechanism A — left */}
        <g>
          <text x={300} y={50} textAnchor="middle"
            fontFamily={F4.mono} fontSize={14} fill={T4.accent}
            style={{ letterSpacing: '0.18em', textTransform: 'uppercase' }}>
            mechanism (a) — disposition
          </text>
          <rect x={60} y={80} width={500} height={400} rx={12}
            fill="none" stroke={T4.accentDim} strokeDasharray="4 6" />

          <Node x={140} y={170} r={28} fill={T4.bgRaised} stroke={T4.accent}
            label="φ" labelPos="inside" fontSize={28} color={T4.accent} />
          <text x={140} y={222} textAnchor="middle" fontFamily={F4.mono} fontSize={13} fill={T4.inkMute}
            style={{ letterSpacing: '0.12em', textTransform: 'uppercase' }}>compile</text>

          <Edge x1={170} y1={170} x2={400} y2={170} stroke={T4.accent} arrow
            particle particleColor={T4.accent} particleDur="2.4s" particleR={3} />

          {/* modulation tensors */}
          <g transform="translate(420, 130)">
            {[0, 1, 2, 3].map((i) => (
              <rect key={i} x={i * 28} y={0} width={20} height={80} rx={3}
                fill={T4.bgRaised} stroke={T4.accent} strokeWidth={1.2}>
                <animate attributeName="opacity" values="0.4;1;0.4" dur="2s"
                  repeatCount="indefinite" begin={`${i * 0.2}s`} />
              </rect>
            ))}
            <text x={56} y={100} textAnchor="middle" fontFamily={F4.mono} fontSize={13} fill={T4.inkMute}
              style={{ letterSpacing: '0.06em' }}>
              M_A · M_B · E_A · E_B
            </text>
          </g>

          <text x={310} y={300} textAnchor="middle"
            fontFamily={F4.serif} fontSize={26} fill={T4.ink}>
            Q / V modulation
          </text>
          <text x={310} y={336} textAnchor="middle"
            fontFamily={F4.sans} fontSize={20} fill={T4.inkDim}>
            per-token probability shifts
          </text>
          <text x={310} y={376} textAnchor="middle"
            fontFamily={F4.mono} fontSize={15} fill={T4.accent}
            style={{ letterSpacing: '0.06em' }}>
            stance · voice · sycophancy
          </text>

          {/* link to shared bridge */}
          <Edge x1={560} y1={270} x2={750} y2={270}
            stroke={T4.accent} strokeWidth={1.5} dash="4 4"
            particle particleColor={T4.accent} particleDur="2.4s" particleR={3} curve={-20} />
        </g>

        {/* Mechanism B — right */}
        <g>
          <text x={1400} y={50} textAnchor="middle"
            fontFamily={F4.mono} fontSize={14} fill={T4.accent3}
            style={{ letterSpacing: '0.18em', textTransform: 'uppercase' }}>
            mechanism (b) — agentic
          </text>
          <rect x={1140} y={80} width={500} height={400} rx={12}
            fill="none" stroke={T4.accent3Dim} strokeDasharray="4 6" />

          <Node x={1560} y={170} r={28} fill={T4.bgRaised} stroke={T4.accent3}
            label="φ_R" labelPos="inside" fontSize={20} color={T4.accent3} />
          <text x={1560} y={222} textAnchor="middle" fontFamily={F4.mono} fontSize={13} fill={T4.inkMute}
            style={{ letterSpacing: '0.12em', textTransform: 'uppercase' }}>retrieve</text>

          <Edge x1={1530} y1={170} x2={1300} y2={170}
            stroke={T4.accent3} arrow
            particle particleColor={T4.accent3} particleDur="2.4s" particleR={3} />

          {/* knowledge graph */}
          <g transform="translate(1170, 110)">
            {[
              { x: 30, y: 30 }, { x: 90, y: 50 }, { x: 50, y: 80 },
              { x: 110, y: 100 }, { x: 30, y: 110 }, { x: 90, y: 130 },
            ].map((p, i) => (
              <Node key={i} x={p.x} y={p.y} r={8}
                fill={T4.bgRaised}
                stroke={i === 2 ? T4.accent3 : T4.rule}
                pulse={i === 2} pulseDelay={0} haloColor={T4.accent3} />
            ))}
            {/* edges */}
            {[[0,1],[0,2],[1,3],[2,3],[2,4],[3,5],[4,5]].map(([a, b], i) => {
              const pts = [{x:30,y:30},{x:90,y:50},{x:50,y:80},{x:110,y:100},{x:30,y:110},{x:90,y:130}];
              return (
                <line key={i} x1={pts[a].x} y1={pts[a].y} x2={pts[b].x} y2={pts[b].y}
                  stroke={T4.rule} strokeWidth={1} />
              );
            })}
          </g>

          <text x={1380} y={300} textAnchor="middle"
            fontFamily={F4.serif} fontSize={26} fill={T4.ink}>
            knowledge injection
          </text>
          <text x={1380} y={336} textAnchor="middle"
            fontFamily={F4.sans} fontSize={20} fill={T4.inkDim}>
            tool names, params, hints
          </text>
          <text x={1380} y={376} textAnchor="middle"
            fontFamily={F4.mono} fontSize={15} fill={T4.accent3}
            style={{ letterSpacing: '0.06em' }}>
            100% R@1 · 108-node graph
          </text>

          <Edge x1={1140} y1={270} x2={950} y2={270}
            stroke={T4.accent3} strokeWidth={1.5} dash="4 4"
            particle particleColor={T4.accent3} particleDur="2.4s" particleR={3} curve={20} />
        </g>
      </svg>

      <Chrome index={index} total={total} chapter="generalization" />
    </Slide>
  );
}

// ============================================================
// 14 — Agentic mode: teacher loop
// ============================================================
function S14_Agentic({ index, total }) {
  return (
    <Slide label="14 Agentic">
      <TitleBlock
        eyebrow="Agentic mode"
        title="Failures become hints. The graph grows."
        sub="On task failure, a teacher LLM writes a guidance note to the knowledge graph. φ_R retrieves it on the next attempt. Compilation in ~20s, no pretraining."
      />

      <svg width="1700" height="540" style={{ position: 'absolute', left: SP4.paddingX, bottom: 90 }}>
        <Defs />

        {/* Trial cycle */}
        <g transform="translate(40, 60)">
          {/* Trial node */}
          <Node x={140} y={200} r={50} fill={T4.bgPanel} stroke={T4.accent2}
            label="trial" labelPos="below" fontSize={20} color={T4.ink} />
          <text x={140} y={208} textAnchor="middle" fontFamily={F4.mono} fontSize={14} fill={T4.accent2}
            style={{ letterSpacing: '0.12em', textTransform: 'uppercase' }}>τ-bench</text>

          {/* Arrow to outcome */}
          <Edge x1={195} y1={200} x2={360} y2={200} stroke={T4.inkDim} arrow
            particle particleColor={T4.accent2} particleDur="2.4s" />

          {/* outcome diamond */}
          <Node x={420} y={200} r={32} shape="diamond" size={70}
            fill={T4.bgPanel} stroke={T4.bad}
            label="fail" labelPos="below" fontSize={18} color={T4.inkDim} />

          {/* Teacher writes */}
          <Edge x1={470} y1={200} x2={620} y2={200} stroke={T4.accent} arrow
            particle particleColor={T4.accent} particleDur="2.4s" particleDelay={0.6} />
          <text x={545} y={188} textAnchor="middle" fontFamily={F4.mono} fontSize={13} fill={T4.accent}
            style={{ letterSpacing: '0.12em', textTransform: 'uppercase' }}>
            teacher writes
          </text>

          {/* Knowledge graph */}
          <g transform="translate(640, 100)">
            <rect x={0} y={0} width={300} height={200} rx={12}
              fill={T4.bgPanel} stroke={T4.accent3} strokeWidth={1.5} />
            <text x={150} y={28} textAnchor="middle" fontFamily={F4.mono} fontSize={13} fill={T4.accent3}
              style={{ letterSpacing: '0.18em', textTransform: 'uppercase' }}>
              knowledge graph
            </text>
            {(() => {
              const nodes = [
                { x: 80, y: 70 }, { x: 150, y: 80 }, { x: 220, y: 65 },
                { x: 80, y: 130 }, { x: 150, y: 140 }, { x: 220, y: 130 },
                { x: 110, y: 175 }, { x: 190, y: 175 },
              ];
              return (
                <g>
                  {[[0,1],[1,2],[0,3],[1,4],[2,5],[3,4],[4,5],[3,6],[5,7],[6,7],[4,7]].map(([a,b], i) => (
                    <line key={i} x1={nodes[a].x} y1={nodes[a].y} x2={nodes[b].x} y2={nodes[b].y}
                      stroke={T4.rule} strokeWidth={1} />
                  ))}
                  {nodes.map((n, i) => (
                    <Node key={i} x={n.x} y={n.y} r={9}
                      fill={T4.bgRaised}
                      stroke={i === 7 ? T4.accent : T4.accent3Dim}
                      pulse={i === 7} haloColor={T4.accent} />
                  ))}
                  {/* "new" indicator */}
                  <text x={190} y={205} textAnchor="middle"
                    fontFamily={F4.mono} fontSize={11} fill={T4.accent}>
                    +note
                  </text>
                </g>
              );
            })()}
          </g>

          {/* φ_R retrieves */}
          <Edge x1={960} y1={200} x2={1110} y2={200} stroke={T4.accent3} arrow
            particle particleColor={T4.accent3} particleDur="2.4s" particleDelay={1.2} />
          <text x={1035} y={188} textAnchor="middle" fontFamily={F4.mono} fontSize={13} fill={T4.accent3}
            style={{ letterSpacing: '0.12em', textTransform: 'uppercase' }}>
            φ_R retrieves
          </text>

          {/* Hint slot */}
          <rect x={1130} y={150} width={220} height={100} rx={10}
            fill={T4.bgPanel} stroke={T4.accent3} strokeWidth={1.5} />
          <text x={1240} y={184} textAnchor="middle" fontFamily={F4.mono} fontSize={13} fill={T4.accent3}
            style={{ letterSpacing: '0.14em', textTransform: 'uppercase' }}>hint</text>
          <text x={1240} y={216} textAnchor="middle" fontFamily={F4.serif} fontSize={20} fill={T4.ink} fontStyle="italic">
            curated injection
          </text>

          {/* Loop back to trial */}
          <Edge x1={1240} y1={250} x2={1240} y2={350} stroke={T4.accentDim} dash="4 4" />
          <Edge x1={1240} y1={350} x2={140} y2={350} stroke={T4.accentDim} dash="4 4"
            particle particleColor={T4.accent} particleDur="3s" particleR={3} />
          <Edge x1={140} y1={350} x2={140} y2={252} stroke={T4.accentDim} dash="4 4" arrow />
          <text x={690} y={340} textAnchor="middle" fontFamily={F4.mono} fontSize={13} fill={T4.inkMute}
            style={{ letterSpacing: '0.18em', textTransform: 'uppercase' }}>
            next trial · informed
          </text>

          {/* Headline result */}
          <g transform="translate(1430, 30)">
            <rect x={0} y={0} width={220} height={400} rx={12}
              fill={T4.bgPanel} stroke={T4.rule} />
            <text x={110} y={40} textAnchor="middle" fontFamily={F4.mono} fontSize={13} fill={T4.inkMute}
              style={{ letterSpacing: '0.14em', textTransform: 'uppercase' }}>
              τ-bench airline
            </text>
            <text x={110} y={120} textAnchor="middle"
              fontFamily={F4.serif} fontSize={70} fill={T4.inkDim}>
              60%
            </text>
            <text x={110} y={150} textAnchor="middle"
              fontFamily={F4.mono} fontSize={13} fill={T4.inkMute}>
              baseline
            </text>
            <line x1={20} y1={180} x2={200} y2={180} stroke={T4.rule} />
            <text x={110} y={250} textAnchor="middle"
              fontFamily={F4.serif} fontSize={70} fill={T4.accent}>
              70%
            </text>
            <text x={110} y={280} textAnchor="middle"
              fontFamily={F4.mono} fontSize={13} fill={T4.accent}>
              HEXIS · 3 trials
            </text>
            <text x={110} y={340} textAnchor="middle"
              fontFamily={F4.sans} fontSize={18} fill={T4.inkDim}>
              + 2 rescues
            </text>
            <text x={110} y={368} textAnchor="middle"
              fontFamily={F4.sans} fontSize={16} fill={T4.inkMute}>
              from teacher loop
            </text>
          </g>
        </g>
      </svg>

      <Chrome index={index} total={total} chapter="agentic" />
    </Slide>
  );
}

// ============================================================
// 15 — Bottleneck Boundary
// ============================================================
function S15_Bottleneck({ index, total }) {
  return (
    <Slide label="15 Bottleneck">
      <TitleBlock
        eyebrow="What rank-16 can’t carry"
        title="The bottleneck has a precise edge."
        sub="Compiled enmeshment steers parametric knowledge but cannot inject novel content. This is the boundary; the three-layer architecture is the answer."
      />

      <div style={{
        position: 'absolute', left: SP4.paddingX, right: SP4.paddingX, top: 380,
        display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 56,
      }}>
        <div style={{ borderLeft: `3px solid ${T4.accent}`, paddingLeft: 28 }}>
          <div style={{
            fontFamily: F4.mono, fontSize: 16, color: T4.accent,
            letterSpacing: '0.18em', textTransform: 'uppercase', marginBottom: 24,
          }}>
            survives compilation
          </div>
          {[
            'Stance direction',
            'Confident voice & register',
            'Parametric-knowledge steering',
            'Procedural intuition (which path to try)',
            'Sycophancy resistance',
          ].map((s, i) => (
            <div key={i} style={{
              fontFamily: F4.serif, fontSize: 28, color: T4.ink,
              padding: '14px 0', borderBottom: `1px solid ${T4.ruleSoft}`,
              display: 'flex', alignItems: 'center', gap: 16,
            }}>
              <span style={{ color: T4.accent, fontFamily: F4.mono, fontSize: 18 }}>
                {String(i + 1).padStart(2, '0')}
              </span>
              {s}
            </div>
          ))}
        </div>

        <div style={{ borderLeft: `3px solid ${T4.inkMute}`, paddingLeft: 28 }}>
          <div style={{
            fontFamily: F4.mono, fontSize: 16, color: T4.inkMute,
            letterSpacing: '0.18em', textTransform: 'uppercase', marginBottom: 24,
          }}>
            needs the curated slot
          </div>
          {[
            'Specific numbers, statistics',
            'Unknown proper nouns',
            'Tool names, parameter values',
            'Citations & evidence sources',
            'Recently-observed failure notes',
          ].map((s, i) => (
            <div key={i} style={{
              fontFamily: F4.serif, fontSize: 28, color: T4.inkDim,
              padding: '14px 0', borderBottom: `1px solid ${T4.ruleSoft}`,
              display: 'flex', alignItems: 'center', gap: 16,
            }}>
              <span style={{ color: T4.inkMute, fontFamily: F4.mono, fontSize: 18 }}>
                {String(i + 1).padStart(2, '0')}
              </span>
              {s}
            </div>
          ))}
        </div>
      </div>

      <Chrome index={index} total={total} chapter="limits" />
    </Slide>
  );
}

// ============================================================
// 16 — Where this goes next
// ============================================================
function S16_Future({ index, total }) {
  const dirs = [
    { tag: 'Level 2', name: 'Gated blending', blurb: 'h′ = h + g(h) ⊙ f(h, M). A learned gate dissolves the multi-turn attractor.' },
    { tag: 'Level 3', name: 'Cross-attention', blurb: 'Treat M as a specialized expert. Richer content through the bottleneck.' },
    { tag: 'Adaptive', name: 'Per-layer rank', blurb: 'More capacity where empirical perturbation is largest. Bimodal usage suggests gain.' },
    { tag: 'Temporal', name: 'Phase-gated M', blurb: 'Decay, oscillation, application during generation but not prefill.' },
  ];

  return (
    <Slide label="16 Future">
      <TitleBlock
        eyebrow="One point validated. Five axes open."
        title="Where this goes next."
      />

      <div style={{
        position: 'absolute', left: SP4.paddingX, right: SP4.paddingX, top: 360,
        display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: 32,
      }}>
        {dirs.map((d, i) => (
          <div key={d.name} className="future-card" style={{
            background: T4.bgPanel, border: `1px solid ${T4.rule}`,
            borderRadius: 12, padding: '32px 36px',
            display: 'flex', gap: 28, alignItems: 'flex-start',
            opacity: 0, transform: 'translateY(24px)',
            animation: `futureCardIn 0.7s cubic-bezier(0.2, 0.8, 0.2, 1) ${0.1 + i * 0.12}s forwards`,
            transition: 'border-color 0.3s, transform 0.3s, box-shadow 0.3s',
            cursor: 'default',
          }}
            onMouseEnter={(e) => {
              e.currentTarget.style.borderColor = T4.accent;
              e.currentTarget.style.transform = 'translateY(-4px)';
              e.currentTarget.style.boxShadow = `0 12px 40px -12px ${T4.accent}`;
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.borderColor = T4.rule;
              e.currentTarget.style.transform = 'translateY(0)';
              e.currentTarget.style.boxShadow = 'none';
            }}>
            <div style={{
              fontFamily: F4.mono, fontSize: 14, color: T4.accent,
              letterSpacing: '0.18em', textTransform: 'uppercase',
              minWidth: 110, paddingTop: 8,
              padding: '6px 12px',
              border: `1px solid ${T4.accent}`, borderRadius: 999,
              animation: `tagPulse 2.4s ease-in-out ${0.6 + i * 0.3}s infinite`,
              alignSelf: 'flex-start',
            }}>
              {d.tag}
            </div>
            <div>
              <div style={{
                fontFamily: F4.serif, fontSize: 36, color: T4.ink, lineHeight: 1.05,
                marginBottom: 14,
              }}>
                {d.name}
              </div>
              <div style={{
                fontFamily: F4.sans, fontSize: 22, color: T4.inkDim, lineHeight: 1.4,
                textWrap: 'pretty',
              }}>
                {d.blurb}
              </div>
            </div>
          </div>
        ))}
      </div>
      <style>{`
        @keyframes futureCardIn {
          to { opacity: 1; transform: translateY(0); }
        }
        @keyframes tagPulse {
          0%, 100% { box-shadow: 0 0 0 0 rgba(212,138,73,0); }
          50% { box-shadow: 0 0 0 6px rgba(212,138,73,0.12); }
        }
      `}</style>

      <Chrome index={index} total={total} chapter="next" />
    </Slide>
  );
}

// ============================================================
// 17 — Summary / closing
// ============================================================
function S17_Summary({ index, total }) {
  return (
    <Slide label="17 Summary" padded={false}>
      {/* Animated background */}
      <svg width="1920" height="1080" style={{ position: 'absolute', inset: 0 }}>
        <Defs />
        <g opacity={0.6}>
          {Array.from({ length: 5 }).map((_, i) => {
            const cx = 1500, cy = 540;
            const angle = (i / 5) * Math.PI * 2 - Math.PI / 2;
            const r = 280;
            const nx = cx + Math.cos(angle) * r;
            const ny = cy + Math.sin(angle) * r;
            return (
              <g key={i}>
                <Edge x1={cx} y1={cy} x2={nx} y2={ny}
                  stroke={T4.rule} strokeWidth={1}
                  particle particleColor={T4.accent} particleDur="3s" particleDelay={i * 0.4} particleR={3} />
                <Node x={nx} y={ny} r={18} fill={T4.bgRaised} stroke={T4.accent2Dim} pulse pulseDelay={i * 0.4} haloColor={T4.accent2} />
              </g>
            );
          })}
          <Node x={1500} y={540} r={50} fill={T4.bgRaised} stroke={T4.accent} halo haloColor={T4.accent} />
          <text x={1500} y={550} textAnchor="middle" fontFamily={F4.mono} fontSize={28} fill={T4.accent}>
            φ
          </text>
        </g>
      </svg>

      <div style={{
        position: 'absolute', left: SP4.paddingX, top: 220, right: 800,
      }}>
        <div style={{
          fontFamily: F4.mono, fontSize: 22, color: T4.accent,
          letterSpacing: '0.24em', textTransform: 'uppercase', marginBottom: 40,
        }}>
          Recap
        </div>
        <h1 style={{
          fontFamily: F4.serif, fontWeight: 400, fontSize: 84,
          lineHeight: 1.02, margin: 0, color: T4.ink, letterSpacing: '-0.015em',
        }}>
          Memory doesn’t have to be<br />
          <span style={{ color: T4.accent, fontStyle: 'italic' }}>content</span>.
        </h1>

        <div style={{
          marginTop: 64, display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '32px 56px',
          maxWidth: 980,
        }}>
          {[
            { k: 'A primitive', v: 'enmeshed networks share the host’s forward pass' },
            { k: 'A schema', v: 'the Mind Tree compiles via φ at inference cost' },
            { k: 'A boundary', v: 'rank-16 carries disposition, not novel specifics' },
            { k: 'A bridge', v: 'one hidden-state channel, two mechanisms' },
          ].map((p, i) => (
            <div key={i}>
              <div style={{
                fontFamily: F4.mono, fontSize: 14, color: T4.accent,
                letterSpacing: '0.18em', textTransform: 'uppercase', marginBottom: 8,
              }}>{p.k}</div>
              <div style={{
                fontFamily: F4.serif, fontSize: 24, color: T4.inkDim, lineHeight: 1.3,
              }}>{p.v}</div>
            </div>
          ))}
        </div>

        <div style={{
          marginTop: 80, fontFamily: F4.mono, fontSize: 18, color: T4.inkMute,
          letterSpacing: '0.06em',
        }}>
          github.com/dgonier/hexis-public &nbsp;·&nbsp; hexis-vllm
        </div>
      </div>

      <div style={{
        position: 'absolute', bottom: 40, left: SP4.paddingX, right: SP4.paddingX,
        display: 'flex', justifyContent: 'space-between',
        fontFamily: F4.mono, fontSize: 24, color: T4.inkMute,
        letterSpacing: '0.08em', textTransform: 'uppercase',
      }}>
        <span>HEXIS · thank you</span>
        <span>{String(index).padStart(2, '0')} / {String(total).padStart(2, '0')}</span>
      </div>
    </Slide>
  );
}

Object.assign(window, { S13_TwoMech, S14_Agentic, S15_Bottleneck, S16_Future, S17_Summary });
