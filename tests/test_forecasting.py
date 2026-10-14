"""
Tests for Demand Forecasting Module.
"""
import pytest
import pandas as pd
import numpy as np
from src.demand_forecasting import DemandForecaster


def test_prepare_time_series():
    # Generate 100 hours of synthetic timestamps
    dates = pd.date_range("2014-04-01 00:00:00", periods=100, freq="h")
    df = pd.DataFrame({
        "pickup_datetime": dates,
        "trip_id": [f"T{i}" for i in range(100)]
    })
    ts_df = DemandForecaster.prepare_time_series(df, freq="h")
    assert "demand" in ts_df.columns
    assert "lag_1h" in ts_df.columns
    assert "rolling_6h_mean" in ts_df.columns
    assert len(ts_df) > 0


def test_train_and_evaluate():
    # Create sufficient history (150 hours)
    dates = pd.date_range("2014-04-01 00:00:00", periods=150, freq="h")
    # Sine wave demand pattern + noise
    demand_vals = (np.sin(np.linspace(0, 20, 150)) * 20 + 50).astype(int)
    records = []
    for dt, cnt in zip(dates, demand_vals):
        for _ in range(cnt):
            records.append({"pickup_datetime": dt})

    df = pd.DataFrame(records)
    ts_df = DemandForecaster.prepare_time_series(df, freq="h")
    output = DemandForecaster.train_and_evaluate(ts_df, test_size_ratio=0.20)

    assert "error" not in output
    assert "metrics" in output
    assert "Naive_Persistence" in output["metrics"]
    assert "Random_Forest" in output["metrics"]
    assert output["metrics"]["Random_Forest"]["MAE"] >= 0
    assert len(output["results_df"]) == output["test_size"]
