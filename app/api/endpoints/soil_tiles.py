# app/api/endpoints/soil_tiles.py

from fastapi import APIRouter, Body
import ee

from app.services.gee.soil_tiles import get_soil_tile

router = APIRouter()


@router.post("/soil/tiles")
def soil_tiles(
    geometry: dict = Body(...),
    dataset: str = Body(...),   
    depth: str = "0-20cm",
):
    ee_geometry = ee.Geometry(geometry)
    return get_soil_tile(ee_geometry, dataset, depth)