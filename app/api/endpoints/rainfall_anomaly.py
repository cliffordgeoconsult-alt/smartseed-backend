from fastapi import APIRouter, Depends, Query
import ee

from app.api.deps import get_geometry
from app.services.gee.rainfall_anomaly import get_seasonal_anomaly

router = APIRouter(prefix="/rainfall", tags=["Rainfall"])

@router.post("/anomaly")
def rainfall_anomaly(
    geometry: ee.Geometry = Depends(get_geometry),
    year: int = Query(..., ge=1981),
    season: str = Query(..., description="long_rains or short_rains")
):

    result = get_seasonal_anomaly(
        geometry=geometry,
        year=year,
        season=season
    )

    return {
        "status": "success",
        "dataset": "CHIRPS",
        "units": "mm",
        **result
    }
