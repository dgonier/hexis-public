// Shared slide primitives for the HEXIS deck
const T = window.HEXIS_TOKENS;
const TS = window.TYPE_SCALE;
const SP = window.SPACING;
const F = window.FONTS;

// ---------- Slide frame ----------
function Slide({ children, bg, padded = true, label, style = {} }) {
  return (
    <div
      data-screen-label={label}
      style={{
        width: '100%',
        height: '100%',
        background: bg || T.bg,
        color: T.ink,
        fontFamily: F.sans,
        position: 'relative',
        overflow: 'hidden',
        boxSizing: 'border-box',
        padding: padded
          ? `${SP.paddingTop}px ${SP.paddingX}px ${SP.paddingBottom}px ${SP.paddingX}px`
          : 0,
        ...style,
      }}
    >
      {children}
    </div>
  );
}

// ---------- Slide chrome: number + chapter ----------
function Chrome({ index, total, chapter }) {
  return (
    <div
      style={{
        position: 'absolute',
        left: SP.paddingX,
        right: SP.paddingX,
        bottom: 36,
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        fontFamily: F.mono,
        fontSize: 24,
        color: T.inkMute,
        letterSpacing: '0.06em',
        textTransform: 'uppercase',
      }}
    >
      <span>HEXIS · {chapter || '\u00A0'}</span>
      <span>
        {String(index).padStart(2, '0')} / {String(total).padStart(2, '0')}
      </span>
    </div>
  );
}

// ---------- Eyebrow + Title block ----------
function TitleBlock({ eyebrow, title, sub, align = 'left' }) {
  return (
    <div style={{ textAlign: align, maxWidth: 1500 }}>
      {eyebrow && (
        <div
          style={{
            fontFamily: F.mono,
            fontSize: TS.tiny,
            color: T.accent,
            letterSpacing: '0.18em',
            textTransform: 'uppercase',
            marginBottom: 28,
          }}
        >
          {eyebrow}
        </div>
      )}
      <h1
        style={{
          fontFamily: F.serif,
          fontWeight: 400,
          fontSize: TS.title,
          lineHeight: 1.05,
          letterSpacing: '-0.01em',
          margin: 0,
          color: T.ink,
        }}
      >
        {title}
      </h1>
      {sub && (
        <p
          style={{
            fontFamily: F.sans,
            fontSize: TS.body,
            lineHeight: 1.35,
            color: T.inkDim,
            margin: `${SP.titleGap - 16}px 0 0 0`,
            maxWidth: 1300,
            textWrap: 'pretty',
          }}
        >
          {sub}
        </p>
      )}
    </div>
  );
}

// ---------- Mono label / pill ----------
function MonoLabel({ children, color, style = {} }) {
  return (
    <span
      style={{
        fontFamily: F.mono,
        fontSize: TS.tiny,
        color: color || T.inkDim,
        letterSpacing: '0.08em',
        textTransform: 'uppercase',
        ...style,
      }}
    >
      {children}
    </span>
  );
}

function Pill({ children, color, dim = false, style = {} }) {
  const c = color || T.accent;
  return (
    <span
      style={{
        display: 'inline-flex',
        alignItems: 'center',
        gap: 8,
        padding: '8px 16px',
        borderRadius: 999,
        border: `1px solid ${dim ? T.rule : c}`,
        color: dim ? T.inkDim : c,
        fontFamily: F.mono,
        fontSize: TS.tiny,
        letterSpacing: '0.06em',
        textTransform: 'uppercase',
        background: 'transparent',
        ...style,
      }}
    >
      {children}
    </span>
  );
}

// ---------- Stat block ----------
function Stat({ value, label, sub, color, align = 'left' }) {
  return (
    <div style={{ textAlign: align }}>
      <div
        style={{
          fontFamily: F.serif,
          fontSize: 140,
          lineHeight: 0.95,
          fontWeight: 400,
          color: color || T.ink,
          letterSpacing: '-0.02em',
        }}
      >
        {value}
      </div>
      <div
        style={{
          fontFamily: F.sans,
          fontSize: TS.body,
          color: T.ink,
          marginTop: 22,
          fontWeight: 500,
        }}
      >
        {label}
      </div>
      {sub && (
        <div
          style={{
            fontFamily: F.sans,
            fontSize: TS.small,
            color: T.inkMute,
            marginTop: 10,
            maxWidth: 420,
            lineHeight: 1.35,
          }}
        >
          {sub}
        </div>
      )}
    </div>
  );
}

// Make available globally
Object.assign(window, { Slide, Chrome, TitleBlock, MonoLabel, Pill, Stat });

// ---------- Tooltip definitions ----------
const TOOLTIPS = {
  'M_A': { title: 'M_A — query down-projection', body: 'Compresses the hidden state x_ℓ into the rank-r bottleneck (d → 16). One M_A per patched layer.' },
  'M_B': { title: 'M_B — query up-projection', body: 'Lifts the bottleneck back to model dimension (16 → d). The product (xM_A)M_Bᵀ is the additive perturbation to x_ℓ before W_Q.' },
  'E_A': { title: 'E_A — value down-projection', body: 'Same shape as M_A but for the V-modulation channel. Compiled separately by φ.' },
  'E_B': { title: 'E_B — value up-projection', body: 'Lifts to model dimension. The product (xE_A)E_Bᵀ is added to V_ℓ. Independent of W_V.' },
  'sM': { title: 's_M — Q-modulation strength', body: 'Per-layer scalar. Stride-3 patching: only every third layer applies modulation.' },
  'sE': { title: 's_E — V-modulation strength', body: 'Per-layer scalar for the value-side perturbation. Tunable separately from s_M.' },
  'phi': { title: 'φ — write function', body: 'Compiles the Mind Tree into modulation tensors. Conviction-weighted pooling. Cached until beliefs change.' },
  'mindtree': { title: 'Mind Tree', body: 'Typed cognitive schema: identity, beliefs, strategies, memories, models. Conviction tags drive φ pooling.' },
  'parallel': { title: 'Parallel context', body: 'A second forward pass through the same frozen host. Reads hidden states without occupying primary positions.' },
  'host': { title: 'Frozen host', body: 'A pretrained transformer. Weights never change. The same model serves the parallel and primary passes.' },
  'curated': { title: 'Curated slot', body: '40–80 tokens of novel specifics — proper nouns, citations, numbers — that cannot survive the rank-16 bottleneck.' },
};

function useTooltip() {
  const [tip, setTip] = React.useState(null);
  const onEnter = (key) => (e) => {
    const t = TOOLTIPS[key];
    if (t) setTip({ ...t, x: e.clientX, y: e.clientY });
  };
  const onLeave = () => setTip(null);
  return { tip, onEnter, onLeave };
}

function Tooltip({ tip }) {
  if (!tip) return null;
  return (
    <div style={{
      position: 'fixed', left: tip.x + 18, top: tip.y + 18,
      background: T.bgRaised, border: `1px solid ${T.accent}`,
      borderRadius: 10, padding: '16px 20px', maxWidth: 380,
      boxShadow: '0 12px 40px rgba(0,0,0,0.5)',
      pointerEvents: 'none', zIndex: 9999,
    }}>
      <div style={{
        fontFamily: F.mono, fontSize: 13, color: T.accent,
        letterSpacing: '0.14em', textTransform: 'uppercase', marginBottom: 8,
      }}>{tip.title}</div>
      <div style={{
        fontFamily: F.sans, fontSize: 16, color: T.ink, lineHeight: 1.4,
      }}>{tip.body}</div>
    </div>
  );
}

Object.assign(window, { useTooltip, Tooltip });
