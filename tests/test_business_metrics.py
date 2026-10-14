"""
Tests for Business Metrics and Executive Indicators.
"""
import pytest
import pandas as pd
from src.business_metrics import BusinessMetrics


def test_calculate_executive_kpis():
    df = pd.DataFrame({
        "trip_id": [f"T{i}" for i in range(10)],
        "pickup_datetime": pd.to_datetime(["2014-04-01 08:30:00"] * 5 + ["2014-04-01 18:00:00"] * 5),
        "fare_amount": [100.0] * 10,
        "trip_distance_km": [5.0] * 10,
        "trip_duration_min": [15.0] * 10,
        "pickup_hour": [8] * 5 + [18] * 5,
        "pickup_day_name": ["Tuesday"] * 10,
        "is_peak_hour": [1] * 10,
        "is_weekend": [0] * 10
    })

    kpis = BusinessMetrics.calculate_executive_kpis(df)
    assert kpis["total_trips"] == 10
    assert kpis["total_recorded_fares"] == 1000.0
    assert kpis["avg_fare"] == 100.0
    assert kpis["avg_distance_km"] == 5.0
    assert kpis["peak_trips_share_pct"] == 100.0
    assert kpis["weekend_trips_share_pct"] == 0.0


def test_kpis_empty_df():
    empty_df = pd.DataFrame()
    kpis = BusinessMetrics.calculate_executive_kpis(empty_df)
    assert kpis["total_trips"] == 0
