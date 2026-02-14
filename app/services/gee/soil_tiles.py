import ee

ISDA_BASE = "ISDASOIL/Africa/v1"

# Visualization settings per parameter
VISUALIZATION_CONFIG = {
    "ph": {"min": 3, "max": 9},
    "nitrogen_total": {"min": 0, "max": 0.5},
    "carbon_organic": {"min": 0, "max": 5},
    "phosphorus_extractable": {"min": 0, "max": 100},
    "potassium_extractable": {"min": 0, "max": 300},
    "calcium_extractable": {"min": 0, "max": 3000},
    "magnesium_extractable": {"min": 0, "max": 1000},
    "sodium_extractable": {"min": 0, "max": 500},
    "sulphur_extractable": {"min": 0, "max": 50},
    "aluminium_extractable": {"min": 0, "max": 100},
    "zinc_extractable": {"min": 0, "max": 20},
    "iron_extractable": {"min": 0, "max": 100},
    "clay_content": {"min": 0, "max": 60},
    "sand_content": {"min": 0, "max": 100},
    "silt_content": {"min": 0, "max": 60},
    "bulk_density": {"min": 0.8, "max": 1.8},
    "texture_class": {"min": 0, "max": 12},
    "bedrock_depth": {"min": 0, "max": 200},
}


def get_soil_tiles(
    geometry: ee.Geometry,
    parameter: str,
    depth: str = "0-20cm",
) -> dict:
    """
    Returns soil tile URL for selected parameter.
    """

    try:
        if parameter not in VISUALIZATION_CONFIG:
            raise ValueError(f"Unsupported soil parameter: {parameter}")

        image = ee.Image(f"{ISDA_BASE}/{parameter}")

        # Depth band
        if parameter == "bedrock_depth":
            band = image.select(0)
        else:
            band_index = 0 if depth == "0-20cm" else 1
            band = image.select(band_index)

        soil = band.clip(geometry)

        vis = VISUALIZATION_CONFIG[parameter]

        vis_params = {
            "min": vis["min"],
            "max": vis["max"],
            "palette": [
                "#0000ff",
                "#00ffff",
                "#ffff00",
                "#ffa500",
                "#ff0000",
            ],
        }

        map_id = soil.getMapId(vis_params)

        return {
            "status": "success",
            "parameter": parameter,
            "depth": depth,
            "tile_url": map_id["tile_fetcher"].url_format,
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
        }