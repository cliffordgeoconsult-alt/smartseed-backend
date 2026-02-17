# app/services/gee/seasonal_performance.py
from app.services.gee.rainfall_anomaly import get_seasonal_anomaly as get_rain_anomaly
from app.services.gee.temperature_anomaly import get_temperature_seasonal_anomaly as get_temp_anomaly
from app.services.gee.ndvi_anomaly import get_seasonal_anomaly as get_ndvi_anomaly

# Map NDVI seasons to rainfall seasons
RAIN_SEASON_MAP = {
    "MAM": "long_rains",
    "JJA": "short_rains",
    "SON": "short_rains",
    "DJF": "long_rains"
}


def compute_seasonal_performance(geometry, year: int, season: str):
    """
    Compute a Seasonal Performance Index (SPI) based on rainfall, temperature, and NDVI anomalies.
    - rainfall: percent anomaly
    - temperature: anomaly in °C
    - NDVI: percent anomaly
    """

    # Determine rainfall season for anomaly lookup
    rain_season = RAIN_SEASON_MAP.get(season, season)

    # Fetch anomalies
    rain = get_rain_anomaly(geometry, year, rain_season)
    temp = get_temp_anomaly(geometry, season, year)
    ndvi = get_ndvi_anomaly(geometry, year, season)

    rain_anom = rain.get("anomaly_percent", 0)
    temp_anom = temp.get("mean_temp_anomaly_c", 0)
    ndvi_anom = ndvi.get("anomaly_percent", 0)

    # Convert temperature anomaly to weighting factor (internal only)
    temp_factor = 1 - abs(temp_anom * 5 / 100) * 0.2
    rain_factor = 1 + (rain_anom / 100) * 0.3
    ndvi_factor = 1 + (ndvi_anom / 100) * 0.2

    spi = rain_factor * temp_factor * ndvi_factor
    spi = max(0.6, min(1.3, spi))

    return {
        "spi": round(spi, 3),
        "rain_anomaly_percent": rain_anom,
        "temperature_anomaly_c": temp_anom,
        "ndvi_anomaly_percent": ndvi_anom
    }