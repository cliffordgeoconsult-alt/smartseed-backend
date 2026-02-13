import ee


def get_soil_summary(geometry: ee.Geometry) -> dict:
    """
    Returns mean topsoil (0–30 cm) soil properties
    from SoilGrids (ISRIC).
    """

    # Load each SoilGrids dataset correctly
    ph = ee.ImageCollection("ISRIC/SoilGrids250m/phh2o_mean").first()
    soc = ee.ImageCollection("ISRIC/SoilGrids250m/soc_mean").first()
    bdod = ee.ImageCollection("ISRIC/SoilGrids250m/bdod_mean").first()
    clay = ee.ImageCollection("ISRIC/SoilGrids250m/clay_mean").first()
    sand = ee.ImageCollection("ISRIC/SoilGrids250m/sand_mean").first()
    silt = ee.ImageCollection("ISRIC/SoilGrids250m/silt_mean").first()

    # Select 0-30cm depth band
    soil = ee.Image.cat([
        ph.select("phh2o_0-30cm_mean"),
        soc.select("soc_0-30cm_mean"),
        bdod.select("bdod_0-30cm_mean"),
        clay.select("clay_0-30cm_mean"),
        sand.select("sand_0-30cm_mean"),
        silt.select("silt_0-30cm_mean"),
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
            "silt_pct": result.get("silt_0-30cm_mean"),
        }
    }