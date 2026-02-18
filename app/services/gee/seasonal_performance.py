# app/services/gee/seasonal_performance.py
from app.services.gee.rainfall_anomaly import get_seasonal_anomaly as get_rain_anomaly
from app.services.gee.temperature_anomaly import get_temperature_seasonal_anomaly as get_temp_anomaly
from app.services.gee.ndvi_anomaly import get_seasonal_anomaly as get_ndvi_anomaly

RAIN_SEASON_MAP = {
    "MAM": "long_rains",
    "SON": "short_rains",
    "JJA": "short_rains",
    "DJF": "long_rains"
}


def compute_seasonal_performance(geometry, year: int, season: str):

    rain_season = RAIN_SEASON_MAP.get(season, season)

    rain = get_rain_anomaly(geometry, year, rain_season)
    temp = get_temp_anomaly(geometry, season, year)
    ndvi = get_ndvi_anomaly(geometry, year, season)

    rain_anom = rain.get("anomaly_percent", 0)
    temp_anom = temp.get("mean_temp_anomaly_c", 0)
    ndvi_anom = ndvi.get("anomaly_percent", 0)

    # Convert anomalies to fuzzy suitability (0–1)

    rain_score = max(0.25, 1 - abs(rain_anom) / 100)
    temp_score = max(0.25, 1 - abs(temp_anom) / 5)
    ndvi_score = max(0.25, 1 + (ndvi_anom / 100))

    climate_score = rain_score * temp_score * ndvi_score

    return {
        "climate_score": round(climate_score, 3),
        "rain_anomaly_percent": rain_anom,
        "temperature_anomaly_c": temp_anom,
        "ndvi_anomaly_percent": ndvi_anom
    }