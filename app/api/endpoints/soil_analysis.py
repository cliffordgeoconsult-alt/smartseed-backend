from fastapi import APIRouter, Depends
from app.api.deps import get_geometry
from app.services.gee.soil_analysis import get_full_soil_analysis
import ee

router = APIRouter()


@router.post("/soil/analysis")
def soil_analysis(
    depth: str = "0-20cm",
    geometry: ee.Geometry = Depends(get_geometry),
):
    return get_full_soil_analysis(
        geometry=geometry,
        depth=depth,
    )