from fastapi import APIRouter, Depends, Query
import ee

from app.api.deps import get_geometry
from app.services.gee.temperature_tiles import get_temperature_tiles

router = APIRouter(
    prefix="/temperature/tiles",
    tags=["Temperature Raster"]
)


@router.post("")
def temperature_tiles(
    geometry: ee.Geometry = Depends(get_geometry),
    start_date: str = Query(..., description="YYYY-MM-DD"),
    end_date: str = Query(..., description="YYYY-MM-DD")
):
    tiles = get_temperature_tiles(
        geometry=geometry,
        start_date=start_date,
        end_date=end_date
    )

    return {
        "status": "success",
        "dataset": "ERA5-Land",
        "units": "°C",
        **tiles
    }
