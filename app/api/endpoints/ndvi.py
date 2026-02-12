from fastapi import APIRouter, Depends, Query
import ee

from app.api.deps import get_geometry
from app.services.gee.ndvi import get_mean_ndvi

router = APIRouter(prefix="/ndvi", tags=["NDVI"])


@router.post("/summary")
def ndvi_summary(
    geometry: ee.Geometry = Depends(get_geometry),
    start_date: str = Query(...),
    end_date: str = Query(...)
):
    """
    Mean NDVI over a geometry for a given time range.
    """

    try:
        mean_ndvi = get_mean_ndvi(
            geometry=geometry,
            start_date=start_date,
            end_date=end_date
        )

        if mean_ndvi is None:
            return {
                "status": "no_data",
                "message": "No Sentinel-2 images found for this period."
            }

        return {
            "status": "success",
            "dataset": "Sentinel-2 SR",
            "index": "NDVI",
            "mean_ndvi": mean_ndvi,
            "range": [-1, 1]
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }