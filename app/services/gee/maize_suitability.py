# app/services/gee/maize_suitability.py
import ee
from app.services.gee.baseline_agro_score import compute_baseline_score
from app.services.gee.seasonal_performance import compute_seasonal_performance


def compute_maize_suitability(geometry: ee.Geometry, year: int, season: str, depth: str = "0-20cm"):
    """
    Compute maize suitability score combining baseline soil score and seasonal performance.
    """

    baseline_score = compute_baseline_score(geometry, depth)
    seasonal = compute_seasonal_performance(geometry, year, season)

    final_score = baseline_score * seasonal["spi"]

    return {
        "baseline_score": round(baseline_score, 2),
        "seasonal_index": round(seasonal["spi"], 3),
        "final_suitability_score": round(final_score, 2),
        "rainfall_anomaly_percent": seasonal["rain_anomaly_percent"],
        "temperature_anomaly_c": seasonal["temperature_anomaly_c"],
        "ndvi_anomaly_percent": seasonal["ndvi_anomaly_percent"],
        "year": year,
        "season": season
    }