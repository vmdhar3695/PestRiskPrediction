# Data Sources — Exact Datasets to Use (No More "Sample Data")

Every dataset below is real, has a working link, and I've marked exactly what it's for.

---

## 1. Pest/Crop Disease Data (for training your ML risk model)

| Dataset | What it contains | Link |
|---|---|---|
| Crop Pest and Disease Detection | Labeled images across multiple pest/disease categories | https://www.kaggle.com/datasets/nirmalsankalana/crop-pest-and-disease-detection |
| Agricultural Pests Dataset | 12 categories of common agricultural pests, labeled images | https://www.kaggle.com/datasets/gauravduttakiit/agricultural-pests-dataset |
| Top Agriculture Crop Disease India | 17 classes, 13,324 images — rice, wheat, corn, sugarcane, potato (India-relevant crops) | https://www.kaggle.com/datasets/kamal01/top-agriculture-crop-disease |
| AgroPest-12 | 12-class crop pest image dataset | https://www.kaggle.com/datasets/rupankarmajumdar/crop-pests-dataset |
| All Agriculture Datasets for India | A curated collection of Indian agriculture datasets (browse this for more options specific to your crop) | https://www.kaggle.com/datasets/thammuio/all-agriculture-related-datasets-for-india |

**How to use these:** you'll need a Kaggle account (free) → click "Download" on each dataset page. If your model is tabular-based (weather → risk score, matching your base paper) rather than image-based, use these mainly for pest occurrence *labels* — pair the label (which pest occurred) with weather data from Source 2 below for the same date/region.

---

## 2. Weather Data (for the environmental factors in your risk model)

**Source: Open-Meteo** — https://open-meteo.com/

- Free, **no API key or signup required**
- Gives historical + forecast: temperature, humidity, rainfall, wind — exactly what your base paper (Lee & Yun, 2023) used
- Historical API docs: https://open-meteo.com/en/docs/historical-weather-api
- Just pick your district's latitude/longitude (e.g. for Guntur, AP: 16.3067° N, 80.4365° E) and pull daily data for whatever date range matches your pest dataset

---

## 3. Soil Data (for your "Soil Health Card" component)

| Source | What it contains | Link |
|---|---|---|
| Soil Health Card Portal (official) | Government portal — search by state/district for soil nutrient data (N, P, K, pH, etc.) | https://soilhealth.dac.gov.in |
| data.gov.in — Soil Health Card datasets | Open datasets tagged "Soil Health Card" — browse and download CSVs directly | https://www.data.gov.in/keywords/Soil%20Health%20Card |
| Google Research — India Soil Health Card scraper (GitHub) | An open-source tool that scrapes public Soil Health Card data — useful if you need programmatic access at scale | https://github.com/google-research-datasets/india-soil-health-card |

**Honest note:** individual farmer-level Soil Health Card data isn't always openly downloadable in bulk — the data.gov.in datasets are often aggregated (state/district-level summaries). For your model, district-level soil nutrient averages are a legitimate and defensible substitute — just say so explicitly in your report ("district-level aggregated Soil Health Card data from data.gov.in, since farmer-level data requires portal-specific access").

---

## 4. Documents for Your RAG Knowledge Base (real government pest-management guidance)

These are the actual PDFs your RAG pipeline should chunk and embed — this is what makes your "advisory" grounded and real, not generic.

| Document | What it contains | Link |
|---|---|---|
| NIPHM Integrated Pest Management Package — Rice | Official Govt of India IPM guidance for rice pests | https://niphm.gov.in/IPMPackages/Rice.pdf |
| NIPHM IPM Packages (full list — other crops) | Browse for your specific crop (cotton, chilli, maize, etc.) | https://niphm.gov.in/IPMPackages/ |
| ICAR Kharif Agro-Advisories for Farmers 2025 | Real, current (2025) crop-wise pest/disease advisory guidance from ICAR | https://icar.org.in/sites/default/files/Circulars/ICAR-En-Kharif-Agro-Advisories-for-Farmers-2025.pdf |
| ICAR-CRIDA District Agricultural Contingency Plans (Andhra Pradesh) | District-specific plans including pest outbreak contingencies — pick your target AP district | https://www.icar-crida.res.in/CP/AndhraPradesh/ (browse for your district, e.g. Visakhapatnam: `.../Visakhapatnam.pdf`) |

**This directly fixes your RAG "problem statement" gap** — these are the real documents your system retrieves from, instead of a vague "agricultural guidelines" placeholder.

---

## 5. Crop Registry / Digital Crop Survey (the hardest one to get)

Being transparent: India's Digital Crop Survey and state Crop Registry data are largely **not yet openly downloadable** — they're operational government systems (state agriculture department databases), not public datasets. For your project:

- **What to say in your report:** "Crop Registry and Digital Crop Survey integration is designed as a data source for production deployment; for this academic prototype we substitute district-level crop-area statistics from data.gov.in (link below), which is public and closely analogous."
- **Public substitute:** data.gov.in Agriculture Census / crop-area statistics — https://www.data.gov.in/sector/agriculture
- If your guide has any institutional contact with the state agriculture department, that's the real path to actual Crop Registry access — worth asking directly rather than trying to scrape it.

---

## 6. Summary Table — What Goes Where

| Your model/module | Which data source above |
|---|---|
| Risk prediction ML model | Section 1 (pest labels) + Section 2 (weather) + Section 3 (soil) |
| RAG knowledge base | Section 4 (real PDFs) |
| Geographic/crop context | Section 5 (public substitute + honest note) |

Put this table (or a version of it) directly in your report's "Data Sources" section — reviewers respond much better to "here is exactly what we used and why" than to "sample data was used."
