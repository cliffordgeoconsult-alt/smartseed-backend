from fastapi import APIRouter, Depends, Query
import ee
from app.api.deps import get_geometry
from app.services.gee.ndvi_anomaly import get_ndvi_anomaly

router = APIRouter(prefix="/ndvi", tags=["NDVI"])


@router.post("/anomaly")
def ndvi_anomaly(
    geometry: ee.Geometry = Depends(get_geometry),
    start_date: str = Query(...),
    end_date: str = Query(...)
):
    return get_ndvi_anomaly(geometry, start_date, end_date)