# app/services/gee/seasonal_performance.py
from app.services.gee.rainfall_anomaly import get_seasonal_anomaly
from app.services.gee.temperature_anomaly import get_seasonal_anomaly as get_temp_anomaly
from app.services.gee.ndvi_anomaly import get_seasonal_anomaly as get_ndvi_anomaly


def compute_seasonal_performance(
    geometry,
    year: int,
    season: str
):

    rain = get_seasonal_anomaly(geometry, year, season)
    temp = get_temp_anomaly(geometry, year, season)
    ndvi = get_ndvi_anomaly(geometry, year, season)

    rain_anom = rain.get("anomaly_percent", 0)
    temp_anom = temp.get("anomaly_percent", 0)
    ndvi_anom = ndvi.get("anomaly_percent", 0)

    # Convert anomaly % to impact factors

    rain_factor = 1 + (rain_anom / 100) * 0.3
    temp_factor = 1 - abs(temp_anom / 100) * 0.2
    ndvi_factor = 1 + (ndvi_anom / 100) * 0.2

    spi = rain_factor * temp_factor * ndvi_factor

    # Prevent unrealistic jumps
    spi = max(0.6, min(1.3, spi))

    return {
        "spi": spi,
        "rain_anomaly_percent": rain_anom,
        "temperature_anomaly_percent": temp_anom,
        "ndvi_anomaly_percent": ndvi_anom
    }