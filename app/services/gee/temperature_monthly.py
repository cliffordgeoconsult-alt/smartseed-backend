# app/services/gee/temperature_monthly.py
import ee
ERA5_DAILY = "ECMWF/ERA5_LAND/DAILY_AGGR"
def get_monthly_temperature(
    geometry: ee.Geometry,
    year: int
):

    collection = (
        ee.ImageCollection(ERA5_DAILY)
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

        mean_stats = mean_img.reduceRegion(
            reducer=ee.Reducer.mean(),
            geometry=geometry,
            scale=1000,
            bestEffort=True,
            maxPixels=1e9
        )

        min_stats = min_img.reduceRegion(
            reducer=ee.Reducer.mean(),
            geometry=geometry,
            scale=1000,
            bestEffort=True,
            maxPixels=1e9
        )

        max_stats = max_img.reduceRegion(
            reducer=ee.Reducer.mean(),
            geometry=geometry,
            scale=1000,
            bestEffort=True,
            maxPixels=1e9
        )

        mean_k = mean_stats.get("temperature_2m")
        min_k = min_stats.get("temperature_2m")
        max_k = max_stats.get("temperature_2m")

        # Safety check
        if mean_k is None:
            results.append({
                "month": month,
                "mean_c": None,
                "min_c": None,
                "max_c": None,
            })
            continue

        results.append({
            "month": month,
            "mean_c": ee.Number(mean_k).subtract(273.15).getInfo(),
            "min_c": ee.Number(min_k).subtract(273.15).getInfo(),
            "max_c": ee.Number(max_k).subtract(273.15).getInfo(),
        })

    return results