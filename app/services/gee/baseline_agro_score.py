# app/services/gee/baseline_agro_score.py
import ee
from app.services.gee.soil_config import ISDA_BASE, VALID_DEPTHS


def compute_baseline_score(geometry: ee.Geometry, depth: str = "0-20cm"):

    if depth not in VALID_DEPTHS:
        raise ValueError("Invalid soil depth")

    band = VALID_DEPTHS[depth]

    ph = ee.Image(f"{ISDA_BASE}/ph").select(band).multiply(0.1)
    oc = ee.Image(f"{ISDA_BASE}/carbon_organic").select(band).multiply(0.1)
    cec = ee.Image(f"{ISDA_BASE}/cation_exchange_capacity").select(band)

    # ---- Fuzzy thresholds (Sys et al.) ----

    ph_score = ph.expression("""
        b(0) <= 5.2 ? 0.4 :
        b(0) <= 5.5 ? 0.6 :
        b(0) <= 5.8 ? 0.85 :
        b(0) <= 6.2 ? 0.95 :
        b(0) <= 6.6 ? 1.0 :
        b(0) <= 7.0 ? 0.95 :
        b(0) <= 7.8 ? 0.85 :
        b(0) <= 8.2 ? 0.6 :
        0.25
    """)

    oc_score = oc.expression("""
        b(0) <= 0.5 ? 0.4 :
        b(0) <= 0.7 ? 0.6 :
        b(0) <= 1.5 ? 0.85 :
        b(0) <= 2.0 ? 0.95 :
        1.0
    """)

    cec_score = cec.expression("""
        b(0) <= 10 ? 0.4 :
        b(0) <= 16 ? 0.85 :
        b(0) <= 24 ? 0.95 :
        1.0
    """)

    soil_score = ph_score.multiply(oc_score).multiply(cec_score)

    result = soil_score.reduceRegion(
        reducer=ee.Reducer.mean(),
        geometry=geometry,
        scale=250,
        maxPixels=1e13
    ).getInfo()

    return list(result.values())[0]