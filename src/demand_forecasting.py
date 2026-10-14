"""
Demand Forecasting Module for Uber Demand Analytics.
Implements Naive, Rolling Average baselines, and Random Forest regression.
Uses strict chronological train/test splitting to prevent future data leakage.
"""
from typing import Dict, Any, Tuple
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, root_mean_squared_error


class DemandForecaster:
    """Predictive forecasting module for temporal ride volume."""

    @staticmethod
    def prepare_time_series(df: pd.DataFrame, freq: str = "h") -> pd.DataFrame:
        """
        Aggregates trip records into regular chronological time buckets (default 1-hour intervals).
        Fills missing time periods with 0 to ensure continuous time index.
        """
        if "pickup_datetime" not in df.columns:
            raise ValueError("pickup_datetime column required for time-series forecasting.")

        ts_df = df.set_index("pickup_datetime").sort_index()
        # Hourly count
        demand_ts = ts_df.resample(freq).size().rename("demand").to_frame()

        # Extract temporal features
        demand_ts["hour"] = demand_ts.index.hour
        demand_ts["dayofweek"] = demand_ts.index.dayofweek
        demand_ts["is_weekend"] = demand_ts["dayofweek"].isin([5, 6]).astype(int)

        # Lagged features (previous hour, previous day)
        demand_ts["lag_1h"] = demand_ts["demand"].shift(1)
        demand_ts["lag_2h"] = demand_ts["demand"].shift(2)
        demand_ts["lag_24h"] = demand_ts["demand"].shift(24)

        # Rolling 6h mean (shifted by 1 to prevent target leakage)
        demand_ts["rolling_6h_mean"] = demand_ts["demand"].shift(1).rolling(window=6, min_periods=1).mean()

        # Drop NA created by lags
        demand_ts.dropna(inplace=True)
        return demand_ts

    @classmethod
    def train_and_evaluate(
        cls,
        demand_ts: pd.DataFrame,
        test_size_ratio: float = 0.20
    ) -> Dict[str, Any]:
        """
        Strict chronological train-test split and multi-model benchmark evaluation.
        """
        n = len(demand_ts)
        if n < 48:
            return {"error": f"Insufficient time series length ({n} points). Minimum 48 hours required."}

        split_idx = int(n * (1.0 - test_size_ratio))
        train = demand_ts.iloc[:split_idx]
        test = demand_ts.iloc[split_idx:]

        feature_cols = ["hour", "dayofweek", "is_weekend", "lag_1h", "lag_2h", "lag_24h", "rolling_6h_mean"]
        X_train, y_train = train[feature_cols], train["demand"]
        X_test, y_test = test[feature_cols], test["demand"]

        # 1. Baseline: Naive Persistence (Predicted value = demand at previous hour lag_1h)
        y_pred_naive = test["lag_1h"].values

        # 2. Baseline: Moving Average (Rolling 6-hour mean)
        y_pred_ma = test["rolling_6h_mean"].values

        # 3. Supervised ML: Random Forest Regressor
        rf = RandomForestRegressor(n_estimators=100, max_depth=8, random_state=42, n_jobs=-1)
        rf.fit(X_train, y_train)
        y_pred_rf = rf.predict(X_test)

        # Evaluation metrics
        def calc_metrics(actual, pred):
            mae = mean_absolute_error(actual, pred)
            rmse = root_mean_squared_error(actual, pred)
            # Safe MAPE (avoid division by zero)
            mask = actual > 0
            mape = np.mean(np.abs((actual[mask] - pred[mask]) / actual[mask])) * 100 if np.sum(mask) > 0 else np.nan
            return {"MAE": round(mae, 2), "RMSE": round(rmse, 2), "MAPE_pct": round(mape, 2) if not np.isnan(mape) else None}

        metrics = {
            "Naive_Persistence": calc_metrics(y_test, y_pred_naive),
            "Moving_Average_6h": calc_metrics(y_test, y_pred_ma),
            "Random_Forest": calc_metrics(y_test, y_pred_rf)
        }

        # Build comparison dataframe for charting
        results_df = pd.DataFrame({
            "timestamp": test.index,
            "actual_demand": y_test.values,
            "naive_prediction": y_pred_naive,
            "moving_avg_prediction": y_pred_ma,
            "random_forest_prediction": y_pred_rf.round(1)
        })

        feature_importances = dict(zip(feature_cols, [round(float(imp), 4) for imp in rf.feature_importances_]))

        return {
            "train_size": len(train),
            "test_size": len(test),
            "split_timestamp": str(test.index[0]),
            "metrics": metrics,
            "results_df": results_df,
            "feature_importances": feature_importances,
            "trained_model": rf
        }
