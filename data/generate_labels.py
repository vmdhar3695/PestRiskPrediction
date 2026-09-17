"""
Generates pest_occurred labels for your weather data using REAL, documented
pest-favorable conditions (sourced from NIPHM/ICAR pest advisories — see
docs/data_sources.md). This solves the "no tabular pest+weather dataset
exists" problem by using domain rules instead of pretending we found real
occurrence records.

BE HONEST IN YOUR REPORT: say clearly that these labels were generated using
documented environmental thresholds (cite the source), not directly observed
field data. This is a normal, defensible approach for a prototype when real
occurrence data isn't publicly available — reviewers respect honesty about
this far more than an unexplained "sample data."

Run:
    python data/generate_labels.py --weather data/weather.csv --crop Rice --out data/merged_dataset.csv
"""

import argparse
import numpy as np
import pandas as pd

# Documented pest-favorable conditions (SIMPLIFIED — replace/expand these with
# thresholds from your specific NIPHM/ICAR PDF once you've read it closely).
# Example: Brown Planthopper (rice) — thrives in high humidity, warm temps,
# continuous rainfall/standing water. Source: NIPHM Rice IPM Package.
PEST_RULES = {
    "Rice": {
        "pest_name": "Brown Planthopper",
        "humidity_threshold": 80,
        "temp_min": 25, "temp_max": 32,
        "rain_threshold": 5,
    },
    "Chilli": {
        "pest_name": "Thrips",
        "humidity_threshold": 40,   # thrips favor LOW humidity, dry conditions
        "temp_min": 28, "temp_max": 36,
        "rain_threshold": 2,        # low rainfall favors thrips
    },
    "Cotton": {
        "pest_name": "Whitefly",
        "humidity_threshold": 55,
        "temp_min": 25, "temp_max": 35,
        "rain_threshold": 3,
    },
}


def generate_soil_placeholder(n_rows: int, seed: int = 42) -> pd.DataFrame:
    """
    Generates placeholder soil values within realistic ranges (based on typical
    Andhra Pradesh Soil Health Card averages). Replace this with real
    district-level averages from soilhealth.dac.gov.in once you've pulled them —
    see data/README.md Step 3.
    """
    rng = np.random.default_rng(seed)
    return pd.DataFrame({
        "soil_n": rng.normal(280, 30, n_rows).round(1),
        "soil_p": rng.normal(22, 5, n_rows).round(1),
        "soil_k": rng.normal(180, 20, n_rows).round(1),
        "soil_ph": rng.normal(6.8, 0.4, n_rows).round(2),
    })


def apply_pest_rule(row, rule) -> int:
    humidity_ok = (
        row["humidity_pct"] >= rule["humidity_threshold"]
        if rule["pest_name"] != "Thrips"
        else row["humidity_pct"] <= rule["humidity_threshold"]
    )
    temp_ok = rule["temp_min"] <= row["temp_mean_c"] <= rule["temp_max"]
    rain_ok = (
        row["rain_mm"] >= rule["rain_threshold"]
        if rule["pest_name"] != "Thrips"
        else row["rain_mm"] <= rule["rain_threshold"]
    )
    conditions_met = sum([humidity_ok, temp_ok, rain_ok])
    # Label as "pest occurred" if at least 2 of 3 favorable conditions are met.
    # This threshold is a simplification you should tune/justify in your report.
    return 1 if conditions_met >= 2 else 0


def build_dataset(weather_path: str, crop: str, region: str = "Guntur") -> pd.DataFrame:
    if crop not in PEST_RULES:
        raise ValueError(f"No rule defined for '{crop}'. Add one to PEST_RULES in this file.")

    df = pd.read_csv(weather_path)
    df["region"] = region
    df["crop"] = crop

    soil_df = generate_soil_placeholder(len(df))
    df = pd.concat([df.reset_index(drop=True), soil_df.reset_index(drop=True)], axis=1)

    rule = PEST_RULES[crop]
    df["pest_occurred"] = df.apply(lambda row: apply_pest_rule(row, rule), axis=1)
    df["pest_name"] = rule["pest_name"]

    print(f"\nGenerated labels for {crop} ({rule['pest_name']}):")
    print(df["pest_occurred"].value_counts().rename({0: "no risk", 1: "risk"}))
    print(f"\nSoil values are PLACEHOLDERS — replace with real district data when available (see data/README.md).")

    return df


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--weather", type=str, required=True, help="Path to weather.csv from fetch_weather.py")
    parser.add_argument("--crop", type=str, required=True, choices=list(PEST_RULES.keys()))
    parser.add_argument("--region", type=str, default="Guntur")
    parser.add_argument("--out", type=str, default="data/merged_dataset.csv")
    args = parser.parse_args()

    df = build_dataset(args.weather, args.crop, args.region)
    df.to_csv(args.out, index=False)
    print(f"\nSaved {len(df)} rows to {args.out} — ready for ml/train_baseline.py")
