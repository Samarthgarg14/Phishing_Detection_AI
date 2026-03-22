import logging
import sys
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.core.config import Config
from app.api.v1.api_router import api_router
from ml.exception.exception import NetworkSecurityException
from models.model_loader import ModelLoader

app = FastAPI(title="Network Security ML API", description="Production-ready Phishing Detection Backend")

# Initialize Singleton Model immediately into RAM layer
try:
    ModelLoader.get_instance().get_model()
except Exception as e:
    logging.warning("Models not found or failed warm-up. They will load exactly once on pipeline completion.")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Core Backend Microservices routing versioned as v1
app.include_router(api_router, prefix="/api/v1")

# Frontend Static and View Serving
app.mount("/static", StaticFiles(directory=Config.FRONTEND_STATIC_DIR), name="static")
templates = Jinja2Templates(directory=Config.FRONTEND_TEMPLATE_DIR)

@app.get("/", tags=["Dashboard UI"])
async def index(request: Request):
    try:
        # Clear model to simulate 'fresh state' on each UI refresh
        ModelLoader.clear_cache()
        return templates.TemplateResponse("index.html", {"request": request})
    except Exception as e:
        logging.error(f"Error serving UI layout: {e}")
        raise NetworkSecurityException(e, sys)

if __name__ == "__main__":
    from uvicorn import run as app_run
    try:
        logging.info("Starting Modular FastAPI application")
        app_run("app.main:app", host="0.0.0.0", port=Config.PORT, log_level="info", reload=True)
    except Exception as e:
        logging.error(f"Error starting FastAPI application: {e}")
        raise NetworkSecurityException(e, sys)