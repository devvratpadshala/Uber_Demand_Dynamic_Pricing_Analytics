"""
Tests for Pricing Simulator Module.
"""
import pytest
from src.pricing_simulator import PricingSimulator


def test_calculate_surge_balanced():
    # Demand = Supply -> Multiplier 1.0
    res = PricingSimulator.calculate_surge(
        base_fare=100.0,
        demand=50,
        driver_supply=50,
        sensitivity=0.75
    )
    assert res["demand_supply_ratio"] == 1.0
    assert res["surge_multiplier"] == 1.0
    assert res["simulated_fare"] == 100.0
    assert res["market_condition"] == "Balanced Market (Normal Rates)"


def test_calculate_surge_high_demand():
    # Demand = 100, Supply = 50 -> DSR = 2.0.
    # Raw mult = 1.0 + 0.75*(2.0 - 1.0) = 1.75
    res = PricingSimulator.calculate_surge(
        base_fare=100.0,
        demand=100,
        driver_supply=50,
        sensitivity=0.75
    )
    assert res["demand_supply_ratio"] == 2.0
    assert res["surge_multiplier"] == 1.75
    assert res["simulated_fare"] == 175.0


def test_calculate_surge_capped():
    # Very high demand capping at max_multiplier = 3.0
    res = PricingSimulator.calculate_surge(
        base_fare=100.0,
        demand=500,
        driver_supply=50,
        sensitivity=1.0,
        max_multiplier=3.0
    )
    assert res["surge_multiplier"] == 3.0
    assert res["simulated_fare"] == 300.0
    assert res["is_capped"] is True


def test_calculate_surge_invalid_supply():
    with pytest.raises(ValueError):
        PricingSimulator.calculate_surge(base_fare=100.0, demand=50, driver_supply=0)


def test_calculate_surge_negative_fare():
    with pytest.raises(ValueError):
        PricingSimulator.calculate_surge(base_fare=-50.0, demand=50, driver_supply=50)
