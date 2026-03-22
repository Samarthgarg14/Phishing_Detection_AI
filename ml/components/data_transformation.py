import sys
import os
import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline

from ml.constants.training_pipeline import TARGAT_COLUMN
from ml.constants.training_pipeline import DATA_TRANSFORMATION_IMPUTER_PARAMS
from ml.entity.artifact import DataTransformationArtifact, DataValidationArtifact

from ml.exception.exception import NetworkSecurityException
from ml.logging.logger import logging
from ml.entity.data_transformation_config import DataTransformationConfig
from ml.utils.main_utils.utils import save_numpy_array_data, load_numpy_array_data, save_object, load_object


class DataTransformation:
    def __init__(self,data_validation_artifact:DataValidationArtifact,data_transformation_config:DataTransformationConfig):
        try:
            self.data_validation_artifact = data_validation_artifact
            self.data_transformation_config = data_transformation_config

        except Exception as e:
            raise NetworkSecurityException(e, sys)    
        
    def get_data_transformation_pipeline(self) -> Pipeline:
        try:
            logging.info("Creating data transformation pipeline")
            imputer:KNNImputer = KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            logging.info("KNN Imputer initialized")
            processor:Pipeline=Pipeline([("imputer",imputer)])
            return processor

        except Exception as e:
            raise NetworkSecurityException(e,sys)    

    def initiate_data_transformation(self) -> DataTransformationArtifact:
        logging.info("Initiating data transformation process")
        try:
            logging.info("Starting data transformation process")
            train_df = pd.read_csv(self.data_validation_artifact.valid_train_file_path)
            test_df = pd.read_csv(self.data_validation_artifact.valid_test_file_path)
            logging.info("Data loaded successfully for transformation")
            input_feature_train=train_df.drop(columns=[TARGAT_COLUMN], axis=1)
            target_feature_train=train_df[TARGAT_COLUMN]
            target_feature_train=target_feature_train.replace(-1,0)

            input_feature_test=test_df.drop(columns=[TARGAT_COLUMN], axis=1)
            target_feature_test=test_df[TARGAT_COLUMN]
            target_feature_test=target_feature_test.replace(-1,0)   

            preprocessor=self.get_data_transformation_pipeline()
            preprocessor_object=preprocessor.fit(input_feature_train)
            tranformed_input_train_feature=preprocessor_object.transform(input_feature_train)
            tranformed_input_test_feature=preprocessor_object.transform(input_feature_test)

            train_arr=np.c_[tranformed_input_train_feature,np.array(target_feature_train)]
            test_arr=np.c_[tranformed_input_test_feature,np.array(target_feature_test)]
            
            save_numpy_array_data(self.data_transformation_config.transformed_train_file_path,array=train_arr)
            save_numpy_array_data(self.data_transformation_config.transformed_test_file_path,array=test_arr)
            save_object(self.data_transformation_config.transformed_object_file_path,preprocessor_object)
            save_object("models/preprocessor.pkl",preprocessor_object)


            data_transformation_artifact=DataTransformationArtifact(
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path
            )
            return data_transformation_artifact
   

        except Exception as e:
            raise NetworkSecurityException(e, sys)        



