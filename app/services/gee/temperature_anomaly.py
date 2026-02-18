# app/services/gee/temperature_anomaly.py
import ee

ERA5_DAILY = "ECMWF/ERA5_LAND/DAILY_AGGR"

SEASONS = {
    "MAM": [3, 4, 5],
    "JJA": [6, 7, 8],
    "SON": [9, 10, 11],
    "DJF": [12, 1, 2]
}

# Helper: Seasonal Collection
def _season_collection(year: int, season: str) -> ee.ImageCollection:
    months = SEASONS[season]
    collection = ee.ImageCollection([])

    for m in months:

        if season == "DJF" and m in [1, 2]:
            y = year + 1
        else:
            y = year

        start = ee.Date.fromYMD(y, m, 1)
        end = start.advance(1, "month")

        col = (
            ee.ImageCollection(ERA5_DAILY)
            .filterDate(start, end)
            .select(["temperature_2m", "temperature_2m_max"])
        )

        collection = collection.merge(col)

    return collection

# SECTION A — CURRENT SEASON OVERVIEW
def get_current_season_overview(geometry, season, year):

    collection = _season_collection(year, season)

    mean_img = collection.select("temperature_2m").mean()
    max_img = collection.select("temperature_2m_max").max()
    min_img = collection.select("temperature_2m").min()

    heat_threshold = 308.15  # 35°C

    hot_days = collection.filter(
        ee.Filter.gt("temperature_2m_max", heat_threshold)
    )

    stats_mean = mean_img.reduceRegion(
        reducer=ee.Reducer.mean(),
        geometry=geometry,
        scale=1000,
        bestEffort=True,
        maxPixels=1e9
    )

    stats_max = max_img.reduceRegion(
        reducer=ee.Reducer.max(),
        geometry=geometry,
        scale=1000,
        bestEffort=True,
        maxPixels=1e9
    )

    stats_min = min_img.reduceRegion(
        reducer=ee.Reducer.min(),
        geometry=geometry,
        scale=1000,
        bestEffort=True,
        maxPixels=1e9
    )

    mean_c = ee.Number(stats_mean.get("temperature_2m")).subtract(273.15)
    max_c = ee.Number(stats_max.get("temperature_2m_max")).subtract(273.15)
    min_c = ee.Number(stats_min.get("temperature_2m")).subtract(273.15)

    return {
        "mean_temp_c": mean_c.getInfo(),
        "hottest_day_c": max_c.getInfo(),
        "coldest_day_c": min_c.getInfo(),
        "heat_stress_days_above_35C": hot_days.size().getInfo()
    }

# SECTION B — 30 YEAR CLIMATE ANOMALY
def get_temperature_seasonal_anomaly(geometry, season, year):

    target = _season_collection(year, season).mean()

    climatology = ee.ImageCollection([])

    for y in range(1991, 2021):
        climatology = climatology.merge(
            _season_collection(y, season)
        )

    climatology_mean = climatology.mean()

    target_stats = target.reduceRegion(
        reducer=ee.Reducer.mean(),
        geometry=geometry,
        scale=1000,
        bestEffort=True,
        maxPixels=1e9
    )

    clim_stats = climatology_mean.reduceRegion(
        reducer=ee.Reducer.mean(),
        geometry=geometry,
        scale=1000,
        bestEffort=True,
        maxPixels=1e9
    )

    target_c = ee.Number(target_stats.get("temperature_2m")).subtract(273.15)
    clim_c = ee.Number(clim_stats.get("temperature_2m")).subtract(273.15)

    anomaly = target_c.subtract(clim_c)

    indicator = ee.Algorithms.If(
        anomaly.gt(0),
        "Warmer than 30-year average",
        "Cooler than 30-year average"
    )

    return {
        "mean_temp_c": target_c.getInfo(),
        "climatology_mean_c": clim_c.getInfo(),
        "anomaly_c": anomaly.getInfo(),
        "indicator": indicator.getInfo()
    }

# SECTION C — 10 YEAR TREND
def get_10yr_temperature_trend(geometry, season, year):

    years = list(range(year - 9, year + 1))
    data = []

    for y in years:
        seasonal = _season_collection(y, season).mean()

        stats = seasonal.reduceRegion(
            reducer=ee.Reducer.mean(),
            geometry=geometry,
            scale=1000,
            bestEffort=True,
            maxPixels=1e9
        )

        temp_c = ee.Number(stats.get("temperature_2m")).subtract(273.15)

        data.append({
            "year": y,
            "mean_temp_c": temp_c.getInfo()
        })

    warming = data[-1]["mean_temp_c"] > data[0]["mean_temp_c"]

    return {
        "trend_period_years": 10,
        "warming_detected": warming,
        "data": data
    }

# SECTION D — AGRONOMIC INTERPRETATION
def get_agronomic_interpretation(mean_temp_c, heat_days):

    if mean_temp_c < 18:
        suitability = "Cool zone – Suitable for late-maturing highland hybrids"
    elif 18 <= mean_temp_c <= 26:
        suitability = "Optimal for most maize hybrids"
    else:
        suitability = "Warm zone – Consider early-maturing or drought-tolerant varieties"

    if heat_days > 10:
        heat_risk = "High heat stress risk during flowering"
    elif heat_days > 3:
        heat_risk = "Moderate heat stress risk"
    else:
        heat_risk = "Low heat stress risk"

    return {
        "temperature_suitability": suitability,
        "heat_stress_risk": heat_risk
    }