# app/services/gee/soil_tiles.py

import ee
from app.services.gee.soil_config import (
    ISDA_BASE,
    SOIL_DATASETS,
    VALID_DEPTHS,
    SOIL_VIS,
)


def get_soil_tile(
    geometry: ee.Geometry,
    dataset: str,
    depth: str,
):

    if dataset not in SOIL_DATASETS:
        return {"status": "error", "message": "Invalid dataset"}

    if depth not in VALID_DEPTHS:
        return {"status": "error", "message": "Invalid depth"}

    try:
        dataset_name = SOIL_DATASETS[dataset]
        band_name = VALID_DEPTHS[depth]

        image = ee.Image(f"{ISDA_BASE}/{dataset_name}")

        if dataset_name == "bedrock_depth":
            band = image.select(0)
        else:
            band = image.select(band_name)

        clipped = band.clip(geometry)

        vis = SOIL_VIS.get(dataset, {"min": 0, "max": 100})

        vis_params = {
            "min": vis["min"],
            "max": vis["max"],
            "palette": ["blue", "cyan", "yellow", "orange", "red"],
        }

        map_id = clipped.getMapId(vis_params)

        return {
            "status": "success",
            "dataset": dataset,
            "depth": depth,
            "tile_url": map_id["tile_fetcher"].url_format,
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
        }