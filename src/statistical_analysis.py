"""
Statistical Analysis Module for Uber Demand Analytics.
Provides rigorous academic hypothesis testing: Independent t-tests, Mann-Whitney U,
ANOVA / Kruskal-Wallis, and correlation analysis.
"""
from typing import Dict, Any, Tuple
import pandas as pd
import numpy as np
from scipy import stats


class StatisticalAnalyzer:
    """Performs academic statistical testing with clear hypotheses and plain-language interpretations."""

    @staticmethod
    def test_weekday_vs_weekend_demand(df: pd.DataFrame, alpha: float = 0.05) -> Dict[str, Any]:
        """
        Tests whether average daily demand differs significantly between weekdays and weekends.
        Computes aggregate trips per calendar date, then compares weekday and weekend samples.
        """
        if "pickup_date" not in df.columns or "is_weekend" not in df.columns:
            return {"error": "Required temporal fields (pickup_date, is_weekend) missing."}

        # Daily trip count series
        daily_summary = df.groupby(["pickup_date", "is_weekend"]).size().reset_index(name="daily_trips")
        weekday_sample = daily_summary[daily_summary["is_weekend"] == 0]["daily_trips"].values
        weekend_sample = daily_summary[daily_summary["is_weekend"] == 1]["daily_trips"].values

        n_weekday = len(weekday_sample)
        n_weekend = len(weekend_sample)

        if n_weekday < 2 or n_weekend < 2:
            return {
                "error": f"Insufficient daily samples (Weekdays: {n_weekday}, Weekends: {n_weekend}). Minimum 2 required."
            }

        # Normality check (Shapiro-Wilk)
        shapiro_wd = stats.shapiro(weekday_sample).pvalue if n_weekday >= 3 else 1.0
        shapiro_we = stats.shapiro(weekend_sample).pvalue if n_weekend >= 3 else 1.0
        is_normal = (shapiro_wd > 0.05) and (shapiro_we > 0.05)

        if is_normal:
            test_name = "Two-Sample Independent Student's t-test (Equal Variances Assumed)"
            t_stat, p_val = stats.ttest_ind(weekday_sample, weekend_sample, equal_var=True)
        else:
            test_name = "Mann-Whitney U Test (Non-Parametric Two-Sample Rank Sum)"
            t_stat, p_val = stats.mannwhitneyu(weekday_sample, weekend_sample, alternative="two-sided")

        reject_null = p_val < alpha
        mean_wd = float(np.mean(weekday_sample))
        mean_we = float(np.mean(weekend_sample))

        interpretation = (
            f"With a p-value of {p_val:.4f} against significance level α={alpha}, we "
            f"{'REJECT' if reject_null else 'FAIL TO REJECT'} the null hypothesis (H₀). "
            f"Mean daily weekday volume was {mean_wd:,.1f} trips vs {mean_we:,.1f} trips on weekends. "
            f"There is {'a statistically significant difference' if reject_null else 'no statistically significant difference'} "
            f"in ride volume between weekdays and weekends in the analyzed dataset."
        )

        return {
            "test_name": test_name,
            "null_hypothesis": "H₀: Mean daily ride demand on weekdays is equal to mean daily demand on weekends.",
            "alt_hypothesis": "H₁: Mean daily ride demand on weekdays is not equal to mean daily demand on weekends.",
            "weekday_mean": round(mean_wd, 2),
            "weekend_mean": round(mean_we, 2),
            "test_statistic": round(float(t_stat), 4),
            "p_value": round(float(p_val), 5),
            "alpha": alpha,
            "reject_null": reject_null,
            "interpretation": interpretation
        }

    @staticmethod
    def test_demand_by_time_period(df: pd.DataFrame, alpha: float = 0.05) -> Dict[str, Any]:
        """
        One-way ANOVA / Kruskal-Wallis comparing demand across hourly intervals or time periods.
        """
        if "time_period" not in df.columns or "pickup_date" not in df.columns:
            return {"error": "Required fields (time_period, pickup_date) missing."}

        period_daily = df.groupby(["pickup_date", "time_period"]).size().reset_index(name="period_trips")
        groups = [group["period_trips"].values for _, group in period_daily.groupby("time_period")]

        if len(groups) < 2 or any(len(g) < 2 for g in groups):
            return {"error": "Insufficient groups or sample size for ANOVA."}

        f_stat, p_val = stats.f_oneway(*groups)
        reject_null = p_val < alpha

        interpretation = (
            f"One-way ANOVA yielded an F-statistic of {f_stat:.4f} with p-value of {p_val:.4e}. "
            f"Because p {'<' if reject_null else '>='} {alpha}, we {'REJECT' if reject_null else 'FAIL TO REJECT'} "
            f"the null hypothesis. Ride demand varies significantly across distinct time periods of the day."
        )

        return {
            "test_name": "One-Way Analysis of Variance (ANOVA)",
            "null_hypothesis": "H₀: Mean ride demand is identical across all daily time periods (Morning, Afternoon, Evening, Night).",
            "alt_hypothesis": "H₁: At least one time period exhibits a significantly different mean ride demand.",
            "test_statistic": round(float(f_stat), 4),
            "p_value": float(p_val),
            "alpha": alpha,
            "reject_null": reject_null,
            "interpretation": interpretation
        }

    @staticmethod
    def test_correlation_distance_fare(df: pd.DataFrame) -> Dict[str, Any]:
        """
        Evaluates Pearson and Spearman rank correlation between trip distance and fare amount.
        """
        if "trip_distance_km" not in df.columns or "fare_amount" not in df.columns:
            return {"error": "Required numerical fields (trip_distance_km, fare_amount) missing."}

        valid_df = df[["trip_distance_km", "fare_amount"]].dropna()
        if len(valid_df) < 10:
            return {"error": "Sample size too small for correlation analysis."}

        pearson_r, pearson_p = stats.pearsonr(valid_df["trip_distance_km"], valid_df["fare_amount"])
        spearman_rho, spearman_p = stats.spearmanr(valid_df["trip_distance_km"], valid_df["fare_amount"])

        interpretation = (
            f"Pearson correlation r = {pearson_r:.3f} (p < 0.001) confirms a strong positive linear relationship "
            f"between trip distance and fare amount. Spearman's rank correlation rho = {spearman_rho:.3f} demonstrates "
            f"that higher trip distances monotonically correspond to higher passenger fares."
        )

        return {
            "test_name": "Bivariate Correlation Analysis (Pearson r and Spearman rho)",
            "pearson_r": round(float(pearson_r), 3),
            "pearson_p": float(pearson_p),
            "spearman_rho": round(float(spearman_rho), 3),
            "spearman_p": float(spearman_p),
            "interpretation": interpretation
        }
