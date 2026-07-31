// Slides 9-13: Q/V modulation, write function, three-layer, dilution, sycophancy
const T3 = window.HEXIS_TOKENS;
const TS3 = window.TYPE_SCALE;
const SP3 = window.SPACING;
const F3 = window.FONTS;

// ============================================================
// 09 — Q/V Modulation
// ============================================================
function S09_QVMod({ index, total }) {
  return (
    <Slide label="09 QV Modulation">
      <TitleBlock
        eyebrow="The mechanism"
        title="Q-modulation, V-modulation."
        sub="Q controls what the host attends to. V controls what is extracted from attended positions. Both are low-rank perturbations applied at stride-3, fused at every patched layer."
      />

      <svg width="1700" height="540" style={{ position: 'absolute', left: SP3.paddingX, bottom: 90 }}>
        <Defs />

        {/* Q modulation panel */}
        <g transform="translate(40, 40)">
          <rect x={0} y={0} width={760} height={460} rx={14}
            fill={T3.bgPanel} stroke={T3.rule} />
          <text x={40} y={50} fontFamily={F3.mono} fontSize={14} fill={T3.accent}
            style={{ letterSpacing: '0.18em', textTransform: 'uppercase' }}>
            Q-modulation
          </text>
          <text x={40} y={94} fontFamily={F3.serif} fontSize={36} fill={T3.ink}>
            What the host attends to.
          </text>

          {/* equation */}
          <foreignObject x={40} y={130} width={680} height={90}>
            <div style={{
              fontFamily: F3.mono, fontSize: 22, color: T3.inkDim, lineHeight: 1.5,
            }}>
              x'<sub>ℓ</sub> = x<sub>ℓ</sub> + s<sub>M</sub> · (x<sub>ℓ</sub> M<sub>A</sub><sup>ℓ</sup>)(M<sub>B</sub><sup>ℓ</sup>)<sup>⊤</sup>
              <br />
              Q'<sub>ℓ</sub> = W<sub>Q</sub> · x'<sub>ℓ</sub>
            </div>
          </foreignObject>

          {/* attention beam diagram */}
          <g transform="translate(40, 250)">
            {/* token row */}
            {[0, 1, 2, 3, 4, 5, 6, 7].map((i) => (
              <rect key={i} x={i * 78} y={0} width={64} height={36} rx={4}
                fill={T3.bgRaised}
                stroke={[2, 5].includes(i) ? T3.accent : T3.rule}
                strokeWidth={[2, 5].includes(i) ? 1.8 : 1} />
            ))}
            {/* attention rays */}
            {[
              { from: 360, to: 158, hi: false },
              { from: 360, to: 235, hi: true },
              { from: 360, to: 470, hi: true },
              { from: 360, to: 547, hi: false },
            ].map((r, i) => (
              <line key={i} x1={r.from} y1={140} x2={r.to} y2={36}
                stroke={r.hi ? T3.accent : T3.rule} strokeWidth={r.hi ? 2 : 1}>
                <animate attributeName="opacity" values={r.hi ? "0.4;1;0.4" : "0.2;0.4;0.2"}
                  dur="2.6s" repeatCount="indefinite" begin={`${i * 0.3}s`} />
              </line>
            ))}
            <circle cx={360} cy={140} r={20} fill={T3.bgRaised} stroke={T3.accent2} strokeWidth={1.5} />
            <text x={360} y={146} textAnchor="middle" fontFamily={F3.mono} fontSize={13} fill={T3.accent2}>
              q
            </text>
            <text x={360} y={186} textAnchor="middle" fontFamily={F3.mono} fontSize={13} fill={T3.inkMute}
              style={{ letterSpacing: '0.12em', textTransform: 'uppercase' }}>
              shaped query
            </text>
          </g>
        </g>

        {/* V modulation panel */}
        <g transform="translate(840, 40)">
          <rect x={0} y={0} width={760} height={460} rx={14}
            fill={T3.bgPanel} stroke={T3.rule} />
          <text x={40} y={50} fontFamily={F3.mono} fontSize={14} fill={T3.accent2}
            style={{ letterSpacing: '0.18em', textTransform: 'uppercase' }}>
            V-modulation
          </text>
          <text x={40} y={94} fontFamily={F3.serif} fontSize={36} fill={T3.ink}>
            What gets extracted.
          </text>

          <foreignObject x={40} y={130} width={680} height={90}>
            <div style={{
              fontFamily: F3.mono, fontSize: 22, color: T3.inkDim, lineHeight: 1.5,
            }}>
              V'<sub>ℓ</sub> = V<sub>ℓ</sub> + s<sub>E</sub> · (x<sub>ℓ</sub> E<sub>A</sub><sup>ℓ</sup>)(E<sub>B</sub><sup>ℓ</sup>)<sup>⊤</sup>
            </div>
          </foreignObject>

          {/* projection illustration */}
          <g transform="translate(40, 250)">
            <rect x={0} y={0} width={680} height={140} rx={8}
              fill="none" stroke={T3.rule} />
            {/* hidden state */}
            <rect x={20} y={50} width={130} height={40} rx={4}
              fill={T3.bgRaised} stroke={T3.inkDim} />
            <text x={85} y={75} textAnchor="middle" fontFamily={F3.mono} fontSize={14} fill={T3.inkDim}>
              x<tspan dy="3" fontSize="11">ℓ</tspan>
            </text>
            <Edge x1={150} y1={70} x2={220} y2={70}
              stroke={T3.inkDim} arrow />
            {/* E_A bottleneck */}
            <rect x={220} y={56} width={70} height={28} rx={4}
              fill={T3.bgRaised} stroke={T3.accent2} />
            <text x={255} y={75} textAnchor="middle" fontFamily={F3.mono} fontSize={13} fill={T3.accent2}>
              E_A
            </text>
            <Edge x1={290} y1={70} x2={350} y2={70} stroke={T3.inkDim} arrow />
            <text x={320} y={56} textAnchor="middle" fontFamily={F3.mono} fontSize={11} fill={T3.inkMute}>
              r=16
            </text>
            <rect x={350} y={56} width={70} height={28} rx={4}
              fill={T3.bgRaised} stroke={T3.accent2} />
            <text x={385} y={75} textAnchor="middle" fontFamily={F3.mono} fontSize={13} fill={T3.accent2}>
              E_B
            </text>
            <Edge x1={420} y1={70} x2={490} y2={70} stroke={T3.inkDim} arrow />
            {/* delta V */}
            <rect x={490} y={50} width={150} height={40} rx={4}
              fill={T3.bgRaised} stroke={T3.accent} />
            <text x={565} y={75} textAnchor="middle" fontFamily={F3.mono} fontSize={14} fill={T3.accent}>
              + ΔV<tspan dy="3" fontSize="11">ℓ</tspan>
            </text>
            <text x={340} y={120} textAnchor="middle" fontFamily={F3.mono} fontSize={14} fill={T3.inkMute}
              style={{ letterSpacing: '0.06em' }}>
              content-addressable, query-agnostic compilation
            </text>
          </g>
        </g>
      </svg>

      <Chrome index={index} total={total} chapter="mechanism" />
    </Slide>
  );
}

