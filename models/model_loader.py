import logging
import sys
from ml.utils.main_utils.utils import load_object
from ml.utils.ml_utils.model.estimator import NetworkModel
from ml.exception.exception import NetworkSecurityException
from app.core.config import Config

class ModelLoader:
    _instance = None
    _network_model = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    @classmethod
    def get_model(cls) -> NetworkModel:
        """Returns a cached singleton of the ML model loaded into memory."""
        if cls._network_model is None:
            try:
                logging.info("Loading models into memory cache...")
                preprocessor = load_object(Config.PREPROCESSOR_FILE)
                final_model = load_object(Config.MODEL_FILE)
                cls._network_model = NetworkModel(preprocessor=preprocessor, model=final_model)
                logging.info("Models loaded successfully!")
            except Exception as e:
                logging.error(f"Error loading models: {e}")
                raise NetworkSecurityException(e, sys)
        return cls._network_model

    @classmethod
    def clear_cache(cls):
        """Forces the models to be purged from memory and disk on page refresh."""
        cls._network_model = None
        import os
        if os.path.exists(Config.MODEL_FILE):
            os.remove(Config.MODEL_FILE)
        if os.path.exists(Config.PREPROCESSOR_FILE):
            os.remove(Config.PREPROCESSOR_FILE)
        logging.info("Model cache and disk files have been cleared.")
