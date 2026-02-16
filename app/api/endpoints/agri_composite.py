# app/api/endpoints/agri_composite.py
from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import Dict, Any
import ee

from app.services.gee.agri_composite import build_agri_composite

router = APIRouter(
    tags=["Agri Composite"]
)


class AgriCompositeRequest(BaseModel):
    geometry: Dict[str, Any] = Field(
        ...,
        description="GeoJSON Polygon geometry"
    )
    start_date: str = Field(
        ...,
        description="Start date in YYYY-MM-DD format"
    )
    end_date: str = Field(
        ...,
        description="End date in YYYY-MM-DD format"
    )
    depth: str = Field(
        default="0-20cm",
        description="Soil depth (0-20cm or 20-50cm)"
    )


@router.post("/agri/composite")
def agri_composite(request: AgriCompositeRequest):
    """
    Returns:
    - Soil Fertility Index heatmap
    - Climate-integrated Maize Suitability Index heatmap
    - Soil Health Composite Index heatmap
    """

    try:
        ee_geometry = ee.Geometry(request.geometry)

        result = build_agri_composite(
            geometry=ee_geometry,
            depth=request.depth,
            start_date=request.start_date,
            end_date=request.end_date,
        )

        return result

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }