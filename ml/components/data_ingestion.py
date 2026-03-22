from ml.exception.exception import NetworkSecurityException
from ml.logging.logger import logging
from ml.entity.data_ingestion_config import DataIngestionConfig

import os
import sys
import numpy as np
import pandas as pd
from typing import List
from sklearn.model_selection import train_test_split
from ml.entity.artifact import DataIngestionArtifact

class NetworkDataIngestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def fetch_data(self) -> pd.DataFrame:
        try:
            logging.info("Reading data from local CSV file")
            file_path = "data/raw/phisingData.csv"
            df = pd.read_csv(file_path)
            print(f"Fetched {len(df)} records from local CSV '{file_path}'")
            if('_id' in df.columns.to_list()):
                df.drop(columns=['_id'], axis=1,inplace=True)
            df.replace({"na": np.nan}, inplace=True)    
            return df
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def split_data(self, df: pd.DataFrame) -> List[pd.DataFrame]:
        try:
            train_df, test_df = train_test_split(df, test_size=self.data_ingestion_config.train_test_split_ratio, random_state=42)
            train_dir_path= os.path.dirname(self.data_ingestion_config.train_file_path)
            test_dir_path= os.path.dirname(self.data_ingestion_config.test_file_path)
            os.makedirs(train_dir_path, exist_ok=True)
            os.makedirs(test_dir_path, exist_ok=True)
            train_df.to_csv(self.data_ingestion_config.train_file_path, index=False, header=True)
            test_df.to_csv(self.data_ingestion_config.test_file_path, index=False, header=True)
            return [train_df, test_df]
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def save_featuredata_to_csv(self, df: pd.DataFrame):
        try:
            os.makedirs(os.path.dirname(self.data_ingestion_config.feature_store_dir), exist_ok=True)
            df.to_csv(self.data_ingestion_config.feature_store_dir, index=False,header=True)
            logging.info(f"Feature data saved to {self.data_ingestion_config.feature_store_dir}")
            return df
        except Exception as e:
            raise NetworkSecurityException(e, sys)  

    def initialize_data_ingestion(self):
        try:
            logging.info("Starting data ingestion process...")
            df = self.fetch_data()
            df=self.save_featuredata_to_csv(df)
            train_df, test_df = self.split_data(df)
            dataingestionartifact=DataIngestionArtifact(
                train_file_path=self.data_ingestion_config.train_file_path,
                test_file_path=self.data_ingestion_config.test_file_path
            )
            logging.info(f"Train and test data saved to {self.data_ingestion_config.train_file_path} and {self.data_ingestion_config.test_file_path}")

            return dataingestionartifact
        
        except Exception as e:
            raise NetworkSecurityException(e, sys)

