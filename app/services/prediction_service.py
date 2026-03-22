import pandas as pd
from models.model_loader import ModelLoader

def predict_single_url(features: dict) -> int:
    """Consumes a feature dictionary, requests the cached Model Singleton, and outputs classification."""
    df = pd.DataFrame([features])
    network_model = ModelLoader.get_model()
    y_pred = network_model.predict(df)[0]
    return y_pred

def predict_batch(df: pd.DataFrame) -> list:
    """Scores an entire uploaded CSV DataFrame and returns predictions."""
    network_model = ModelLoader.get_model()
    y_pred = network_model.predict(df)
    return y_pred
