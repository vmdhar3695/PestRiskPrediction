# AI-Based Pest Risk Prediction and Crop Protection Advisory System
### FINAL COMPLETE GUIDE — Everything in One File

---

# 1. PROJECT OVERVIEW (Plain English)

**The problem:** Farmers usually find out about a pest attack only after visible crop damage — too late to act cheaply.

**The solution:** Predict pest risk *before* it happens using weather, soil, and pest-history data, then use an AI (LLM) grounded in real agricultural documents (via RAG) to explain, in plain language, what to actually do about it.

**Two halves:**
1. **Prediction half** — data in → risk score out (classic ML/DL)
2. **Advisory half** — risk score + real government pest documents → plain-language advisory (LLM + RAG)

---

# 2. ABSTRACT

Indian farmers face significant crop losses due to pest outbreaks that can spread rapidly before timely preventive action is taken. Pest occurrence is influenced by crop type, weather conditions, historical pest patterns, soil characteristics, and geographical location. Farmers, particularly those who lack timely access to agricultural information, may identify pest problems only after visible crop damage has occurred.

This project builds an **AI-based Pest Risk Monitoring and Crop Protection Advisory System** for farmers and agriculture field officers. The system analyzes environmental and agricultural factors — pest data, rainfall and dry-spell information, Crop Registry, Digital Crop Survey, and Soil Health Card data — to estimate the likelihood of pest outbreaks for specific crops and geographical regions, and generates plain-language, actionable advisories using a Large Language Model (LLM) grounded in verified agricultural knowledge through Retrieval-Augmented Generation (RAG).

**Scope:** predicts risk, monitors, alerts, and gives evidence-based advisories. Does **not** replace agricultural experts, prescribe pesticides, or guarantee outbreak prevention. Success measured with accuracy, precision, recall, F1-score, plus usability of generated advisories.

---

# 3. THE WORKFLOW — Explain This to Your Guide, Step by Step

Use this exact sequence when presenting. Each step says what happens, what data it uses, and what it produces — so your guide can follow the whole system end to end.

```
STEP 1: DATA COLLECTION
  Weather data (Open-Meteo API) + Soil data (Soil Health Card,
  district-level) + Pest history (Kaggle datasets) + Crop Registry
  (public substitute data)
        │
        ▼
STEP 2: DATA PREPARATION
  Merge all sources into one table:
  [crop, region, date, temperature, humidity, rainfall, soil N-P-K → did a pest occur?]
        │
        ▼
STEP 3: RISK PREDICTION MODEL (the "brain")
  Baseline model (Random Forest) built first → measured →
  Improved model (LSTM, matches base paper) built next → measured →
  COMPARE the two (Experiment 1) → produces a risk score (e.g. "78% risk")
        │
        ▼
STEP 4: EXPLAINABILITY LAYER
  Show WHY the risk is high (e.g. "72% humidity + recent rainfall +
  past outbreak history in this block")
        │
        ▼
STEP 5: RAG KNOWLEDGE BASE (the "trusted library")
  Real government PDFs (NIPHM IPM packages, ICAR advisories) are
  chunked and stored in a vector database (ChromaDB)
        │
        ▼
STEP 6: LLM + RAG ADVISORY GENERATION (the "voice")
  Risk score + explanation → retrieve matching real documents →
  LLM writes a plain-language advisory grounded in those documents →
  COMPARE against a plain LLM with no retrieval (Experiment 2)
        │
        ▼
STEP 7: DELIVERY TO THE FARMER
  Dashboard (Streamlit): shows risk map + explanation + advisory
  WhatsApp alert (Twilio): pushes high-risk alerts directly
        │
        ▼
STEP 8: FEEDBACK LOOP
  Farmer marks "pest appeared / did not appear" → logged →
  used to improve the model over time
```

