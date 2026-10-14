# Technical Methodology Document

## Overview
This document specifies the technical architecture, mathematical formulations, data pipelines, and validation strategies implemented in the **Uber Demand & Dynamic Pricing Analytics** system.

---

## 1. Data Ingestion & Sanitization Pipeline
### 1.1 Ingestion Architecture
The data ingestion engine (`src/data_loader.py`) implements multi-format schema detection:
- Automatic detection of `demonstration`, `nyc_tlc_raw`, and `kaggle_uber_fares` headers.
- Safe buffer streaming to support interactive Streamlit file uploads up to 50,000 rows.

### 1.2 Validation Rules (`src/data_validator.py`)
- **Geographic Bounding:** Valid coordinate envelope: Latitude $[40.40, 41.10]$, Longitude $[-74.30, -73.60]$.
- **Fare Filtering:** Fares outside the range $[₹10, ₹50,000]$ are flagged as corrupt data.
- **Deduplication:** Full-row duplicate scans applied prior to aggregation.

---

## 2. Feature Engineering
Feature transformations (`src/feature_engineering.py`) are computed deterministically without target leakage:
1. **Temporal Features:** `pickup_hour`, `pickup_dayofweek`, `is_weekend`, `is_peak_hour`, `time_period`.
2. **Spatial Distance:** Haversine formula for spherical great-circle distance:
   $$d = 2r \arcsin\left(\sqrt{\sin^2\left(\frac{\Delta\phi}{2}\right) + \cos(\phi_1)\cos(\phi_2)\sin^2\left(\frac{\Delta\lambda}{2}\right)}\right)$$
3. **Unit Economics:** $\text{Fare per km} = \frac{\text{Fare Amount}}{\text{Distance (km)}}$.

---

## 3. Statistical Analysis Protocol
1. **Shapiro-Wilk Normality Test:** Evaluates whether sample daily trip frequencies follow Gaussian distributions.
2. **Two-Sample Hypothesis Testing:** Selects between parametric Student's t-test and non-parametric Mann-Whitney U test depending on normality.
3. **One-Way ANOVA:** Compares variance across discrete diurnal time blocks.
4. **Correlation Analysis:** Pearson ($r$) and Spearman ($\rho$) coefficients to assess linearity and monotonicity between distance and trip fares.

---

## 4. Time-Series Forecasting Strategy
1. **Chronological Splitting:** Uses a continuous train/test split (80% historical, 20% future horizon). Random K-Fold splits are strictly prohibited to prevent data leakage.
2. **Feature Set:**
   - Temporal indices ($h$, $\text{day of week}$, $\text{is\_weekend}$).
   - Autoregressive lag features ($y_{t-1}, y_{t-2}, y_{t-24}$).
   - Rolling moving average ($6\text{h}$ mean, shifted by 1 hour).
3. **Models Evaluated:**
   - Naive Persistence: $\hat{y}_t = y_{t-1}$.
   - Rolling Moving Average: $\hat{y}_t = \frac{1}{6}\sum_{i=1}^6 y_{t-i}$.
   - Random Forest Regressor ($n=100$, $\text{max\_depth}=8$).
