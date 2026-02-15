# app/services/gee/temperature_monthly.py
import ee
from datetime import datetime
from calendar import monthrange

def get_monthly_temperature(
    geometry: ee.Geometry,
    year: int
):
    """
    Returns monthly mean, min, max temperature (°C)
    using ERA5-Land.
    """

    collection = (
        ee.ImageCollection("ECMWF/ERA5_LAND/DAILY_AGGR")
        .filterBounds(geometry)
        .filterDate(f"{year}-01-01", f"{year}-12-31")
        .select("temperature_2m")
    )

    results = []

    for month in range(1, 13):
        start = ee.Date.fromYMD(year, month, 1)
        end = start.advance(1, "month")

        monthly = collection.filterDate(start, end)

        mean_img = monthly.mean()
        min_img = monthly.min()
        max_img = monthly.max()

        stats = ee.Dictionary({
            "mean_c": mean_img.reduceRegion(
                reducer=ee.Reducer.mean(),
                geometry=geometry,
                scale=1000,
                bestEffort=True
            ).get("temperature_2m"),

            "min_c": min_img.reduceRegion(
                reducer=ee.Reducer.mean(),
                geometry=geometry,
                scale=1000,
                bestEffort=True
            ).get("temperature_2m"),

            "max_c": max_img.reduceRegion(
                reducer=ee.Reducer.mean(),
                geometry=geometry,
                scale=1000,
                bestEffort=True
            ).get("temperature_2m"),
        })

        results.append(
            ee.Feature(
                None,
                stats.set("month", month)
            )
        )

    fc = ee.FeatureCollection(results)

    data = fc.getInfo()["features"]

    # Convert Kelvin → Celsius
    output = []
    for f in data:
        p = f["properties"]
        output.append({
            "month": p["month"],
            "mean_c": p["mean_c"] - 273.15 if p["mean_c"] else None,
            "min_c": p["min_c"] - 273.15 if p["min_c"] else None,
            "max_c": p["max_c"] - 273.15 if p["max_c"] else None,
        })

    return output
