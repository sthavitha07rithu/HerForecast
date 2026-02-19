# HerForecast
### Interpreting Biological Rhythms into Human-Centered Daily Guidance

---

## 1. Problem Context

Wearable devices are highly capable at measuring the body, yet limited at explaining it.

Most outputs appear as scores, trends, or alerts thus requiring interpretation and often encouraging optimization behavior.

For many users, especially everyday women navigating cyclical physiological changes, raw metrics do not answer a practical question:

> **“What kind of day is this for me?”**

HerForecast explores a different approach: transforming multi-sensor biological signals into understandable daily context rather than performance feedback.

---

## 2. Design Objective

Create a science-grounded intelligence layer that:

- Combines multiple physiological signals (PPG, GSR, SpO2, temperature, hormonal patterns)
- Infers cyclical biological state
- Communicates meaning instead of measurement
- Supports preparedness rather than evaluation
- Provides guidance without urgency or alarm

The system aims to interpret variation, not correct it.

---

## 3. System Concept

HerForecast models cyclical physiology and converts it into experiential insight.

**Pipeline**

```

Biomarkers → Phase inference → State interpretation → Human language feedback

```

Instead of presenting raw data:

> “HRV decreased.”

The system communicates context:

> “Your body may prefer slower pacing and lower cognitive load today.”

---

## 4. Functional Outcome

The platform:

- Predicts menstrual phase from biomarker patterns
- Maps phases to emotional and energy tendencies
- Produces supportive daily guidance
- Frames biological variation as normal and informative

The output is designed to feel like explanation, not instruction.

---

## 5. System Architecture

```

Multi-Sensor Biomarkers
↓
Feature Processing & ML Inference
↓
Phase Classification
↓
State Mapping Engine
↓
Compassionate Language Output

```

### Backend
- FastAPI service
- Loads trained scikit-learn pipeline
- Processes structured biomarker inputs
- Predicts menstrual phase
- Maps phase to emotional & preparedness messaging

### Frontend
- React (Vite)
- Uploads biomarker CSV
- Displays phase state
- Renders warm, intuitive insight

---

## 6. Physiological Inputs

HerForecast integrates the following signals:

- SpO2 (oxygen saturation)
- GSR mean (sympathetic arousal proxy)
- GSR phasic variability
- RMSSD (heart rate variability)
- Heart rate
- Skin temperature
- Estrogen
- Progesterone
- Day in cycle

These signals are fused to infer cyclic biological state patterns.

---

## 7. Model Design

The predictive engine is a **scikit-learn Pipeline** combining:

- Missing value imputation
- Feature scaling
- Cyclic feature encoding
- Random Forest probabilistic classifier

The model outputs phase probabilities which are translated into supportive emotional states via a mapping layer.

**Required version**

```

scikit-learn==1.7.2

````

Version consistency is necessary for reproducibility.

---

## 8. Reproducible Setup

### 8.1 Backend Setup

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
````

Backend runs at:

```
http://127.0.0.1:8000
```

Swagger documentation:

```
http://127.0.0.1:8000/docs
```

---

### 8.2 Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at:

```
http://localhost:5173
```

Backend must be running before using the UI.

---

## 9. CSV Input Format (Simulation)

**Required columns**

```
spo2
gsr_mean
gsr_phasic_std
ppg_rmssd
heart_rate
skin_temp
estrogen
progesterone
day_in_cycle
```

**Example**

```
spo2,gsr_mean,gsr_phasic_std,ppg_rmssd,heart_rate,skin_temp,estrogen,progesterone,day_in_cycle
97.8,6.5,0.55,32.0,82.0,37.4,220.0,38.0,22
```

Each row represents one prediction instance.

---

## 10. Design Philosophy

HerForecast is guided by three principles:

#### Translate Data into Human States

Not dashboards. Not scores. Not warnings.

#### Avoid Anxiety Framing

No alerts. No deficit language. No performance metrics.

#### Respect Biological Rhythms

Cyclical shifts are normal, not problems to optimize away.

---

## 11. Innovation

HerForecast moves beyond:

* Fitness tracking
* Hormone tracking dashboards
* Clinical symptom logging

It introduces a preparedness intelligence layer that contextualizes daily physiological variation within cyclical rhythms.

---

## 12. Limitations

* Prototype system
* Trained on limited data
* Not intended for diagnosis or treatment

---

## 13. Future Directions

* Real-world wearable integration
* Multimodal fusion including audio context
* Adaptive personalized phase modeling
* Privacy-preserving inference

---

## 14. Disclaimer

HerForecast is an experimental intelligence prototype designed for educational and research purposes.

It does **not** provide medical advice, diagnosis, or treatment.

---

::contentReference[oaicite:0]{index=0}
```
