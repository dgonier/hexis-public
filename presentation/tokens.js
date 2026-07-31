// Design tokens for HEXIS deck
window.HEXIS_TOKENS = {
  // Colors — deep ink palette with warm accent
  bg: '#0e1014',
  bgPanel: '#15181f',
  bgRaised: '#1c2029',
  ink: '#eef0f3',
  inkDim: '#aab1bd',
  inkMute: '#6f7682',
  rule: '#272b34',
  ruleSoft: '#1e222b',
  // Accents
  accent: 'oklch(0.74 0.15 52)',     // warm orange — "compiled M"
  accentDim: 'oklch(0.56 0.12 52)',
  accent2: 'oklch(0.78 0.09 200)',   // teal — "primary context / host"
  accent2Dim: 'oklch(0.56 0.07 200)',
  accent3: 'oklch(0.78 0.10 290)',   // violet — "parallel context / phi"
  accent3Dim: 'oklch(0.56 0.08 290)',
  good: 'oklch(0.78 0.12 145)',
  bad: 'oklch(0.68 0.16 25)',
};

window.TYPE_SCALE = {
  display: 110,
  title: 64,
  subtitle: 44,
  body: 32,
  small: 26,
  tiny: 22,
  mono: 24,
};

window.SPACING = {
  paddingTop: 100,
  paddingBottom: 80,
  paddingX: 110,
  titleGap: 52,
  itemGap: 28,
};

window.FONTS = {
  serif: '"Source Serif 4", "Source Serif Pro", "Iowan Old Style", Georgia, serif',
  sans: '"Inter", system-ui, -apple-system, sans-serif',
  mono: '"JetBrains Mono", "Berkeley Mono", ui-monospace, "SF Mono", Menlo, monospace',
};