**One-sentence summary to say out loud to your guide:**
*"Data flows in, our model predicts risk and explains why, that risk triggers a lookup into real government pest documents, an LLM turns that into plain-language advice, and it reaches the farmer through a dashboard or WhatsApp — with a feedback loop so the system improves over time."*

---

# 4. WHY THIS IS "RESEARCH ORIENTED" (Not Just an App)

Your form marks this Research Oriented — meaning your guide/panel expects two real experiments with numbers, not just a working demo.

### Experiment 1 — Is the ML model actually better than a simple one?

| Model | What it is | Built in |
|---|---|---|
| Simple baseline | Basic rule or plain Random Forest | Step 3 (first pass) |
| Improved model | LSTM on sequential weather data | Step 3 (second pass) |

Report as a table:

| Model | Accuracy | Precision | Recall | F1-score |
|---|---|---|---|---|
| Simple baseline | | | | |
| LSTM (improved) | | | | |

### Experiment 2 — Is RAG actually better than a plain chatbot?

Ask 8–10 real pest questions two ways — (1) plain LLM, no retrieval, (2) your RAG pipeline. Compare which answer is more specific, locally correct, and less likely to be made up. Put 3–4 clear example pairs in your report.

### Research Objectives (for your report's introduction)
1. Design an ML model that predicts pest/disease risk for a crop-region pair using environmental + agricultural data.
2. Design a RAG pipeline that turns a risk prediction into an accurate, locally-relevant advisory.
3. Evaluate whether LSTM beats a simple baseline (Experiment 1).
4. Evaluate whether RAG beats plain LLM output (Experiment 2).

---

# 5. TECH STACK

### Start here (MVP — recommended for a first-time team)

| Layer | Tool | Why |
|---|---|---|
| Frontend | **Streamlit** (Python) | No separate frontend language to learn |
| Backend | **FastAPI** (Python) | Same language as your ML code |
| Database | **SQLite** | Zero setup |
| ML Model | **scikit-learn/XGBoost** → **LSTM (PyTorch)** | Matches base paper's method |
| Vector DB (RAG) | **ChromaDB** | Easiest to set up locally |
| RAG Orchestration | **LangChain** or **LlamaIndex** | Standard, current, well-documented |
| LLM | Anthropic/OpenAI API, or **Ollama** (Llama 3/Mistral) for free/offline | Use API if budget allows, Ollama if not |
| Alerts | **Twilio WhatsApp API** (free sandbox) | Real WhatsApp alerts, no business approval needed |

### Upgrade later (once core pipeline works)

| Layer | Upgrade to |
|---|---|
| Frontend | React.js + Tailwind + Leaflet (for the risk map) |
| Database | PostgreSQL + PostGIS (real geospatial queries) |
| Vector DB | FAISS (once documents scale up) |
| Deployment | Docker + GitHub Actions |

---

# 6. DATA SOURCES — Exact Datasets (No More "Sample Data")

### Pest/Crop Disease Data (for training your ML model)
| Dataset | Link |
|---|---|
| Crop Pest and Disease Detection | https://www.kaggle.com/datasets/nirmalsankalana/crop-pest-and-disease-detection |
| Agricultural Pests Dataset (12 categories) | https://www.kaggle.com/datasets/gauravduttakiit/agricultural-pests-dataset |
| Top Agriculture Crop Disease India (17 classes, India crops) | https://www.kaggle.com/datasets/kamal01/top-agriculture-crop-disease |
| AgroPest-12 | https://www.kaggle.com/datasets/rupankarmajumdar/crop-pests-dataset |
| All Agriculture Datasets for India (browse more) | https://www.kaggle.com/datasets/thammuio/all-agriculture-related-datasets-for-india |

### Weather Data
**Open-Meteo** — https://open-meteo.com/ — free, no API key needed, historical + forecast temperature/humidity/rainfall. Docs: https://open-meteo.com/en/docs/historical-weather-api

