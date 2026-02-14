from fastapi import APIRouter, Depends
from app.api.deps import get_geometry
from app.services.gee.soil_tiles import get_soil_tiles
import ee

router = APIRouter()


@router.post("/soil/tiles")
def soil_tiles(
    dataset: str,
    depth: str = "0-20cm",
    geometry: ee.Geometry = Depends(get_geometry),
):
    return get_soil_tiles(
        geometry=geometry,
        dataset=dataset,
        depth=depth,
    )