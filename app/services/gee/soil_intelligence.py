# app/services/gee/soil_intelligence.py

from app.services.gee.soil_calculations import calculate_base_saturation
from app.services.gee.soil_interpretation import (
    classify_ph,
    classify_texture,
)

def build_soil_intelligence(raw):

    ph = raw["ph"]["mean"]
    cec = raw["cec"]["mean"]

    ca = raw["calcium"]["mean"]
    mg = raw["magnesium"]["mean"]
    k = raw["potassium"]["mean"]
    na = raw["sodium"]["mean"]

    clay = raw["clay"]["mean"]
    sand = raw["sand"]["mean"]
    silt = raw["silt"]["mean"]

    base_sat = calculate_base_saturation(ca, mg, k, na, cec)

    return {
        "ph_status": classify_ph(ph),
        "texture_class": classify_texture(clay, sand, silt),
        "base_saturation": base_sat,
        "cec": cec,
    }