### Soil Data
| Source | Link |
|---|---|
| Soil Health Card Portal (official) | https://soilhealth.dac.gov.in |
| data.gov.in Soil Health Card datasets | https://www.data.gov.in/keywords/Soil%20Health%20Card |
| Google Research India Soil Health Card scraper (GitHub) | https://github.com/google-research-datasets/india-soil-health-card |

*Honest note: farmer-level data isn't always openly downloadable in bulk — district-level aggregated data is a legitimate, defensible substitute; say so explicitly in your report.*

### RAG Knowledge Base Documents (real government pest guidance)
| Document | Link |
|---|---|
| NIPHM IPM Package — Rice | https://niphm.gov.in/IPMPackages/Rice.pdf |
| NIPHM IPM Packages (all crops, browse) | https://niphm.gov.in/IPMPackages/ |
| ICAR Kharif Agro-Advisories 2025 | https://icar.org.in/sites/default/files/Circulars/ICAR-En-Kharif-Agro-Advisories-for-Farmers-2025.pdf |
| ICAR-CRIDA District Contingency Plans (Andhra Pradesh) | https://www.icar-crida.res.in/CP/AndhraPradesh/ (pick your district) |

### Crop Registry / Digital Crop Survey (hardest to get)
Not openly downloadable in India yet — these are operational government systems, not public datasets.
**What to say in your report:** *"Crop Registry and Digital Crop Survey integration is designed as a data source for production deployment; for this academic prototype we substitute district-level crop-area statistics from data.gov.in, which is public and closely analogous."*
Public substitute: https://www.data.gov.in/sector/agriculture

---

# 7. SYSTEM ARCHITECTURE DIAGRAM

```
   Data Sources                     Backend (FastAPI)              Interfaces
 ─────────────────               ───────────────────           ─────────────────
 Weather API (Open-Meteo)        Pest Risk ML Model             Streamlit Dashboard
 Soil Health Card       ───►     (XGBoost → LSTM)     ───►      (risk map + explain)
 Crop Registry substitute               +
 Pest history (Kaggle)           RAG pipeline                   WhatsApp Alerts
 Agri PDFs (NIPHM/ICAR)          (ChromaDB + LangChain)  ───►    (Twilio)
                                        +
                                 LLM (advisory generator)        Chat/Voice Assistant
```

---

# 8. STEP-BY-STEP BUILD PLAN (Weeks)

| Phase | Weeks | What to do |
|---|---|---|
| 1 | 1–2 | Collect data from Section 6 |
| 2 | 3–4 | Build baseline ML model; measure accuracy/precision/recall/F1 |
| 3 | 5–6 | Build LSTM model; **run Experiment 1** |
| 4 | 5–7 | Build FastAPI endpoints: `/predict-risk`, `/regions`, `/advisory` |
| 5 | 6–8 | Build RAG knowledge base from NIPHM/ICAR PDFs |
| 6 | 8–9 | Connect LLM + RAG; **run Experiment 2** |
| 7 | 9–10 | Build Streamlit dashboard |
| 8 | 10–11 | Add WhatsApp alerts + feedback loop |
| 9 | 11–12 | Compile results, write report, prepare demo |

---

# 9. UNIQUE FEATURES

| Feature | What it does |
|---|---|
| RAG-grounded advisory chat | Answers grounded in real ICAR/NIPHM documents, not LLM memory |
| Region-aware retrieval | Advice filtered by district/soil/season before generation |
| Explainable risk score | Shows *why* risk is high |
| Multilingual/voice support | Telugu/Hindi/English, typed or spoken |
| WhatsApp alerts | Meets farmers where they already are |
| Feedback loop | Farmer marks "pest appeared / did not" → improves model over time |

---

# 10. REFERENCES — Base Paper + 3 (all 2023+, all free)

1. **[BASE PAPER]** Lee, S., & Yun, C. M. (2023). *A deep learning model for predicting risks of crop pests and diseases from sequential environmental data.* Plant Methods, 19, 145.
   https://pmc.ncbi.nlm.nih.gov/articles/PMC10720067/
