from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from app.core.config import settings
from app.routers import documents, query, analysis

app = FastAPI(
    title="LegalLens AI",
    description="AI-powered contract intelligence platform with grounded, citation-backed Q&A.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(documents.router, prefix="/api/documents", tags=["documents"])
app.include_router(query.router, prefix="/api/query", tags=["query"])
app.include_router(analysis.router, prefix="/api/analysis", tags=["analysis"])


@app.get("/health")
def health_check():
    return {"status": "ok", "service": "legallens-ai-backend"}


# Serve the built frontend (if present) so a single container can host both
# the API and the UI — used for the combined Hugging Face Spaces deployment.
# API routes above are matched first, so this only catches everything else.
_frontend_dist = os.path.join(os.path.dirname(__file__), "..", "static")
if os.path.isdir(_frontend_dist):
    app.mount("/", StaticFiles(directory=_frontend_dist, html=True), name="frontend")
