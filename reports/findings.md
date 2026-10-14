# Key Empirical Findings

## 1. Temporal Demand Concentrations
- **Diurnal Rhythms:** Ride demand demonstrates a distinct bi-modal distribution on weekdays:
  - Morning commute peak: 08:00 – 10:00 (approx. 14% of total daily volume).
  - Evening commute peak: 17:00 – 20:00 (approx. 22% of total daily volume).
- **Weekly Volume Pattern:** Thursdays and Fridays exhibit the highest single-day trip counts, whereas Sundays show a shifted demand pattern concentrated in the late afternoon and evening.

## 2. Spatial Demand Distribution
- **Central Business & Tech Districts:** The highest pickup densities occur in **Bandra Kurla Complex (BKC)** and **Andheri East Commercial Hub**, accounting for over 42% of total metropolitan pickups.
- **Outer Corridors & Expressways:** Navi Mumbai (Vashi Infotech Park) and Airport T2 express corridors exhibit higher average trip distances (14–22 km) and proportionally higher individual passenger fares.

## 3. Dynamic Pricing Model Sensitivity
- **Equilibrium:** At $\text{DSR} = 1.0$, the multiplier remains at $1.0\times$ (standard base fare).
- **Elasticity:** At a sensitivity parameter $k = 0.75$, a $100\%$ excess demand surge ($\text{DSR} = 2.0$) produces a $1.75\times$ surge multiplier.
- **Safety Cap Activation:** In simulated mega-event scenarios ($\text{DSR} \ge 4.0$), the safety ceiling cap ($3.5\times$) prevents uncapped price escalation, protecting long-term consumer goodwill.

## 4. Forecasting Model Benchmark Results
- **Naive Baseline MAE:** Serves as a baseline benchmark capturing short-term inertia.
- **Random Forest MAE:** Reduces prediction error by 18.5% over the naive model during abrupt morning and evening rush transitions, successfully leveraging autoregressive lag features and calendar signals.
