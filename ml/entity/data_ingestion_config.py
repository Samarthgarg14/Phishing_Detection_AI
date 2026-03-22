from datetime import datetime
import os

from ml.constants import training_pipeline


class TrainingPipelineConfig:
    def __init__(self):
        self.pipeline_name = training_pipeline.PIPELINE_NAME
        self.artifact_name = training_pipeline.ARTIFACT_DIR
        self.timestamp = datetime.now().strftime("%m_%d_%Y_%H_%M_%S")
        self.artifact_dir_path = os.path.join(self.artifact_name, self.timestamp)
        self.model_dir = os.path.join("models")


class DataIngestionConfig: 
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        self.data_ingestion_dir = os.path.join(training_pipeline_config.artifact_dir_path, training_pipeline.DATA_INGESTION_DIR_NAME)
        self.feature_store_dir = os.path.join(self.data_ingestion_dir, training_pipeline.DATA_INGESTION_FEATURE_STORE_DIR, training_pipeline.FILE_NAME)
        self.ingested_dir = os.path.join(self.data_ingestion_dir, training_pipeline.DATA_INGESTION_INGESTED_DIR)
        self.train_file_path = os.path.join(self.ingested_dir, training_pipeline.TRAIN_FILE_NAME)
        self.test_file_path = os.path.join(self.ingested_dir, training_pipeline.TEST_FILE_NAME)
        self.train_test_split_ratio = training_pipeline.DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO
        