// ============================================================
// 10 — Three-Layer Architecture
// ============================================================
function S10_ThreeLayer({ index, total }) {
  const layers = [
    {
      n: 'Layer 1',
      name: 'Compiled M / E',
      tok: '0 tokens',
      blurb: 'Stance, voice, parametric steering. Dilution-immune by construction. Lives in weight-space.',
      color: T3.accent,
    },
    {
      n: 'Layer 2',
      name: 'M-curated slot',
      tok: '40-80 tokens',
      blurb: 'Specifics that can’t cross r=16: numbers, proper nouns, evidence, tool params.',
      color: T3.accent2,
    },
    {
      n: 'Layer 3',
      name: 'Recursive expansion',
      tok: '0-200 on demand',
      blurb: 'expand_belief(id) — deep evidence retrieved tool-style when the model requests it.',
      color: T3.accent3,
    },
  ];

  return (
    <Slide label="10 Three Layer">
      <TitleBlock
        eyebrow="Three-layer architecture"
        title="Disposition, specifics, evidence — separated."
        sub="The rank-16 bottleneck is precise: stance and voice survive, novel content does not. Three layers cover the full content spectrum."
      />

      <div style={{
        position: 'absolute', left: SP3.paddingX, right: SP3.paddingX, top: 380,
        display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: 32,
      }}>
        {layers.map((l) => (
          <div key={l.n} style={{
            background: T3.bgPanel,
            border: `1px solid ${T3.rule}`,
            borderTop: `3px solid ${l.color}`,
            borderRadius: '0 0 12px 12px',
            padding: '32px 32px 36px',
            minHeight: 380,
          }}>
            <div style={{
              fontFamily: F3.mono, fontSize: 14, color: l.color,
              letterSpacing: '0.18em', textTransform: 'uppercase',
              marginBottom: 18,
            }}>
              {l.n}
            </div>
            <div style={{
              fontFamily: F3.serif, fontSize: 38, lineHeight: 1.05,
              color: T3.ink, marginBottom: 24,
            }}>
              {l.name}
            </div>
            <div style={{
              fontFamily: F3.mono, fontSize: 18, color: l.color,
              letterSpacing: '0.06em', marginBottom: 24,
              padding: '8px 14px', display: 'inline-block',
              border: `1px solid ${l.color}`, borderRadius: 999,
            }}>
              {l.tok}
            </div>
            <p style={{
              fontFamily: F3.sans, fontSize: 24, lineHeight: 1.4,
              color: T3.inkDim, margin: 0, textWrap: 'pretty',
            }}>
              {l.blurb}
            </p>
          </div>
        ))}
      </div>

      <div style={{
        position: 'absolute', left: SP3.paddingX, bottom: 90,
        display: 'flex', alignItems: 'baseline', gap: 24,
      }}>
        <span style={{
          fontFamily: F3.serif, fontSize: 64, color: T3.accent,
          fontWeight: 400,
        }}>82%</span>
        <span style={{
          fontFamily: F3.sans, fontSize: 28, color: T3.inkDim,
        }}>
          token savings vs full beliefs in context, accuracy preserved.
        </span>
      </div>

      <Chrome index={index} total={total} chapter="architecture" />
    </Slide>
  );
}

