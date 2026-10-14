"""
Descriptive Analytics Module for Uber Demand.
Computes temporal breakdowns, aggregations, and spatial volume distributions.
"""
from typing import Dict, Any, List
import pandas as pd
import numpy as np


class DescriptiveAnalytics:
    """Calculates descriptive aggregations across temporal and geographic dimensions."""

    @staticmethod
    def get_hourly_demand(df: pd.DataFrame) -> pd.DataFrame:
        """Aggregates demand (trips count) by 24 hours of the day."""
        if "pickup_hour" not in df.columns:
            return pd.DataFrame(columns=["pickup_hour", "trip_count", "percentage"])

        hourly = df["pickup_hour"].value_counts().sort_index().reset_index()
        hourly.columns = ["pickup_hour", "trip_count"]
        total = len(df)
        hourly["percentage"] = ((hourly["trip_count"] / total) * 100).round(2)
        return hourly

    @staticmethod
    def get_daily_demand(df: pd.DataFrame) -> pd.DataFrame:
        """Aggregates demand by day of week (Monday through Sunday)."""
        if "pickup_dayofweek" not in df.columns:
            return pd.DataFrame()

        day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        if "pickup_day_name" in df.columns:
            daily = df["pickup_day_name"].value_counts().reindex(day_order).fillna(0).reset_index()
            daily.columns = ["day_name", "trip_count"]
            daily["percentage"] = ((daily["trip_count"] / len(df)) * 100).round(2)
            return daily
        return pd.DataFrame()

    @staticmethod
    def get_hour_day_heatmap_matrix(df: pd.DataFrame) -> pd.DataFrame:
        """
        Builds a 7 x 24 pivot table: Day of week vs Hour of day.
        """
        if "pickup_day_name" not in df.columns or "pickup_hour" not in df.columns:
            return pd.DataFrame()

        day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        pivot = pd.crosstab(
            index=df["pickup_day_name"],
            columns=df["pickup_hour"],
            values=None,
            normalize=False
        )
        # Reindex days
        pivot = pivot.reindex(day_order).fillna(0)
        # Ensure all 24 hours exist
        for h in range(24):
            if h not in pivot.columns:
                pivot[h] = 0
        pivot = pivot[sorted(pivot.columns)]
        return pivot

    @staticmethod
    def get_time_period_summary(df: pd.DataFrame) -> pd.DataFrame:
        """Summarizes trips and metrics by time period (Morning, Afternoon, Evening Peak, Night)."""
        if "time_period" not in df.columns:
            return pd.DataFrame()

        period_order = ["Morning", "Afternoon", "Evening Peak", "Night", "Late Night"]
        agg_map = {"pickup_datetime": "count"}
        if "fare_amount" in df.columns:
            agg_map["fare_amount"] = "mean"
        if "trip_distance_km" in df.columns:
            agg_map["trip_distance_km"] = "mean"

        summary = df.groupby("time_period").agg(agg_map).reindex(period_order).dropna(how="all").reset_index()
        summary.rename(columns={"pickup_datetime": "trip_count"}, inplace=True)
        if "fare_amount" in summary.columns:
            summary["fare_amount"] = summary["fare_amount"].round(2)
        if "trip_distance_km" in summary.columns:
            summary["trip_distance_km"] = summary["trip_distance_km"].round(2)
        return summary
