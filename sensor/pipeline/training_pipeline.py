import imp
import os,sys
from sensor.logger import logging
from sensor.exception import SensorException
from sensor.entity.config_entity import (
                                                TrainingPipelineConfig,
                                                DataIngestionConfig,
                                                DataValidationConfig,
                                                DataTransformationConfig,
                                                ModelTrainerConfig
                                )
from sensor.entity.artifact_entity import (
                                                DataIngestionArtifact,
                                                DataValidationArtifact,
                                                DataTransformationArtifact,
                                                ModelTrainerArtifact
                                            )
from sensor.components.data_ingestion import DataIngestion
from sensor.components.data_validation import DataValidation
from sensor.components.data_transformation import DataTransformation
from sensor.components.model_trainer import ModelTrainer
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

    def start_data_transformation(self, data_validation_artifact:DataValidationArtifact):
        try:
            data_transformation_config = DataTransformationConfig(training_pipeline_config=self.train_pipeline_config)
            data_transformer  = DataTransformation(data_transformation_config=data_transformation_config,
                                                    data_validation_artifact=data_validation_artifact
                                                )
            data_transfomation_artifact:DataTransformationArtifact=data_transformer.initate_data_transformation()
            return data_transfomation_artifact
        except  Exception as e:
            raise  SensorException(e,sys)
    
    def start_model_trainer(self,data_transformation_artifact:DataTransformationArtifact):
        try:
            model_trainer_config =ModelTrainerConfig(training_pipeline_config=self.train_pipeline_config) 
            model_trainer=ModelTrainer(model_trainer_config, data_transformation_artifact)
            model_trainer_artifact:ModelTrainerArtifact=model_trainer.initiate_model_training()
            return model_trainer_artifact
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
            data_transformation_artifact=self.start_data_transformation(data_validation_artifact)
            # print(data_transformation_artifact.transformed_train_file_path, data_transformation_artifact.transformed_test_file_path,data_transformation_artifact.transformed_object_file_path)
            # data_transformation_artifact = DataTransformationArtifact("artifact/11_04_2022_21_45_11/data_transformation/transformed_object/preprocessing.pkl",
            # "artifact/11_04_2022_21_45_11/data_transformation/transformed/train.npy",
            # "artifact/11_04_2022_21_45_11/data_transformation/transformed/test.npy"
            # )
            model_trainer_artifact=self.start_model_trainer(data_transformation_artifact)
        except  Exception as e:
            raise  SensorException(e,sys)