import ee

S2_COLLECTION = "COPERNICUS/S2_SR_HARMONIZED"


def _add_ndvi(image: ee.Image) -> ee.Image:
    """
    Adds NDVI band to an image.
    NDVI = (B8 - B4) / (B8 + B4)
    """
    ndvi = image.normalizedDifference(["B8", "B4"]).rename("NDVI")
    return image.addBands(ndvi)


def get_mean_ndvi(
    geometry: ee.Geometry,
    start_date: str,
    end_date: str
) -> float | None:
    """
    Returns mean NDVI over a geometry for a given date range.
    """

    collection = (
        ee.ImageCollection(S2_COLLECTION)
        .filterBounds(geometry)
        .filterDate(start_date, end_date)
        .filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE", 20))
        .map(_add_ndvi)
    )

    # If no images available
    size = collection.size().getInfo()
    if size == 0:
        return None

    mean_image = collection.select("NDVI").mean()

    stats = mean_image.reduceRegion(
        reducer=ee.Reducer.mean(),
        geometry=geometry,
        scale=10,
        bestEffort=True,
        maxPixels=1e13
    )

    ndvi_value = stats.get("NDVI")

    if ndvi_value is None:
        return None

    return ee.Number(ndvi_value).getInfo()