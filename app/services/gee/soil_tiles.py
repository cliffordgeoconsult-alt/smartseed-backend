import ee

ISDA_BASE = "ISDASOIL/Africa/v1"

VIS_CONFIG = {
    "ph": {"min": 3, "max": 9},
    "nitrogen_total": {"min": 0, "max": 0.5},
    "carbon_organic": {"min": 0, "max": 5},
    "clay_content": {"min": 0, "max": 60},
    "sand_content": {"min": 0, "max": 100},
    "silt_content": {"min": 0, "max": 60},
}


def get_soil_tiles(
    geometry: ee.Geometry,
    dataset: str,
    depth: str = "0-20cm",
) -> dict:

    try:
        image = ee.Image(f"{ISDA_BASE}/{dataset}")

        band_name = "mean_0_20" if depth == "0-20cm" else "mean_20_50"

        band = image.select(band_name).clip(geometry)

        vis = VIS_CONFIG.get(dataset, {"min": 0, "max": 100})

        map_id = band.getMapId({
            "min": vis["min"],
            "max": vis["max"],
            "palette": [
                "#0000ff",
                "#00ffff",
                "#ffff00",
                "#ffa500",
                "#ff0000",
            ],
        })

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