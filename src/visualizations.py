"""
Interactive Visualizations Module for Uber Demand and Dynamic Pricing Analytics.
Generates responsive Plotly charts adhering to clean aesthetic and accessibility guidelines.
"""
from typing import Optional, List, Dict
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go


class Visualizer:
    """Generates rich Plotly charts with consistent themes and labels."""

    THEME = "plotly_white"
    PRIMARY_COLOR = "#1f77b4"
    ACCENT_COLOR = "#ff7f0e"

    @classmethod
    def plot_hourly_demand(cls, hourly_df: pd.DataFrame) -> go.Figure:
        """Interactive bar chart of ride demand by hour of the day."""
        fig = px.bar(
            hourly_df,
            x="pickup_hour",
            y="trip_count",
            text="trip_count",
            labels={"pickup_hour": "Hour of Day (24-Hour Clock)", "trip_count": "Total Ride Requests"},
            title="Observed Ride Demand by Hour of the Day",
            template=cls.THEME,
            color="trip_count",
            color_continuous_scale="Viridis"
        )
        fig.update_traces(texttemplate="%{text:,}", textposition="outside")
        fig.update_layout(
            xaxis=dict(tickmode="linear", tick0=0, dtick=1),
            margin=dict(l=40, r=40, t=50, b=40),
            coloraxis_showscale=False
        )
        return fig

    @classmethod
    def plot_daily_demand(cls, daily_df: pd.DataFrame) -> go.Figure:
        """Interactive bar chart of ride demand by day of week."""
        fig = px.bar(
            daily_df,
            x="day_name",
            y="trip_count",
            text="trip_count",
            labels={"day_name": "Day of the Week", "trip_count": "Total Ride Requests"},
            title="Weekly Rhythm: Observed Ride Demand by Day of Week",
            template=cls.THEME,
            color="trip_count",
            color_continuous_scale="Blues"
        )
        fig.update_traces(texttemplate="%{text:,}", textposition="outside")
        fig.update_layout(margin=dict(l=40, r=40, t=50, b=40), coloraxis_showscale=False)
        return fig

    @classmethod
    def plot_demand_heatmap(cls, pivot_df: pd.DataFrame) -> go.Figure:
        """Heatmap of Day of Week vs Hour of Day."""
        fig = px.imshow(
            pivot_df,
            labels=dict(x="Hour of Day (0-23)", y="Day of Week", color="Trips"),
            x=[f"{h:02d}:00" for h in pivot_df.columns],
            y=pivot_df.index,
            color_continuous_scale="YlOrRd",
            title="Demand Concentration Matrix: Day of Week vs. Hour of Day",
            aspect="auto",
            template=cls.THEME
        )
        fig.update_layout(margin=dict(l=40, r=40, t=50, b=40))
        return fig

    @classmethod
    def plot_zone_demand(cls, zone_df: pd.DataFrame) -> go.Figure:
        """Bar chart of demand distribution across urban zones."""
        col = "Total Trips" if "Total Trips" in zone_df.columns else zone_df.columns[1]
        sorted_df = zone_df.sort_values(by=col, ascending=True)
        fig = px.bar(
            sorted_df,
            x=col,
            y="pickup_zone",
            orientation="h",
            text=col,
            labels={col: "Total Pickups Observed", "pickup_zone": "Pickup Zone / District"},
            title="Spatial Demand Distribution Across Urban Pickup Zones",
            template=cls.THEME,
            color=col,
            color_continuous_scale="Tealgrn"
        )
        fig.update_traces(texttemplate="%{text:,}", textposition="outside")
        fig.update_layout(margin=dict(l=40, r=40, t=50, b=40), coloraxis_showscale=False)
        return fig

    @classmethod
    def plot_geographic_scatter(cls, df: pd.DataFrame, max_points: int = 2500) -> go.Figure:
        """Scatter map of pickup coordinates."""
        if "pickup_latitude" not in df.columns or "pickup_longitude" not in df.columns:
            return go.Figure()

        sample = df.sample(min(len(df), max_points), random_state=42)
        center_lat = float(sample["pickup_latitude"].mean())
        center_lon = float(sample["pickup_longitude"].mean())
        fig = px.scatter_mapbox(
            sample,
            lat="pickup_latitude",
            lon="pickup_longitude",
            color="pickup_zone" if "pickup_zone" in sample.columns else None,
            zoom=10.5,
            center=dict(lat=center_lat, lon=center_lon),
            title=f"Indian Urban Metro Pickups Distribution ({len(sample):,} Observed Points)",
            mapbox_style="open-street-map",
            template=cls.THEME
        )
        fig.update_layout(margin=dict(l=0, r=0, t=40, b=0))
        return fig

    @classmethod
    def plot_fare_vs_distance(cls, df: pd.DataFrame, max_points: int = 1500) -> go.Figure:
        """Scatter plot with trendline showing relationship between trip distance and fare."""
        if "trip_distance_km" not in df.columns or "fare_amount" not in df.columns:
            return go.Figure()

        sample = df.sample(min(len(df), max_points), random_state=42)
        fig = px.scatter(
            sample,
            x="trip_distance_km",
            y="fare_amount",
            trendline="ols",
            labels={"trip_distance_km": "Trip Distance (km)", "fare_amount": "Fare Amount (₹)"},
            title="Econometric Relationship: Trip Distance vs. Fare Charged",
            template=cls.THEME,
            opacity=0.6,
            color_discrete_sequence=["#2ca02c"]
        )
        fig.update_layout(margin=dict(l=40, r=40, t=50, b=40))
        return fig

    @classmethod
    def plot_pricing_simulation_curves(cls, demand_ratios: List[float], multipliers: List[float], fares: List[float]) -> go.Figure:
        """Plots simulated surge multipliers and final fares against demand-to-supply ratio."""
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=demand_ratios,
            y=multipliers,
            mode="lines+markers",
            name="Surge Multiplier (x)",
            line=dict(color="#d62728", width=3)
        ))
        fig.add_trace(go.Scatter(
            x=demand_ratios,
            y=fares,
            mode="lines",
            name="Simulated Fare (₹)",
            yaxis="y2",
            line=dict(color="#1f77b4", width=3, dash="dash")
        ))

        fig.update_layout(
            title="Dynamic Pricing Response Curve across Demand-to-Supply Ratios",
            xaxis=dict(title="Demand / Driver Supply Ratio"),
            yaxis=dict(title="Multiplier (x)", side="left"),
            yaxis2=dict(title="Simulated Fare (₹)", side="right", overlaying="y"),
            template=cls.THEME,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(l=40, r=40, t=60, b=40)
        )
        return fig
