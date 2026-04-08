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


# Serve static frontend files
FRONTEND_DIR = Path(__file__).resolve().parent.parent.parent / "public"

@app.get("/{path:path}")
async def serve_static_or_index(path: str):
    file_path = FRONTEND_DIR / path
    if path != "" and file_path.exists() and file_path.is_file():
        return FileResponse(file_path)
    
    index_path = FRONTEND_DIR / "index.html"
    if index_path.exists():
        return FileResponse(index_path)
        
    return {"message": "Frontend not found. Use /docs for API documentation."}
