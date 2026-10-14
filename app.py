"""
Main Streamlit Application Entrypoint.
Uber Demand and Dynamic Pricing Analytics: A Data-Driven Approach.
"""
import sys
from pathlib import Path
import streamlit as st
import pandas as pd

# Add project root to sys.path to enable clean imports across pages
ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from config.settings import DEFAULT_DATASET_PATH, RAW_DATASET_PATH, CURRENCY_SYMBOL
from src.data_loader import DataLoader
from src.data_validator import DataValidator
from src.preprocessing import DataPreprocessor
from src.feature_engineering import FeatureEngineer

# Page Configuration
st.set_page_config(
    page_title="Uber Demand & Dynamic Pricing Analytics",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E293B;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #64748B;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background-color: #F8FAFC;
        border-radius: 8px;
        padding: 1rem;
        border-left: 4px solid #3B82F6;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_data(show_spinner=False)
def load_and_prepare_dataset(source_type: str, file_path_or_buffer=None, nrows: int = 25000):
    """Cached loader and preprocessor to maintain rapid dashboard response."""
    if source_type == "demonstration":
        raw_df, schema = DataLoader.load_default_demonstration(nrows=nrows)
    elif source_type == "raw_tlc":
        raw_df, schema = DataLoader.load_raw_tlc_sample(nrows=nrows)
    elif source_type == "uploaded" and file_path_or_buffer is not None:
        raw_df, schema = DataLoader.load_from_buffer(file_path_or_buffer, nrows=nrows)
    else:
        raw_df, schema = DataLoader.load_default_demonstration(nrows=nrows)

    # Validate raw
    validation_report = DataValidator.validate_dataset(raw_df, schema)

    # Preprocess & Feature Engineer
    clean_df, clean_summary = DataPreprocessor.clean_and_filter(raw_df)
    enriched_df = FeatureEngineer.engineer_all(clean_df)

    return {
        "raw_df": raw_df,
        "clean_df": enriched_df,
        "schema": schema,
        "validation_report": validation_report,
        "clean_summary": clean_summary
    }


def main():
    # Sidebar: Dataset Selection & Scope Controls
    st.sidebar.title("🚖 Analytics Controls")
    dataset_option = st.sidebar.radio(
        "Select Active Dataset:",
        options=["Bundled Demonstration Dataset", "Raw FiveThirtyEight NYC TLC Data", "Upload Custom CSV"],
        index=0
    )

    uploaded_file = None
    if dataset_option == "Upload Custom CSV":
        uploaded_file = st.sidebar.file_uploader(
            "Upload Ride CSV",
            type=["csv"],
            help="Upload a CSV with pickup timestamps and optional coordinate/fare columns."
        )

    # Map radio choice to loader key
    if dataset_option == "Bundled Demonstration Dataset":
        source_key = "demonstration"
        arg_val = None
    elif dataset_option == "Raw FiveThirtyEight NYC TLC Data":
        source_key = "raw_tlc"
        arg_val = None
    else:
        if uploaded_file is not None:
            source_key = "uploaded"
            arg_val = uploaded_file
        else:
            st.sidebar.info("Awaiting CSV upload. Falling back to demonstration dataset.")
            source_key = "demonstration"
            arg_val = None

    row_limit = st.sidebar.slider("Maximum Rows to Ingest:", min_value=5000, max_value=50000, value=25000, step=5000)

    with st.spinner("Ingesting, validating, and preprocessing ride records..."):
        data_bundle = load_and_prepare_dataset(source_key, arg_val, nrows=row_limit)

    # Store in session state for child pages
    st.session_state["data_bundle"] = data_bundle
    df = data_bundle["clean_df"]

    # Main Home View
    st.markdown('<div class="main-header">Uber Demand & Dynamic Pricing Analytics</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Business Analytics & Visualization (BAV) — CVM University Mini-Project</div>', unsafe_allow_html=True)

    st.info(
        "📌 **Academic Integrity Disclosure:** This analytical system is built for academic research in Business Analytics. "
        "Dynamic pricing scenarios and surge multipliers are simulated using explicit economic models and are clearly distinguished "
        "from Uber's proprietary operational algorithms."
    )

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Records Ingested", f"{len(df):,}")
    with col2:
        st.metric("Date Span", f"{df['pickup_datetime'].min().strftime('%d %b %Y')} – {df['pickup_datetime'].max().strftime('%d %b %Y')}" if 'pickup_datetime' in df.columns else "N/A")
    with col3:
        st.metric("Dataset Type", data_bundle["schema"].replace("_", " ").title())
    with col4:
        st.metric("Data Quality Retention", f"{data_bundle['clean_summary']['retention_rate_pct']}%")

    st.markdown("---")
    st.subheader("📑 Project Overview & Module Navigation")
    st.markdown("""
    Use the sidebar menu on the left to explore each analytical module:

    1. **1 Executive Overview:** Top-level KPIs, total volume, peak indicators, and period-over-period performance.
    2. **2 Demand Analytics:** Granular temporal breakdowns (hourly, daily), heatmap concentration matrices, and spatial zone distributions.
    3. **3 Pricing Simulator:** Interactive supply-demand surge scenario simulator with sensitivity controls and response curves.
    4. **4 Demand Forecasting:** Predictive time-series modeling comparing Naive baselines, Moving Averages, and Random Forest Regressor.
    5. **5 Data Quality:** Transparent audit dashboard detailing missing fields, outliers, geographic bounds, and cleaning actions.
    """)

    st.subheader("🔍 Ingested Data Sample (Top 5 Clean Records)")
    st.dataframe(df.head(5), use_container_width=True)


if __name__ == "__main__":
    main()
