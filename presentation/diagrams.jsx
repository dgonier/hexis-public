// Reusable animated node-graph components for the HEXIS deck
const TT = window.HEXIS_TOKENS;
const TTS = window.TYPE_SCALE;
const FF = window.FONTS;

// ============================================================
// SVG primitives
// ============================================================

function Node({
  x, y, r = 26, label, sublabel,
  fill = TT.bgRaised, stroke = TT.rule, color = TT.ink,
  pulse = false, pulseDelay = 0, halo = false, haloColor,
  shape = 'circle',  // 'circle' | 'square' | 'diamond'
  size,             // for square/diamond
  textOffset = 0,
  fontSize = 18,
  labelPos = 'below', // 'below' | 'above' | 'right' | 'left' | 'inside'
}) {
  const rr = size || r * 2;
  const sub = sublabel ? (
    <text
      x={x}
      y={labelPos === 'below' ? y + r + 26 + 22 : y - r - 14 - 22}
      textAnchor="middle"
      fontFamily={FF.mono}
      fontSize={13}
      fill={TT.inkMute}
      style={{ letterSpacing: '0.06em', textTransform: 'uppercase' }}
    >
      {sublabel}
    </text>
  ) : null;

  let labelEl = null;
  if (label) {
    let lx = x, ly = y, anchor = 'middle';
    if (labelPos === 'below') { ly = y + r + 26 + textOffset; }
    else if (labelPos === 'above') { ly = y - r - 14 + textOffset; }
    else if (labelPos === 'right') { lx = x + r + 14; ly = y + 6; anchor = 'start'; }
    else if (labelPos === 'left') { lx = x - r - 14; ly = y + 6; anchor = 'end'; }
    else if (labelPos === 'inside') { ly = y + 6; }
    labelEl = (
      <text x={lx} y={ly} textAnchor={anchor} fontFamily={FF.sans} fontSize={fontSize} fill={color} fontWeight={500}>
        {label}
      </text>
    );
  }

  let shapeEl;
  if (shape === 'square') {
    shapeEl = (
      <rect
        x={x - rr / 2} y={y - rr / 2} width={rr} height={rr} rx={6}
        fill={fill} stroke={stroke} strokeWidth={1.5}
      />
    );
  } else if (shape === 'diamond') {
    shapeEl = (
      <rect
        x={x - rr / 2} y={y - rr / 2} width={rr} height={rr} rx={4}
        transform={`rotate(45 ${x} ${y})`}
        fill={fill} stroke={stroke} strokeWidth={1.5}
      />
    );
  } else {
    shapeEl = (
      <circle cx={x} cy={y} r={r} fill={fill} stroke={stroke} strokeWidth={1.5} />
    );
  }

  return (
    <g>
      {halo && (
        <circle cx={x} cy={y} r={r + 12}
          fill="none" stroke={haloColor || stroke} strokeWidth={1} opacity={0.35}
        >
          <animate attributeName="r" values={`${r + 6};${r + 22};${r + 6}`} dur="2.4s" repeatCount="indefinite" begin={`${pulseDelay}s`} />
          <animate attributeName="opacity" values="0.5;0;0.5" dur="2.4s" repeatCount="indefinite" begin={`${pulseDelay}s`} />
        </circle>
      )}
      {shapeEl}
      {pulse && (
        <circle cx={x} cy={y} r={r} fill="none" stroke={haloColor || stroke} strokeWidth={1.5}>
          <animate attributeName="r" values={`${r};${r + 18}`} dur="1.8s" repeatCount="indefinite" begin={`${pulseDelay}s`} />
          <animate attributeName="opacity" values="0.7;0" dur="1.8s" repeatCount="indefinite" begin={`${pulseDelay}s`} />
        </circle>
      )}
      {labelEl}
      {sub}
    </g>
  );
}