2. Madhuri, E. V. et al. (2025). *Transforming Pest Management with Artificial Intelligence Technologies: The Future of Crop Protection.* Journal of Crop Health (ICAR-IARI New Delhi & ICRISAT Hyderabad).
   https://oar.icrisat.org/13210/1/Journal%20of%20Crop%20Health_77_1-17_2025.pdf
3. (2024). *Integrating IoT for Soil Monitoring and Hybrid Machine Learning in Predicting Tomato Crop Disease in a Typical South India Station* (Anakapalle, Andhra Pradesh).
   https://pmc.ncbi.nlm.nih.gov/articles/PMC11479041/
4. (2025/2026). *Empowering farmers with artificial intelligence: a retrieval-augmented generation based large language model advisory framework.* Journal of Agricultural Engineering.
   https://www.agroengineering.org/jae/article/view/1908
5. (2025/2026). Yang, Y., Chen, L., Diao, Z., Gao, P., Zhang, B., & Zhao, C. (2026).*Recent advances in crop pest detection, forecasting and early warning: A review.*
   Artificial Intelligence in Agriculture, 16, 998–1024.
   https://doi.org/10.1016/j.aiia.2026.03.009

**How to download:** open each link → Ctrl+P → Save as PDF → print.

---

# 11. GLOSSARY (for defending your project verbally)

- **Pest Risk Prediction** — estimating outbreak likelihood before it happens, using data instead of waiting for damage.
- **RAG (Retrieval-Augmented Generation)** — LLM answers using real retrieved documents instead of its own memory, reducing wrong/made-up advice.
- **Vector Database** — stores document chunks so the system can quickly find the most relevant ones for a question.
- **Precision** — of everything predicted "high risk," how often you were right.
- **Recall** — of everything that actually happened, how often you caught it in advance.
- **F1-score** — balance between precision and recall.
- **Baseline model** — the simple model you compare your better model against, to prove the extra work was worth it.

---

# 12. ANTICIPATED QUESTIONS + SIMPLE ANSWERS

**Q: Why an LLM at all, why not just show a risk score?**
A: A number doesn't tell a farmer what to do. The LLM converts the prediction into clear, actionable steps.

**Q: How do you stop the LLM from giving wrong pesticide advice?**
A: RAG — the LLM can only answer using real retrieved documents, not its own memory. Tested directly in Experiment 2.

**Q: What data will you actually use?**
A: See Section 6 — real weather API, real government soil/pest documents, real Kaggle pest datasets, with an honest substitute for Crop Registry data, clearly labeled as such.

**Q: What's novel about this vs. existing apps?**
A: Most tools either detect pests from photos or just show a risk number. We close the loop: automatic prediction → automatic RAG-grounded advisory, region-aware, delivered via WhatsApp.

**Q: How will you evaluate success?**
A: Experiment 1 (accuracy/precision/recall/F1, baseline vs. LSTM) and Experiment 2 (RAG vs. plain LLM).

---

# 13. REVIEW 0 CHECKLIST

- [ ] Print base paper + 3 references (Section 10)
- [ ] Create GitHub repo, add guide as Owner/Admin, add teammates as Members
- [ ] Add `README.md` (or this file) to repo root
- [ ] Add abstract (Section 2) to the repo
- [ ] Be ready to explain the workflow (Section 3) end to end
- [ ] Double-check your team's Regd. Nos. against the actual form

---

# 14. TEAM

| S.No | Regd. No. | Name |
|---|---|---|
| 1 | 23BQ1A61C5 | S.V.D. Deepthi |
| 2 | 23BQ1A61D2 | E. Tejaswi |
| 3 | 23BQ1A61B4 | R. Kalyan Kumar Naik |
| 4 | 24BQ5A6118 | U. Pravallika

*(Please verify these against your actual form — small digits were hard to read in the photo.)*
