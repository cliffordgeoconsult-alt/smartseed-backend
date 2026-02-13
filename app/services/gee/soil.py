import ee


SOIL_IMAGE = "projects/soilgrids-isric/soilgrids"


def get_soil_summary(geometry: ee.Geometry) -> dict:
    """
    Returns mean topsoil (0–30 cm) soil properties
    from SoilGrids (ISRIC).
    """

    soil = ee.Image(SOIL_IMAGE).select([
        "phh2o_0-30cm_mean",
        "soc_0-30cm_mean",
        "bdod_0-30cm_mean",
        "clay_0-30cm_mean",
        "sand_0-30cm_mean",
        "silt_0-30cm_mean"
    ])

    stats = soil.reduceRegion(
        reducer=ee.Reducer.mean(),
        geometry=geometry,
        scale=250,
        bestEffort=True,
        maxPixels=1e13
    )

    result = stats.getInfo()

    if not result:
        return {
            "status": "no_data",
            "message": "No soil data available."
        }

    return {
        "status": "success",
        "source": "SoilGrids (ISRIC)",
        "depth_cm": "0–30",
        "scale_m": 250,
        "aggregation": "mean",
        "ph": result.get("phh2o_0-30cm_mean"),
        "organic_carbon_g_kg": result.get("soc_0-30cm_mean"),
        "bulk_density_cg_cm3": result.get("bdod_0-30cm_mean"),
        "texture": {
            "clay_pct": result.get("clay_0-30cm_mean"),
            "sand_pct": result.get("sand_0-30cm_mean"),
            "silt_pct": result.get("silt_0-30cm_mean")
        }
    }