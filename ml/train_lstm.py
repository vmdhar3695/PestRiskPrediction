"""
PHASE 3 — Improved Sequential Model (LSTM)
=============================================
Trains an LSTM on sequential weather data, following the approach in your
base paper (Lee & Yun, 2023). This is your EXPERIMENT 1 "after" model —
compare its accuracy/precision/recall/F1 against train_baseline.py's results.

This script uses a SLIDING WINDOW: it looks at the last `window_size` days
of weather to predict pest risk on the next day, since pest risk builds up
over consecutive days of favorable conditions (not just one day's weather).

Run:
    python ml/train_lstm.py --data data/merged_dataset.csv --target pest_occurred --window 7
"""

import argparse
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from torch.utils.data import TensorDataset, DataLoader
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

FEATURE_COLUMNS = [
    "temp_mean_c", "humidity_pct", "rain_mm",
    "soil_n", "soil_p", "soil_k", "soil_ph",
]


class PestRiskLSTM(nn.Module):
    def __init__(self, n_features: int, hidden_size: int = 32):
        super().__init__()
        self.lstm = nn.LSTM(n_features, hidden_size, batch_first=True)
        self.fc = nn.Linear(hidden_size, 1)

    def forward(self, x):
        _, (h_n, _) = self.lstm(x)
        out = self.fc(h_n[-1])
        return torch.sigmoid(out)


def make_sequences(df: pd.DataFrame, target_col: str, window_size: int):
    """Turns a flat table into (window_size-day sequence -> next-day label) pairs."""
    X_seq, y_seq = [], []
    features = df[FEATURE_COLUMNS].values
    labels = df[target_col].values
    for i in range(len(df) - window_size):
        X_seq.append(features[i:i + window_size])
        y_seq.append(labels[i + window_size])
    return np.array(X_seq), np.array(y_seq)


def train_and_evaluate(data_path: str, target_col: str, window_size: int, epochs: int = 20):
    df = pd.read_csv(data_path).sort_values("date")

    missing = [c for c in FEATURE_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"Your CSV is missing columns: {missing}. Check data/README.md.")

    scaler = StandardScaler()
    df[FEATURE_COLUMNS] = scaler.fit_transform(df[FEATURE_COLUMNS])

    X, y = make_sequences(df, target_col, window_size)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    X_train_t = torch.tensor(X_train, dtype=torch.float32)
    y_train_t = torch.tensor(y_train, dtype=torch.float32).unsqueeze(1)
    X_test_t = torch.tensor(X_test, dtype=torch.float32)
    y_test_t = torch.tensor(y_test, dtype=torch.float32).unsqueeze(1)

    train_loader = DataLoader(TensorDataset(X_train_t, y_train_t), batch_size=16, shuffle=True)

    model = PestRiskLSTM(n_features=len(FEATURE_COLUMNS))
    criterion = nn.BCELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

    for epoch in range(epochs):
        model.train()
        total_loss = 0
        for xb, yb in train_loader:
            optimizer.zero_grad()
            pred = model(xb)
            loss = criterion(pred, yb)
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
        if (epoch + 1) % 5 == 0:
            print(f"Epoch {epoch+1}/{epochs} - loss: {total_loss/len(train_loader):.4f}")

    model.eval()
    with torch.no_grad():
        y_pred_prob = model(X_test_t).numpy().flatten()
        y_pred = (y_pred_prob >= 0.5).astype(int)

    results = {
        "accuracy": accuracy_score(y_test, y_pred),
        "precision": precision_score(y_test, y_pred, average="weighted", zero_division=0),
        "recall": recall_score(y_test, y_pred, average="weighted", zero_division=0),
        "f1_score": f1_score(y_test, y_pred, average="weighted", zero_division=0),
    }

    print("\n=== LSTM MODEL RESULTS (Experiment 1 — 'after') ===")
    for metric, value in results.items():
        print(f"{metric:10s}: {value:.3f}")
    print("\nCompare these numbers against train_baseline.py's output for your Experiment 1 table.")

    torch.save(model.state_dict(), "ml/lstm_model.pt")
    print("\nModel saved to ml/lstm_model.pt")

    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=str, required=True, help="Path to merged CSV dataset")
    parser.add_argument("--target", type=str, default="pest_occurred", help="Target/label column name")
    parser.add_argument("--window", type=int, default=7, help="Number of past days to look at")
    parser.add_argument("--epochs", type=int, default=20)
    args = parser.parse_args()

    train_and_evaluate(args.data, args.target, args.window, args.epochs)
