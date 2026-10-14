"""
Hypothetical Dynamic Pricing Scenario Simulator.
Simulates market clearing surge pricing scenarios based on user-adjustable demand and supply.
Strictly labelled as an educational simulation, not Uber's proprietary algorithm.
"""
from typing import Dict, Any, List
import numpy as np


class PricingSimulator:
    """
    Hypothetical dynamic surge pricing simulator with mathematically explicit formulation.
    Formula:
        Demand-to-Supply Ratio (DSR) = Demand / Driver Supply
        Raw Multiplier = 1.0 + Sensitivity * max(0.0, DSR - 1.0)
        Surge Multiplier = clamp(Raw Multiplier, min_multiplier, max_multiplier)
        Simulated Fare = Base Fare * Surge Multiplier
    """

    @staticmethod
    def calculate_surge(
        base_fare: float,
        demand: int | float,
        driver_supply: int | float,
        sensitivity: float = 0.75,
        min_multiplier: float = 1.0,
        max_multiplier: float = 3.5
    ) -> Dict[str, Any]:
        """
        Calculates simulated surge multiplier and final trip fare.
        Validates domain inputs to prevent impossible mathematical states.
        """
        # Defensive validation
        if driver_supply <= 0:
            raise ValueError("Driver supply must be strictly positive (> 0).")
        if base_fare < 0:
            raise ValueError("Base fare cannot be negative.")
        if demand < 0:
            raise ValueError("Demand cannot be negative.")
        if min_multiplier > max_multiplier:
            raise ValueError("Minimum multiplier cannot exceed maximum multiplier.")
        if sensitivity < 0:
            raise ValueError("Sensitivity must be non-negative.")

        # Imbalance ratio
        dsr = float(demand) / float(driver_supply)

        # Multiplier formula
        excess_demand = max(0.0, dsr - 1.0)
        raw_mult = 1.0 + (sensitivity * excess_demand)
        surge_multiplier = float(np.clip(raw_mult, min_multiplier, max_multiplier))

        # Final simulated fare
        simulated_fare = round(base_fare * surge_multiplier, 2)
        fare_increase = round(simulated_fare - base_fare, 2)
        pct_increase = round(((surge_multiplier - 1.0) * 100.0), 1)

        # Market condition status label
        if dsr < 0.8:
            market_condition = "Driver Oversupply (Low Demand)"
        elif dsr <= 1.2:
            market_condition = "Balanced Market (Normal Rates)"
        elif dsr <= 2.0:
            market_condition = "Moderate Demand Surge"
        elif dsr <= 3.0:
            market_condition = "High Demand Surge"
        else:
            market_condition = "Severe Supply Shortage (Max Surge Capped)"

        return {
            "base_fare": round(base_fare, 2),
            "demand": float(demand),
            "driver_supply": float(driver_supply),
            "demand_supply_ratio": round(dsr, 2),
            "surge_multiplier": round(surge_multiplier, 2),
            "simulated_fare": simulated_fare,
            "fare_increase": fare_increase,
            "pct_increase": pct_increase,
            "market_condition": market_condition,
            "is_capped": surge_multiplier >= max_multiplier
        }

    @classmethod
    def simulate_curve(
        cls,
        base_fare: float,
        driver_supply: float,
        demand_range: List[float],
        sensitivity: float = 0.75,
        min_multiplier: float = 1.0,
        max_multiplier: float = 3.5
    ) -> Dict[str, List[float]]:
        """Simulates an entire response curve across a range of demand points."""
        ratios = []
        multipliers = []
        fares = []

        for d in demand_range:
            res = cls.calculate_surge(
                base_fare=base_fare,
                demand=d,
                driver_supply=driver_supply,
                sensitivity=sensitivity,
                min_multiplier=min_multiplier,
                max_multiplier=max_multiplier
            )
            ratios.append(res["demand_supply_ratio"])
            multipliers.append(res["surge_multiplier"])
            fares.append(res["simulated_fare"])

        return {
            "demand_ratios": ratios,
            "multipliers": multipliers,
            "fares": fares
        }
