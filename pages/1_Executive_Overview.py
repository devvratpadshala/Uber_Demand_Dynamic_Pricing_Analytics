"""
Executive Overview Dashboard Page.
Module 1: Top-Level Business KPIs, Volume Metrics, and High-Level Insights.
"""
import streamlit as st
import pandas as pd
from src.business_metrics import BusinessMetrics
from config.settings import CURRENCY_SYMBOL

st.set_page_config(page_title="Executive Overview | Uber Analytics", page_icon="📊", layout="wide")

st.title("📊 Executive Overview")
st.markdown("Top-level operational and business indicators derived from active ride-hailing observations.")

# Retrieve data from session state or load default
if "data_bundle" not in st.session_state:
    st.warning("Data not initialized. Please load the main application dashboard first.")
    st.stop()

df = st.session_state["data_bundle"]["clean_df"]
kpis = BusinessMetrics.calculate_executive_kpis(df)

# Top KPI Metric Cards
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.metric("Total Trips Observed", f"{kpis['total_trips']:,}")
with c2:
    st.metric("Avg Trips / Day", f"{kpis.get('avg_trips_per_day', 0):,}")
with c3:
    if kpis.get("has_fares"):
        st.metric("Avg Trip Fare", f"{CURRENCY_SYMBOL}{kpis.get('avg_fare', 0):.2f}")
    else:
        st.metric("Avg Trip Fare", "N/A (No Fare Data)")
with c4:
    if kpis.get("has_distances"):
        st.metric("Avg Trip Distance", f"{kpis.get('avg_distance_km', 0):.2f} km")
    else:
        st.metric("Avg Trip Distance", "N/A (No Distance)")

st.markdown("---")

c5, c6, c7, c8 = st.columns(4)
with c5:
    st.metric("Peak Demand Hour", kpis.get("peak_hour_label", "N/A"))
with c6:
    st.metric("Highest Demand Day", kpis.get("highest_demand_day", "N/A"))
with c7:
    st.metric("Peak Period Share", f"{kpis.get('peak_trips_share_pct', 0)}%")
with c8:
    st.metric("Weekend Share", f"{kpis.get('weekend_trips_share_pct', 0)}%")

st.markdown("---")

# Executive Business Insights Section
st.subheader("💡 Data-Supported Executive Findings")
col_left, col_right = st.columns(2)

with col_left:
    st.markdown("### Operational Demand Dynamics")
    st.write(
        f"- **Peak Hour Window:** The single highest concentration of demand occurs at "
        f"**{kpis.get('peak_hour_label', 'peak hours')}**, accounting for **{kpis.get('peak_hour_trips', 0):,}** pickups."
    )
    st.write(
        f"- **Weekly Distribution:** **{kpis.get('highest_demand_day', 'Weekdays')}** records the maximum observed trip density, "
        f"while **{kpis.get('lowest_demand_day', 'Sundays')}** exhibits lower demand volume."
    )
    st.write(
        f"- **Rush Hour Exposure:** **{kpis.get('peak_trips_share_pct', 0)}%** of all trips occur during scheduled morning and evening rush intervals."
    )

with col_right:
    st.markdown("### Economic & Revenue Metrics")
    if kpis.get("has_fares"):
        st.write(
            f"- **Gross Observed Fares:** Total fare revenue recorded across the dataset is **{CURRENCY_SYMBOL}{kpis.get('total_recorded_fares', 0):,.2f}**."
        )
        st.write(
            f"- **Median Fare vs. Average:** The median fare is **{CURRENCY_SYMBOL}{kpis.get('median_fare', 0):.2f}**, demonstrating a well-bounded central tendency."
        )
        if kpis.get("has_distances"):
            st.write(
                f"- **Passenger Mobility:** Total passenger distance traveled sums to **{kpis.get('total_passenger_km', 0):,.1f} passenger-km**."
            )
    else:
        st.info("The active dataset does not include fare variables. Load the Demonstration Dataset to explore financial metrics.")

# Zone Summary Table if available
if kpis.get("has_zones"):
    st.markdown("---")
    st.subheader("🏙️ Demand & Economics by Urban Zone")
    zone_perf = BusinessMetrics.get_zone_performance(df)
    st.dataframe(zone_perf, use_container_width=True)
