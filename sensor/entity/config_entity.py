from datetime import datetime
import os
from time import time
from sensor.constant import training_pipeline

class TrainingPipelineConfig:
    """
    Training Pipeline configuration option
    """

    def __init__(self,timestamp=datetime.now(), pipeline_name=training_pipeline.PIPELINE_NAME):
        timestamp = timestamp.strftime("%m_%d_%Y_%H_%M_%S")
        self.pipeline_name=pipeline_name
        # create dir with current timestamp inside ARTIFACT_DIR 
        self.artifact_dir:str=os.path.join(training_pipeline.ARTIFACT_DIR, timestamp)
        self.timestamp = timestamp

    
class DataIngestionConfig:
    """
    DataIngestion Configuration
    central place to control Data Ingestion workflow management
    
    """
    def __init__(self, training_pipeline_config:TrainingPipelineConfig) -> None:
        self.data_ingestion_dir:str = os.path.join(
            training_pipeline_config.artifact_dir, training_pipeline.DATA_INGESTION_DIR_NAME
        )

        self.feature_store_file_path:str = os.path.join(
            self.data_ingestion_dir,
            training_pipeline.DATA_INGESTION_FEATUER_STORE_DIR,
            training_pipeline.FILE_NAME
        )

        self.training_file_path:str= os.path.join(
            self.data_ingestion_dir,
            training_pipeline.DATA_INGESTION_INGESTED_DIR,
            training_pipeline.TRAIN_FILE_NAME
        )

        self.testing_file_path:str= os.path.join(
            self.data_ingestion_dir,
            training_pipeline.DATA_INGESTION_INGESTED_DIR,
            training_pipeline.TEST_FILE_NAME
        )

        self.train_test_split_ratio:float =training_pipeline.DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO
        self.collection_name:str=training_pipeline.DATA_INGESTION_COLLECTION_NAME

    

