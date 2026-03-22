import json
import logging
import os
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from ml.pipeline.training_pipeline import TrainingPipeline

router = APIRouter()

@router.get("/train")
async def train():
    try:
        logging.info("Training pipeline started directly via the new Router architecture.")
        train_pipeline = TrainingPipeline()
        train_pipeline.run_pipeline()
        return JSONResponse(content={"status": "success", "message": "Training successful"})
    except Exception as e:
        logging.error(f"Error in training route: {e}")
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e)})

@router.get("/health")
async def health_check():
    return JSONResponse(content={"status": "success", "message": "API is online, ML architecture loaded securely."})

@router.get("/metrics")
async def get_metrics():
    try:
        metrics_path = "models/metrics.json"
        if not os.path.exists(metrics_path):
            return JSONResponse(content={"status": "not_trained"})
        with open(metrics_path, "r") as f:
            data = json.load(f)
        return JSONResponse(content={"status": "success", "data": data})
    except Exception as e:
        logging.error(f"Error reading metrics: {e}")
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e)})
