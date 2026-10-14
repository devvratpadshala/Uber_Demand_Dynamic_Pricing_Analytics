"""
Dynamic Pricing Simulator Page.
Module 3: Interactive Hypothetical Surge Pricing Scenario Modeling & Sensitivity Analysis.
"""
import streamlit as st
import numpy as np
import pandas as pd
from src.pricing_simulator import PricingSimulator
from src.visualizations import Visualizer
from config.settings import (
    DEFAULT_BASE_FARE,
    DEFAULT_MIN_MULTIPLIER,
    DEFAULT_MAX_MULTIPLIER,
    DEFAULT_SENSITIVITY,
    DEFAULT_DRIVER_SUPPLY,
    CURRENCY_SYMBOL
)

st.set_page_config(page_title="Pricing Simulator | Uber Analytics", page_icon="⚡", layout="wide")

st.title("⚡ Dynamic Pricing Simulator")
st.markdown("Interactive scenario modeling of hypothetical market-clearing surge pricing mechanics.")

st.info(
    "⚠️ **Educational Simulation Model:** This module uses an explicit microeconomic surge function to illustrate "
    "how supply-demand imbalances can govern dynamic pricing. This is not Uber's proprietary algorithm."
)

# Sidebar Simulator Controls
st.sidebar.subheader("🎛️ Simulation Controls")
base_fare = st.sidebar.number_input("Base Fare (₹)", min_value=10.0, max_value=500.0, value=DEFAULT_BASE_FARE, step=5.0)
driver_supply = st.sidebar.slider("Active Driver Supply in Zone:", min_value=5, max_value=200, value=DEFAULT_DRIVER_SUPPLY, step=5)
observed_demand = st.sidebar.slider("Incoming Ride Demand (Requests):", min_value=5, max_value=300, value=75, step=5)

with st.sidebar.expander("⚙️ Advanced Parameters"):
    sensitivity = st.slider("Pricing Sensitivity (k):", min_value=0.1, max_value=2.0, value=DEFAULT_SENSITIVITY, step=0.05)
    min_mult = st.number_input("Floor Multiplier (Min):", min_value=1.0, max_value=1.5, value=DEFAULT_MIN_MULTIPLIER, step=0.1)
    max_mult = st.number_input("Ceiling Multiplier (Max Cap):", min_value=2.0, max_value=5.0, value=DEFAULT_MAX_MULTIPLIER, step=0.5)

# Calculate simulation output
sim_res = PricingSimulator.calculate_surge(
    base_fare=base_fare,
    demand=observed_demand,
    driver_supply=driver_supply,
    sensitivity=sensitivity,
    min_multiplier=min_mult,
    max_multiplier=max_mult
)

# KPI Cards
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.metric("Demand-to-Supply Ratio", f"{sim_res['demand_supply_ratio']:.2f}")
with c2:
    st.metric("Surge Multiplier", f"{sim_res['surge_multiplier']:.2f}x")
with c3:
    st.metric("Simulated Trip Fare", f"{CURRENCY_SYMBOL}{sim_res['simulated_fare']:.2f}", delta=f"+{sim_res['pct_increase']}%")
with c4:
    st.metric("Market State", sim_res["market_condition"])

st.markdown("---")

col_left, col_right = st.columns([1, 1.2])

with col_left:
    st.subheader("📐 Model Formulation & Assumptions")
    st.latex(r"\text{DSR} = \frac{\text{Demand}}{\text{Supply}}")
    st.latex(r"M_{\text{raw}} = 1.0 + k \cdot \max(0, \text{DSR} - 1.0)")
    st.latex(r"M = \operatorname{clamp}(M_{\text{raw}}, M_{\min}, M_{\max})")
    st.latex(r"\text{Final Fare} = \text{Base Fare} \times M")

    st.markdown("""
    **Key Theoretical Insights:**
    - When **Demand ≤ Supply** ($\text{DSR} \le 1.0$), multiplier remains at the baseline floor ($1.0\times$).
    - When **Demand > Supply**, each unit of excess demand incrementally drives the multiplier by sensitivity constant $k$.
    - The safety cap ($M_{\max}$) prevents astronomical price spikes during sudden urban mobility bottlenecks.
    """)

with col_right:
    st.subheader("📈 Dynamic Pricing Response Curve")
    demand_test_range = list(np.linspace(10, 300, 30))
    curve_data = PricingSimulator.simulate_curve(
        base_fare=base_fare,
        driver_supply=driver_supply,
        demand_range=demand_test_range,
        sensitivity=sensitivity,
        min_multiplier=min_mult,
        max_multiplier=max_mult
    )
    fig_curve = Visualizer.plot_pricing_simulation_curves(
        curve_data["demand_ratios"],
        curve_data["multipliers"],
        curve_data["fares"]
    )
    st.plotly_chart(fig_curve, use_container_width=True)

# Preset Scenarios
st.markdown("---")
st.subheader("🎭 Preset Operational Scenarios")
scenarios = [
    {"Scenario": "Early Morning Off-Peak", "Demand": 20, "Supply": 60, "Description": "Abundant idle vehicles, standard baseline fare"},
    {"Scenario": "Regular Afternoon Traffic", "Demand": 50, "Supply": 50, "Description": "Perfect market equilibrium (DSR = 1.0)"},
    {"Scenario": "Evening Rush Hour (5-7 PM)", "Demand": 110, "Supply": 55, "Description": "High demand, 2.0x DSR, moderate surge"},
    {"Scenario": "Severe Rainstorm / Mega Event", "Demand": 220, "Supply": 40, "Description": "Acute bottleneck, triggers ceiling multiplier cap"}
]

scenario_results = []
for s in scenarios:
    r = PricingSimulator.calculate_surge(
        base_fare=base_fare,
        demand=s["Demand"],
        driver_supply=s["Supply"],
        sensitivity=sensitivity,
        min_multiplier=min_mult,
        max_multiplier=max_mult
    )
    scenario_results.append({
        "Scenario": s["Scenario"],
        "Demand": s["Demand"],
        "Supply": s["Supply"],
        "DSR": r["demand_supply_ratio"],
        "Multiplier": f"{r['surge_multiplier']:.2f}x",
        "Final Fare (₹)": f"{CURRENCY_SYMBOL}{r['simulated_fare']:.2f}",
        "Market Condition": r["market_condition"],
        "Description": s["Description"]
    })

st.dataframe(pd.DataFrame(scenario_results), use_container_width=True)
