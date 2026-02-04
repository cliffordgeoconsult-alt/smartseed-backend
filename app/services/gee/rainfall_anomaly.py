import ee

CHIRPS_ID = "UCSB-CHG/CHIRPS/DAILY"


SEASONS = {
    "long_rains": ("03-01", "05-31"),
    "short_rains": ("10-01", "12-31")
}


def get_seasonal_anomaly(
    geometry: ee.Geometry,
    year: int,
    season: str,
    baseline_start_year: int = 2004,
    baseline_end_year: int = 2023
):
    if season not in SEASONS:
        raise ValueError("Invalid season")

    start_mm, end_mm = SEASONS[season]

    season_start = f"{year}-{start_mm}"
    season_end = f"{year}-{end_mm}"

    chirps = ee.ImageCollection(CHIRPS_ID).filterBounds(geometry)

    # Current season rainfall
    current = (
        chirps
        .filterDate(season_start, season_end)
        .sum()
        .reduceRegion(
            reducer=ee.Reducer.mean(),
            geometry=geometry,
            scale=5000,
            maxPixels=1e13
        )
        .get("precipitation")
    )

    # Long-term mean
    baseline_images = []
    for y in range(baseline_start_year, baseline_end_year + 1):
        baseline_images.append(
            chirps
            .filterDate(f"{y}-{start_mm}", f"{y}-{end_mm}")
            .sum()
        )

    baseline_mean = (
        ee.ImageCollection(baseline_images)
        .mean()
        .reduceRegion(
            reducer=ee.Reducer.mean(),
            geometry=geometry,
            scale=5000,
            maxPixels=1e13
        )
        .get("precipitation")
    )

    current_val = ee.Number(current).getInfo()
    baseline_val = ee.Number(baseline_mean).getInfo()

    anomaly_percent = (
        ((current_val - baseline_val) / baseline_val) * 100
        if baseline_val and baseline_val != 0
        else None
    )

    return {
        "season": season,
        "year": year,
        "total_mm": current_val,
        "long_term_mean_mm": baseline_val,
        "anomaly_percent": anomaly_percent,
        "interpretation": (
            "Below normal" if anomaly_percent < -10 else
            "Above normal" if anomaly_percent > 10 else
            "Near normal"
        )
    }
