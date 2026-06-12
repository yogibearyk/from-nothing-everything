import { useState } from "react";

const fib = (n) => {
  if (n <= 0) return 0;
  if (n <= 2) return 1;
  let a = 1, b = 1;
  for (let i = 3; i <= n; i++) [a, b] = [b, a + b];
  return b;
};

const STAGES = [
  { n: 1, label: "Identity", desc: "The golden ratio φ. The first self-similar split. Nothing physical yet — just the seed of structure.", color: "#fef3c7", ring: false },
  { n: 2, label: "Duality", desc: "The first pairing: φ meets its mirror φ⁻¹. Still pre-physical — mathematics bootstrapping itself.", color: "#fef3c7", ring: false },
  { n: 3, label: "A line", desc: "2 positions → 1 dimension. The simplest spatial extent. A universe that is just a thread.", color: "#fde68a", ring: true },
  { n: 4, label: "A surface", desc: "3 positions → 2 dimensions. A sheet. Flatland. Gravity has no dynamics here — there's nowhere for it to curve.", color: "#fcd34d", ring: true },
  { n: 5, label: "Space", desc: "5 positions → 3 dimensions. Volume appears — up/down, left/right, forward/back. But no time yet: a frozen sculpture.", color: "#fbbf24", ring: true },
  { n: 6, label: "Our Universe", desc: "8 positions → 4 dimensions: 3 of space + 1 of time. Light moves. Atoms form. Stars burn. Chemistry happens. Life. Us. Everything we have ever seen lives here.", color: "#2563eb", ring: true, highlight: true },
  { n: 7, label: "The Dark Sector", desc: "13 positions. The first stage beyond ours. Dark matter candidates, dark bosons — particles that interact gravitationally but barely touch light. We detect their pull but cannot see them.", color: "#6366f1", ring: true },
  { n: 8, label: "Deeper dark", desc: "21 positions. More hidden particles, screened by D² ≈ 0.27 from stage 7. Even harder to detect. Like hearing music through two walls instead of one.", color: "#4f46e5", ring: true },
  { n: 9, label: "Fading signal", desc: "34 positions. Three walls of screening. The signal from here is 2% of stage 6. Our best instruments are reaching toward this level.", color: "#4338ca", ring: true },
  { n: 10, label: "Almost silent", desc: "55 positions. Four walls. The signal is 0.5% of stage 6. Barely a whisper in the data.", color: "#3730a3", ring: true },
  { n: 11, label: "The Planck Stage", desc: "89 positions total. This is the floor where gravity lives. The VEV tower first exceeds the Planck mass here. Beyond this stage, energies surpass what gravity can handle perturbatively.", color: "#c9a227", ring: true, isPlanck: true },
  { n: 12, label: "Beyond the Planck", desc: "144 positions. Trans-Planckian — gravity is non-perturbative. Black holes, topology change, quantum foam. The tower continues, but our physics cannot follow.", color: "#78716c", ring: true },
  { n: 13, label: "And deeper still…", desc: "233 positions. The tower never stops. Each stage adds more modes, each screened by another factor of D². The signal from here is unimaginably faint.", color: "#a8a29e", ring: true },
];

const OnionRing = ({ stage, maxRadius, selectedStage, onSelect }) => {
  const idx = stage.n - 3;
  if (!stage.ring) return null;
  const totalRings = 11;
  const r = ((idx + 1) / totalRings) * maxRadius;
  const thickness = maxRadius / totalRings - 1;
  const isSelected = selectedStage === stage.n;
  const opacity = stage.n > 11 ? 0.3 : stage.n > 7 ? 0.5 + (11 - stage.n) * 0.1 : 1;

  return (
    <circle
      cx={maxRadius + 10}
      cy={maxRadius + 10}
      r={r}
      fill="none"
      stroke={isSelected ? "#fff" : stage.color}
      strokeWidth={isSelected ? 4 : thickness}
      opacity={opacity}
      onClick={() => onSelect(stage.n)}
      style={{ cursor: "pointer" }}
    />
  );
};

export default function PhysicalTower() {
  const [selectedStage, setSelectedStage] = useState(6);
  const [view, setView] = useState("onion");
  const selected = STAGES.find((s) => s.n === selectedStage) || STAGES[5];
  const modes = fib(selectedStage);
  const G = 1 / (modes * modes);

  const maxR = 150;

  return (
    <div style={{
      maxWidth: 420, margin: "0 auto", fontFamily: "'Georgia', serif",
      color: "#1e293b", padding: "12px", background: "#0f172a", minHeight: "100vh",
    }}>
      <h2 style={{ textAlign: "center", fontSize: 18, fontWeight: 400, color: "#fef3c7", margin: "8px 0 2px", letterSpacing: "0.03em" }}>
        What the Tower Looks Like
      </h2>
      <p style={{ textAlign: "center", fontSize: 11, color: "#64748b", margin: "0 0 12px" }}>
        Tap a ring to explore what lives at each stage
      </p>

      {/* Cosmic Onion */}
      <div style={{ display: "flex", justifyContent: "center", position: "relative" }}>
        <svg width={maxR * 2 + 20} height={maxR * 2 + 20}>
          {/* Background glow */}
          <defs>
            <radialGradient id="glow">
              <stop offset="0%" stopColor="#2563eb" stopOpacity="0.15" />
              <stop offset="40%" stopColor="#4f46e5" stopOpacity="0.08" />
              <stop offset="100%" stopColor="#0f172a" stopOpacity="0" />
            </radialGradient>
          </defs>
          <circle cx={maxR + 10} cy={maxR + 10} r={maxR} fill="url(#glow)" />

          {/* Rings from outside in */}
          {[...STAGES].reverse().map((s) => (
            <OnionRing key={s.n} stage={s} maxRadius={maxR} selectedStage={selectedStage} onSelect={setSelectedStage} />
          ))}

          {/* Center dot — us */}
          <circle cx={maxR + 10} cy={maxR + 10} r={6} fill="#2563eb"
            stroke={selectedStage === 6 ? "#fff" : "#60a5fa"} strokeWidth={2}
            onClick={() => setSelectedStage(6)} style={{ cursor: "pointer" }} />

          {/* Labels */}
          <text x={maxR + 10} y={maxR + 28} textAnchor="middle" fontSize="9" fill="#93c5fd" fontWeight="600">Us</text>
          <text x={maxR + 10} y={18} textAnchor="middle" fontSize="8" fill="#c9a227">Planck shell (89 modes)</text>
          <text x={maxR + 10} y={maxR * 2 + 8} textAnchor="middle" fontSize="8" fill="#64748b">→ Ω (infinity)</text>
        </svg>
      </div>

      {/* Stage info card */}
      <div style={{
        margin: "12px 0", padding: 14, borderRadius: 10,
        background: selectedStage === 6 ? "rgba(37,99,235,0.15)" :
          selectedStage === 11 ? "rgba(201,162,39,0.15)" :
            "rgba(255,255,255,0.05)",
        border: `1px solid ${selected.color}33`,
      }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "baseline" }}>
          <span style={{ fontSize: 16, color: selected.color, fontWeight: 600 }}>
            Stage {selectedStage}: {selected.label}
          </span>
          <span style={{ fontSize: 11, color: "#94a3b8" }}>
            {fib(selectedStage)} positions
          </span>
        </div>
        <p style={{ fontSize: 13, color: "#cbd5e1", lineHeight: 1.65, margin: "8px 0 0" }}>
          {selected.desc}
        </p>
        {selectedStage >= 6 && (
          <div style={{ marginTop: 10, paddingTop: 8, borderTop: "1px solid rgba(255,255,255,0.08)" }}>
            <div style={{ fontSize: 11, color: "#94a3b8" }}>
              Modes visible up to this stage: <strong style={{ color: "#e2e8f0" }}>{modes}</strong>
            </div>
            {selectedStage <= 13 && (
              <div style={{ fontSize: 11, color: "#94a3b8", marginTop: 2 }}>
                Screening from stage 6: D^{2*(selectedStage - 6)} ≈ {(Math.pow(0.265, selectedStage - 6) * 100).toFixed(selectedStage > 9 ? 2 : 1)}%
              </div>
            )}
          </div>
        )}
      </div>

      {/* Navigation buttons */}
      <div style={{ display: "flex", gap: 6, justifyContent: "center", flexWrap: "wrap", margin: "8px 0" }}>
        {STAGES.filter(s => s.ring).map((s) => (
          <button key={s.n} onClick={() => setSelectedStage(s.n)}
            style={{
              padding: "4px 10px", fontSize: 10, border: `1px solid ${s.color}66`,
              borderRadius: 14, cursor: "pointer", color: selectedStage === s.n ? "#0f172a" : s.color,
              background: selectedStage === s.n ? s.color : "transparent",
              opacity: s.n > 11 ? 0.5 : 1,
            }}>
            {s.n}
          </button>
        ))}
      </div>

      {/* Gravity connection */}
      <div style={{
        margin: "16px 0", padding: 14, borderRadius: 10,
        background: "rgba(201,162,39,0.08)", border: "1px solid rgba(201,162,39,0.2)",
      }}>
        <div style={{ fontSize: 14, color: "#c9a227", fontWeight: 600, marginBottom: 8 }}>
          How this creates gravity
        </div>
        <p style={{ fontSize: 12, color: "#cbd5e1", lineHeight: 1.7, margin: 0 }}>
          Everything from the center (us) out to the Planck shell is one whole.
          The whole is divided equally among <strong>{fib(11)}</strong> positions — every ring, every mode, weighted the same by gravity's democracy.
        </p>
        <div style={{
          display: "flex", justifyContent: "center", alignItems: "center",
          gap: 12, margin: "12px 0 8px",
        }}>
          <div style={{ textAlign: "center" }}>
            <div style={{ fontSize: 9, color: "#94a3b8" }}>one mode's share</div>
            <div style={{ fontSize: 20, color: "#fef3c7" }}>1/89</div>
          </div>
          <div style={{ fontSize: 16, color: "#64748b" }}>→</div>
          <div style={{ textAlign: "center" }}>
            <div style={{ fontSize: 9, color: "#94a3b8" }}>squared = gravity</div>
            <div style={{ fontSize: 20, color: "#c9a227" }}>1/89²</div>
          </div>
        </div>
        <p style={{ fontSize: 11, color: "#94a3b8", lineHeight: 1.6, margin: 0 }}>
          The gold shell (stage 11) has 89 total modes. Our visible universe (the blue center) is just 8 of them. Dark matter, dark energy, and the entire gravitational structure fill the remaining 81. We live in the bright core of something vastly deeper.
        </p>
      </div>

      {/* The physical metaphor */}
      <div style={{
        margin: "12px 0", padding: 14, borderRadius: 10,
        background: "rgba(255,255,255,0.03)", border: "1px solid rgba(255,255,255,0.06)",
      }}>
        <div style={{ fontSize: 13, color: "#e2e8f0", fontWeight: 600, marginBottom: 6 }}>
          Reading the picture
        </div>
        <p style={{ fontSize: 12, color: "#94a3b8", lineHeight: 1.7, margin: "0 0 8px" }}>
          Think of the rings as layers of an onion. You live at the center — stage 6, where light exists and atoms hold together. Each layer outward is harder to see: the dark sector (stage 7) is like looking through frosted glass. Each additional layer adds another pane of glass, dimming the signal by about 73%.
        </p>
        <p style={{ fontSize: 12, color: "#94a3b8", lineHeight: 1.7, margin: "0 0 8px" }}>
          Gravity doesn't care about the glass. It reaches through every layer equally — that's what makes it special. It counts ALL 89 layers, not just the ones you can see through. And the strength of gravity comes from that count: 89 layers, each carrying 1/89 of the whole, giving a gravitational pull of (1/89)².
        </p>
        <p style={{ fontSize: 12, color: "#94a3b8", lineHeight: 1.7, margin: 0 }}>
          The onion goes on forever — layers beyond 89, beyond 233, beyond any number. But our gravity only sees to layer 89, because that's where the tower's energy first crosses the Planck threshold. The layers beyond exist, but they're past gravity's own horizon.
        </p>
      </div>

      <div style={{ textAlign: "center", fontSize: 10, color: "#475569", margin: "16px 0 8px", lineHeight: 1.5 }}>
        G = (φ + φ⁻¹)² / (φ¹¹ + φ⁻¹¹)²
        <br />
        From Nothing, Everything
      </div>
    </div>
  );
}
