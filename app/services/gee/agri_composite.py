# app/services/gee/agri_composite.py
import ee
from datetime import datetime
from app.services.gee.soil_config import ISDA_BASE, VALID_DEPTHS

def normalize(image, min_val, max_val):
    return image.subtract(min_val).divide(max_val - min_val).clamp(0, 1)


def build_agri_composite(
    geometry: ee.Geometry,
    depth: str,
    start_date: str,
    end_date: str,
):

    if depth not in VALID_DEPTHS:
        return {"status": "error", "message": "Invalid depth"}

    band = VALID_DEPTHS[depth]

    # SOIL LAYERS
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
        .multiply(1000)  # m → mm
    )

    temperature = (
        era5.select("temperature_2m")
        .mean()
        .subtract(273.15)  # Kelvin → Celsius
    )

    # NORMALIZATION
    ph_score = normalize(ph, 5.5, 7)
    oc_score = normalize(oc, 1, 4)
    cec_score = normalize(cec, 5, 35)
    bs_score = normalize(base_sat, 40, 80)
    texture_score = normalize(clay, 15, 45)

    rain_score = normalize(rainfall, 500, 1200)  # maize ideal rainfall
    temp_score = normalize(temperature, 18, 28)  # maize ideal temp

    # SOIL FERTILITY INDEX
    sfi = (
        ph_score.multiply(0.30)
        .add(oc_score.multiply(0.25))
        .add(cec_score.multiply(0.25))
        .add(bs_score.multiply(0.20))
    ).multiply(100)

    # MAIZE SUITABILITY INDEX (Now climate integrated)
    msi = (
        ph_score.multiply(0.20)
        .add(oc_score.multiply(0.15))
        .add(texture_score.multiply(0.10))
        .add(bs_score.multiply(0.15))
        .add(rain_score.multiply(0.20))
        .add(temp_score.multiply(0.20))
    ).multiply(100)

    # SOIL HEALTH INDEX
    shi = (
        oc_score.multiply(0.40)
        .add(cec_score.multiply(0.30))
        .add(texture_score.multiply(0.30))
    ).multiply(100)

    # Clip
    sfi = sfi.clip(geometry)
    msi = msi.clip(geometry)
    shi = shi.clip(geometry)

    palette = ["red", "orange", "yellow", "green"]

    return {
        "status": "success",
        "soil_fertility_tile": sfi.getMapId({
            "min": 0,
            "max": 100,
            "palette": palette,
        })["tile_fetcher"].url_format,

        "maize_suitability_tile": msi.getMapId({
            "min": 0,
            "max": 100,
            "palette": palette,
        })["tile_fetcher"].url_format,

        "soil_health_tile": shi.getMapId({
            "min": 0,
            "max": 100,
            "palette": palette,
        })["tile_fetcher"].url_format,
    }