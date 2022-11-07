import imp
import os,sys
from sensor.logger import logging
from sensor.exception import SensorException
from sensor.entity.config_entity import (
                                                TrainingPipelineConfig,
                                                DataIngestionConfig,
                                                DataValidationConfig,
                                                DataTransformationConfig,
                                                ModelTrainerConfig,
                                                ModelEvaluationConfig,
                                                ModelPusherConfig
                                )
from sensor.entity.artifact_entity import (
                                                DataIngestionArtifact,
                                                DataValidationArtifact,
                                                DataTransformationArtifact,
                                                ModelTrainerArtifact,
                                                ModelEvaluationArtifact,
                                                ModelPusherArtifact
                                            )
from sensor.components.data_ingestion import DataIngestion
from sensor.components.data_validation import DataValidation
from sensor.components.data_transformation import DataTransformation
from sensor.components.model_evaluation import ModelEvalution
from sensor.components.model_trainer import ModelTrainer
from sensor.components.model_pusher import ModelPusher
from sensor.cloud_storage.s3_syncer import s3Sync
from sensor.constant.s3_bucket import TRAINING_BUCKET_NAME
from sensor.constant.training_pipeline import SAVED_MODEL_DIR
class TrainPipeline:
    is_pipeline_running=False
    def __init__(self) -> None:
        self.train_pipeline_config= TrainingPipelineConfig()
        self.s3_sync = s3Sync()
    

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
            data_transformer  = DataTransformation(
                                                    data_transformation_config=data_transformation_config,
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

    def start_model_evaluation(self, model_trainer_artifact:ModelTrainerArtifact, data_validation_artifact:DataValidationArtifact)-> ModelEvaluationArtifact:
        try:
            model_evaluation_config = ModelEvaluationConfig(training_pipeline_config=self.train_pipeline_config)
            model_evaluation_component:ModelEvalution = ModelEvalution(
                                                                        model_evaluation_config=model_evaluation_config,
                                                                        model_trainer_artifact=model_trainer_artifact,
                                                                        data_validation_artifact=data_validation_artifact
                                                                    )
                    
            model_eval_artifact:ModelEvaluationArtifact= model_evaluation_component.initiate_model_evaluation(model_trainer_artifact)
            return model_eval_artifact
        except  Exception as e:
            raise  SensorException(e,sys)

    def start_model_pusher(self,model_evaluation_artifact:ModelEvaluationArtifact)->ModelPusherArtifact:
        try:
            model_pusher_config = ModelPusherConfig(
                training_pipeline_config=self.train_pipeline_config
            )
            model_pusher_component = ModelPusher(   
                                                    model_pusher_config=model_pusher_config,
                                                    model_eval_artifact=model_evaluation_artifact
                                                )

            model_pusher_artifact:ModelPusherArtifact= model_pusher_component.initiate_model_pusher()
            return model_pusher_artifact

        except  Exception as e:
            raise  SensorException(e,sys)

    def sync_artifact_dir_to_s3(self):
        try:
            aws_buket_url = f"s3://{TRAINING_BUCKET_NAME}/artifact/{self.train_pipeline_config.timestamp}"
            print(aws_buket_url)
            self.s3_sync.sync_folder_to_s3(folder = self.train_pipeline_config.artifact_dir,aws_bucket_url=aws_buket_url)
        except Exception as exp:
            raise SensorException(exp)

    def sync_saved_model_dir_to_s3(self):
        try:
            aws_buket_url = f"s3://{TRAINING_BUCKET_NAME}/{SAVED_MODEL_DIR}"
            self.s3_sync.sync_folder_to_s3(folder = SAVED_MODEL_DIR,aws_bucket_url=aws_buket_url)
        except Exception as e:
            raise SensorException(e,sys)


    def run_pipeline(self)->None:
        try:
            TrainPipeline.is_pipeline_running=True
            data_ingested_artifact:DataIngestionArtifact=self.start_data_ingestion()
            data_validation_artifact=self.start_data_validaton(data_ingestion_artifact=data_ingested_artifact)
            data_transformation_artifact=self.start_data_transformation(data_validation_artifact)
            # logging.info("Data Validation Artifact : {data_validation_artifact}")

            # logging.info("Data Transformation Artifact : {data_transformation_artifact}")

            
            model_trainer_artifact=self.start_model_trainer(data_transformation_artifact)
            logging.info(f"Model training Artifact generate : {model_trainer_artifact}")
            model_eval_artifact:ModelEvaluationArtifact = self.start_model_evaluation(model_trainer_artifact, data_validation_artifact)
            if not model_eval_artifact.is_model_accepted:
                raise Exception("currently trained Model is not better than the best model")
            model_pusher_artifact:ModelPusherArtifact = self.start_model_pusher(model_evaluation_artifact=model_eval_artifact)      
            TrainPipeline.is_pipeline_running=False
            self.sync_artifact_dir_to_s3()
            self.sync_saved_model_dir_to_s3()
        except  Exception as e:
            self.sync_artifact_dir_to_s3()
            TrainPipeline.is_pipeline_running=False
            raise  SensorException(e)