"""
Data Loader Module for Uber Demand and Dynamic Pricing Analytics.
Handles loading demo data, user-uploaded CSVs, raw TLC data, with schema detection and caching.
"""
from pathlib import Path
from typing import Optional, Tuple, Dict, Any
import pandas as pd
import numpy as np

from config.settings import DEFAULT_DATASET_PATH, RAW_DATASET_PATH


class DataLoader:
    """Robust CSV loader supporting multiple schemas and memory efficiency."""

    KNOWN_SCHEMAS = {
        "demonstration": [
            "trip_id", "pickup_datetime", "pickup_latitude", "pickup_longitude",
            "pickup_zone", "trip_distance_km", "trip_duration_min", "fare_amount",
            "passenger_count", "base_dispatch_code"
        ],
        "nyc_tlc_raw": [
            "Date/Time", "Lat", "Lon", "Base"
        ],
        "kaggle_uber_fares": [
            "key", "fare_amount", "pickup_datetime", "pickup_longitude",
            "pickup_latitude", "dropoff_longitude", "dropoff_latitude", "passenger_count"
        ]
    }

    @staticmethod
    def detect_schema_type(columns: list) -> str:
        """Detect the schema category based on column names."""
        cols = [c.strip().lower() for c in columns]
        if "fare_amount" in cols and "trip_distance_km" in cols:
            return "demonstration"
        elif "date/time" in cols or ("lat" in cols and "lon" in cols and "fare_amount" not in cols):
            return "nyc_tlc_raw"
        elif "fare_amount" in cols and ("pickup_longitude" in cols or "pickup_latitude" in cols):
            return "kaggle_uber_fares"
        return "custom_generic"

    @classmethod
    def load_from_path(cls, file_path: str | Path, nrows: Optional[int] = None) -> Tuple[pd.DataFrame, str]:
        """
        Load a CSV file from a local filesystem path.
        Returns: (DataFrame, detected_schema)
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Dataset not found at: {file_path}")

        # Read first row for schema detection
        sample_df = pd.read_csv(path, nrows=2)
        schema_type = cls.detect_schema_type(list(sample_df.columns))

        # Standardized reading
        df = pd.read_csv(path, nrows=nrows)
        return df, schema_type

    @classmethod
    def load_from_buffer(cls, file_buffer, nrows: Optional[int] = None) -> Tuple[pd.DataFrame, str]:
        """
        Load a CSV dataset from a file-like buffer (e.g. Streamlit UploadedFile).
        Returns: (DataFrame, detected_schema)
        """
        sample_df = pd.read_csv(file_buffer, nrows=2)
        schema_type = cls.detect_schema_type(list(sample_df.columns))

        if hasattr(file_buffer, "seek"):
            file_buffer.seek(0)

        df = pd.read_csv(file_buffer, nrows=nrows)
        return df, schema_type

    @classmethod
    def load_default_demonstration(cls, nrows: Optional[int] = None) -> Tuple[pd.DataFrame, str]:
        """Load bundled demonstration dataset."""
        return cls.load_from_path(DEFAULT_DATASET_PATH, nrows=nrows)

    @classmethod
    def load_raw_tlc_sample(cls, nrows: Optional[int] = None) -> Tuple[pd.DataFrame, str]:
        """Load bundled raw NYC TLC Uber data."""
        return cls.load_from_path(RAW_DATASET_PATH, nrows=nrows)
