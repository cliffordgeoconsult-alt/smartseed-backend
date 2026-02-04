import ee
from datetime import datetime


def compute_rainfall(
    geometry: ee.Geometry,
    start_date: str,
    end_date: str
) -> dict:
    """
    Compute rainfall statistics using CHIRPS DAILY.
    Returns total and mean rainfall (mm).
    """

    # Validate dates early
    datetime.fromisoformat(start_date)
    datetime.fromisoformat(end_date)

    collection = (
        ee.ImageCollection("UCSB-CHG/CHIRPS/DAILY")
        .filterDate(start_date, end_date)
        .filterBounds(geometry)
    )

    image_count = collection.size()

    # Sum rainfall over time
    total_rainfall = collection.sum()

    stats = total_rainfall.reduceRegion(
        reducer=ee.Reducer.mean(),
        geometry=geometry,
        scale=5566,   # CHIRPS native resolution
        maxPixels=1e13
    )

    total_mm = ee.Number(stats.get("precipitation"))

    result = ee.Dictionary({
        "total_mm": total_mm,
        "days": image_count,
        "mean_mm_per_day": total_mm.divide(image_count)
    })

    return result.getInfo()
