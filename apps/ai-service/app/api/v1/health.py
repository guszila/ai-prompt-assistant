from fastapi import APIRouter
from app.services.health_service import HealthService

router = APIRouter(tags=["Health"])


@router.get("/health")
async def health_check():
    """Health check endpoint returning service status."""
    return HealthService.get_health()
