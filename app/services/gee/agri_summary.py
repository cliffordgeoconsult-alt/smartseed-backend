# app/services/gee/agri_summary.py
import ee
from app.services.gee.soil_config import ISDA_BASE, VALID_DEPTHS


def normalize(image, min_val, max_val):
    return image.subtract(min_val).divide(max_val - min_val).clamp(0, 1)


def build_agri_summary(
    geometry: ee.Geometry,
    depth: str,
    start_date: str,
    end_date: str,
):

    if depth not in VALID_DEPTHS:
        return {"status": "error", "message": "Invalid depth"}

    band = VALID_DEPTHS[depth]

    # SOIL
    ph = ee.Image(f"{ISDA_BASE}/ph").select(band).multiply(0.1)
    oc = ee.Image(f"{ISDA_BASE}/carbon_organic").select(band).multiply(0.1)
    cec = ee.Image(f"{ISDA_BASE}/cation_exchange_capacity").select(band)
    clay = ee.Image(f"{ISDA_BASE}/clay_content").select(band)

    ca = ee.Image(f"{ISDA_BASE}/calcium_extractable").select(band).multiply(0.1)
    mg = ee.Image(f"{ISDA_BASE}/magnesium_extractable").select(band).multiply(0.1)
    k = ee.Image(f"{ISDA_BASE}/potassium_extractable").select(band).multiply(0.1)

    base_sat = ca.add(mg).add(k).divide(cec).multiply(100)

    # CLIMATE
    era5 = (
        ee.ImageCollection("ECMWF/ERA5_LAND/DAILY_AGGR")
        .filterDate(start_date, end_date)
        .filterBounds(geometry)
    )

    rainfall = (
        era5.select("total_precipitation_sum")
        .sum()
        .multiply(1000)
    )

    temperature = (
        era5.select("temperature_2m")
        .mean()
        .subtract(273.15)
    )

    # MAIZE SUITABILITY SCORE
    ph_score = normalize(ph, 5.5, 7)
    oc_score = normalize(oc, 1, 4)
    rain_score = normalize(rainfall, 500, 1200)
    temp_score = normalize(temperature, 18, 28)

    suitability = (
        ph_score.multiply(0.25)
        .add(oc_score.multiply(0.20))
        .add(rain_score.multiply(0.30))
        .add(temp_score.multiply(0.25))
    ).multiply(100)

    # REDUCE TO REGION MEAN
    reducer = ee.Reducer.mean()

    result = suitability.reduceRegion(
        reducer=reducer,
        geometry=geometry,
        scale=250,
        maxPixels=1e13,
    ).getInfo()

    rain_val = rainfall.reduceRegion(
        reducer=reducer,
        geometry=geometry,
        scale=250,
        maxPixels=1e13,
    ).getInfo()

    temp_val = temperature.reduceRegion(
        reducer=reducer,
        geometry=geometry,
        scale=250,
        maxPixels=1e13,
    ).getInfo()

    return {
        "status": "success",
        "maize_suitability_score": list(result.values())[0],
        "mean_rainfall_mm": list(rain_val.values())[0],
        "mean_temperature_c": list(temp_val.values())[0],
    }