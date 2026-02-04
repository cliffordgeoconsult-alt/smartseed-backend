import ee

SRTM = "USGS/SRTMGL1_003"


def get_elevation_tiles(geometry: ee.Geometry) -> dict:
    """
    Returns map tiles URL for elevation (meters)
    """

    dem = (
        ee.Image(SRTM)
        .select("elevation")
        .clip(geometry)
    )

    vis_params = {
        "min": 0,
        "max": 3000,
        "palette": [
            "#081d58",
            "#253494",
            "#225ea8",
            "#1d91c0",
            "#41b6c4",
            "#7fcdbb",
            "#c7e9b4",
            "#edf8b1",
            "#ffffd9"
        ]
    }

    map_id = dem.getMapId(vis_params)

    return {
        "tile_url": map_id["tile_fetcher"].url_format
    }
