import ee

ERA5_DAILY = "ECMWF/ERA5_LAND/DAILY_AGGR"

SEASONS = {
    "MAM": [3, 4, 5],
    "JJA": [6, 7, 8],
    "SON": [9, 10, 11],
    "DJF": [12, 1, 2]
}


def _season_collection(year: int, season: str) -> ee.ImageCollection:
    """
    Build a proper Earth Engine ImageCollection for a season
    """
    months = SEASONS[season]
    collection = ee.ImageCollection([])

    for m in months:
        if m == 12:
            col = ee.ImageCollection(ERA5_DAILY).filterDate(
                f"{year}-12-01", f"{year}-12-31"
            )
        elif m in [1, 2]:
            col = ee.ImageCollection(ERA5_DAILY).filterDate(
                f"{year + 1}-{m:02d}-01",
                f"{year + 1}-{m:02d}-28"
            )
        else:
            col = ee.ImageCollection(ERA5_DAILY).filterDate(
                f"{year}-{m:02d}-01",
                f"{year}-{m:02d}-28"
            )

        collection = collection.merge(col)

    return collection


def get_temperature_seasonal_anomaly(
    geometry: ee.Geometry,
    season: str,
    year: int
) -> dict:
    """
    Temperature anomaly (°C) = season(year) − season(year-1)
    """

    if season not in SEASONS:
        raise ValueError("Invalid season. Use MAM, JJA, SON, or DJF")

    # Target season
    target_mean = (
        _season_collection(year, season)
        .select("temperature_2m")
        .mean()
    )

    # Reference season (previous year)
    ref_mean = (
        _season_collection(year - 1, season)
        .select("temperature_2m")
        .mean()
    )

    # Reduce over geometry
    target_stats = target_mean.reduceRegion(
        reducer=ee.Reducer.mean(),
        geometry=geometry,
        scale=1000,
        bestEffort=True
    )

    ref_stats = ref_mean.reduceRegion(
        reducer=ee.Reducer.mean(),
        geometry=geometry,
        scale=1000,
        bestEffort=True
    )

    # Extract values safely
    target_k = target_stats.get("temperature_2m")
    ref_k = ref_stats.get("temperature_2m")

    target_c = ee.Number(target_k).subtract(273.15)
    ref_c = ee.Number(ref_k).subtract(273.15)

    anomaly = target_c.subtract(ref_c)

    return {
        "season": season,
        "target_year": year,
        "reference_year": year - 1,
        "mean_temp_target_c": target_c.getInfo(),
        "mean_temp_reference_c": ref_c.getInfo(),
        "mean_temp_anomaly_c": anomaly.getInfo()
    }
