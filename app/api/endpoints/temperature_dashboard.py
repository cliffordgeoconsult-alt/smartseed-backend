# app/api/endpoints/temperature_dashboard.py
from fastapi import APIRouter, HTTPException
import ee

from app.services.gee.temperature_dashboard import (
    get_current_season_overview,
    get_seasonal_anomaly_30yr,
    get_10yr_temperature_trend,
    get_agronomic_interpretation
)

router = APIRouter(
    prefix="/temperature-dashboard",
    tags=["Temperature Dashboard"]
)

@router.post("/")
def temperature_dashboard(payload: dict):
    """
    SmartSeed Temperature Intelligence Dashboard Endpoint

    Sections:
    A - Current Season Overview
    B - 30-Year Seasonal Anomaly
    C - 10-Year Trend
    D - Agronomic Interpretation
    """

    try:
        geometry_geojson = payload.get("geometry")
        season = payload.get("season")
        year = payload.get("year")

        if not geometry_geojson or not season or not year:
            raise HTTPException(status_code=400, detail="geometry, season and year are required")

        geometry = ee.Geometry(geometry_geojson)

        overview = get_current_season_overview(
            geometry=geometry,
            season=season,
            year=year
        )

        anomaly = get_seasonal_anomaly_30yr(
            geometry=geometry,
            season=season,
            year=year
        )

        trend = get_10yr_temperature_trend(
            geometry=geometry,
            season=season,
            year=year
        )

        agronomic = get_agronomic_interpretation(
            mean_temp_c=overview["mean_temp_c"],
            heat_days=overview["heat_stress_days_above_35C"]
        )

        return {
            "section_a_overview": overview,
            "section_b_anomaly": anomaly,
            "section_c_trend": trend,
            "section_d_agronomic_interpretation": agronomic
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))