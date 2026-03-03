import { useState } from "react";

const initialForm = {
  day_in_study: 14,
  lh: 3.1,
  estrogen: 180.0,
  pdg: 12.0,
  wrist_temp_mean: 36.4,
  rmssd_mean: 42.5
};

const phaseStyles = {
  Menstrual: { label: "Menstrual", className: "phase-menstrual", emoji: "🌸" },
  Follicular: { label: "Follicular", className: "phase-follicular", emoji: "🌿" },
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
    setResult(null);

    try {
      const response = await fetch(
        "https://herforecast.onrender.com/predict",
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            wearable_data: {
              spo2: 98,
              gsr_mean: 0.35,
              gsr_phasic_std: 0.05,
              ppg_rmssd: form.rmssd_mean,
              heart_rate: 72,
              skin_temp: form.wrist_temp_mean
            },
            hormone_data: {
              estrogen: form.estrogen,
              progesterone: form.pdg
            },
            day_in_cycle: form.day_in_study
          })
        }
      );

      if (!response.ok) {
        throw new Error("Server error");
      }

      const data = await response.json();
      setResult(data);

    } catch (err) {
      setResult({
        error: true,
        message:
          "Unable to reach the backend right now. Please try again shortly."
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="page">
      <section className="card">
        <h1>HerForecast</h1>
        <p className="subtitle">
          Calm daily wellness signals from wearable biomarkers.
        </p>

        <form onSubmit={submit} className="form">
          <div className="grid">
            <label>
              Cycle Day
              <input
                type="number"
                value={form.day_in_study}
                onChange={(e) =>
                  onChange("day_in_study", Number(e.target.value))
                }
              />
            </label>

            <label>
              LH
              <input
                type="number"
                step="0.1"
                value={form.lh}
                onChange={(e) => onChange("lh", Number(e.target.value))}
              />
            </label>

            <label>
              Estrogen
              <input
                type="number"
                step="0.1"
                value={form.estrogen}
                onChange={(e) => onChange("estrogen", Number(e.target.value))}
              />
            </label>

            <label>
              PdG
              <input
                type="number"
                step="0.1"
                value={form.pdg}
                onChange={(e) => onChange("pdg", Number(e.target.value))}
              />
            </label>

            <label>
              HRV (RMSSD mean)
              <input
                type="number"
                step="0.1"
                value={form.rmssd_mean}
                onChange={(e) =>
                  onChange("rmssd_mean", Number(e.target.value))
                }
              />
            </label>

            <label>
              Wrist Temp
              <input
                type="number"
                step="0.1"
                value={form.wrist_temp_mean}
                onChange={(e) =>
                  onChange("wrist_temp_mean", Number(e.target.value))
                }
              />
            </label>
          </div>

          <button disabled={loading}>
            {loading ? "Checking..." : "Get my daily forecast"}
          </button>
        </form>
      </section>

      {result && (
        <section className="card result">
          {result.error ? (
            <p>{result.message}</p>
          ) : (
            <>
              <h2>Your forecast</h2>

              <div
                className={`phase-highlight ${
                  phaseStyles[result.predicted_phase]?.className ??
                  "phase-default"
                }`}
              >
                <div className="phase-title">Current cycle phase</div>
                <div className="phase-value">
                  <span className="phase-emoji">
                    {phaseStyles[result.predicted_phase]?.emoji ?? "💗"}
                  </span>
                  {phaseStyles[result.predicted_phase]?.label ??
                    result.predicted_phase ??
                    "N/A"}
                </div>
              </div>

              <p>
                <strong>Mood trend:</strong>{" "}
                {result.predicted_mood ?? "N/A"}
              </p>

              <p>
                <strong>Confidence:</strong>{" "}
                {result.confidence
                  ? (result.confidence * 100).toFixed(1) + "%"
                  : "N/A"}
              </p>

              {result.probabilities && (
                <div className="probabilities">
                  <h3>Probability Breakdown</h3>
                  {Object.entries(result.probabilities).map(
                    ([phase, prob]) => (
                      <div key={phase}>
                        {phase}: {(prob * 100).toFixed(1)}%
                      </div>
                    )
                  )}
                </div>
              )}
            </>
          )}
        </section>
      )}
    </main>
  );
}

