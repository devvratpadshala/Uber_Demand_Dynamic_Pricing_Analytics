"""
Data Quality and Validation Dashboard Page.
Module 5: Missing Values, Geographic Bounding, Duplicate Audit, and Cleaned Dataset Export.
"""
import streamlit as st
import pandas as pd
from src.data_validator import DataValidator

st.set_page_config(page_title="Data Quality Audit | Uber Analytics", page_icon="🛡️", layout="wide")

st.title("🛡️ Data Quality & Audit Dashboard")
st.markdown("Detailed verification of data integrity, missing values, duplicates, outliers, and automated sanitization.")

if "data_bundle" not in st.session_state:
    st.warning("Data not initialized. Please load the main application dashboard first.")
    st.stop()

bundle = st.session_state["data_bundle"]
raw_df = bundle["raw_df"]
clean_df = bundle["clean_df"]
v_report = bundle["validation_report"]
c_summary = bundle["clean_summary"]

# Top Metrics
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.metric("Total Rows Loaded", f"{v_report['total_rows']:,}")
with c2:
    st.metric("Valid Ingested Records", f"{v_report['valid_rows']:,}")
with c3:
    st.metric("Duplicate Rows Detected", f"{v_report['duplicates_count']:,}")
with c4:
    st.metric("Cleaning Retention Rate", f"{c_summary['retention_rate_pct']}%")

st.markdown("---")

col_left, col_right = st.columns(2)

with col_left:
    st.subheader("📋 Missing Values by Column")
    missing_data = []
    for col, stats in v_report["missing_summary"].items():
        missing_data.append({
            "Column Name": col,
            "Missing Count": stats["count"],
            "Missing Percentage (%)": f"{stats['pct']}%"
        })
    st.dataframe(pd.DataFrame(missing_data), use_container_width=True)

with col_right:
    st.subheader("⚠️ Detected Anomalies & Outliers")
    anomalies = v_report.get("anomalies", {})
    if anomalies:
        anomaly_list = [{"Anomaly Category": k.replace("_", " ").title(), "Occurrences": v} for k, v in anomalies.items()]
        st.dataframe(pd.DataFrame(anomaly_list), use_container_width=True)
    else:
        st.success("No anomalies detected in the raw dataset.")

st.markdown("---")
st.subheader("🧹 Applied Sanitization & Preprocessing Actions")
if c_summary["actions_taken"]:
    for act in c_summary["actions_taken"]:
        st.write(f"- ✅ {act}")
else:
    st.info("No records required dropping; dataset conformed cleanly to boundary rules.")

st.markdown("---")
st.subheader("📥 Export Cleaned Dataset")
st.write("Download the verified, preprocessed, and feature-engineered dataset for external audit or modeling.")
csv_data = clean_df.to_csv(index=False).encode("utf-8")
st.download_button(
    label="Download Cleaned Dataset (CSV)",
    data=csv_data,
    file_name="uber_demand_cleaned_preprocessed.csv",
    mime="text/csv"
)
