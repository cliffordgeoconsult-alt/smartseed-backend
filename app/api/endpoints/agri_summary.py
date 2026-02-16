# app/api/endpoints/agri_summary.py
from fastapi import APIRouter
from pydantic import BaseModel
import ee

from app.services.gee.agri_summary import build_agri_summary

router = APIRouter(tags=["Agri Summary"])

class AgriSummaryRequest(BaseModel):
    geometry: dict
    start_date: str
    end_date: str
    depth: str = "0-20cm"

@router.post("/agri/summary")
def agri_summary(request: AgriSummaryRequest):

    ee_geometry = ee.Geometry(request.geometry)

    return build_agri_summary(
        ee_geometry,
        request.depth,
        request.start_date,
        request.end_date,
    )