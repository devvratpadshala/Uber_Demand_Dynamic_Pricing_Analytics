"""
Demand Analytics Page.
Module 2: Granular Temporal Trends, Day-Hour Heatmaps, Spatial Distributions, and Statistical Tests.
"""
import streamlit as st
import pandas as pd
from src.descriptive_analytics import DescriptiveAnalytics
from src.visualizations import Visualizer
from src.statistical_analysis import StatisticalAnalyzer

st.set_page_config(page_title="Demand Analytics | Uber Analytics", page_icon="📈", layout="wide")

st.title("📈 Demand Analytics")
st.markdown("Detailed exploration of ride demand patterns across temporal, spatial, and statistical dimensions.")

if "data_bundle" not in st.session_state:
    st.warning("Data not initialized. Please load the main application dashboard first.")
    st.stop()

df = st.session_state["data_bundle"]["clean_df"]

tab1, tab2, tab3 = st.tabs(["🕒 Temporal Patterns", "🗺️ Geographic & Zone Analysis", "🧪 Statistical Hypothesis Testing"])

with tab1:
    st.subheader("Hourly & Daily Demand Trends")
    c1, c2 = st.columns(2)
    with c1:
        hourly_df = DescriptiveAnalytics.get_hourly_demand(df)
        fig_hour = Visualizer.plot_hourly_demand(hourly_df)
        st.plotly_chart(fig_hour, use_container_width=True)

    with c2:
        daily_df = DescriptiveAnalytics.get_daily_demand(df)
        fig_day = Visualizer.plot_daily_demand(daily_df)
        st.plotly_chart(fig_day, use_container_width=True)

    st.subheader("Demand Concentration Matrix (Day of Week vs. Hour of Day)")
    pivot_matrix = DescriptiveAnalytics.get_hour_day_heatmap_matrix(df)
    if not pivot_matrix.empty:
        fig_heat = Visualizer.plot_demand_heatmap(pivot_matrix)
        st.plotly_chart(fig_heat, use_container_width=True)
    else:
        st.info("Insufficient temporal fields for heatmap rendering.")

    st.subheader("Demand Breakdown by Time of Day Period")
    period_df = DescriptiveAnalytics.get_time_period_summary(df)
    if not period_df.empty:
        st.dataframe(period_df, use_container_width=True)

with tab2:
    st.subheader("Spatial Zone Distribution")
    if "pickup_zone" in df.columns:
        zone_summary = df["pickup_zone"].value_counts().reset_index()
        zone_summary.columns = ["pickup_zone", "Total Trips"]
        fig_zone = Visualizer.plot_zone_demand(zone_summary)
        st.plotly_chart(fig_zone, use_container_width=True)
    else:
        st.info("Spatial zone features not present in active dataset.")

    st.subheader("Geographic Pickups Distribution Map")
    if "pickup_latitude" in df.columns and "pickup_longitude" in df.columns:
        fig_map = Visualizer.plot_geographic_scatter(df)
        st.plotly_chart(fig_map, use_container_width=True)
    else:
        st.info("Geographic coordinates unavailable for map plotting.")

    if "fare_amount" in df.columns and "trip_distance_km" in df.columns:
        st.subheader("Econometric Fare vs. Trip Distance Relationship")
        fig_scatter = Visualizer.plot_fare_vs_distance(df)
        st.plotly_chart(fig_scatter, use_container_width=True)

with tab3:
    st.subheader("Academic Statistical Hypothesis Testing (BAV)")
    st.markdown("Hypothesis testing conducted at significance level α = 0.05.")

    st.markdown("### 1. Weekday vs. Weekend Demand Comparison")
    stat_test1 = StatisticalAnalyzer.test_weekday_vs_weekend_demand(df)
    if "error" in stat_test1:
        st.warning(stat_test1["error"])
    else:
        col_t1, col_t2 = st.columns(2)
        with col_t1:
            st.write(f"**Test Applied:** {stat_test1['test_name']}")
            st.write(f"**Null Hypothesis:** {stat_test1['null_hypothesis']}")
            st.write(f"**Alternative Hypothesis:** {stat_test1['alt_hypothesis']}")
        with col_t2:
            st.metric("Test Statistic", f"{stat_test1['test_statistic']}")
            st.metric("p-value", f"{stat_test1['p_value']}")
            st.metric("Decision", "Reject H₀" if stat_test1["reject_null"] else "Fail to Reject H₀")
        st.success(f"**Interpretation:** {stat_test1['interpretation']}")

    st.markdown("---")
    st.markdown("### 2. Time-of-Day Demand Variance (One-Way ANOVA)")
    stat_test2 = StatisticalAnalyzer.test_demand_by_time_period(df)
    if "error" in stat_test2:
        st.warning(stat_test2["error"])
    else:
        st.write(f"**Test Applied:** {stat_test2['test_name']}")
        st.write(f"**Null Hypothesis:** {stat_test2['null_hypothesis']}")
        st.metric("F-Statistic", f"{stat_test2['test_statistic']}")
        st.metric("p-value", f"{stat_test2['p_value']:.4e}")
        st.success(f"**Interpretation:** {stat_test2['interpretation']}")

    if "fare_amount" in df.columns and "trip_distance_km" in df.columns:
        st.markdown("---")
        st.markdown("### 3. Distance vs. Fare Correlation Analysis")
        stat_test3 = StatisticalAnalyzer.test_correlation_distance_fare(df)
        if "error" not in stat_test3:
            col_c1, col_c2 = st.columns(2)
            with col_c1:
                st.metric("Pearson Correlation (r)", f"{stat_test3['pearson_r']}")
            with col_c2:
                st.metric("Spearman Rank Correlation (ρ)", f"{stat_test3['spearman_rho']}")
            st.info(f"**Interpretation:** {stat_test3['interpretation']}")
