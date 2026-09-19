from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_v1_router
from app.core.config import settings
from app.services.health_service import HealthService


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup and shutdown lifespan management."""
    yield


app = FastAPI(
    title="AI Engineering Assistant - AI Service",
    description="Backend service for prompt transformation and engineering agents",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS configuration for desktop application
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root-level health check endpoint
@app.get("/health", tags=["Health"])
async def root_health():
    """Root health check endpoint."""
    return HealthService.get_health()


# Versioned API routes
app.include_router(api_v1_router)
