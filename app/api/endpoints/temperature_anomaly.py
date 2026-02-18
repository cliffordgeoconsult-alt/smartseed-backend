# app/api/endpoints/temperature_anomaly.py
# This module defines the API endpoint for the temperature anomaly dashboard, which provides an overview of current seasonal temperatures, anomalies, trends, and agronomic interpretations based on ERA5-Land data.
from fastapi import APIRouter, Depends, Query
import ee

from app.api.deps import get_geometry
from app.services.gee.temperature_anomaly import (
    get_current_season_overview,
    get_temperature_seasonal_anomaly,
    get_10yr_temperature_trend,
    get_agronomic_interpretation
)

router = APIRouter(prefix="/temperature", tags=["Temperature"])


@router.post("/dashboard")
def temperature_dashboard(
    season: str = Query(..., description="MAM, JJA, SON, DJF"),
    year: int = Query(..., ge=1981),
    geometry: ee.Geometry = Depends(get_geometry)
):

    # Section A
    overview = get_current_season_overview(
        geometry=geometry,
        season=season,
        year=year
    )

    # Section B
    anomaly = get_temperature_seasonal_anomaly(
        geometry=geometry,
        season=season,
        year=year
    )

    # Section C
    trend = get_10yr_temperature_trend(
        geometry=geometry,
        season=season,
        year=year
    )

    # Section D
    agronomic = get_agronomic_interpretation(
        mean_temp_c=overview["mean_temp_c"],
        heat_days=overview["heat_stress_days_above_35C"]
    )

    return {
        "status": "success",
        "dataset": "ERA5-Land",
        "units": "°C",
        "section_a_overview": overview,
        "section_b_anomaly": anomaly,
        "section_c_trend": trend,
        "section_d_agronomic_interpretation": agronomic
    }