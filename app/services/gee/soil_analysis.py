import ee

ISDA_BASE = "ISDASOIL/Africa/v1"

SOIL_PARAMETERS = {
    "ph": "ph",
    "nitrogen": "nitrogen_total",
    "organic_carbon": "carbon_organic",
    "phosphorus": "phosphorus_extractable",
    "potassium": "potassium_extractable",
    "calcium": "calcium_extractable",
    "magnesium": "magnesium_extractable",
    "sodium": "sodium_extractable",
    "sulphur": "sulphur_extractable",
    "aluminium": "aluminium_extractable",
    "zinc": "zinc_extractable",
    "iron": "iron_extractable",
    "clay": "clay_content",
    "sand": "sand_content",
    "silt": "silt_content",
    "bulk_density": "bulk_density",
    "texture_class": "texture_class",
    "bedrock_depth": "bedrock_depth",
}


def get_full_soil_analysis(
    geometry: ee.Geometry,
    depth: str = "0-20cm"
) -> dict:
    """
    Returns complete soil profile for selected geometry.
    """

    try:
        results = {}

        for key, param in SOIL_PARAMETERS.items():

            image = ee.Image(f"{ISDA_BASE}/{param}")

            # Depth handling
            if param == "bedrock_depth":
                band = image.select(0)
            else:
                band_index = 0 if depth == "0-20cm" else 1
                band = image.select(band_index)

            soil = band.clip(geometry)

            stats = soil.reduceRegion(
                reducer=ee.Reducer.mean()
                    .combine(ee.Reducer.min(), "", True)
                    .combine(ee.Reducer.max(), "", True),
                geometry=geometry,
                scale=250,
                maxPixels=1e13,
            )

            results[key] = stats.getInfo()

        return {
            "status": "success",
            "depth": depth,
            "soil_profile": results
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
        }