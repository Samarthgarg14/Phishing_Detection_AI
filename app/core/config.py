import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    PORT = int(os.getenv("PORT", 8000))
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    MODEL_DIR = "models"
    PREPROCESSOR_FILE = os.path.join(MODEL_DIR, "preprocessor.pkl")
    MODEL_FILE = os.path.join(MODEL_DIR, "model.pkl")
    FRONTEND_STATIC_DIR = "frontend/static"
    FRONTEND_TEMPLATE_DIR = "frontend/templates"
