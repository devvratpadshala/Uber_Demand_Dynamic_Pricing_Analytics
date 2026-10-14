"""
Tests for Data Preprocessing and Validation.
"""
import pytest
import pandas as pd
from src.preprocessing import DataPreprocessor
from src.data_validator import DataValidator


def test_standardize_column_names():
    df = pd.DataFrame({
        "Date/Time": ["2014-04-01 00:00:00"],
        "Lat": [40.75],
        "Lon": [-73.98],
        "Base": ["B02512"]
    })
    clean = DataPreprocessor.standardize_column_names(df)
    assert "pickup_datetime" in clean.columns
    assert "pickup_latitude" in clean.columns
    assert "pickup_longitude" in clean.columns
    assert "base_dispatch_code" in clean.columns


def test_clean_and_filter_removes_outliers():
    # Construct DF with invalid fare and out of bounds lat (outside Indian metro bounds 18.70 - 19.50)
    df = pd.DataFrame({
        "pickup_datetime": ["2014-04-01 00:00:00", "2014-04-01 01:00:00", "2014-04-01 02:00:00"],
        "pickup_latitude": [19.07, 35.00, 19.12],  # 35.00 is out of Indian metro bounds
        "pickup_longitude": [72.87, 72.87, 72.88],
        "fare_amount": [120.0, 50.0, -10.0]  # -10 is invalid
    })
    clean_df, summary = DataPreprocessor.clean_and_filter(df, drop_anomalies=True)
    # Only row 0 is completely valid
    assert len(clean_df) == 1
    assert summary["dropped_rows"] == 2


def test_validator_detects_empty():
    empty_df = pd.DataFrame()
    report = DataValidator.validate_dataset(empty_df)
    assert not report["is_valid"]
    assert report["total_rows"] == 0
