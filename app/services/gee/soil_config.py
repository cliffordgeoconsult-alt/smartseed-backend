# app/services/gee/soil_config.py
ISDA_BASE = "ISDASOIL/Africa/v1"

VALID_DEPTHS = {
    "0-20cm": "mean_0_20",
    "20-50cm": "mean_20_50",
}

SOIL_LAYERS = {
    # Core chemistry
    "ph": "ph",
    "organic_carbon": "carbon_organic",
    "cec": "cation_exchange_capacity",

    # Exchangeable bases (cmolc/kg)
    "calcium": "calcium_extractable",
    "magnesium": "magnesium_extractable",
    "potassium": "potassium_extractable",

    # Texture (%)
    "clay": "clay_content",
    "sand": "sand_content",
    "silt": "silt_content",

    # Physical
    "bulk_density": "bulk_density",
}

# ISDA scaling factors
SOIL_SCALING = {
    "ph": 0.1,                # stored ×10
    "organic_carbon": 0.1,    # stored ×10
    "bulk_density": 0.01,     # stored ×100

    "calcium": 1,
    "magnesium": 1,
    "potassium": 1,
    "cec": 1,
    "clay": 1,
    "sand": 1,
    "silt": 1,
}

SOIL_VIS = {
    "ph": {"min": 4, "max": 8},
    "organic_carbon": {"min": 0, "max": 6},
    "cec": {"min": 0, "max": 40},
    "calcium": {"min": 0, "max": 20},
    "magnesium": {"min": 0, "max": 10},
    "potassium": {"min": 0, "max": 2},
    "clay": {"min": 0, "max": 60},
    "sand": {"min": 0, "max": 80},
    "silt": {"min": 0, "max": 60},
}