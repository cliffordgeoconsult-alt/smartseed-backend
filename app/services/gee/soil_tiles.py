import ee
from app.services.gee.soil_config import (
    ISDA_BASE,
    SOIL_LAYERS,
    VALID_DEPTHS,
    SOIL_VIS,
)

def get_soil_tile(geometry: ee.Geometry, dataset: str, depth: str):

    if dataset not in SOIL_LAYERS:
        return {"status": "error", "message": "Invalid dataset"}

    if depth not in VALID_DEPTHS:
        return {"status": "error", "message": "Invalid depth"}

    dataset_name = SOIL_LAYERS[dataset]
    band_name = VALID_DEPTHS[depth]

    image = ee.Image(f"{ISDA_BASE}/{dataset_name}")
    band = image.select(band_name)
    clipped = band.clip(geometry)

    vis = SOIL_VIS.get(dataset, {"min": 0, "max": 100})

    map_id = clipped.getMapId({
        "min": vis["min"],
        "max": vis["max"],
        "palette": ["blue", "cyan", "yellow", "orange", "red"],
    })

    return {
        "status": "success",
        "tile_url": map_id["tile_fetcher"].url_format,
    }