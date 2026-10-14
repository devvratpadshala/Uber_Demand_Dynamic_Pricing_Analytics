# Viva-Voce Oral Examination Preparation Guide
## Subject: Business Analytics and Visualization (BAV) — CVM University

This guide prepares you to explain the technical, statistical, and business aspects of your project during faculty evaluation.

---

### Q1: What is the primary objective of this project?
**Answer:** The project delivers an interactive business analytics platform to model ride-hailing demand patterns, evaluate statistical differences in temporal demand, benchmark time-series forecasting models, and simulate supply-demand dynamic surge pricing in an educational and explainable manner.

---

### Q2: What dataset did you use, and what are its limitations?
**Answer:** The project uses a rich dataset calibrated specifically for **Indian Metropolitan Urban Mobility (Mumbai MMR & Western Corridors)**, covering key business districts like **Bandra Kurla Complex (BKC), Andheri East, South Mumbai & Fort, Powai Tech Zone, Airport T2, and Navi Mumbai**.  
*Data formulation:* Trip pickup timestamps reflect continuous urban demand cycles, while coordinates, distances (1.0 to 35.0 km), Indian traffic transit durations, and fares (Base ₹50 + ₹14.5/km + ₹2/min) are calibrated to Indian metropolitan economics. Proprietary internal Uber dispatch matching and real surge multipliers remain confidential to Uber and are transparently modeled via scenario simulations.

---

### Q3: How did you calculate ride demand?
**Answer:** Ride demand is quantified by aggregating trip pickup frequencies across temporal buckets:
- Hourly demand (0 to 23 hours).
- Daily volume across days of the week.
- Continuous 1-hour time-series resampled intervals for forecasting.

---

### Q4: How does your Dynamic Pricing Simulator work?
**Answer:** It uses an explicit microeconomic surge model:
$$\text{Demand-to-Supply Ratio (DSR)} = \frac{\text{Observed Demand}}{\text{Driver Supply}}$$
$$\text{Multiplier } M = \operatorname{clamp}(1.0 + k \cdot \max(0, \text{DSR} - 1.0), M_{\min}, M_{\max})$$
$$\text{Final Fare} = \text{Base Fare} \times M$$
When demand equals or is below supply ($\text{DSR} \le 1.0$), the multiplier stays at $1.0\times$. When demand exceeds supply, excess demand scales the multiplier by sensitivity factor $k$ up to a maximum safety ceiling $M_{\max}$.

---

### Q5: What statistical tests did you implement and why?
**Answer:**
1. **Two-Sample Test (t-test / Mann-Whitney U):** Tests if weekday daily demand differs significantly from weekend demand ($p < 0.05$).
2. **One-Way ANOVA:** Tests if demand varies significantly across daily time blocks (Morning, Afternoon, Evening, Night).
3. **Pearson & Spearman Correlation:** Verifies the econometric relationship between trip distance and fare amount.

---

### Q6: How did you evaluate your Demand Forecasting models?
**Answer:** We performed a **chronological out-of-sample train/test split** (80% train, 20% test) to prevent future data from leaking into the past. We benchmarked:
1. **Naive Persistence ($t-1\text{h}$)**
2. **6-Hour Moving Average**
3. **Random Forest Regressor** using lag features ($t-1\text{h}, t-2\text{h}, t-24\text{h}$) and calendar variables.  
We evaluated using **MAE**, **RMSE**, and **MAPE**.

---

### Q7: Why is chronological splitting critical in time-series forecasting?
**Answer:** In time-series data, observations are autocorrelation-dependent. Standard random K-Fold cross-validation would use future data points to predict past events, causing massive data leakage and giving artificially optimistic, invalid evaluation metrics.

---

### Q8: What business recommendations did you derive?
**Answer:**
1. Pre-position drivers 30–45 minutes prior to identified morning (08:00–10:00) and evening (17:00–20:00) rush peaks.
2. Implement protective surge multiplier caps ($M_{\max} \le 3.5\times$) to avoid brand alienation during extreme urban mobility bottlenecks.
3. Offer targeted quest bonuses during high-yield late-night weekend windows to incentivize driver retention.
