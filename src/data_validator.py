"""
Data Validation Module for Uber Demand and Dynamic Pricing Analytics.
Validates input schemas, missing values, duplicate records, outliers, and geographic bounds.
"""
from typing import Dict, Any, List, Tuple
import pandas as pd
import numpy as np

from config.settings import LAT_MIN, LAT_MAX, LON_MIN, LON_MAX


class DataValidator:
    """Validates data integrity, provides cleaning summaries, and isolates invalid records."""

    @staticmethod
    def validate_dataset(df: pd.DataFrame, schema_type: str = "auto") -> Dict[str, Any]:
        """
        Run a battery of validation checks and generate a comprehensive quality report.
        """
        total_rows = len(df)
        if total_rows == 0:
            return {
                "is_valid": False,
                "error": "Dataset is empty.",
                "total_rows": 0,
                "valid_rows": 0,
                "invalid_rows": 0,
                "missing_summary": {},
                "duplicates_count": 0,
                "anomalies": {}
            }

        missing_counts = df.isnull().sum().to_dict()
        missing_pct = ((df.isnull().sum() / total_rows) * 100).round(2).to_dict()
        missing_summary = {
            col: {"count": int(missing_counts[col]), "pct": float(missing_pct[col])}
            for col in df.columns
        }

        # Check duplicate rows
        duplicates_count = int(df.duplicated().sum())

        anomalies: Dict[str, int] = {}
        invalid_mask = pd.Series(False, index=df.index)

        # 1. Coordinate check if latitude/longitude exist
        lat_col = next((c for c in df.columns if c.lower() in ["lat", "pickup_latitude", "pickup_lat"]), None)
        lon_col = next((c for c in df.columns if c.lower() in ["lon", "pickup_longitude", "pickup_lon"]), None)

        if lat_col and lon_col:
            numeric_lat = pd.to_numeric(df[lat_col], errors="coerce")
            numeric_lon = pd.to_numeric(df[lon_col], errors="coerce")
            geo_invalid = (
                numeric_lat.isna() | numeric_lon.isna() |
                (numeric_lat < LAT_MIN) | (numeric_lat > LAT_MAX) |
                (numeric_lon < LON_MIN) | (numeric_lon > LON_MAX)
            )
            anomalies["out_of_bounds_coordinates"] = int(geo_invalid.sum())
            invalid_mask = invalid_mask | geo_invalid

        # 2. Fare checks if fare exists
        fare_col = next((c for c in df.columns if "fare" in c.lower()), None)
        if fare_col:
            numeric_fare = pd.to_numeric(df[fare_col], errors="coerce")
            fare_invalid = numeric_fare.isna() | (numeric_fare <= 0) | (numeric_fare > 50000)
            anomalies["invalid_fares"] = int(fare_invalid.sum())
            invalid_mask = invalid_mask | fare_invalid

        # 3. Distance checks if distance exists
        dist_col = next((c for c in df.columns if "distance" in c.lower()), None)
        if dist_col:
            numeric_dist = pd.to_numeric(df[dist_col], errors="coerce")
            dist_invalid = numeric_dist.isna() | (numeric_dist <= 0) | (numeric_dist > 500)
            anomalies["invalid_distances"] = int(dist_invalid.sum())
            invalid_mask = invalid_mask | dist_invalid

        # 4. Duration checks if duration exists
        dur_col = next((c for c in df.columns if "duration" in c.lower()), None)
        if dur_col:
            numeric_dur = pd.to_numeric(df[dur_col], errors="coerce")
            dur_invalid = numeric_dur.isna() | (numeric_dur <= 0) | (numeric_dur > 1440)
            anomalies["invalid_durations"] = int(dur_invalid.sum())
            invalid_mask = invalid_mask | dur_invalid

        # 5. Timestamp validation
        dt_col = next((c for c in df.columns if "date" in c.lower() or "time" in c.lower()), None)
        if dt_col:
            parsed_dt = pd.to_datetime(df[dt_col], errors="coerce")
            dt_invalid = parsed_dt.isna()
            anomalies["invalid_timestamps"] = int(dt_invalid.sum())
            invalid_mask = invalid_mask | dt_invalid

        invalid_count = int(invalid_mask.sum())
        valid_count = total_rows - invalid_count

        return {
            "is_valid": valid_count > 0,
            "total_rows": total_rows,
            "valid_rows": valid_count,
            "invalid_rows": invalid_count,
            "duplicates_count": duplicates_count,
            "missing_summary": missing_summary,
            "anomalies": anomalies,
            "columns": list(df.columns),
            "invalid_mask": invalid_mask
        }
