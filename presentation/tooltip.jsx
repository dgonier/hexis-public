// Reusable tooltip primitive + concept dictionary for hover explanations
const TT_TT = window.HEXIS_TOKENS;
const TT_F = window.FONTS;

// Concept dictionary — keyed term → { title, body, color? }
const CONCEPTS = {
  'M_A': { title: 'M_A — down-projection', body: 'd × r matrix. Compresses the host hidden state into a rank-r bottleneck. Shape: 2560 → 16.', color: TT_TT.accent },
  'M_B': { title: 'M_B — up-projection', body: 'r × d matrix. Reconstructs the perturbation back to model dimension. Shape: 16 → 2560.', color: TT_TT.accent },
  'E_A': { title: 'E_A — value down-projection', body: 'Mirrors M_A but for the V (value) stream. Decides which features of x_ℓ to extract.', color: TT_TT.accent2 },
  'E_B': { title: 'E_B — value up-projection', body: 'Up-projects the value perturbation back to d. Adds ΔV directly to V_ℓ.', color: TT_TT.accent2 },
  'phi': { title: 'φ — write function', body: 'A small network. Reads parallel-context hidden states, writes the M / E modulation tensors that steer the primary forward pass.', color: TT_TT.accent },
  'mindtree': { title: 'Mind Tree', body: 'Typed cognitive schema: identity · beliefs · strategies · memories · models · values. Each node carries conviction (strong / moderate / agnostic) and a novel flag.', color: TT_TT.accent2 },
  'rank': { title: 'rank r = 16', body: 'The bottleneck width. Rank 16 carries stance, voice, parametric steering. Novel specifics (numbers, names) cannot survive the compression.', color: TT_TT.accent },
  'stride': { title: 'stride-3 patching', body: 'φ writes M / E only into every third layer. Sufficient for stance; cheaper than every-layer patching.', color: TT_TT.accent3 },
  'curated': { title: 'Curated slot', body: '40–80 tokens of novel content (numbers, proper nouns, citations) selected by M activation scores. Lives in primary context — the only piece that has to.', color: TT_TT.accent2 },
  'expand': { title: 'expand_belief(id)', body: 'Tool the model can call when deeper evidence is needed. Pulls 0–200 tokens from the Mind Tree on demand. Layer 3.', color: TT_TT.accent3 },
  'host': { title: 'Frozen host', body: 'Base LLM. Weights never change. The same layers process both the parallel and primary passes.', color: TT_TT.ink },
  'parallel': { title: 'Parallel context', body: 'A second forward pass over the Mind Tree, processed by the same frozen host. Never occupies primary token positions.', color: TT_TT.accent },
  'sM': { title: 's_M — modulation scale', body: 'Scalar that controls how strongly the M perturbation is applied. Tuned per layer.', color: TT_TT.accent },
  'sE': { title: 's_E — value scale', body: 'Scalar that controls how strongly the E perturbation is applied to V.', color: TT_TT.accent2 },
  'B': { title: 'Blending function B', body: 'How M is fused into the host. Level 1 (this work): additive low-rank. Level 2: gated. Level 3: cross-attention.', color: TT_TT.accent },
};

function useTooltip() {
  const [tip, setTip] = React.useState(null);
  const onEnter = (key) => (e) => {
    const c = CONCEPTS[key];
    if (!c) return;
    const r = e.currentTarget.getBoundingClientRect();
    const slide = e.currentTarget.closest('[data-screen-label]');
    const sr = slide ? slide.getBoundingClientRect() : { left: 0, top: 0, width: 1920 };
    const scale = sr.width / 1920;
    setTip({
      x: (r.left + r.width / 2 - sr.left) / scale,
      y: (r.top - sr.top) / scale,
      ...c,
    });
  };
  const onLeave = () => setTip(null);
  return { tip, onEnter, onLeave };
}

// Render the floating tooltip in slide coords
function Tooltip({ tip }) {
  if (!tip) return null;
  const W = 380;
  const left = Math.max(20, Math.min(1920 - W - 20, tip.x - W / 2));
  return (
    <div style={{
      position: 'absolute',
      left, top: Math.max(20, tip.y - 130),
      width: W,
      background: TT_TT.bgRaised,
      border: `1px solid ${tip.color || TT_TT.accent}`,
      borderRadius: 10,
      padding: '16px 20px',
      pointerEvents: 'none',
      zIndex: 100,
      boxShadow: '0 12px 40px rgba(0,0,0,0.5)',
      animation: 'hexisFade 0.18s ease-out',
    }}>
      <div style={{
        fontFamily: TT_F.mono, fontSize: 14,
        color: tip.color || TT_TT.accent,
        letterSpacing: '0.14em', textTransform: 'uppercase',
        marginBottom: 10, fontWeight: 600,
      }}>
        {tip.title}
      </div>
      <div style={{
        fontFamily: TT_F.sans, fontSize: 18, lineHeight: 1.4,
        color: TT_TT.ink, textWrap: 'pretty',
      }}>
        {tip.body}
      </div>
    </div>
  );
}

// Wrap any element so it's hover-keyed to a concept
function H({ k, children, style = {}, on }) {
  return (
    <span
      onMouseEnter={on?.onEnter(k)}
      onMouseLeave={on?.onLeave}
      style={{
        cursor: 'help',
        borderBottom: `1px dotted ${TT_TT.accent}`,
        paddingBottom: 1,
        ...style,
      }}
    >{children}</span>
  );
}

// SVG hover hotspot
function SH({ k, x, y, w, h, on, rx = 4 }) {
  return (
    <rect
      x={x} y={y} width={w} height={h} rx={rx}
      fill="transparent"
      style={{ cursor: 'help' }}
      onMouseEnter={on?.onEnter(k)}
      onMouseLeave={on?.onLeave}
    />
  );
}

// Inject animation keyframes once
if (typeof document !== 'undefined' && !document.getElementById('hexis-tooltip-css')) {
  const st = document.createElement('style');
  st.id = 'hexis-tooltip-css';
  st.textContent = `@keyframes hexisFade { from { opacity: 0; transform: translateY(4px); } to { opacity: 1; transform: translateY(0); } }`;
  document.head.appendChild(st);
}

Object.assign(window, { CONCEPTS, useTooltip, Tooltip, H, SH });
