import ee
from datetime import datetime

ERA5_DAILY = "ECMWF/ERA5_LAND/DAILY_AGGR"

def get_temperature_summary(
    geometry: ee.Geometry,
    start_date: str,
    end_date: str
) -> dict:
    """
    Returns mean and max 2m air temperature (°C) over a geometry and period
    """

    collection = (
        ee.ImageCollection(ERA5_DAILY)
        .filterDate(start_date, end_date)
        .select([
            "temperature_2m",
            "temperature_2m_max"
        ])
    )

    # Mean over time
    temp_mean_img = collection.select("temperature_2m").mean()
    temp_max_img = collection.select("temperature_2m_max").max()

    # Reduce over geometry
    mean_stats = temp_mean_img.reduceRegion(
        reducer=ee.Reducer.mean(),
        geometry=geometry,
        scale=1000,
        bestEffort=True
    )

    max_stats = temp_max_img.reduceRegion(
        reducer=ee.Reducer.max(),
        geometry=geometry,
        scale=1000,
        bestEffort=True
    )

    # Convert Kelvin → Celsius
    mean_c = ee.Number(mean_stats.get("temperature_2m")).subtract(273.15)
    max_c = ee.Number(max_stats.get("temperature_2m_max")).subtract(273.15)

    return {
        "mean_c": mean_c.getInfo(),
        "max_c": max_c.getInfo(),
        "start_date": start_date,
        "end_date": end_date
    }
