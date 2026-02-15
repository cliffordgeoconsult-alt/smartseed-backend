# app/services/gee/ndvi.py
import ee
import calendar

S2_COLLECTION = "COPERNICUS/S2_SR_HARMONIZED"


def _add_ndvi(image: ee.Image) -> ee.Image:
    ndvi = image.normalizedDifference(["B8", "B4"]).rename("NDVI")
    return image.addBands(ndvi)


def _collection(geometry, start_date, end_date):
    return (
        ee.ImageCollection(S2_COLLECTION)
        .filterBounds(geometry)
        .filterDate(start_date, end_date)
        .filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE", 20))
        .map(_add_ndvi)
        .select("NDVI")
    )


# NDVI SUMMARY
def get_ndvi_summary(geometry, start_date, end_date):

    collection = _collection(geometry, start_date, end_date)

    if collection.size().getInfo() == 0:
        return None

    image = collection.mean()

    stats = image.reduceRegion(
        reducer=ee.Reducer.mean()
            .combine(ee.Reducer.min(), "", True)
            .combine(ee.Reducer.max(), "", True),
        geometry=geometry,
        scale=10,
        bestEffort=True,
        maxPixels=1e13
    ).getInfo()

    return stats

# NDVI MONTHLY TIME SERIES
def get_ndvi_timeseries(geometry, start_year, end_year):

    results = []

    for year in range(start_year, end_year + 1):
        for month in range(1, 13):

            start = f"{year}-{month:02d}-01"
            last_day = calendar.monthrange(year, month)[1]
            end = f"{year}-{month:02d}-{last_day}"

            collection = _collection(geometry, start, end)

            if collection.size().getInfo() == 0:
                continue

            mean_val = collection.mean().reduceRegion(
                reducer=ee.Reducer.mean(),
                geometry=geometry,
                scale=10,
                bestEffort=True,
                maxPixels=1e13
            ).get("NDVI")

            results.append({
                "year": year,
                "month": month,
                "mean_ndvi": ee.Number(mean_val).getInfo()
            })

    return results