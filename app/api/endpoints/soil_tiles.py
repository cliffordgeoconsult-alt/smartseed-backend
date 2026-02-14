from fastapi import APIRouter, Depends
from app.api.deps import get_geometry
from app.services.gee.soil_tiles import get_soil_tiles
import ee

router = APIRouter()


@router.post("/soil/tiles")
def soil_tiles(
    parameter: str,
    depth: str = "0-20cm",
    geometry: ee.Geometry = Depends(get_geometry),
):
    """
    Returns soil tile layer for frontend visualization.
    """

    return get_soil_tiles(
        geometry=geometry,
        parameter=parameter,
        depth=depth,
    )