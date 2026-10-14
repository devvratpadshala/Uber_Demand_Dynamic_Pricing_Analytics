# Project Limitations and Analytical Boundaries

## 1. Proprietary Algorithm Boundary
- **Uber Proprietary Systems:** Neither Uber's internal dispatch algorithm, real-time matching engine, nor proprietary surge multiplier data are available in open datasets.
- **Simulation Distinction:** All dynamic pricing analyses in this system are explicitly labelled as **educational microeconomic simulations**, not empirical representations of Uber's proprietary pricing algorithms.

## 2. Dataset Scope Constraints
- **Univariate Trip Events:** The public NYC TLC FOIL dataset contains pickup coordinates and timestamps. It does not record passenger cancellations, wait times, or unfulfilled ride requests (unmet demand).
- **Driver Supply Measurement:** Driver supply in the pricing simulator is user-adjustable rather than empirically observed from telemetry tracking.
- **Geography:** The primary empirical dataset reflects April 2014 New York City mobility. Findings should not be assumed to mirror modern Indian or suburban ride-hailing dynamics without localized calibration.

## 3. Machine Learning Generalization
- **Historical Lags:** Forecasting relies on regular historical aggregations. Severe unexpected exogenous shocks (such as sudden extreme weather or transit outages) cannot be anticipated purely by historical autoregression without external weather API integration.
