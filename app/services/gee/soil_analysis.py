import ee

ISDA_BASE = "ISDASOIL/Africa/v1"

SOIL_DATASETS = {
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
    Returns full soil statistics for selected geometry.
    """

    try:
        results = {}

        band_name = "mean_0_20" if depth == "0-20cm" else "mean_20_50"

        for key, dataset in SOIL_DATASETS.items():

            image = ee.Image(f"{ISDA_BASE}/{dataset}")

            # Bedrock only has one band usually
            if dataset == "bedrock_depth":
                band = image.select(0)
            else:
                band = image.select(band_name)

            soil = band.clip(geometry)

            stats = soil.reduceRegion(
                reducer=ee.Reducer.mean()
                    .combine(ee.Reducer.min(), "", True)
                    .combine(ee.Reducer.max(), "", True)
                    .combine(ee.Reducer.stdDev(), "", True),
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