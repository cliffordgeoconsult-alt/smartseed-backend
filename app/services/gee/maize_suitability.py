# app/services/gee/maize_suitability.py
import ee
from app.services.gee.baseline_agro_score import compute_baseline_score
from app.services.gee.seasonal_performance import compute_seasonal_performance


def classify(score: float):
    if score > 0.75:
        return "Very Highly Suitable"
    elif score > 0.5:
        return "Moderately Suitable"
    elif score > 0.25:
        return "Marginally Suitable"
    else:
        return "Unsuitable"


def compute_maize_suitability(
    geometry: ee.Geometry,
    year: int,
    season: str,
    depth: str = "0-20cm"
):

    soil_score = compute_baseline_score(geometry, depth)
    seasonal = compute_seasonal_performance(geometry, year, season)

    final_score = soil_score * seasonal["climate_score"]
    final_score = max(0, min(1, final_score))

    return {
        "soil_score": round(soil_score, 3),
        "climate_score": seasonal["climate_score"],
        "suitability_score": round(final_score, 3),
        "suitability_class": classify(final_score),
        "rainfall_anomaly_percent": seasonal["rain_anomaly_percent"],
        "temperature_anomaly_c": seasonal["temperature_anomaly_c"],
        "ndvi_anomaly_percent": seasonal["ndvi_anomaly_percent"],
        "year": year,
        "season": season
    }

