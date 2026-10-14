"""
Feature Engineering Module for Uber Demand and Dynamic Pricing Analytics.
Extracts temporal, spatial, traffic, and unit economics features calibrated for Indian Metros.
"""
from typing import Optional
import pandas as pd
import numpy as np

from config.settings import MORNING_PEAK, EVENING_PEAK


class FeatureEngineer:
    """Engineers time, location, distance, and pricing features without target leakage."""

    @staticmethod
    def haversine_distance(lat1: pd.Series, lon1: pd.Series, lat2: pd.Series, lon2: pd.Series) -> pd.Series:
        """
        Calculate the great-circle distance between two points on the Earth in kilometers.
        """
        r = 6371.0  # Earth radius in kilometers
        phi1 = np.radians(lat1)
        phi2 = np.radians(lat2)
        delta_phi = np.radians(lat2 - lat1)
        delta_lambda = np.radians(lon2 - lon1)

        a = np.sin(delta_phi / 2.0)**2 + np.cos(phi1) * np.cos(phi2) * np.sin(delta_lambda / 2.0)**2
        c = 2.0 * np.arctan2(np.sqrt(a), np.sqrt(1.0 - a))
        return (r * c).round(2)

    @classmethod
    def extract_temporal_features(cls, df: pd.DataFrame) -> pd.DataFrame:
        """Derives time-based features from pickup_datetime."""
        df = df.copy()
        if "pickup_datetime" not in df.columns:
            return df

        dt = pd.to_datetime(df["pickup_datetime"])
        df["pickup_date"] = dt.dt.date
        df["pickup_hour"] = dt.dt.hour
        df["pickup_dayofweek"] = dt.dt.dayofweek  # 0=Monday, 6=Sunday
        df["pickup_day_name"] = dt.dt.day_name()
        df["pickup_month"] = dt.dt.month
        df["pickup_quarter"] = dt.dt.quarter

        # Weekend indicator (5=Sat, 6=Sun)
        df["is_weekend"] = df["pickup_dayofweek"].isin([5, 6]).astype(int)

        # Peak hours indicator (Indian office commute hours)
        morning = (df["pickup_hour"] >= MORNING_PEAK[0]) & (df["pickup_hour"] < MORNING_PEAK[1])
        evening = (df["pickup_hour"] >= EVENING_PEAK[0]) & (df["pickup_hour"] < EVENING_PEAK[1])
        df["is_peak_hour"] = (morning | evening).astype(int)

        # Time period category
        def categorize_period(h: int) -> str:
            if 6 <= h < 12:
                return "Morning Rush"
            elif 12 <= h < 17:
                return "Afternoon"
            elif 17 <= h < 22:
                return "Evening Peak"
            elif 22 <= h < 24:
                return "Late Night"
            else:
                return "Early Hours"

        df["time_period"] = df["pickup_hour"].apply(categorize_period)
        return df

    @classmethod
    def extract_spatial_features(cls, df: pd.DataFrame) -> pd.DataFrame:
        """Derives Indian spatial zones and distances if coordinate fields exist."""
        df = df.copy()

        # If coordinates exist but zone is missing, assign Indian metro zone clusters
        if "pickup_latitude" in df.columns and "pickup_longitude" in df.columns and "pickup_zone" not in df.columns:
            def assign_indian_zone(lat, lon):
                if pd.isna(lat) or pd.isna(lon):
                    return "Unknown Zone"
                # Indian Metro Cluster matching
                if lat >= 19.10 and lon <= 72.88:
                    return "Andheri East Commercial Hub"
                elif lat >= 19.05 and lat < 19.10 and lon <= 72.88:
                    return "Bandra Kurla Complex (BKC)"
                elif lat < 19.00:
                    return "South Mumbai & Fort Financial District"
                elif lat >= 19.10 and lon > 72.88:
                    return "Powai Hiranandani Tech Zone"
                elif lon > 72.95:
                    return "Navi Mumbai & Vashi Infotech Park"
                else:
                    return "Chhatrapati Shivaji Terminal & Airport T2"

            df["pickup_zone"] = [assign_indian_zone(lat, lon) for lat, lon in zip(df["pickup_latitude"], df["pickup_longitude"])]

        # If dropoff coordinates exist but distance is missing, compute haversine distance
        if ("pickup_latitude" in df.columns and "dropoff_latitude" in df.columns and
            "trip_distance_km" not in df.columns):
            df["trip_distance_km"] = cls.haversine_distance(
                df["pickup_latitude"], df["pickup_longitude"],
                df["dropoff_latitude"], df["dropoff_longitude"]
            )

        return df

    @classmethod
    def extract_economic_features(cls, df: pd.DataFrame) -> pd.DataFrame:
        """Calculates derived unit economics metrics (fare per km, fare per min)."""
        df = df.copy()
        if "fare_amount" in df.columns and "trip_distance_km" in df.columns:
            valid_dist = df["trip_distance_km"] > 0.1
            df["fare_per_km"] = np.where(valid_dist, (df["fare_amount"] / df["trip_distance_km"]).round(2), np.nan)

        if "fare_amount" in df.columns and "trip_duration_min" in df.columns:
            valid_dur = df["trip_duration_min"] > 0.5
            df["fare_per_min"] = np.where(valid_dur, (df["fare_amount"] / df["trip_duration_min"]).round(2), np.nan)

        return df

    @classmethod
    def engineer_all(cls, df: pd.DataFrame) -> pd.DataFrame:
        """Run complete feature engineering pipeline."""
        df = cls.extract_temporal_features(df)
        df = cls.extract_spatial_features(df)
        df = cls.extract_economic_features(df)
        return df
