from fastapi import APIRouter, Depends
import ee

from app.api.deps import get_geometry
from app.services.gee.soil import get_soil_summary

router = APIRouter(prefix="/soil", tags=["Soil"])


@router.post("/summary")
def soil_summary(
    geometry: ee.Geometry = Depends(get_geometry)
):
    """
    Returns mean soil properties (0–30cm).
    """

    try:
        data = get_soil_summary(geometry)

        return data

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }