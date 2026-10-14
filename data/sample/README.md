# Demonstration / Sample Datasets

This directory contains bundled demonstration datasets calibrated for multi-dimensional business analytics (demand volume, spatial distribution, fares, and pricing simulations).

## 1. uber_demand_demonstration_dataset.csv
- **Origin:** Grounded directly on the actual FiveThirtyEight NYC TLC April 2014 pickup timestamps and coordinates (25,000 verified trip events).
- **Enriched Operational Fields (Clearly Labelled Synthetic Modeling):**
  - 	rip_id: Synthetic unique identifier
  - pickup_datetime: Actual NYC TLC pickup timestamp
  - pickup_latitude: Actual NYC TLC latitude
  - pickup_longitude: Actual NYC TLC longitude
  - pickup_zone: Derived spatial cluster zone (Midtown East, Midtown West, Lower Manhattan, Brooklyn Downtown, Upper Manhattan, Queens / Airport Hub)
  - 	rip_distance_km: Synthetic distance calibrated on urban trip log-normal distribution (mean ~4.5 km)
  - 	rip_duration_min: Calibrated urban transit duration (correlated with distance + transit delay)
  - are_amount: Standard fare structure (base fare INR 50 + distance rate + duration rate + peak multiplier + stochastic variance)
  - passenger_count: Discrete empirical passenger distribution (1 to 6)
  - ase_dispatch_code: Actual TLC base identifier
- **Important Disclosure:** Fares, trip distances, and passenger counts are synthesized based on explicit urban mobility assumptions to enable end-to-end BAV curriculum exercises (EDA, Regression, Statistical Hypothesis Testing, and Scenario Simulation).
