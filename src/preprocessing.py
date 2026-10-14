"""
Data Preprocessing Module for Uber Demand and Dynamic Pricing Analytics.
Cleans raw input data, standardizes column names, applies explicit rules, and returns clean data.
"""
from typing import Tuple, Dict, Any
import pandas as pd
import numpy as np

from config.settings import LAT_MIN, LAT_MAX, LON_MIN, LON_MAX


class DataPreprocessor:
    """Preprocesses and standardizes heterogeneous ride-hailing datasets."""

    COLUMN_MAPPINGS = {
        # TLC Raw formats
        "date/time": "pickup_datetime",
        "lat": "pickup_latitude",
        "lon": "pickup_longitude",
        "base": "base_dispatch_code",
        # Kaggle NYC fare formats
        "fare_amount": "fare_amount",
        "pickup_datetime": "pickup_datetime",
        "pickup_longitude": "pickup_longitude",
        "pickup_latitude": "pickup_latitude",
        "dropoff_longitude": "dropoff_longitude",
        "dropoff_latitude": "dropoff_latitude",
        "passenger_count": "passenger_count"
    }

    @classmethod
    def standardize_column_names(cls, df: pd.DataFrame) -> pd.DataFrame:
        """Standardize various column naming conventions into unified snake_case."""
        df = df.copy()
        new_cols = {}
        for c in df.columns:
            clean_c = c.strip()
            lower_c = clean_c.lower()
            if lower_c in cls.COLUMN_MAPPINGS:
                new_cols[c] = cls.COLUMN_MAPPINGS[lower_c]
            else:
                new_cols[c] = clean_c.lower().replace(" ", "_").replace("-", "_")
        df.rename(columns=new_cols, inplace=True)
        return df

    @classmethod
    def clean_and_filter(cls, df: pd.DataFrame, drop_anomalies: bool = True) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """
        Cleans data types, parses timestamps, removes duplicate rows, and handles anomalies.
        Returns: (cleaned_df, cleaning_summary_dict)
        """
        initial_count = len(df)
        df_clean = cls.standardize_column_names(df)

        actions_taken = []

        # 1. Deduplication
        dups = df_clean.duplicated().sum()
        if dups > 0 and drop_anomalies:
            df_clean = df_clean.drop_duplicates()
            actions_taken.append(f"Removed {dups:,} duplicate records.")

        # 2. Parse pickup datetime
        if "pickup_datetime" in df_clean.columns:
            df_clean["pickup_datetime"] = pd.to_datetime(df_clean["pickup_datetime"], errors="coerce")
            invalid_dt = df_clean["pickup_datetime"].isna().sum()
            if invalid_dt > 0 and drop_anomalies:
                df_clean = df_clean.dropna(subset=["pickup_datetime"])
                actions_taken.append(f"Dropped {invalid_dt:,} records with unparseable timestamps.")

        # 3. Clean coordinates
        if "pickup_latitude" in df_clean.columns and "pickup_longitude" in df_clean.columns:
            df_clean["pickup_latitude"] = pd.to_numeric(df_clean["pickup_latitude"], errors="coerce")
            df_clean["pickup_longitude"] = pd.to_numeric(df_clean["pickup_longitude"], errors="coerce")
            if drop_anomalies:
                valid_geo = (
                    (df_clean["pickup_latitude"] >= LAT_MIN) &
                    (df_clean["pickup_latitude"] <= LAT_MAX) &
                    (df_clean["pickup_longitude"] >= LON_MIN) &
                    (df_clean["pickup_longitude"] <= LON_MAX)
                )
                geo_dropped = (~valid_geo).sum()
                if geo_dropped > 0:
                    df_clean = df_clean[valid_geo]
                    actions_taken.append(f"Filtered out {geo_dropped:,} records outside Indian urban metropolitan bounds.")

        # 4. Clean fares if present
        if "fare_amount" in df_clean.columns:
            df_clean["fare_amount"] = pd.to_numeric(df_clean["fare_amount"], errors="coerce")
            if drop_anomalies:
                valid_fares = (df_clean["fare_amount"] > 0) & (df_clean["fare_amount"] <= 50000)
                fare_dropped = (~valid_fares).sum()
                if fare_dropped > 0:
                    df_clean = df_clean[valid_fares]
                    actions_taken.append(f"Removed {fare_dropped:,} non-positive or extreme outlier fare records.")

        # 5. Clean distances if present
        if "trip_distance_km" in df_clean.columns:
            df_clean["trip_distance_km"] = pd.to_numeric(df_clean["trip_distance_km"], errors="coerce")
            if drop_anomalies:
                valid_dist = (df_clean["trip_distance_km"] > 0) & (df_clean["trip_distance_km"] <= 500)
                dist_dropped = (~valid_dist).sum()
                if dist_dropped > 0:
                    df_clean = df_clean[valid_dist]
                    actions_taken.append(f"Removed {dist_dropped:,} non-positive or extreme trip distance records.")

        # Reset index
        df_clean.reset_index(drop=True, inplace=True)
        final_count = len(df_clean)

        summary = {
            "initial_rows": initial_count,
            "final_rows": final_count,
            "dropped_rows": initial_count - final_count,
            "retention_rate_pct": round((final_count / initial_count) * 100, 2) if initial_count > 0 else 0.0,
            "actions_taken": actions_taken
        }

        return df_clean, summary
