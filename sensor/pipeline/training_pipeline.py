import imp
import os,sys
from sensor.logger import logging
from sensor.exception import SensorException
from sensor.entity.config_entity import TrainingPipelineConfig, DataIngestionConfig
from sensor.entity.artifact_entity import DataIngestionArtifact
from sensor.components.data_ingestion import DataIngestion
class TrainPipeline:
    def __init__(self, train_pipeline_config:TrainingPipelineConfig) -> None:
        self.train_pipeline_config= TrainingPipelineConfig()
    

    def start_data_ingestion(self)->DataIngestionArtifact:
        try:
            self.data_ingestion_config = DataIngestionConfig(self.train_pipeline_config)
            logging.info("Starting Data Ingestion Stage:")
            data_ingestion = DataIngestion(self.data_ingestion_config)
            data_ingestion_artifact=data_ingestion.initiate_date_ingestion()
            logging.info("Finished Data Ingestion, DataIngestion Artifact generated")
            return data_ingestion_artifact
        except Exception as exp:
            raise SensorException(exp)  

    def start_data_validaton(self):
        try:
            pass
        except  Exception as e:
            raise  SensorException(e,sys)

    def start_data_transformation(self):
        try:
            pass
        except  Exception as e:
            raise  SensorException(e,sys)
    
    def start_model_trainer(self):
        try:
            pass
        except  Exception as e:
            raise  SensorException(e,sys)

    def start_model_evaluation(self):
        try:
            pass
        except  Exception as e:
            raise  SensorException(e,sys)

    def start_model_pusher(self):
        try:
            pass
        except  Exception as e:
            raise  SensorException(e,sys)

    def run_pipeline(self):
        try:
            data_ingested_artifact:DataIngestionArtifact=self.start_data_ingestion()
        except  Exception as e:
            raise  SensorException(e,sys)