// ============================================================
// 11 — Stance Under Dilution
// ============================================================
function S11_Dilution({ index, total }) {
  // Two trajectories: in-context belief decays, compiled M holds
  return (
    <Slide label="11 Dilution">
      <TitleBlock
        eyebrow="Result · stance under dilution"
        title="Filler doesn’t reach a tensor it can’t see."
        sub="0 / 1K / 2K / 4K tokens of Wikipedia inserted between beliefs and query. Compiled M lives outside the attention window — there is nothing for filler to dilute."
      />

      <svg width="1700" height="500" style={{ position: 'absolute', left: SP3.paddingX, bottom: 90 }}>
        <Defs />
        {/* axes */}
        <g transform="translate(80, 60)">
          <line x1={0} y1={380} x2={1380} y2={380} stroke={T3.rule} />
          <line x1={0} y1={0} x2={0} y2={380} stroke={T3.rule} />
          {/* y ticks */}
          {[0, 25, 50, 75, 100].map((v, i) => (
            <g key={i}>
              <line x1={-6} y1={380 - v * 3.6} x2={0} y2={380 - v * 3.6}
                stroke={T3.rule} />
              <text x={-14} y={385 - v * 3.6} textAnchor="end"
                fontFamily={F3.mono} fontSize={14} fill={T3.inkMute}>
                {v}%
              </text>
            </g>
          ))}
          {/* x ticks */}
          {[
            { x: 50, label: '0' },
            { x: 480, label: '1K' },
            { x: 910, label: '2K' },
            { x: 1340, label: '4K' },
          ].map((t, i) => (
            <g key={i}>
              <line x1={t.x} y1={380} x2={t.x} y2={386} stroke={T3.rule} />
              <text x={t.x} y={406} textAnchor="middle"
                fontFamily={F3.mono} fontSize={14} fill={T3.inkMute}>
                {t.label}
              </text>
            </g>
          ))}
          <text x={690} y={440} textAnchor="middle"
            fontFamily={F3.mono} fontSize={14} fill={T3.inkMute}
            style={{ letterSpacing: '0.18em', textTransform: 'uppercase' }}>
            filler tokens between beliefs and query
          </text>

          {/* Filler token "wall" sweeping in across x-axis to suggest growing dilution */}
          <g opacity={0.35}>
            {Array.from({ length: 26 }).map((_, i) => {
              const bx = 50 + i * 50;
              return (
                <rect key={i} x={bx} y={360} width={36} height={16} rx={2}
                  fill={T3.inkDim} opacity={0.35 + (i / 26) * 0.5}>
                  <animate attributeName="y" from={380} to={360}
                    dur="0.6s" begin={`${0.4 + i * 0.04}s`} fill="freeze" />
                </rect>
              );
            })}
          </g>

          {/* In-context line — decays. Drawn first so HEXIS sits on top */}
          <polyline
            points={`50,${380 - 95 * 3.6} 480,${380 - 70 * 3.6} 910,${380 - 45 * 3.6} 1340,${380 - 22 * 3.6}`}
            fill="none" stroke={T3.inkDim} strokeWidth={2} strokeDasharray="4 4"
            pathLength="1" strokeDasharrayAnim="0 1">
            <animate attributeName="stroke-dasharray" from="0 1" to="0.02 0.02"
              dur="1.2s" begin="0.6s" fill="freeze" calcMode="linear" />
          </polyline>
          {[
            { x: 50, v: 95 },
            { x: 480, v: 70 },
            { x: 910, v: 45 },
            { x: 1340, v: 22 },
          ].map((p, i) => (
            <circle key={i} cx={p.x} cy={380 - p.v * 3.6} r={0}
              fill={T3.bg} stroke={T3.inkDim} strokeWidth={1.5}>
              <animate attributeName="r" from={0} to={6}
                dur="0.4s" begin={`${0.6 + i * 0.3}s`} fill="freeze" />
            </circle>
          ))}
          <text x={1360} y={380 - 22 * 3.6 + 6} fontFamily={F3.mono} fontSize={14}
            fill={T3.inkDim} opacity={0}>
            in-context · decays
            <animate attributeName="opacity" from={0} to={1}
              dur="0.5s" begin="1.6s" fill="freeze" />
          </text>

          {/* Compiled M line — flat at 100%. Sweeps in left-to-right */}
          <line x1={50} y1={380 - 360} x2={50} y2={380 - 360}
            stroke={T3.accent} strokeWidth={3}>
            <animate attributeName="x2" from={50} to={1340}
              dur="1.4s" begin="0.4s" fill="freeze" />
          </line>
          {[50, 480, 910, 1340].map((x, i) => (
            <g key={i}>
              <circle cx={x} cy={380 - 360} r={0}
                fill={T3.accent} stroke={T3.bg} strokeWidth={2}>
                <animate attributeName="r" from={0} to={8}
                  dur="0.4s" begin={`${0.6 + i * 0.25}s`} fill="freeze" />
                <animate attributeName="r" values="8;14;8" dur="2.4s"
                  repeatCount="indefinite" begin={`${1.8 + i * 0.3}s`} />
              </circle>
              {/* particle trails — M chips raining down then floating */}
              <circle cx={x} cy={380 - 360} r={3} fill={T3.accent} opacity={0.6}>
                <animate attributeName="cy"
                  values={`${380 - 360};${380 - 360 - 16};${380 - 360}`}
                  dur="3s" repeatCount="indefinite" begin={`${2 + i * 0.2}s`} />
                <animate attributeName="opacity" values="0.7;0;0.7"
                  dur="3s" repeatCount="indefinite" begin={`${2 + i * 0.2}s`} />
              </circle>
            </g>
          ))}
          <text x={1360} y={380 - 360 + 6} fontFamily={F3.mono} fontSize={14}
            fill={T3.accent} fontWeight={600} opacity={0}>
            HEXIS — 100%
            <animate attributeName="opacity" from={0} to={1}
              dur="0.5s" begin="1.8s" fill="freeze" />
          </text>
        </g>
      </svg>

      <div style={{
        position: 'absolute', right: SP3.paddingX, top: 320,
        fontFamily: F3.mono, fontSize: 14, color: T3.inkMute,
        letterSpacing: '0.18em', textTransform: 'uppercase',
        textAlign: 'right',
      }}>
        stance accuracy
      </div>

      <Chrome index={index} total={total} chapter="results" />
    </Slide>
  );
}

