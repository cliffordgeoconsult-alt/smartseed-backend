# app/api/endpoints/soil_analysis.py

from fastapi import APIRouter, Body
import ee

from app.services.gee.soil_analysis import get_soil_analysis

router = APIRouter()


@router.post("/soil/analysis")
def soil_analysis(
    geometry: dict = Body(...),
    depth: str = "0-20cm",
):
    ee_geometry = ee.Geometry(geometry)
    return get_soil_analysis(ee_geometry, depth)