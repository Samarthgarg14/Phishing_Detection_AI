from datetime import datetime
import os

from ml.constants import training_pipeline
from ml.entity.data_ingestion_config import TrainingPipelineConfig

class DataValidationConfig:
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        self.data_validation_dir = os.path.join(training_pipeline_config.artifact_dir_path, training_pipeline.DATA_VALIDATION_DIR_NAME)
        self.validated_dir = os.path.join(self.data_validation_dir, training_pipeline.DATA_VALIDATION_VALID_DIR)
        self.invalid_dir = os.path.join(self.data_validation_dir, training_pipeline.DATA_VALIDATION_INVALID_DIR)
        self.valid_train_file_path = os.path.join(self.validated_dir, training_pipeline.TRAIN_FILE_NAME)
        self.valid_test_file_path = os.path.join(self.validated_dir, training_pipeline.TEST_FILE_NAME)
        self.invalid_train_file_path = os.path.join(self.invalid_dir, training_pipeline.TRAIN_FILE_NAME)
        self.invalid_test_file_path = os.path.join(self.invalid_dir, training_pipeline.TEST_FILE_NAME)
        self.drift_report_dir = os.path.join(self.data_validation_dir, training_pipeline.DATA_VALIDATION_DRIFT_REPORT_DIR)
        self.drift_report_file_path = os.path.join(self.drift_report_dir, training_pipeline.DATA_VALIDATION_DRIFT_REPORT_FILE_NAME)