import ee

SOILGRID_IMAGE = "ISRIC/SoilGrids250m"


def get_soil_summary(geometry: ee.Geometry) -> dict:
    """
    Returns mean topsoil (0–30 cm) soil properties
    from SoilGrids (ISRIC).

    RAW values only. No interpretation.
    """

    soil = ee.Image(SOILGRID_IMAGE).select([
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

    return {
        "ph": stats.get("phh2o_0-30cm_mean").getInfo(),
        "organic_carbon_g_kg": stats.get("soc_0-30cm_mean").getInfo(),
        "bulk_density_cg_cm3": stats.get("bdod_0-30cm_mean").getInfo(),
        "texture": {
            "clay_pct": stats.get("clay_0-30cm_mean").getInfo(),
            "sand_pct": stats.get("sand_0-30cm_mean").getInfo(),
            "silt_pct": stats.get("silt_0-30cm_mean").getInfo()
        },
        "depth_cm": "0–30",
        "scale_m": 250,
        "aggregation": "mean",
        "source": "SoilGrids (ISRIC)"
    }
