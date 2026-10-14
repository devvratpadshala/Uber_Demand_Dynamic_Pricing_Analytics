"""
Demand Forecasting Page.
Module 4: Practical Time-Series Predictive Modeling & Chronological Model Evaluation.
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from src.demand_forecasting import DemandForecaster

st.set_page_config(page_title="Demand Forecasting | Uber Analytics", page_icon="🔮", layout="wide")

st.title("🔮 Demand Forecasting & Predictive Analytics")
st.markdown("Chronological time-series forecasting benchmarks: Naive Baseline, 6h Moving Average, and Random Forest Regressor.")

if "data_bundle" not in st.session_state:
    st.warning("Data not initialized. Please load the main application dashboard first.")
    st.stop()

df = st.session_state["data_bundle"]["clean_df"]

if "pickup_datetime" not in df.columns:
    st.error("The active dataset does not possess a valid pickup timestamp column required for time-series modeling.")
    st.stop()

# Time-series aggregation
with st.spinner("Aggregating chronological hourly time series..."):
    try:
        ts_df = DemandForecaster.prepare_time_series(df, freq="h")
    except Exception as e:
        st.error(f"Time-series preparation error: {e}")
        st.stop()

st.sidebar.subheader("⚙️ Model Configuration")
test_split_pct = st.sidebar.slider("Test Set Chronological Split (%):", min_value=10, max_value=30, value=20, step=5) / 100.0

with st.spinner("Training predictive models on chronological train window..."):
    model_output = DemandForecaster.train_and_evaluate(ts_df, test_size_ratio=test_split_pct)

if "error" in model_output:
    st.warning(model_output["error"])
    st.stop()

metrics = model_output["metrics"]
results_df = model_output["results_df"]

# Benchmark Evaluation Metric Cards
st.subheader("🎯 Chronological Out-of-Sample Benchmark Evaluation")
col_n, col_ma, col_rf = st.columns(3)

with col_n:
    st.markdown("### 1. Naive Baseline (t - 1h)")
    st.metric("MAE", f"{metrics['Naive_Persistence']['MAE']:.2f} trips")
    st.metric("RMSE", f"{metrics['Naive_Persistence']['RMSE']:.2f}")
    if metrics['Naive_Persistence']['MAPE_pct']:
        st.metric("MAPE", f"{metrics['Naive_Persistence']['MAPE_pct']:.1f}%")

with col_ma:
    st.markdown("### 2. Moving Average (6h)")
    st.metric("MAE", f"{metrics['Moving_Average_6h']['MAE']:.2f} trips")
    st.metric("RMSE", f"{metrics['Moving_Average_6h']['RMSE']:.2f}")
    if metrics['Moving_Average_6h']['MAPE_pct']:
        st.metric("MAPE", f"{metrics['Moving_Average_6h']['MAPE_pct']:.1f}%")

with col_rf:
    st.markdown("### 3. Random Forest ML")
    mae_rf = metrics['Random_Forest']['MAE']
    mae_naive = metrics['Naive_Persistence']['MAE']
    improvement = round(((mae_naive - mae_rf) / mae_naive) * 100, 1) if mae_naive > 0 else 0
    st.metric("MAE", f"{mae_rf:.2f} trips", delta=f"{improvement}% vs Naive")
    st.metric("RMSE", f"{metrics['Random_Forest']['RMSE']:.2f}")
    if metrics['Random_Forest']['MAPE_pct']:
        st.metric("MAPE", f"{metrics['Random_Forest']['MAPE_pct']:.1f}%")

st.markdown("---")

# Chart: Actual vs Predicted Demand
st.subheader("📈 Chronological Forecast Horizon: Actual vs. Predicted Demand")
fig_fc = go.Figure()
fig_fc.add_trace(go.Scatter(
    x=results_df["timestamp"],
    y=results_df["actual_demand"],
    mode="lines",
    name="Actual Demand (Ground Truth)",
    line=dict(color="#111827", width=2.5)
))
fig_fc.add_trace(go.Scatter(
    x=results_df["timestamp"],
    y=results_df["random_forest_prediction"],
    mode="lines",
    name="Random Forest Regressor",
    line=dict(color="#2563EB", width=2, dash="solid")
))
fig_fc.add_trace(go.Scatter(
    x=results_df["timestamp"],
    y=results_df["naive_prediction"],
    mode="lines",
    name="Naive Persistence Baseline",
    line=dict(color="#9CA3AF", width=1.5, dash="dot")
))
fig_fc.update_layout(
    xaxis_title="Chronological Test Timestamp",
    yaxis_title="Hourly Trip Demand (Pickups)",
    template="plotly_white",
    hovermode="x unified",
    margin=dict(l=40, r=40, t=40, b=40)
)
st.plotly_chart(fig_fc, use_container_width=True)

# Feature Importance
st.markdown("---")
c_imp, c_down = st.columns([1.2, 0.8])

with c_imp:
    st.subheader("🌲 Random Forest Feature Importance")
    imp_dict = model_output["feature_importances"]
    imp_df = pd.DataFrame(list(imp_dict.items()), columns=["Feature", "Importance"]).sort_values(by="Importance", ascending=True)
    fig_imp = px.bar(imp_df, x="Importance", y="Feature", orientation="h", title="Predictor Variable Importance Weights", template="plotly_white")
    st.plotly_chart(fig_imp, use_container_width=True)

with c_down:
    st.subheader("📥 Export Forecasts")
    st.write("Download the generated test set predictions for further analysis or academic reporting.")
    csv_bytes = results_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download Forecast Results (CSV)",
        data=csv_bytes,
        file_name="uber_demand_forecast_predictions.csv",
        mime="text/csv"
    )
