import { useState } from "react";

/*
  Full adaptation method comparison for NeurIPS paper.
  All metrics in O-notation where applicable.
  
  Variables:
    d = model dimension (e.g. 2560)
    r = adapter/modulation rank (e.g. 16)
    L = number of layers patched
    N = number of memory/belief tokens in context
    A = number of adaptations (personas, topics, tasks)
    M = number of base model updates
    T = tokens generated
*/

const columns = [
  { key: "method", label: "Method", width: 130 },
  { key: "trainPerModel", label: "Train cost\n(new base model)", width: 130 },
  { key: "trainPerAdapt", label: "Train cost\n(new adaptation)", width: 130 },
  { key: "totalTraining", label: "Total training\nscaling", width: 90 },
  { key: "inferenceLatency", label: "Inference overhead\n(per generated token)", width: 150 },
  { key: "vram", label: "Extra VRAM\n(at inference)", width: 130 },
  { key: "adaptive", label: "Adaptive", width: 65 },
  { key: "outsideCtx", label: "Outside\ncontext", width: 65 },
];

const rows = [
  {
    method: "LoRA (merged)",
    trainPerModel: { text: "O(M · A · epochs)", color: "red" },
    trainPerAdapt: { text: "O(epochs · |D|)", color: "red" },
    totalTraining: { text: "O(M × A)", color: "red" },
    inferenceLatency: { text: "O(0)", note: "absorbed into weights", color: "green" },
    vram: { text: "O(0)", note: "no extra", color: "green" },
    adaptive: false,
    outsideCtx: true,
    group: "weights"
  },
  {
    method: "LoRA (hot-swap)",
    trainPerModel: { text: "O(M · A · epochs)", color: "red" },
    trainPerAdapt: { text: "O(epochs · |D|)", color: "red" },
    totalTraining: { text: "O(M × A)", color: "red" },
    inferenceLatency: { text: "O(L · d · r)", note: "per token per layer", color: "yellow" },
    vram: { text: "O(L · d · r)", note: "~50MB/adapter", color: "yellow" },
    adaptive: false,
    outsideCtx: true,
    group: "weights"
  },
  {
    method: "Adapters",
    trainPerModel: { text: "O(M · A · epochs)", color: "red" },
    trainPerAdapt: { text: "O(epochs · |D|)", color: "red" },
    totalTraining: { text: "O(M × A)", color: "red" },
    inferenceLatency: { text: "O(L · d · r)", note: "FFN per layer", color: "yellow" },
    vram: { text: "O(L · d · r)", note: "adapter params", color: "yellow" },
    adaptive: false,
    outsideCtx: true,
    group: "weights"
  },
  {
    method: "Prefix Tuning",
    trainPerModel: { text: "O(M · A · epochs)", color: "red" },
    trainPerAdapt: { text: "O(epochs · |D|)", color: "red" },
    totalTraining: { text: "O(M × A)", color: "red" },
    inferenceLatency: { text: "O(L · P · d)", note: "attn over P prefix tokens", color: "yellow" },
    vram: { text: "O(L · P · d)", note: "prefix KV cache", color: "yellow" },
    adaptive: false,
    outsideCtx: false,
    group: "weights"
  },
  {
    method: "RAG",
    trainPerModel: { text: "O(0)", color: "green" },
    trainPerAdapt: { text: "O(0)", color: "green" },
    totalTraining: { text: "O(1)", color: "green" },
    inferenceLatency: { text: "O(T · N · d)", note: "attn over N retrieved tokens", color: "red" },
    vram: { text: "O(N · L · d)", note: "KV cache grows with N", color: "red" },
    adaptive: true,
    outsideCtx: false,
    group: "context"
  },
  {
    method: "Reflexion",
    trainPerModel: { text: "O(0)", color: "green" },
    trainPerAdapt: { text: "O(0)", color: "green" },
    totalTraining: { text: "O(1)", color: "green" },
    inferenceLatency: { text: "O(T · N · d)", note: "grows with reflections", color: "red" },
    vram: { text: "O(N · L · d)", note: "unbounded growth", color: "red" },
    adaptive: true,
    outsideCtx: false,
    group: "context"
  },
  {
    method: "System Prompt",
    trainPerModel: { text: "O(0)", color: "green" },
    trainPerAdapt: { text: "O(0)", color: "green" },
    totalTraining: { text: "O(1)", color: "green" },
    inferenceLatency: { text: "O(T · N · d)", note: "prompt tokens in attn", color: "yellow" },
    vram: { text: "O(N · L · d)", note: "KV cache", color: "yellow" },
    adaptive: true,
    outsideCtx: false,
    group: "context"
  },
  {
    method: "RepEng / ActAdd",
    trainPerModel: { text: "O(|C| · fwd)", note: "extract from contrastive set", color: "yellow" },
    trainPerAdapt: { text: "O(0)", note: "fixed direction", color: "green" },
    totalTraining: { text: "O(M)", color: "yellow" },
    inferenceLatency: { text: "O(L · d)", note: "one vector add/layer", color: "green" },
    vram: { text: "O(L · d)", note: "~10KB", color: "green" },
    adaptive: false,
    outsideCtx: true,
    group: "activations"
  },
  {
    method: "Enmeshed (HEXIS)",
    trainPerModel: { text: "O(epochs · |D|)", note: "train φ once", color: "yellow" },
    trainPerAdapt: { text: "O(1 fwd pass)", note: "compile beliefs → tensors", color: "green" },
    totalTraining: { text: "O(M + A)", color: "gold" },
    inferenceLatency: { text: "O(L · d · r)", note: "2 matmuls/layer, FIXED", color: "green" },
    vram: { text: "O(L · d · r)", note: "~50KB, FIXED", color: "green" },
    adaptive: true,
    outsideCtx: true,
    group: "enmeshed",
    highlight: true
  },
];

