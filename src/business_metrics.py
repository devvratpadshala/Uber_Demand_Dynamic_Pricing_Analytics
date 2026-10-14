"""
Business Metrics and Executive KPIs Calculation Module.
Computes observed operational indicators, volume statistics, and period-over-period trends.
"""
from typing import Dict, Any, Optional
import pandas as pd
import numpy as np


class BusinessMetrics:
    """Calculates executive metrics and operational performance indicators."""

    @staticmethod
    def calculate_executive_kpis(df: pd.DataFrame) -> Dict[str, Any]:
        """
        Compute top-level business indicators supported by the active dataset.
        Handles missing fields gracefully.
        """
        total_trips = len(df)
        if total_trips == 0:
            return {"total_trips": 0}

        kpis: Dict[str, Any] = {
            "total_trips": total_trips,
            "has_fares": "fare_amount" in df.columns,
            "has_distances": "trip_distance_km" in df.columns,
            "has_durations": "trip_duration_min" in df.columns,
            "has_zones": "pickup_zone" in df.columns
        }

        # Date range & daily averages
        if "pickup_datetime" in df.columns:
            min_date = df["pickup_datetime"].min()
            max_date = df["pickup_datetime"].max()
            num_days = max(1, (max_date - min_date).days + 1)
            kpis["date_min"] = min_date.strftime("%Y-%m-%d")
            kpis["date_max"] = max_date.strftime("%Y-%m-%d")
            kpis["total_days_observed"] = num_days
            kpis["avg_trips_per_day"] = round(total_trips / num_days, 1)

        # Fare and revenue metrics
        if "fare_amount" in df.columns:
            total_fare_rev = float(df["fare_amount"].sum())
            avg_fare = float(df["fare_amount"].mean())
            median_fare = float(df["fare_amount"].median())
            kpis["total_recorded_fares"] = round(total_fare_rev, 2)
            kpis["avg_fare"] = round(avg_fare, 2)
            kpis["median_fare"] = round(median_fare, 2)

        # Distance metrics
        if "trip_distance_km" in df.columns:
            kpis["avg_distance_km"] = round(float(df["trip_distance_km"].mean()), 2)
            kpis["total_passenger_km"] = round(float(df["trip_distance_km"].sum()), 1)

        # Duration metrics
        if "trip_duration_min" in df.columns:
            kpis["avg_duration_min"] = round(float(df["trip_duration_min"].mean()), 1)

        # Peak hour metrics
        if "pickup_hour" in df.columns:
            hourly_counts = df["pickup_hour"].value_counts()
            peak_hour = int(hourly_counts.idxmax())
            kpis["peak_hour_24h"] = peak_hour
            kpis["peak_hour_label"] = f"{peak_hour:02d}:00 - {peak_hour+1:02d}:00"
            kpis["peak_hour_trips"] = int(hourly_counts.max())

        # Day of week metrics
        if "pickup_day_name" in df.columns:
            dow_counts = df["pickup_day_name"].value_counts()
            kpis["highest_demand_day"] = str(dow_counts.idxmax())
            kpis["lowest_demand_day"] = str(dow_counts.idxmin())

        # Peak vs off-peak percentage
        if "is_peak_hour" in df.columns:
            peak_pct = round((df["is_peak_hour"].sum() / total_trips) * 100, 1)
            kpis["peak_trips_share_pct"] = peak_pct

        # Weekend vs weekday percentage
        if "is_weekend" in df.columns:
            weekend_pct = round((df["is_weekend"].sum() / total_trips) * 100, 1)
            kpis["weekend_trips_share_pct"] = weekend_pct

        return kpis

    @staticmethod
    def get_zone_performance(df: pd.DataFrame) -> pd.DataFrame:
        """Summarizes volume and economic performance aggregated by zone."""
        if "pickup_zone" not in df.columns:
            return pd.DataFrame()

        agg_dict: Dict[str, Any] = {"trip_id": "count"} if "trip_id" in df.columns else {"pickup_datetime": "count"}
        rename_dict = {"trip_id": "Total Trips", "pickup_datetime": "Total Trips"}

        if "fare_amount" in df.columns:
            agg_dict["fare_amount"] = ["mean", "sum"]
        if "trip_distance_km" in df.columns:
            agg_dict["trip_distance_km"] = "mean"

        zone_df = df.groupby("pickup_zone").agg(agg_dict)
        zone_df.columns = ["_".join(c).strip("_") for c in zone_df.columns.values]
        zone_df.reset_index(inplace=True)
        return zone_df