// Edge: line + optional moving particle
function Edge({
  x1, y1, x2, y2,
  stroke = TT.rule, strokeWidth = 1.5, dash,
  particle = false, particleColor, particleDur = '2.6s', particleDelay = 0, particleR = 4,
  arrow = false, opacity = 1, curve = 0,
}) {
  // Optional curve via control point perpendicular offset
  let pathD = `M ${x1} ${y1} L ${x2} ${y2}`;
  let isPath = false;
  if (curve) {
    const mx = (x1 + x2) / 2, my = (y1 + y2) / 2;
    const dx = x2 - x1, dy = y2 - y1;
    const len = Math.sqrt(dx * dx + dy * dy) || 1;
    const px = -dy / len, py = dx / len;
    const cx = mx + px * curve, cy = my + py * curve;
    pathD = `M ${x1} ${y1} Q ${cx} ${cy} ${x2} ${y2}`;
    isPath = true;
  }

  return (
    <g opacity={opacity}>
      <path
        d={pathD}
        fill="none"
        stroke={stroke}
        strokeWidth={strokeWidth}
        strokeDasharray={dash}
        markerEnd={arrow ? 'url(#arrowhead)' : undefined}
      />
      {particle && (
        <circle r={particleR} fill={particleColor || TT.accent}>
          <animateMotion dur={particleDur} repeatCount="indefinite" begin={`${particleDelay}s`} path={pathD} />
        </circle>
      )}
    </g>
  );
}

function Defs() {
  return (
    <defs>
      <marker id="arrowhead" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
        <path d="M 0 0 L 10 5 L 0 10 Z" fill={TT.inkDim} />
      </marker>
      <marker id="arrowhead-accent" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
        <path d="M 0 0 L 10 5 L 0 10 Z" fill={TT.accent} />
      </marker>
      <marker id="arrowhead-accent2" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
        <path d="M 0 0 L 10 5 L 0 10 Z" fill={TT.accent2} />
      </marker>
      <linearGradient id="hostGrad" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0%" stopColor={TT.bgRaised} />
        <stop offset="100%" stopColor={TT.bgPanel} />
      </linearGradient>
      <linearGradient id="accentGrad" x1="0" y1="0" x2="1" y2="0">
        <stop offset="0%" stopColor={TT.accent} stopOpacity="0" />
        <stop offset="100%" stopColor={TT.accent} stopOpacity="0.9" />
      </linearGradient>
    </defs>
  );
}

// ============================================================
// Host transformer column — n stacked layers
// ============================================================
function HostColumn({
  x, y, layers = 8, layerW = 220, layerH = 36, gap = 10,
  patched = [], // indices that get modulation
  label = 'frozen host model',
  patchedColor = TT.accent,
  showQV = false,
}) {
  const totalH = layers * layerH + (layers - 1) * gap;
  return (
    <g>
      {/* Frame */}
      <rect
        x={x - 14} y={y - 14}
        width={layerW + 28} height={totalH + 28}
        rx={10}
        fill="none" stroke={TT.rule} strokeWidth={1} strokeDasharray="3 4"
      />
      <text
        x={x + layerW / 2} y={y - 24}
        textAnchor="middle" fontFamily={FF.mono} fontSize={13}
        fill={TT.inkMute} style={{ letterSpacing: '0.12em', textTransform: 'uppercase' }}
      >
        {label}
      </text>
      {Array.from({ length: layers }).map((_, i) => {
        const yi = y + i * (layerH + gap);
        const isPatched = patched.includes(i);
        return (
          <g key={i}>
            <rect
              x={x} y={yi} width={layerW} height={layerH} rx={4}
              fill={TT.bgRaised}
              stroke={isPatched ? patchedColor : TT.rule}
              strokeWidth={isPatched ? 1.5 : 1}
            />
            <text
              x={x + 12} y={yi + layerH / 2 + 5}
              fontFamily={FF.mono} fontSize={12} fill={TT.inkMute}
            >
              L{String(i).padStart(2, '0')}
            </text>
            {isPatched && (
              <>
                <text
                  x={x + layerW - 12} y={yi + layerH / 2 + 5}
                  textAnchor="end"
                  fontFamily={FF.mono} fontSize={12} fill={patchedColor}
                >
                  {showQV ? 'Q+V' : '+M'}
                </text>
                <circle cx={x + layerW + 8} cy={yi + layerH / 2} r={3} fill={patchedColor}>
                  <animate attributeName="opacity" values="0.4;1;0.4" dur="2s" repeatCount="indefinite" begin={`${i * 0.1}s`} />
                </circle>
              </>
            )}
          </g>
        );
      })}
    </g>
  );
}

Object.assign(window, { Node, Edge, Defs, HostColumn });
