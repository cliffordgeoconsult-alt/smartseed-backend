from fastapi import APIRouter, Depends, Query
import ee

from app.api.deps import get_geometry
from app.services.gee.rainfall import compute_rainfall

router = APIRouter(
    prefix="/rainfall",
    tags=["Rainfall"]
)


@router.post("/analyze")
def rainfall_analysis(
    geometry: ee.Geometry = Depends(get_geometry),
    start_date: str = Query(..., description="YYYY-MM-DD"),
    end_date: str = Query(..., description="YYYY-MM-DD")
):
    """
    Compute rainfall for county / ward / farm / point
    """

    rainfall = compute_rainfall(
        geometry=geometry,
        start_date=start_date,
        end_date=end_date
    )

    return {
        "status": "success",
        "rainfall": rainfall,
        "units": "mm",
        "dataset": "CHIRPS"
    }
