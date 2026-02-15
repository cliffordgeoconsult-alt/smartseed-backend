# services/gee/rainfall.py
import ee
from datetime import datetime


CHIRPS_ID = "UCSB-CHG/CHIRPS/DAILY"

# Custom Date Range Rainfall
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
        ee.ImageCollection(CHIRPS_ID)
        .filterDate(start_date, end_date)
        .filterBounds(geometry)
    )
    image_count = collection.size()

    total_rainfall = collection.sum()

    stats = total_rainfall.reduceRegion(
        reducer=ee.Reducer.mean(),
        geometry=geometry,
        scale=5566,
        maxPixels=1e13
    )

    total_mm = ee.Number(stats.get("precipitation"))

    result = ee.Dictionary({
        "total_mm": total_mm,
        "days": image_count,
        "mean_mm_per_day": total_mm.divide(image_count)
    })

    return result.getInfo()

# Annual Rainfall (Single Year)
def get_annual_rainfall(
    geometry: ee.Geometry,
    year: int
):

    if year < 1981:
        raise ValueError("CHIRPS data starts from 1981.")

    collection = (
        ee.ImageCollection(CHIRPS_ID)
        .filterBounds(geometry)
        .filterDate(f"{year}-01-01", f"{year}-12-31")
    )

    total_img = collection.sum()

    stats = total_img.reduceRegion(
        reducer=ee.Reducer.mean(),
        geometry=geometry,
        scale=5566,
        maxPixels=1e13
    )

    total_mm = ee.Number(stats.get("precipitation")).getInfo()

    return {
        "year": year,
        "total_mm": total_mm
    }