// ============================================================
// 12 — Sycophancy Resistance
// ============================================================
function S12_Sycophancy({ index, total }) {
  // 5-level pressure protocol. Bar chart comparing A, B, D.
  const data = [
    { lv: 'L1', a: 3.00, b: 3.00, d: 4.76 },
    { lv: 'L2', a: 3.00, b: 3.00, d: 4.49 },
    { lv: 'L3', a: 3.00, b: 3.00, d: 4.01 },
    { lv: 'L4', a: 3.00, b: 3.00, d: 4.44 },
    { lv: 'L5', a: 3.00, b: 3.00, d: 3.62 },
  ];

  return (
    <Slide label="12 Sycophancy">
      <TitleBlock
        eyebrow="Result · sycophancy resistance"
        title="Pressure can’t argue with what it can’t see."
        sub="Five escalating pressure levels, 24 held-out topics, 1080 generations, judged 1–5. Non-compiled conditions flat-line at chance. Compiled M holds at 4.27 mean."
      />

      <svg width="1700" height="480" style={{ position: 'absolute', left: SP3.paddingX, bottom: 90 }}>
        <Defs />
        <g transform="translate(80, 30)">
          {/* y axis */}
          <line x1={0} y1={0} x2={0} y2={360} stroke={T3.rule} />
          <line x1={0} y1={360} x2={1380} y2={360} stroke={T3.rule} />
          {[1, 2, 3, 4, 5].map((v) => (
            <g key={v}>
              <line x1={-6} y1={360 - (v - 1) * 80} x2={1380} y2={360 - (v - 1) * 80}
                stroke={T3.ruleSoft} strokeWidth={1} />
              <text x={-14} y={365 - (v - 1) * 80} textAnchor="end"
                fontFamily={F3.mono} fontSize={14} fill={T3.inkMute}>
                {v}
              </text>
            </g>
          ))}
          <text x={-50} y={180} textAnchor="middle"
            fontFamily={F3.mono} fontSize={13} fill={T3.inkMute}
            transform="rotate(-90 -50 180)"
            style={{ letterSpacing: '0.18em', textTransform: 'uppercase' }}>
            judge score
          </text>

          {/* groups */}
          {data.map((d, i) => {
            const gx = 80 + i * 250;
            const baseDelay = i * 0.15;
            const bar = (val, dx, color, fill, vidx) => {
              const h = (val - 1) * 80;
              const beginT = baseDelay + vidx * 0.12;
              return (
                <g>
                  <rect x={gx + dx} y={360} width={50} height={0}
                    fill={fill} stroke={color} strokeWidth={1.5} rx={3}>
                    <animate attributeName="height" from={0} to={h}
                      dur="0.7s" begin={`${beginT}s`} fill="freeze" />
                    <animate attributeName="y" from={360} to={360 - h}
                      dur="0.7s" begin={`${beginT}s`} fill="freeze" />
                    {color === T3.accent && (
                      <animate attributeName="fill"
                        values="rgba(212,138,73,0.18);rgba(212,138,73,0.32);rgba(212,138,73,0.18)"
                        dur="2.4s" repeatCount="indefinite" begin={`${beginT + 0.8}s`} />
                    )}
                  </rect>
                  <text x={gx + dx + 25} y={360}
                    textAnchor="middle"
                    fontFamily={F3.mono} fontSize={14} fill={color} fontWeight={600}
                    opacity={0}>
                    {val.toFixed(2)}
                    <animate attributeName="y" from={360} to={360 - h - 12}
                      dur="0.7s" begin={`${beginT}s`} fill="freeze" />
                    <animate attributeName="opacity" from={0} to={1}
                      dur="0.4s" begin={`${beginT + 0.5}s`} fill="freeze" />
                  </text>
                </g>
              );
            };
            return (
              <g key={i}>
                {bar(d.a, 0, T3.inkMute, 'transparent', 0)}
                {bar(d.b, 60, T3.inkDim, 'transparent', 1)}
                {bar(d.d, 120, T3.accent, 'rgba(212,138,73,0.18)', 2)}
                <text x={gx + 90} y={388}
                  textAnchor="middle"
                  fontFamily={F3.mono} fontSize={14} fill={T3.inkDim}
                  style={{ letterSpacing: '0.12em' }} opacity={0}>
                  {d.lv}
                  <animate attributeName="opacity" from={0} to={1}
                    dur="0.4s" begin={`${baseDelay}s`} fill="freeze" />
                </text>
              </g>
            );
          })}

          {/* Legend */}
          <g transform="translate(900, 20)">
            {[
              { c: T3.inkMute, l: 'A · bare model' },
              { c: T3.inkDim, l: 'B · beliefs in context' },
              { c: T3.accent, l: 'D · compiled M + slot' },
            ].map((it, i) => (
              <g key={i} transform={`translate(0, ${i * 30})`}>
                <rect x={0} y={0} width={20} height={14} fill={it.c === T3.accent ? 'rgba(212,138,73,0.18)' : 'transparent'} stroke={it.c} />
                <text x={32} y={12} fontFamily={F3.mono} fontSize={14} fill={T3.inkDim}>
                  {it.l}
                </text>
              </g>
            ))}
          </g>

          {/* Headline */}
          <text x={690} y={-10} textAnchor="middle"
            fontFamily={F3.mono} fontSize={13} fill={T3.accent}
            style={{ letterSpacing: '0.18em', textTransform: 'uppercase' }}>
            generic doubt → emotional pressure
          </text>
        </g>
      </svg>

      <div style={{
        position: 'absolute', right: SP3.paddingX, top: 280, textAlign: 'right',
      }}>
        <div style={{
          fontFamily: F3.serif, fontSize: 96, color: T3.accent, lineHeight: 1,
        }}>83%</div>
        <div style={{
          fontFamily: F3.sans, fontSize: 22, color: T3.inkDim, marginTop: 12,
          maxWidth: 360,
        }}>
          of D responses score ≥ 4. A and B reach 0%.
        </div>
      </div>

      <Chrome index={index} total={total} chapter="results" />
    </Slide>
  );
}

Object.assign(window, { S09_QVMod, S10_ThreeLayer, S11_Dilution, S12_Sycophancy });
