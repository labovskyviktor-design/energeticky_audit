"""
Energetický Audit a Certifikácia Budov — FastAPI Application Entry Point

Production-grade energy audit and building certification software
following Slovak Technical Standards (STN).
"""

from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.api.thermal import router as thermal_router
from app.api.energy import router as energy_router

app = FastAPI(
    title="Energetický Audit a Certifikácia Budov",
    description=(
        "Softvér na energetický audit a certifikáciu budov "
        "podľa slovenských technických noriem (STN). "
        "Praktická časť diplomovej práce."
    ),
    version="0.1.0",
)

# CORS — allow frontend dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API routers
app.include_router(thermal_router)
app.include_router(energy_router)

@app.get("/health")
async def health_check() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "ok", "service": "energy-audit-backend"}

@app.get("/")
async def root():
    """Root endpoint — on Vercel, static files from public/ are served automatically."""
    return {"message": "Energy Audit API is running. Use /docs for documentation."}
