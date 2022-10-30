import imp
import os,sys
from sensor.logger import logging
from sensor.exception import SensorException
from sensor.entity.config_entity import TrainingPipelineConfig, DataIngestionConfig, DataValidationConfig
from sensor.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from sensor.components.data_ingestion import DataIngestion
from sensor.components.data_validation import DataValidation
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

    def start_data_validaton(self,data_ingestion_artifact:DataIngestionArtifact):
        try:
            data_validation_config=DataValidationConfig(training_pipeline_config=self.train_pipeline_config)
            data_valiadtor= DataValidation(
                                            data_validation_config=data_validation_config, 
                                            data_ingestion_artifact=data_ingestion_artifact
                                        )
            data_validation_artifact:DataValidationArtifact= data_valiadtor.initiate_data_validation_steps()
            return data_validation_artifact
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
            data_validation_artifact=self.start_data_validaton(data_ingestion_artifact=data_ingested_artifact)
            
        except  Exception as e:
            raise  SensorException(e,sys)