const colorMap = {
  red: { bg: "#FEE2E2", text: "#991B1B", border: "#FECACA" },
  yellow: { bg: "#FEF3C7", text: "#92400E", border: "#FDE68A" },
  green: { bg: "#D1FAE5", text: "#065F46", border: "#A7F3D0" },
  gold: { bg: "#FEF3C7", text: "#B45309", border: "#FDE68A" },
};

const groupColors = {
  weights: "#6B7280",
  context: "#7C3AED",
  activations: "#2563EB",
  enmeshed: "#DC2626",
};

const groupLabels = {
  weights: "Weight modification",
  context: "Context injection",
  activations: "Activation steering",
  enmeshed: "Enmeshed network",
};

export default function ComparisonTable() {
  const [hoveredRow, setHoveredRow] = useState(null);

  return (
    <div style={{
      fontFamily: "'IBM Plex Sans', 'Source Sans 3', system-ui, sans-serif",
      background: "#FAFAFA", minHeight: "100vh",
      display: "flex", flexDirection: "column", alignItems: "center",
      padding: "24px 12px"
    }}>
      <div style={{ maxWidth: 1050, width: "100%", overflowX: "auto" }}>
        <h2 style={{ fontSize: 17, fontWeight: 700, color: "#111", marginBottom: 4 }}>
          Table 1: Adaptation Method Comparison — All Costs in O-Notation
        </h2>
        <p style={{ fontSize: 11.5, color: "#666", marginBottom: 12, lineHeight: 1.5 }}>
          <em>d</em> = model dim, <em>r</em> = rank, <em>L</em> = layers, <em>N</em> = memory tokens in context,
          <em> T</em> = generated tokens, <em>A</em> = adaptations, <em>M</em> = model updates,
          <em> |D|</em> = training data, <em>|C|</em> = contrastive set, <em>P</em> = prefix length.
          Training costs are total GPU-hours; inference costs are per generation call.
        </p>

        <table style={{
          width: "100%", borderCollapse: "collapse",
          background: "white", border: "1px solid #E5E7EB",
          borderRadius: 3, overflow: "hidden",
          fontSize: 11
        }}>
          <thead>
            <tr style={{ background: "#F9FAFB", borderBottom: "2px solid #E5E7EB" }}>
              {columns.map((col) => (
                <th key={col.key} style={{
                  padding: "8px 8px", textAlign: col.key === "method" ? "left" : "center",
                  fontSize: 10, fontWeight: 700, color: "#374151",
                  whiteSpace: "pre-line", verticalAlign: "bottom",
                  borderRight: col.key === "totalTraining" ? "2px solid #E5E7EB" : "1px solid #F3F4F6",
                  width: col.width
                }}>
                  {col.label}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {rows.map((row, i) => {
              const prevGroup = i > 0 ? rows[i - 1].group : null;
              const showSep = prevGroup && prevGroup !== row.group;
              const gc = groupColors[row.group];

              return (
                <tr
                  key={i}
                  onMouseEnter={() => setHoveredRow(i)}
                  onMouseLeave={() => setHoveredRow(null)}
                  style={{
                    borderTop: showSep ? `2px solid ${gc}33` : "none",
                    borderBottom: "1px solid #F3F4F6",
                    background: row.highlight
                      ? (hoveredRow === i ? "#FFFBEB" : "#FFFDF7")
                      : (hoveredRow === i ? "#FAFAFA" : "white"),
                    transition: "background 0.1s"
                  }}
                >
                  {/* Method name */}
                  <td style={{
                    padding: "7px 8px", fontWeight: row.highlight ? 700 : 600,
                    color: gc, borderRight: "1px solid #F3F4F6",
                    display: "flex", alignItems: "center", gap: 6
                  }}>
                    <span style={{
                      width: 3, height: 20, borderRadius: 2,
                      background: gc, flexShrink: 0, opacity: 0.6
                    }} />
                    {row.method}
                  </td>

                  {/* Training per model */}
                  <td style={{ padding: "5px 6px", textAlign: "center", borderRight: "1px solid #F3F4F6" }}>
                    <CostCell {...row.trainPerModel} />
                  </td>

                  {/* Training per adaptation */}
                  <td style={{ padding: "5px 6px", textAlign: "center", borderRight: "1px solid #F3F4F6" }}>
                    <CostCell {...row.trainPerAdapt} />
                  </td>

                  {/* Total scaling */}
                  <td style={{
                    padding: "5px 6px", textAlign: "center",
                    borderRight: "2px solid #E5E7EB",
                    fontFamily: "'IBM Plex Mono', monospace",
                    fontSize: 12, fontWeight: 800,
                    color: colorMap[row.totalTraining.color].text
                  }}>
                    {row.totalTraining.text}
                  </td>

                  {/* Inference latency */}
                  <td style={{ padding: "5px 6px", textAlign: "center", borderRight: "1px solid #F3F4F6" }}>
                    <CostCell {...row.inferenceLatency} />
                  </td>

                  {/* VRAM */}
                  <td style={{ padding: "5px 6px", textAlign: "center", borderRight: "1px solid #F3F4F6" }}>
                    <CostCell {...row.vram} />
                  </td>

                  {/* Adaptive */}
                  <td style={{ padding: "5px 4px", textAlign: "center", borderRight: "1px solid #F3F4F6" }}>
                    <BoolCell value={row.adaptive} />
                  </td>

                  {/* Outside context */}
                  <td style={{ padding: "5px 4px", textAlign: "center" }}>
                    <BoolCell value={row.outsideCtx} />
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>

        {/* Key insight callout */}
        <div style={{
          marginTop: 14, padding: "10px 14px",
          background: "#FFFBEB", border: "1px solid #FDE68A", borderRadius: 3,
          fontSize: 11.5, color: "#92400E", lineHeight: 1.6
        }}>
          <strong>Key comparison:</strong> Context methods (RAG, Reflexion) have <strong>O(T · N · d)</strong> inference cost
          — it grows with both generated tokens and memory size.
          Enmeshed networks have <strong>O(T · L · d · r)</strong> — it grows with generated tokens
          but is <strong>constant</strong> in memory size N.
          100 beliefs or 10,000 beliefs: same inference cost.
          The cost of beliefs is paid once during compilation, not per generated token.
        </div>

        {/* Scaling example */}
        <div style={{
          marginTop: 10, padding: "10px 14px",
          background: "white", border: "1px solid #E5E7EB", borderRadius: 3,
          fontSize: 11.5, color: "#374151", lineHeight: 1.6
        }}>
          <strong>Scaling example:</strong> 100 personas, Qwen 4B → 8B upgrade.
          <div style={{ display: "flex", flexWrap: "wrap", gap: 6, marginTop: 6 }}>
            <Tag bg="#FEE2E2" color="#991B1B">LoRA: retrain 100 adapters — O(100 · epochs)</Tag>
            <Tag bg="#FEF3C7" color="#92400E">HEXIS: retrain φ once + 100 fwd passes — O(1 · epochs + 100)</Tag>
            <Tag bg="#D1FAE5" color="#065F46">RAG: O(0) training — but O(N) per token at inference forever</Tag>
          </div>
        </div>

        {/* Group legend */}
        <div style={{ marginTop: 16, display: "flex", gap: 20, flexWrap: "wrap" }}>
          {Object.entries(groupLabels).map(([key, label]) => (
            <div key={key} style={{ display: "flex", alignItems: "center", gap: 6 }}>
              <span style={{ width: 3, height: 14, borderRadius: 2, background: groupColors[key] }} />
              <span style={{ fontSize: 11, color: "#555" }}>{label}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

function CostCell({ text, note, color }) {
  const c = colorMap[color];
  return (
    <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 2 }}>
      <span style={{
        fontSize: 10.5, fontWeight: 600, padding: "2px 7px", borderRadius: 3,
        background: c.bg, color: c.text, border: `1px solid ${c.border}`,
        fontFamily: text.startsWith("O(") ? "'IBM Plex Mono', monospace" : "inherit",
        whiteSpace: "nowrap"
      }}>
        {text}
      </span>
      {note && <span style={{ fontSize: 7.5, color: "#999", lineHeight: 1.2, maxWidth: 120, textAlign: "center" }}>{note}</span>}
    </div>
  );
}

function BoolCell({ value }) {
  return (
    <span style={{
      fontSize: 13, fontWeight: 700,
      color: value ? "#065F46" : "#991B1B"
    }}>
      {value ? "✓" : "✗"}
    </span>
  );
}

function Tag({ children, bg, color }) {
  return (
    <span style={{ padding: "3px 8px", borderRadius: 3, background: bg, color, fontSize: 10.5, fontWeight: 600 }}>
      {children}
    </span>
  );
}
