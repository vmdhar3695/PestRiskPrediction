"""
PHASE 7 — Streamlit Dashboard
================================
A simple farmer/field-officer-facing dashboard: pick a crop + region, see the
risk score, why it's high, and the generated advisory.

Run:
    streamlit run app/streamlit_app.py
(Make sure the backend is running first: uvicorn backend.main:app --reload)
"""

import streamlit as st
import requests

API_BASE = "http://127.0.0.1:8000"

st.set_page_config(page_title="Pest Risk Advisory System", layout="centered")
st.title("🌾 AI Pest Risk Prediction & Crop Protection Advisory")

st.markdown("Enter today's conditions to see the pest risk and get an advisory.")

col1, col2 = st.columns(2)
with col1:
    crop = st.selectbox("Crop", ["Rice", "Chilli", "Cotton", "Sugarcane"])
    region = st.selectbox("Region", ["Guntur", "Krishna"])
with col2:
    temp = st.slider("Mean temperature (°C)", 15.0, 45.0, 30.0)
    humidity = st.slider("Humidity (%)", 0.0, 100.0, 75.0)

rain = st.slider("Rainfall (mm)", 0.0, 100.0, 10.0)

if st.button("Predict Risk"):
    with st.spinner("Calculating risk..."):
        response = requests.post(f"{API_BASE}/predict-risk", json={
            "crop": crop, "region": region,
            "temp_mean_c": temp, "humidity_pct": humidity, "rain_mm": rain,
        })
        result = response.json()

    risk_level = result["risk_level"]
    color = {"high": "🔴", "moderate": "🟡", "low": "🟢"}[risk_level]

    st.metric("Risk Score", f"{result['risk_score']:.0%}", risk_level.upper())
    st.write(f"{color} **Contributing factors:** {result['contributing_factors']}")

    with st.spinner("Generating advisory..."):
        advisory_response = requests.post(f"{API_BASE}/advisory", json={
            "crop": crop, "region": region, "risk_score": result["risk_score"],
        })
        advisory = advisory_response.json()["advisory"]

    st.subheader("📋 Advisory")
    st.write(advisory)
