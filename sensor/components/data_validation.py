import os, sys
from sensor.exception import SensorException
from sensor.logger import logging
from sensor.constant import training_pipeline
from sensor.entity.config_entity import DataValidationConfig
from sensor.entity.artifact_entity import DataValidationArtifact, DataIngestionArtifact
from datetime import datetime
import pandas as pd
from sensor.utils.main_utils import read_yaml_file, write_yaml_file
from scipy.stats import ks_2samp


class DataValidation:

    def __init__(self, data_validation_config:DataValidationConfig, data_ingestion_artifact:DataIngestionArtifact) -> None:
        try:
            self.data_validation_config = data_validation_config
            self.data_ingestion_artifact= data_ingestion_artifact
            self._schema_config=read_yaml_file(training_pipeline.SCHEMA_FILE_PATH)
        except Exception as exp:
            raise SensorException(exp)


    @staticmethod
    def read_data(csv_file_path:str)->pd.DataFrame:
        try:
            # don't do this if file is very large, read in chunk
            return pd.read_csv(csv_file_path)
        except Exception as exp:
            raise SensorException(exp)

    def validate_no_of_columns(self, dataframe:pd.DataFrame)->bool: 
        """
        Total no of columns should be same in schema file and dataframe
        """
        try:
            columns = self._schema_config["columns"]
            logging.info(f"Required number of columns: {len(columns)}")
            logging.info(f"Data frame has columns: {len(dataframe.columns)}")
            return len(dataframe.columns)==len(columns)
        except Exception as exp:
            raise SensorException(exp)

    def is_numerical_columns_exists(self, dataframe:pd.DataFrame)->bool:
        """
        All the numerical columns in schema file should be present in dataframe columns
        """
        try:
            numerical_columns_in_schema = self._schema_config["numerical_columns"]
            dataframe_columns=set(dataframe.columns)
            numerical_column_present = True
            missing_numerical_columns = []
            for num_col in numerical_columns_in_schema:
                if num_col not in dataframe_columns:
                    numerical_column_present= False
                    missing_numerical_columns.append(num_col)

            logging.info(f"Missing numerical columns: [{missing_numerical_columns}]")
            return numerical_column_present

        except Exception as exp:
            raise SensorException(exp)


    def detect_data_drift(self, base_df:pd.DataFrame, current_df:pd.DataFrame,threshold=0.05)->bool:
        """
            compare Test DataFrame and Train DataFrame statistics and check
            Divergence for columns, and report any data drift statistics

            @param base_df: pd.DataFrame = Base DataFrame
            @param current_df : pd.DataFrame = Target DataFram
            @param threshold: float = Test statistic significant level (alpha) default => 0.05 ( 5 %)

            Returns : boolean
        """
        try:
            
            status=True
            report={}

            for column in base_df.columns:
                base_col = base_df[column]
                current_col = current_df[column]
                is_same_dist = ks_2samp(base_col, current_col)

                if threshold<=is_same_dist.pvalue:
                    is_found=False
                else:
                    is_found = True 
                    status=False
                report.update({column:{
                    "p_value":float(is_same_dist.pvalue),
                    "drift_status":is_found
                    }})

            drift_report_file_path = self.data_validation_config.drift_report_file_path

            #Create directory
            dir_path = os.path.dirname(drift_report_file_path)
            os.makedirs(dir_path,exist_ok=True)
            write_yaml_file(file_path=drift_report_file_path,content=report)
            return status
        except Exception as exp:
            raise SensorException(exp)


    def initiate_data_validation_steps(self)-> DataValidationArtifact:
        """
        Call Each Data Validation Predicate functions to step through data validation process
        """
        try:
            error_message = ""
            # reading data from Data Ingestion Artifacts 
            train_file_path = self.data_ingestion_artifact.trained_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            
            train_data_frame = DataValidation.read_data(train_file_path)
            test_data_frame=DataValidation.read_data(test_file_path)

            # validation for if No of columns should match
            status = self.validate_no_of_columns(dataframe=train_data_frame)
            if not status:
                error_message=f"{error_message}Train dataframe does not contain all columns.\n"
            status = self.validate_no_of_columns(dataframe=test_data_frame)
            if not status:
                error_message=f"{error_message}Test dataframe does not contain all columns.\n"

            # validate Numerical columns

            status = self.is_numerical_columns_exists(dataframe=train_data_frame)
            if not status:
                error_message=f"{error_message}Train dataframe does not contain all numerical columns columns.\n"
            status = self.is_numerical_columns_exists(dataframe=test_data_frame)
            if not status:
                error_message=f"{error_message}Test dataframe does not contain all numerical columns columns.\n"
            print(error_message)
            print("*"*30)
            if len(error_message)>0:
                raise Exception(error_message)

            # if validation is approved by all steps
            # check data drift

            status = self.detect_data_drift(base_df=train_data_frame, current_df=test_data_frame)

            data_validation_artifact = DataValidationArtifact(
                validation_status=status,
                valid_train_file_path=self.data_ingestion_artifact.trained_file_path,
                valid_test_file_path=self.data_ingestion_artifact.test_file_path,
                invalid_train_file_path=None,
                invalid_test_file_path=None,
                drift_report_file_path=self.data_validation_config.drift_report_file_path,
            )

            logging.info(f"Data validation artifact: {data_validation_artifact}")

            return data_validation_artifact

            
        except Exception as exp:
            raise SensorException(exp)


