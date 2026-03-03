import { useState } from "react";

const initialForm = {
  id: 1,
  study_interval: 2022,
  is_weekend: false,
  day_in_study: 30,
  lh: 3.1,
  estrogen: 120.0,
  pdg: 2.0,
  wrist_temp_mean: 34.6,
  rmssd_mean: 42.0,
  oxygen_ratio_mean: 1.2,
  sleep_points_mean: 62,
  exertion_points_mean: 38,
  fatigue: "Moderate",
  stress: "Low",
  moodswing: "Very Low/Little",
  sleepissue: "Low"
};

const phaseStyles = {
  Menstrual: { label: "Menstrual", className: "phase-menstrual", emoji: "🌸" },
  Follicular: { label: "Follicular", className: "phase-follicular", emoji: "🌿" },
  Fertility: { label: "Fertility", className: "phase-fertility", emoji: "✨" },
  Ovulation: { label: "Ovulation", className: "phase-fertility", emoji: "✨" },
  Luteal: { label: "Luteal", className: "phase-luteal", emoji: "🌙" }
};

export default function App() {
  const [form, setForm] = useState(initialForm);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const onChange = (key, value) => {
    setForm((prev) => ({ ...prev, [key]: value }));
  };

  const submit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const response = await fetch("http://localhost:8000/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(form)
      });
      const data = await response.json();
      setResult(data);
    } catch (err) {
      setResult({
        friendly_message: "Unable to reach the backend right now. Please try again shortly.",
        disclaimer: "This is wellness guidance, not medical advice."
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="page">
      <section className="card">
        <h1>HerForecast</h1>
        <p className="subtitle">Calm daily wellness signals from wearable biomarkers.</p>

        <form onSubmit={submit} className="form">
          <div className="grid">
            <label>
              LH
              <input type="number" step="0.1" value={form.lh} onChange={(e) => onChange("lh", Number(e.target.value))} />
            </label>
            <label>
              Estrogen
              <input type="number" step="0.1" value={form.estrogen} onChange={(e) => onChange("estrogen", Number(e.target.value))} />
            </label>
            <label>
              PdG
              <input type="number" step="0.1" value={form.pdg} onChange={(e) => onChange("pdg", Number(e.target.value))} />
            </label>
            <label>
              HRV (RMSSD mean)
              <input type="number" step="0.1" value={form.rmssd_mean} onChange={(e) => onChange("rmssd_mean", Number(e.target.value))} />
            </label>
            <label>
              Wrist Temp Mean
              <input type="number" step="0.1" value={form.wrist_temp_mean} onChange={(e) => onChange("wrist_temp_mean", Number(e.target.value))} />
            </label>
            <label>
              Sleep Points
              <input type="number" step="1" value={form.sleep_points_mean} onChange={(e) => onChange("sleep_points_mean", Number(e.target.value))} />
            </label>
          </div>
          <button disabled={loading}>{loading ? "Checking..." : "Get my daily forecast"}</button>
        </form>
      </section>

      {result && (
        <section className="card result">
          <h2>Your forecast</h2>
          <div className={`phase-highlight ${phaseStyles[result.phase]?.className ?? "phase-default"}`}>
            <div className="phase-title">Current cycle phase</div>
            <div className="phase-value">
              <span className="phase-emoji">{phaseStyles[result.phase]?.emoji ?? "💗"}</span>
              {phaseStyles[result.phase]?.label ?? result.phase ?? "N/A"}
            </div>
          </div>
          <p><strong>Mood trend:</strong> {result.mood ?? "N/A"}</p>
          <p><strong>Phase confidence:</strong> {result.phase_confidence ?? "N/A"}</p>
          <p><strong>Mood confidence:</strong> {result.mood_confidence ?? "N/A"}</p>
          <p className="message">{result.friendly_message}</p>
          <p className="disclaimer">{result.disclaimer}</p>
        </section>
      )}
    </main>
  );
}

