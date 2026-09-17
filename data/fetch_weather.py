"""
PHASE 1 — Data Collection: Weather Data
=========================================
Pulls historical daily weather data (temperature, humidity, rainfall) from
Open-Meteo — a free API that needs NO API key and NO signup.

Run:
    python data/fetch_weather.py --lat 16.3067 --lon 80.4365 --start 2023-01-01 --end 2024-12-31 --out data/weather.csv

Docs: https://open-meteo.com/en/docs/historical-weather-api
"""

import argparse
import requests
import pandas as pd

BASE_URL = "https://archive-api.open-meteo.com/v1/archive"


def fetch_weather(lat: float, lon: float, start_date: str, end_date: str) -> pd.DataFrame:
    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": start_date,
        "end_date": end_date,
        "daily": [
            "temperature_2m_max",
            "temperature_2m_min",
            "temperature_2m_mean",
            "relative_humidity_2m_mean",
            "precipitation_sum",
            "rain_sum",
        ],
        "timezone": "Asia/Kolkata",
    }
    response = requests.get(BASE_URL, params=params, timeout=30)
    response.raise_for_status()
    data = response.json()

    df = pd.DataFrame(data["daily"])
    df = df.rename(columns={
        "time": "date",
        "temperature_2m_max": "temp_max_c",
        "temperature_2m_min": "temp_min_c",
        "temperature_2m_mean": "temp_mean_c",
        "relative_humidity_2m_mean": "humidity_pct",
        "precipitation_sum": "precipitation_mm",
        "rain_sum": "rain_mm",
    })
    return df


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--lat", type=float, required=True, help="Latitude of your target district")
    parser.add_argument("--lon", type=float, required=True, help="Longitude of your target district")
    parser.add_argument("--start", type=str, required=True, help="Start date YYYY-MM-DD")
    parser.add_argument("--end", type=str, required=True, help="End date YYYY-MM-DD")
    parser.add_argument("--out", type=str, default="data/weather.csv", help="Output CSV path")
    args = parser.parse_args()

    df = fetch_weather(args.lat, args.lon, args.start, args.end)
    df.to_csv(args.out, index=False)
    print(f"Saved {len(df)} rows of weather data to {args.out}")
