from ml.entity.data_validation_entity import DataValidationConfig
from ml.entity.artifact import DataValidationArtifact,DataIngestionArtifact
from ml.exception.exception import NetworkSecurityException    
from ml.logging.logger import logging
from ml.constants.training_pipeline import SCHEMA_FILE_PATH
import os
import sys
import pandas as pd
from scipy.stats import ks_2samp
from ml.utils.main_utils.utils import read_yaml_file,write_yaml_file

class NetworkDataValidation:
    def __init__(self, data_validation_config: DataValidationConfig, data_ingestion_artifact: DataIngestionArtifact):
        try:
            self.data_validation_config = data_validation_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self.schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        

    def validateColumns(self, df: pd.DataFrame) -> bool:

        try:
            expected_columns = [list(i.keys())[0] for i in self.schema_config['columns']]

            actual_columns = df.columns.to_list()
            if set(expected_columns) == set(actual_columns):
                logging.info("Columns validation passed.")
                return True
            else:
                logging.error(f"Columns validation failed. Expected: {expected_columns}, Actual: {actual_columns}")
                return False
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def isNumericalColumnExist(self, df: pd.DataFrame) -> bool:
        try:
            numerical_columns = df.select_dtypes(include=['int64']).columns.tolist()
            if numerical_columns:
                logging.info(f"Numerical columns found")
                return True
            else:
                return False
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def validateDataDrift(self, base_df,current_df,threshhold=0.05) -> bool: 
        try:
            status = True
            drift_report = {}
            for column in base_df.columns:
                d1=base_df[column]
                d2=current_df[column]
                is_same_dist=ks_2samp(d1,d2)
                status=True
                if(threshhold < is_same_dist.pvalue):
                    is_found= False
                else:
                    is_found = True
                    status = False
                drift_report.update({column: {
                    "p_value": float(is_same_dist.pvalue),
                    "is_found": is_found
                }})
            drift_report_file_path = self.data_validation_config.drift_report_file_path
            os.makedirs(os.path.dirname(drift_report_file_path), exist_ok=True)
            write_yaml_file(drift_report_file_path, drift_report)
            return status



        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def initiate_validate_data(self) -> DataValidationArtifact:
        try:
            train_file_path= self.data_ingestion_artifact.train_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path
            train_df = pd.read_csv(train_file_path)
            test_df = pd.read_csv(test_file_path)
            logging.info("Data loaded successfully for validation.")
            is_train_valid = self.validateColumns(train_df)
            is_test_valid = self.validateColumns(test_df)
            is_train_numerical_valid = self.isNumericalColumnExist(train_df)
            is_test_numerical_valid = self.isNumericalColumnExist(test_df)
            is_data_drift_valid = self.validateDataDrift(train_df, test_df)
            #print(is_train_valid, is_test_valid, is_train_numerical_valid, is_test_numerical_valid, is_data_drift_valid)
            validation_status = is_train_valid and is_test_valid and is_train_numerical_valid and is_test_numerical_valid and is_data_drift_valid
            if validation_status:
                logging.info("Data validation passed successfully.")
                dir_path=os.path.dirname(self.data_validation_config.valid_train_file_path)
                os.makedirs(dir_path, exist_ok=True)
                train_df.to_csv(self.data_validation_config.valid_train_file_path, index=False,header=True)
                dir_path=os.path.dirname(self.data_validation_config.valid_test_file_path)
                os.makedirs(dir_path, exist_ok=True) 
                test_df.to_csv(self.data_validation_config.valid_test_file_path, index=False,header=True)
            
            data_validation_artifact = DataValidationArtifact(
                validationStatus=validation_status,
                valid_train_file_path=self.data_validation_config.valid_train_file_path,
                valid_test_file_path=self.data_validation_config.valid_test_file_path,
                invalid_train_file_path=self.data_validation_config.invalid_train_file_path,
                invalid_test_file_path=self.data_validation_config.invalid_test_file_path,
                drift_report_file_path=self.data_validation_config.drift_report_file_path
            )
            return data_validation_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)

