import { useState, useEffect } from "react";

const fib = (n) => {
  if (n <= 0) return 0;
  if (n <= 2) return 1;
  let a = 1, b = 1;
  for (let i = 3; i <= n; i++) [a, b] = [b, a + b];
  return b;
};

const PHI = (1 + Math.sqrt(5)) / 2;

export default function UniverseGravity() {
  const [stage, setStage] = useState(11);
  const [showTower, setShowTower] = useState(true);
  const modes = fib(stage);
  const G = 1 / (modes * modes);
  const gGrav = 1 / modes;

  const stageLabels = {
    3: "Minimum spacetime",
    5: "3D space",
    6: "Our 4D universe",
    7: "Dark sector begins",
    11: "Our Planck stage",
    13: "Deeper universe",
    15: "Much deeper",
  };

  const WedgeCircle = ({ n, radius, label, highlight }) => {
    const cx = radius + 4;
    const cy = radius + 4;
    const slices = Math.min(n, 120);
    const wedges = [];

    for (let i = 0; i < slices; i++) {
      const a1 = (2 * Math.PI * i) / slices - Math.PI / 2;
      const a2 = (2 * Math.PI * (i + 1)) / slices - Math.PI / 2;
      const x1 = cx + radius * Math.cos(a1);
      const y1 = cy + radius * Math.sin(a1);
      const x2 = cx + radius * Math.cos(a2);
      const y2 = cy + radius * Math.sin(a2);
      const large = a2 - a1 > Math.PI ? 1 : 0;
      const isFirst = i === 0;
      wedges.push(
        <path
          key={i}
          d={`M${cx},${cy} L${x1},${y1} A${radius},${radius} 0 ${large} 1 ${x2},${y2} Z`}
          fill={isFirst && highlight ? "#c9a227" : isFirst ? "#e8d48b" : "transparent"}
          stroke={n <= 40 ? "#334155" : "#94a3b8"}
          strokeWidth={n <= 40 ? 0.8 : 0.3}
          opacity={isFirst ? 1 : 0.7}
        />
      );
    }

    return (
      <svg width={(radius + 4) * 2} height={(radius + 4) * 2 + 28} viewBox={`0 0 ${(radius + 4) * 2} ${(radius + 4) * 2 + 28}`}>
        <circle cx={cx} cy={cy} r={radius} fill="#f1f5f9" stroke="#475569" strokeWidth={1.5} />
        {wedges}
        {highlight && n <= 60 && (
          <text x={cx} y={cy + radius + 18} textAnchor="middle" fontSize="11" fill="#334155" fontFamily="serif">
            {label}
          </text>
        )}
        {highlight && n > 60 && (
          <text x={cx} y={cy + radius + 18} textAnchor="middle" fontSize="10" fill="#334155" fontFamily="serif">
            {label}
          </text>
        )}
      </svg>
    );
  };

  const TowerBar = () => {
    const stages = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13];
    const maxF = fib(13);
    return (
      <div style={{ display: "flex", flexDirection: "column", gap: 2, padding: "0 8px" }}>
        {stages.map((s) => {
          const f = fib(s);
          const w = Math.max(8, (f / maxF) * 100);
          const isOurs = s === 6;
          const isPlanck = s === stage;
          const beyondPlanck = s > stage;
          return (
            <div key={s} style={{ display: "flex", alignItems: "center", gap: 6, opacity: beyondPlanck ? 0.35 : 1 }}>
              <span style={{ fontSize: 11, width: 18, textAlign: "right", fontFamily: "monospace", color: "#64748b" }}>{s}</span>
              <div style={{
                height: 16,
                width: `${w}%`,
                backgroundColor: isPlanck ? "#c9a227" : isOurs ? "#2563eb" : beyondPlanck ? "#cbd5e1" : "#64748b",
                borderRadius: 3,
                display: "flex",
                alignItems: "center",
                justifyContent: "flex-end",
                paddingRight: 6,
                transition: "all 0.3s",
              }}>
                <span style={{ fontSize: 9, color: "#fff", fontWeight: 600 }}>{f}</span>
              </div>
              <span style={{ fontSize: 9, color: "#94a3b8", fontStyle: "italic", whiteSpace: "nowrap" }}>
                {isOurs && "← us"}
                {isPlanck && s !== 6 && "← Planck"}
                {s === 7 && s !== stage && "dark"}
              </span>
            </div>
          );
        })}
        <div style={{ display: "flex", alignItems: "center", gap: 6, opacity: 0.25 }}>
          <span style={{ fontSize: 11, width: 18, textAlign: "right", fontFamily: "monospace", color: "#64748b" }}>∞</span>
          <div style={{ height: 16, width: "100%", backgroundColor: "#e2e8f0", borderRadius: 3, display: "flex", alignItems: "center", justifyContent: "center" }}>
            <span style={{ fontSize: 9, color: "#94a3b8" }}>∞ → Ω</span>
          </div>
        </div>
      </div>
    );
  };

  return (
    <div style={{
      maxWidth: 420,
      margin: "0 auto",
      fontFamily: "'Georgia', 'Times New Roman', serif",
      color: "#1e293b",
      padding: "16px 12px",
      background: "linear-gradient(180deg, #fefce8 0%, #fff 30%)",
      minHeight: "100vh",
    }}>
      <h2 style={{ textAlign: "center", fontSize: 20, fontWeight: 400, margin: "0 0 4px", letterSpacing: "0.02em" }}>
        The Universe as the Infinite Tower
      </h2>
      <p style={{ textAlign: "center", fontSize: 12, color: "#64748b", margin: "0 0 16px" }}>
        Maya / Chakra Math — From Nothing, Everything
      </p>

      <div style={{ display: "flex", gap: 8, justifyContent: "center", marginBottom: 16 }}>
        <button
          onClick={() => setShowTower(true)}
          style={{
            padding: "6px 14px", fontSize: 12, border: "1px solid #c9a227",
            borderRadius: 20, cursor: "pointer",
            background: showTower ? "#c9a227" : "transparent",
            color: showTower ? "#fff" : "#c9a227",
          }}
        >The Tower</button>
        <button
          onClick={() => setShowTower(false)}
          style={{
            padding: "6px 14px", fontSize: 12, border: "1px solid #c9a227",
            borderRadius: 20, cursor: "pointer",
            background: !showTower ? "#c9a227" : "transparent",
            color: !showTower ? "#fff" : "#c9a227",
          }}
        >Gravity</button>
      </div>

      {showTower ? (
        <div>
          <p style={{ fontSize: 13, lineHeight: 1.6, margin: "0 0 12px", color: "#475569" }}>
            The tower grows through stages. Each stage has F(N) positions — a Fibonacci number.
            Our universe lives at <span style={{ color: "#2563eb", fontWeight: 600 }}>stage 6</span> (8 positions → 4 spacetime dimensions).
            The <span style={{ color: "#c9a227", fontWeight: 600 }}>Planck stage</span> is where gravity saturates.
            Beyond it, stages fade into the infinite.
          </p>
          <TowerBar />
          <div style={{ marginTop: 16, padding: "12px", background: "#f8fafc", borderRadius: 8, border: "1px solid #e2e8f0" }}>
            <p style={{ fontSize: 12, margin: 0, color: "#475569", lineHeight: 1.6 }}>
              <strong>Planck stage:</strong> {stage} → <strong>{modes}</strong> gravitational modes
              <br />
              <strong>G</strong> = 1/{modes}² = {G.toExponential(3)}
              <br />
              <span style={{ fontSize: 11, color: "#94a3b8" }}>
                Drag the slider to explore different Planck stages
              </span>
            </p>
          </div>
        </div>
      ) : (
        <div>
          <p style={{ fontSize: 13, lineHeight: 1.6, margin: "0 0 12px", color: "#475569" }}>
            The whole (Ω = 1) is divided into <strong>{modes}</strong> equal parts.
            Each part is <strong>1/{modes}</strong> of the whole.
            The gold wedge is one mode's share.
            Gravity = (one share)² = <strong>1/{modes}²</strong>.
          </p>
          <div style={{ display: "flex", justifyContent: "center" }}>
            <WedgeCircle n={modes} radius={Math.min(130, modes <= 13 ? 100 : 130)} label={`1/${modes} of the whole`} highlight={true} />
          </div>
          <div style={{ textAlign: "center", marginTop: 8 }}>
            <div style={{ fontSize: 22, fontWeight: 300, color: "#c9a227" }}>
              G = 1/{modes}²
            </div>
            <div style={{ fontSize: 13, color: "#64748b" }}>
              = {G < 0.001 ? G.toExponential(3) : G.toFixed(4)}
            </div>
            {stage === 11 && (
              <div style={{ fontSize: 11, color: "#2563eb", marginTop: 4, fontStyle: "italic" }}>
                This is our universe's gravitational constant
              </div>
            )}
          </div>
        </div>
      )}

      <div style={{ marginTop: 20, padding: "0 4px" }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "baseline", marginBottom: 4 }}>
          <span style={{ fontSize: 12, color: "#64748b" }}>Planck stage: <strong style={{ color: "#1e293b", fontSize: 16 }}>{stage}</strong></span>
          <span style={{ fontSize: 11, color: "#94a3b8" }}>
            {stageLabels[stage] || `F(${stage}) = ${modes} modes`}
          </span>
        </div>
        <input
          type="range" min={3} max={17} value={stage}
          onChange={(e) => setStage(Number(e.target.value))}
          style={{ width: "100%", accentColor: "#c9a227" }}
        />
        <div style={{ display: "flex", justifyContent: "space-between", fontSize: 10, color: "#94a3b8" }}>
          <span>3 (max gravity)</span>
          <span>17 (weaker →)</span>
        </div>
      </div>

      <div style={{
        marginTop: 20, padding: 14, background: "#1e293b", borderRadius: 10,
        color: "#e2e8f0", fontSize: 12, lineHeight: 1.7,
      }}>
        <div style={{ fontSize: 14, color: "#c9a227", marginBottom: 6, fontWeight: 600 }}>
          What this picture says
        </div>
        {stage <= 5 ? (
          <p style={{ margin: 0 }}>
            At stage {stage}, there are only <strong>{modes}</strong> gravitational modes.
            Each is a large fraction (1/{modes}) of the whole.
            Gravity is <strong>strong</strong> — G = {G.toFixed(4)}.
            {stage < 6 && " But with fewer than 4 spacetime dimensions, gravity as we know it doesn't yet exist."}
          </p>
        ) : stage <= 11 ? (
          <p style={{ margin: 0 }}>
            {stage === 6 ? "Our universe has 4 dimensions from 8 positions at stage 6. " : ""}
            {stage === 11 ? "This is our universe. " : ""}
            The whole is divided into <strong>{modes}</strong> equal parts.
            Each mode's share is 1/{modes} — {stage === 11 ? "about 1.1%" : (100/modes).toFixed(1) + "%"} of the whole.
            Gravity is <strong>{stage === 11 ? "0.013%" : (G * 100).toFixed(3) + "%"}</strong> — {stage >= 9 ? "weak enough for atoms and life." : "still quite strong."}
          </p>
        ) : (
          <p style={{ margin: 0 }}>
            A hypothetical universe at Planck stage {stage} has <strong>{modes}</strong> modes.
            Each is a tiny fraction (1/{modes}) of the whole.
            Gravity is <strong>extremely weak</strong>: G = {G.toExponential(2)}.
            As stages increase toward ∞, gravity vanishes entirely — the undivided whole, Ω.
          </p>
        )}
      </div>

      <div style={{ marginTop: 16, textAlign: "center", fontSize: 11, color: "#94a3b8", lineHeight: 1.6 }}>
        G(N) = (φ + φ⁻¹)² / (φᴺ − ψᴺ)²
        <br />
        G × M² = 1 always — the whole is always one
      </div>
    </div>
  );
}
