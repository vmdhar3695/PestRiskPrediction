# Pest Risk Prediction & Crop Protection Advisory System — Starter Project

This is a real, runnable starting point for your project — matches the phased plan in `docs/PROJECT_GUIDE.md`.

## Folder Structure

```
pest_risk_project/
├── data/                  # Phase 1: data collection
│   ├── fetch_weather.py   #   -> pulls free weather data (Open-Meteo, no API key)
│   └── README.md          #   -> instructions for pest + soil data
├── ml/                    # Phase 2-3: risk prediction models
│   ├── train_baseline.py  #   -> Random Forest baseline (Experiment 1, "before")
│   └── train_lstm.py      #   -> LSTM improved model (Experiment 1, "after")
├── rag/                   # Phase 5-6: RAG advisory pipeline
│   ├── source_pdfs/       #   -> put downloaded NIPHM/ICAR PDFs here
│   ├── build_knowledge_base.py  # -> chunks PDFs into ChromaDB
│   └── generate_advisory.py     # -> RAG-grounded + plain-LLM modes (Experiment 2)
├── backend/               # Phase 4: API
│   └── main.py            #   -> FastAPI endpoints
├── app/                   # Phase 7: dashboard
│   └── streamlit_app.py   #   -> farmer-facing UI
├── docs/                  # Reference documents
│   ├── PROJECT_GUIDE.md   #   -> the full guide (overview, research plan, references)
│   └── data_sources.md    #   -> exact dataset links
├── requirements.txt
└── .env.example           # -> copy to .env and fill in your API key
```

## First-Time Setup

```bash
# 1. Create a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set up your API key
cp .env.example .env
# then open .env and paste your Anthropic or OpenAI API key
```

## Run Order (matches your phased plan)

```bash
# Phase 1: get weather data
python data/fetch_weather.py --lat 16.3067 --lon 80.4365 --start 2023-01-01 --end 2024-12-31 --out data/weather.csv
# Then manually download pest + soil data (see data/README.md) and merge into data/merged_dataset.csv

# Phase 2: train baseline model
python ml/train_baseline.py --data data/merged_dataset.csv

# Phase 3: train LSTM model (compare its numbers against Phase 2 — this is Experiment 1)
python ml/train_lstm.py --data data/merged_dataset.csv

# Phase 5: build the RAG knowledge base
# (first, download PDFs from docs/data_sources.md into rag/source_pdfs/)
python rag/build_knowledge_base.py

# Phase 6: test the advisory generator (compare with vs without RAG — this is Experiment 2)
python rag/generate_advisory.py --question "What should I do about aphids on tomato in rainy season?"
python rag/generate_advisory.py --question "What should I do about aphids on tomato in rainy season?" --no-rag

# Phase 4 + 7: run the backend and dashboard together (two terminals)
uvicorn backend.main:app --reload
streamlit run app/streamlit_app.py
```

## What's Already Working vs. What You Need to Fill In

| Component | Status |
|---|---|
| Weather data fetch | ✅ Fully working, just run it |
| Pest/soil data | ⚠️ You need to download manually (links in `docs/data_sources.md`) and write a small merge script matching the shape in `data/README.md` |
| Baseline model | ✅ Fully working once you have `data/merged_dataset.csv` |
| LSTM model | ✅ Fully working, same data requirement |
| RAG knowledge base | ✅ Fully working once you download PDFs into `rag/source_pdfs/` |
| Advisory generation | ✅ Fully working once you set your API key in `.env` |
| Backend API | ✅ Fully working, has placeholder region data (edit `STUB_REGIONS` in `backend/main.py`) |
| Dashboard | ✅ Fully working, connects to the backend |
| WhatsApp alerts (Phase 8) | ❌ Not yet built — add once the core pipeline works |
| Feedback loop (Phase 8) | ❌ Not yet built — add once the core pipeline works |

## Next Immediate Step

Start with **Phase 1**: run `fetch_weather.py`, then go download one pest dataset and one soil dataset from `docs/data_sources.md`, and write the merge script. Everything else in this repo is ready and waiting for that merged CSV.
