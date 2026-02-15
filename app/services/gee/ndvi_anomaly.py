import ee
from app.services.gee.ndvi import get_ndvi_summary
from app.services.gee.ndvi_climatology import get_ndvi_climatology


def get_ndvi_anomaly(geometry, start_date, end_date):

    current = get_ndvi_summary(geometry, start_date, end_date)

    if current is None:
        return None

    climatology = get_ndvi_climatology(geometry)

    historical_values = [
        item["mean_ndvi"]
        for item in climatology["monthly_climatology"]
    ]

    historical_mean = sum(historical_values) / len(historical_values)

    current_mean = current["NDVI_mean"]

    anomaly = current_mean - historical_mean

    return {
        "current_mean_ndvi": current_mean,
        "historical_mean_ndvi": historical_mean,
        "anomaly": anomaly,
        "baseline_period": climatology["baseline_period"]
    }