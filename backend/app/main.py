from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from backend.app.config import settings
from backend.app.routers import copilot

app = FastAPI(
    title="AI Content Production Copilot API",
    description="Production-grade backend service orchestrating multi-agent story writing & audio generation pipelines.",
    version="1.0.0"
)

# Enable CORS for frontend interactions
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount the static directory to serve generated story markdown and audio MP3 files
# This makes file:///outputs/ audio/ and stories/ retrievable via http://localhost:8000/static/...
app.mount("/static", StaticFiles(directory=str(settings.OUTPUT_DIR)), name="static")

# Register api routers
app.include_router(copilot.router)

@app.get("/health")
def health_check():
    """
    Health check endpoint for container probes or monitoring services.
    """
    return {
        "status": "healthy",
        "service": "AI Content Production Copilot Backend"
    }
