# app/services/gee/ndvi_anomaly.py
import ee

S2_COLLECTION = "COPERNICUS/S2_SR"

SEASONS = {
    "MAM": [3, 4, 5],
    "JJA": [6, 7, 8],
    "SON": [9, 10, 11],
    "DJF": [12, 1, 2]
}


def _season_collection(year: int, season: str) -> ee.ImageCollection:
    months = SEASONS[season]
    collection = ee.ImageCollection([])

    for m in months:
        if m == 12:
            col = ee.ImageCollection(S2_COLLECTION).filterDate(
                f"{year}-12-01", f"{year}-12-31"
            )
        elif m in [1, 2]:
            col = ee.ImageCollection(S2_COLLECTION).filterDate(
                f"{year + 1}-{m:02d}-01",
                f"{year + 1}-{m:02d}-28"
            )
        else:
            col = ee.ImageCollection(S2_COLLECTION).filterDate(
                f"{year}-{m:02d}-01",
                f"{year}-{m:02d}-28"
            )

        collection = collection.merge(col)

    return collection


def _compute_ndvi(image):
    return image.normalizedDifference(["B8", "B4"]).rename("NDVI")


def get_seasonal_anomaly(
    geometry: ee.Geometry,
    year: int,
    season: str
) -> dict:

    if season not in SEASONS:
        raise ValueError("Invalid season. Use MAM, JJA, SON, or DJF")

    # Target season NDVI
    target_ndvi = (
        _season_collection(year, season)
        .map(_compute_ndvi)
        .mean()
        .clip(geometry)
    )

    # Reference season NDVI (previous year)
    ref_ndvi = (
        _season_collection(year - 1, season)
        .map(_compute_ndvi)
        .mean()
        .clip(geometry)
    )

    target_val = target_ndvi.reduceRegion(
        reducer=ee.Reducer.mean(),
        geometry=geometry,
        scale=10,
        bestEffort=True
    ).get("NDVI")

    ref_val = ref_ndvi.reduceRegion(
        reducer=ee.Reducer.mean(),
        geometry=geometry,
        scale=10,
        bestEffort=True
    ).get("NDVI")

    target_val = ee.Number(target_val)
    ref_val = ee.Number(ref_val)

    anomaly = target_val.subtract(ref_val)

    anomaly_percent = anomaly.divide(ref_val).multiply(100)

    return {
        "season": season,
        "year": year,
        "mean_ndvi_target": target_val.getInfo(),
        "mean_ndvi_reference": ref_val.getInfo(),
        "anomaly_percent": anomaly_percent.getInfo()
    }