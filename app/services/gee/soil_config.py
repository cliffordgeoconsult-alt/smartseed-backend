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

    # Exchangeable bases
    "calcium": "calcium_extractable",
    "magnesium": "magnesium_extractable",
    "potassium": "potassium_extractable",
    "sodium": "sodium_extractable",

    # Texture
    "clay": "clay_content",
    "sand": "sand_content",
    "silt": "silt_content",

    # Physical
    "bulk_density": "bulk_density",
}

SOIL_VIS = {
    "ph": {"min": 3, "max": 9},
    "organic_carbon": {"min": 0, "max": 10},
    "cec": {"min": 0, "max": 40},
    "calcium": {"min": 0, "max": 20},
    "magnesium": {"min": 0, "max": 10},
    "potassium": {"min": 0, "max": 2},
    "clay": {"min": 0, "max": 60},
    "sand": {"min": 0, "max": 80},
    "silt": {"min": 0, "max": 60},
}