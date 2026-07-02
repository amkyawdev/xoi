"""Health check routes"""

from fastapi import APIRouter

from api.schemas import HealthResponse


router = APIRouter()


@router.get("", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Basic health check"""
    return HealthResponse(
        status="healthy",
        version="0.1.0"
    )


@router.get("/ready")
async def readiness_check() -> dict:
    """Readiness check"""
    return {"ready": True}


@router.get("/live")
async def liveness_check() -> dict:
    """Liveness check"""
    return {"alive": True}
