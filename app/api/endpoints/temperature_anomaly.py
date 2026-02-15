# app/api/endpoints/temperature_anomaly.py
from fastapi import APIRouter, Depends, Query
import ee

from app.api.deps import get_geometry
from app.services.gee.temperature_anomaly import (
    get_temperature_seasonal_anomaly
)

router = APIRouter()


@router.post("/temperature/anomaly")
def temperature_anomaly(
    season: str = Query(..., description="MAM, JJA, SON, DJF"),
    year: int = Query(..., ge=1981),
    geometry: ee.Geometry = Depends(get_geometry)
):
    result = get_temperature_seasonal_anomaly(
        geometry=geometry,
        season=season,
        year=year
    )

    interpretation = (
        "Hotter than last year"
        if result["mean_temp_anomaly_c"] > 0
        else "Cooler than last year"
    )

    return {
        "status": "success",
        "dataset": "ERA5-Land",
        "units": "°C",
        "interpretation": interpretation,
        **result
    }
