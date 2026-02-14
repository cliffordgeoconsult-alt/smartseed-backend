# app/services/gee/soil_config.py

ISDA_BASE = "ISDASOIL/Africa/v1"

# Supported depths
VALID_DEPTHS = {
    "0-20cm": "mean_0_20",
    "20-50cm": "mean_20_50",
}

# Numeric soil datasets only
SOIL_DATASETS = {
    "ph": "ph",
    "nitrogen": "nitrogen_total",
    "organic_carbon": "carbon_organic",
    "carbon_total": "carbon_total",
    "phosphorus": "phosphorus_extractable",
    "potassium": "potassium_extractable",
    "calcium": "calcium_extractable",
    "magnesium": "magnesium_extractable",
    "sulphur": "sulphur_extractable",
    "zinc": "zinc_extractable",
    "iron": "iron_extractable",
    "aluminium": "aluminium_extractable",
    "cec": "cation_exchange_capacity",
    "clay": "clay_content",
    "sand": "sand_content",
    "silt": "silt_content",
    "bulk_density": "bulk_density",
    "bedrock_depth": "bedrock_depth",
}

# Visualization ranges per dataset
SOIL_VIS = {
    "ph": {"min": 3, "max": 9},
    "nitrogen": {"min": 0, "max": 0.5},
    "organic_carbon": {"min": 0, "max": 10},
    "clay": {"min": 0, "max": 60},
    "sand": {"min": 0, "max": 80},
    "silt": {"min": 0, "max": 60},
    "cec": {"min": 0, "max": 40},
}