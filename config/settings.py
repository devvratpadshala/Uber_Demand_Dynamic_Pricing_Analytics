"""
Global Configuration and Settings for Uber Demand and Dynamic Pricing Analytics.
Calibrated for Indian Urban Mobility & Metros (Mumbai MMR / Western Corridor).
"""
from pathlib import Path

# Base Paths (Relative to project root, ensuring portability)
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
SAMPLE_DATA_DIR = DATA_DIR / "sample"
MODELS_DIR = BASE_DIR / "models"
OUTPUTS_DIR = BASE_DIR / "outputs"
REPORTS_DIR = BASE_DIR / "reports"

# Default Demonstration Dataset Path
DEFAULT_DATASET_PATH = SAMPLE_DATA_DIR / "uber_demand_demonstration_dataset.csv"
RAW_DATASET_PATH = RAW_DATA_DIR / "uber-raw-data-apr14-sample.csv"

# Currency formatting (Indian Rupee format)
CURRENCY_SYMBOL = "₹"
CURRENCY_CODE = "INR"

# Geographic Bounding Box for Indian Metro validation (Mumbai MMR / Western Urban Region: Lat [18.70, 19.50], Lon [72.60, 73.30])
LAT_MIN, LAT_MAX = 18.70, 19.50
LON_MIN, LON_MAX = 72.60, 73.30

# Rush Hour Definitions for Indian Metros (24-hour clock)
# Indian office timings: Morning 08:30 - 11:30, Evening 17:00 - 21:00
MORNING_PEAK = (8, 12)   # 08:00 to 11:59
EVENING_PEAK = (17, 22)  # 17:00 to 21:59

# Pricing Model Defaults (Calibrated to Indian Urban Mobility)
DEFAULT_BASE_FARE = 50.0        # ₹50 base flag-down fare
DEFAULT_BASE_KM_RATE = 14.5     # ₹14.5 per kilometer
DEFAULT_MIN_MULTIPLIER = 1.0    # 1.0x minimum floor
DEFAULT_MAX_MULTIPLIER = 3.5    # 3.5x maximum surge cap
DEFAULT_SENSITIVITY = 0.75      # Sensitivity constant
DEFAULT_DRIVER_SUPPLY = 50      # Active driver pool
