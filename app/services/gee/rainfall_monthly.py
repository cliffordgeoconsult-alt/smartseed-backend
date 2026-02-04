import ee

CHIRPS = "UCSB-CHG/CHIRPS/DAILY"


def get_monthly_rainfall(
    geometry: ee.Geometry,
    year: int
):
    """
    Returns monthly total rainfall (mm) for a given year
    """

    collection = (
        ee.ImageCollection(CHIRPS)
        .filterBounds(geometry)
        .filterDate(f"{year}-01-01", f"{year}-12-31")
        .select("precipitation")
    )

    results = []

    for month in range(1, 13):
        start = ee.Date.fromYMD(year, month, 1)
        end = start.advance(1, "month")

        monthly = collection.filterDate(start, end)

        total_img = monthly.sum()

        stats = total_img.reduceRegion(
            reducer=ee.Reducer.mean(),
            geometry=geometry,
            scale=5000,
            bestEffort=True
        )

        results.append(
            ee.Feature(
                None,
                {
                    "month": month,
                    "total_mm": stats.get("precipitation")
                }
            )
        )

    fc = ee.FeatureCollection(results)
    data = fc.getInfo()["features"]

    output = []
    for f in data:
        p = f["properties"]
        output.append({
            "month": p["month"],
            "total_mm": p["total_mm"]
        })

    return output
