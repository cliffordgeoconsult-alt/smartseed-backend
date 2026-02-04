from fastapi import APIRouter, Depends
import ee

from app.api.deps import get_geometry
from app.services.gee.soil import get_soil_summary

router = APIRouter(
    prefix="/soil",
    tags=["Soil"]
)


@router.post("/summary")
def soil_summary(
    geometry: ee.Geometry = Depends(get_geometry)
):
    """
    Mean topsoil (0–30 cm) soil properties
    from SoilGrids (ISRIC).
    """

    data = get_soil_summary(geometry)

    return {
        "status": "success",
        "soil": data
    }
