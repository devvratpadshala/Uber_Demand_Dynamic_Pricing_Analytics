# Data Dictionary: Uber Demand & Dynamic Pricing Analytics
## Calibrated for Indian Metropolitan Regions (Mumbai MMR & Western Urban Corridors)

This document details all columns used across the application, specifying data types, units, source origin, and analytical relevance.

| Column Name | Data Type | Units | Origin | Description | Analytical Relevance |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `trip_id` | String | Categorical | Derived / Synthetic | Unique identifier for each ride observation (`IND_UBER_XXXXXX`) | Record tracking, deduplication |
| `pickup_datetime` | Datetime | YYYY-MM-DD HH:MM:SS | Time Series | Exact timestamp of trip request/pickup | Time-series aggregation, peak hour analysis |
| `pickup_latitude` | Float | Decimal Degrees | Indian Geocoordinates | Latitude coordinate of the pickup point (e.g. 19.0657 for BKC) | Spatial heatmaps, cluster bounding |
| `pickup_longitude` | Float | Decimal Degrees | Indian Geocoordinates | Longitude coordinate of the pickup point (e.g. 72.8687 for BKC) | Spatial heatmaps, cluster bounding |
| `pickup_zone` | String | Categorical | Derived | Indian Metro Hub (BKC, Andheri East, South Mumbai & Fort, Powai Tech Zone, Airport T2, Navi Mumbai) | Regional demand segmentation |
| `trip_distance_km` | Float | Kilometers (km) | Synthesized | Estimated road distance traversed (1.0 to 35.0 km) | Fare-distance correlation, duration modeling |
| `trip_duration_min` | Float | Minutes | Synthesized | Elapsed trip duration accounting for Indian urban traffic conditions | Velocity analysis, congestion proxy |
| `fare_amount` | Float | INR (₹) | Synthesized | Total trip fare in Indian Rupees (Base ₹50 + ₹14.5/km + ₹2/min) | Revenue analysis, econometric regression |
| `passenger_count` | Integer | Count | Synthesized | Number of passengers occupying the vehicle (1 to 6) | Vehicle utilization, carpooling potential |
| `base_dispatch_code` | String | Categorical | Regional Fleet | Fleet dispatch affiliation (e.g. UBER_BKC_EXPRESS, UBER_MUM_CENTRAL) | Fleet operator distribution |
| `pickup_hour` | Integer | 0 - 23 | Derived | Hour of the day extracted from `pickup_datetime` | Diurnal demand cycle analysis |
| `pickup_dayofweek` | Integer | 0 - 6 | Derived | Day of week (0 = Monday, 6 = Sunday) | Weekly rhythm, weekend vs weekday tests |
| `is_weekend` | Integer / Bool | 0 or 1 | Derived | Indicator whether trip occurred on Saturday/Sunday | Two-sample hypothesis testing |
| `is_peak_hour` | Integer / Bool | 0 or 1 | Derived | Indicator whether trip occurred during Indian rush hours (08-12, 17-22) | Surge pricing scenario trigger |
| `fare_per_km` | Float | INR / km | Derived | Unit fare efficiency metric (₹ / km) | Price sensitivity, anomaly detection |
| `simulated_surge_mult` | Float | Multiplier (x.xx) | Simulated | Dynamic pricing surge multiplier from scenario model | Scenario sensitivity and elasticity study |
| `simulated_fare` | Float | INR (₹) | Simulated | Hypothetical fare in Indian Rupees after applying dynamic multiplier | Revenue impact and consumer surplus analysis |

---

### Data Lineage & Integrity Rules
1. **Zero / Negative Fares:** Flagged as invalid records during ingestion.
2. **Coordinate Bounding:** Valid Indian Metropolitan envelope is Latitude [18.70, 19.50] and Longitude [72.60, 73.30]. Coordinates outside are flagged as geographic outliers.
3. **Trip Distance:** Valid range [0.5 km, 100 km]. Values outside are flagged.
4. **Duration:** Valid range [1 min, 300 min].
