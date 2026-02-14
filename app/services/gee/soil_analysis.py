# app/services/gee/soil_analysis.py

import ee
from app.services.gee.soil_config import (
    ISDA_BASE,
    SOIL_DATASETS,
    VALID_DEPTHS,
)


def get_soil_analysis(geometry: ee.Geometry, depth: str):

    if depth not in VALID_DEPTHS:
        return {"status": "error", "message": "Invalid depth"}

    band_name = VALID_DEPTHS[depth]

    try:
        results = {}

        for key, dataset in SOIL_DATASETS.items():

            image = ee.Image(f"{ISDA_BASE}/{dataset}")

            # Bedrock depth has no layered bands
            if dataset == "bedrock_depth":
                band = image.select(0)
            else:
                band = image.select(band_name)

            clipped = band.clip(geometry)

            stats = clipped.reduceRegion(
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
            "soil_profile": results,
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
        }