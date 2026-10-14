"""
Tests for Data Loader Module.
"""
import pytest
import pandas as pd
from src.data_loader import DataLoader
from config.settings import DEFAULT_DATASET_PATH, RAW_DATASET_PATH


def test_detect_schema_type():
    demo_cols = ["trip_id", "fare_amount", "trip_distance_km", "pickup_datetime"]
    assert DataLoader.detect_schema_type(demo_cols) == "demonstration"

    raw_cols = ["Date/Time", "Lat", "Lon", "Base"]
    assert DataLoader.detect_schema_type(raw_cols) == "nyc_tlc_raw"

    kaggle_cols = ["key", "fare_amount", "pickup_longitude", "pickup_latitude"]
    assert DataLoader.detect_schema_type(kaggle_cols) == "kaggle_uber_fares"

    generic_cols = ["col_a", "col_b"]
    assert DataLoader.detect_schema_type(generic_cols) == "custom_generic"


def test_load_default_demonstration():
    assert DEFAULT_DATASET_PATH.exists(), "Demo dataset file should exist."
    df, schema = DataLoader.load_default_demonstration(nrows=100)
    assert len(df) == 100
    assert schema == "demonstration"
    assert "fare_amount" in df.columns
    assert "pickup_datetime" in df.columns


def test_load_raw_tlc_sample():
    assert RAW_DATASET_PATH.exists(), "Raw TLC sample file should exist."
    df, schema = DataLoader.load_raw_tlc_sample(nrows=50)
    assert len(df) == 50
    assert schema == "nyc_tlc_raw"
    assert "Date/Time" in df.columns
