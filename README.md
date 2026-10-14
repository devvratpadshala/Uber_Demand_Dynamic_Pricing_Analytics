# Uber Demand & Dynamic Pricing Analytics
## A Data-Driven Approach to Understanding Ride Demand, Pricing Patterns, and Business Optimization

**Subject:** Business Analytics and Visualization (BAV)  
**Program:** B.Tech Artificial Intelligence & Data Science, Semester VII  
**Institution:** CVM University  

---

## 📌 Project Overview
This project delivers a production-grade, interactive business analytics and dynamic pricing simulation system for urban ride-hailing operations. Built using Python, Streamlit, Plotly, Scikit-learn, and Statsmodels, the platform demonstrates the full analytical lifecycle:
$$\text{Data Ingestion} \rightarrow \text{Validation} \rightarrow \text{Sanitization} \rightarrow \text{EDA} \rightarrow \text{Feature Engineering} \rightarrow \text{Statistical Tests} \rightarrow \text{Forecasting} \rightarrow \text{Pricing Simulation}$$

### Key Modules:
1. **Executive Overview (`1_Executive_Overview.py`):** Real-time operational KPIs, period averages, peak demand volume, and executive insights.
2. **Demand Analytics (`2_Demand_Analytics.py`):** Diurnal patterns, day-of-week rhythms, 7x24 demand concentration heatmaps, spatial cluster distributions, and academic hypothesis testing (t-test / Mann-Whitney U, ANOVA, Pearson/Spearman correlations).
3. **Dynamic Pricing Simulator (`3_Pricing_Simulator.py`):** Interactive microeconomic surge pricing simulator with user-tunable sensitivity ($k$), demand-supply ratios, safety caps ($M_{\max}$), and response curves.
4. **Demand Forecasting (`4_Demand_Forecasting.py`):** Chronological out-of-sample time-series benchmarks comparing Naive Persistence ($t-1\text{h}$), 6-hour Moving Averages, and a Random Forest Regressor with feature importance analysis and CSV export.
5. **Data Quality Dashboard (`5_Data_Quality.py`):** Complete audit of missing values, out-of-bounds geographic coordinates, fare anomalies, duplicate filtering, and cleaned dataset export.

---

## 💻 Tech Stack & Requirements
- **Python:** 3.10, 3.11, 3.12, 3.13, or 3.14 (Verified on Python 3.14 Windows environment)
- **Dashboard & UI:** `Streamlit`, `Plotly`
- **Data Engineering:** `Pandas`, `NumPy`
- **Machine Learning & Stats:** `Scikit-learn`, `SciPy`, `Statsmodels`
- **Testing:** `Pytest`

---

## 🚀 Quick Start on Windows

### Method 1: Automated Batch Scripts (Recommended)
1. **First-Time Setup:**  
   Double-click `setup_project.bat` in the project root directory.  
   This creates a local `.venv` environment and installs all dependencies from `requirements.txt`.
2. **Launch Application:**  
   Double-click `run_project.bat`.  
   The interactive dashboard will automatically open in your default browser at `http://localhost:8501`.

### Method 2: Manual Terminal Execution (PowerShell / Command Prompt)
Open PowerShell or Command Prompt inside this folder:
```powershell
# 1. (Optional) Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate

# 2. Install dependencies
python -m pip install -r requirements.txt

# 3. Launch Streamlit app
streamlit run app.py
```

To stop the running application, press `Ctrl + C` in the terminal.

---

## 🧪 Running Automated Tests
The project includes a comprehensive suite of 15 unit tests covering data loaders, schema detection, outlier sanitization, business KPIs, surge pricing math, and predictive forecasting:
```powershell
python -m pytest tests -v
```

---

## 📂 Project Structure
```
Uber_Demand_Dynamic_Pricing_Analytics/
├── app.py                      # Main Streamlit application entrypoint
├── requirements.txt            # Python dependencies
├── README.md                   # User guide and project manual
├── setup_project.bat           # Automated Windows setup script
├── run_project.bat             # One-click Windows application launcher
├── .gitignore                  # Git ignore rules
│
├── config/
│   └── settings.py             # System paths, constants, and pricing defaults
│
├── data/
│   ├── raw/                    # Original FiveThirtyEight NYC TLC Uber trips
│   ├── processed/              # Sanitized data exports
│   ├── sample/                 # Bundled multi-dimensional demonstration data
│   └── DATA_DICTIONARY.md      # Field descriptions, units, and lineages
│
├── src/
│   ├── data_loader.py          # Multi-format CSV ingestion & schema detection
│   ├── data_validator.py       # Data quality audit & anomaly detection
│   ├── preprocessing.py        # Schema standardization & record sanitization
│   ├── feature_engineering.py  # Temporal, spatial & unit economic extraction
│   ├── business_metrics.py     # Executive KPI calculation engine
│   ├── descriptive_analytics.py# Hourly/daily breakdowns & heatmap matrices
│   ├── statistical_analysis.py # Hypothesis testing (t-test, ANOVA, correlation)
│   ├── pricing_simulator.py    # Explicit surge pricing mathematical engine
│   ├── demand_forecasting.py   # Chronological time-series forecasting & ML
│   └── visualizations.py       # High-performance interactive Plotly charts
│
├── pages/
│   ├── 1_Executive_Overview.py # Executive overview KPI dashboard
│   ├── 2_Demand_Analytics.py   # Temporal, spatial & statistical analytics
│   ├── 3_Pricing_Simulator.py  # Interactive dynamic pricing simulator
│   ├── 4_Demand_Forecasting.py # Predictive modeling & forecast exports
│   └── 5_Data_Quality.py       # Quality audit & cleaned data download
│
├── reports/
│   ├── project_report.md       # Comprehensive academic project report
│   ├── methodology.md          # Technical methodology and workflows
│   ├── findings.md             # Key empirical findings & analytics summary
│   ├── limitations.md          # Explicit boundaries, constraints & disclosures
│   ├── business_recommendations.md # Managerial strategies & trade-offs
│   └── viva_preparation.md     # Viva-voce oral exam Q&A guide
│
└── tests/
    ├── test_data_loader.py     # Schema detection and loader tests
    ├── test_preprocessing.py   # Validation and cleaning tests
    ├── test_business_metrics.py# KPI engine unit tests
    ├── test_pricing_simulator.py# Surge multiplier boundary & math tests
    └── test_forecasting.py     # Time-series split and ML regression tests
```

---

## 🎓 Academic Integrity & Data Policy
- **No Claim of Internal Uber Data:** Uber proprietary surge algorithms, dispatch matching software, and driver earnings records are not claimed or accessed.
- **Data Grounding:** Real geospatial pickup coordinates and timestamps are sourced from the **FiveThirtyEight NYC TLC Freedom of Information Law (FOIL)** dataset (CC BY 4.0).
- **Hypothetical Pricing Formulation:** The dynamic pricing simulator operates on an explicit microeconomic supply-demand multiplier model ($M = \operatorname{clamp}(1 + k \cdot \max(0, \text{DSR} - 1), M_{\min}, M_{\max})$), clearly labelled as an educational simulation.
