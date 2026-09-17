"""
PHASE 2 — Baseline ML Model
=============================
Trains a simple Random Forest to predict pest risk from your merged dataset
(see data/README.md for the expected table shape). This is your EXPERIMENT 1
"before" model — you'll compare the LSTM (train_lstm.py) against this.

Run:
    python ml/train_baseline.py --data data/merged_dataset.csv --target pest_occurred
"""

import argparse
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score


FEATURE_COLUMNS = [
    "temp_mean_c", "humidity_pct", "rain_mm",
    "soil_n", "soil_p", "soil_k", "soil_ph",
]


def train_and_evaluate(data_path: str, target_col: str):
    df = pd.read_csv(data_path)

    missing = [c for c in FEATURE_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(
            f"Your CSV is missing columns: {missing}. "
            f"Check data/README.md for the expected table shape, or edit "
            f"FEATURE_COLUMNS at the top of this file to match your data."
        )

    X = df[FEATURE_COLUMNS]
    y = df[target_col]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    model = RandomForestClassifier(n_estimators=200, random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    results = {
        "accuracy": accuracy_score(y_test, y_pred),
        "precision": precision_score(y_test, y_pred, average="weighted", zero_division=0),
        "recall": recall_score(y_test, y_pred, average="weighted", zero_division=0),
        "f1_score": f1_score(y_test, y_pred, average="weighted", zero_division=0),
    }

    print("\n=== BASELINE MODEL RESULTS (Experiment 1 — 'before') ===")
    for metric, value in results.items():
        print(f"{metric:10s}: {value:.3f}")
    print("\nSave these numbers — you'll compare them against your LSTM results.")

    joblib.dump(model, "ml/baseline_model.pkl")
    print("\nModel saved to ml/baseline_model.pkl")

    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=str, required=True, help="Path to merged CSV dataset")
    parser.add_argument("--target", type=str, default="pest_occurred", help="Target/label column name")
    args = parser.parse_args()

    train_and_evaluate(args.data, args.target)
