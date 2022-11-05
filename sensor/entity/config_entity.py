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

    


class DataValidationConfig:
    """
    DataValidation Configuration
    central place to control Data Validation workflow management
    
    """
    def __init__(self, training_pipeline_config:TrainingPipelineConfig) -> None:
        self.data_validation_dir:str=os.path.join(training_pipeline_config.artifact_dir, 
                training_pipeline.DATA_VALIDATION_DIR_NAME
        )
        self.valid_data_dir:str=os.path.join(self.data_validation_dir, training_pipeline.DATA_VALIDATION_VALID_DIR)
        self.invalid_data_dir:str=os.path.join(self.data_validation_dir, training_pipeline.DATA_VALIDATION_INVALID_DIR)
        self.valid_train_file_path: str=os.path.join(self.valid_data_dir, training_pipeline.TRAIN_FILE_NAME)
        self.valid_test_file_path: str=os.path.join(self.valid_data_dir, training_pipeline.TEST_FILE_NAME)
        self.invalid_train_file_path:str = os.path.join(self.invalid_data_dir, training_pipeline.TRAIN_FILE_NAME)
        self.invalid_test_file_path:str = os.path.join(self.invalid_data_dir, training_pipeline.TEST_FILE_NAME)
        self.drift_report_file_path: str = os.path.join(
            self.data_validation_dir,
            training_pipeline.DATA_VALIDATION_DRIFT_REPORT_DIR,
            training_pipeline.DATA_VALIDATION_DRIFT_REPORT_FILE_NAME,
        )


class DataTransformationConfig:
    """
    DataTransformation Configuration
    central place to control Data Transformatio workflow management
    
    """
    def __init__(self, training_pipeline_config:TrainingPipelineConfig, ) -> None:
        self.data_transformation_dir:str = os.path.join(training_pipeline_config.artifact_dir,
                                                    training_pipeline.DATA_TRANSFORMATION_DIR_NAME
                                                    )
        self.transformed_train_file_path:str = os.path.join(self.data_transformation_dir,
                                                        training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR,
                                                        training_pipeline.TRAIN_FILE_NAME.replace(".csv",".npy")
                                                    )
        self.transformed_test_file_path:str = os.path.join(self.data_transformation_dir,
                                                        training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR,
                                                        training_pipeline.TEST_FILE_NAME.replace(".csv",".npy")
                                                    )

        self.transformed_object_file_path:str=os.path.join(
                                                    self.data_transformation_dir,
                                                    training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR,
                                                    training_pipeline.PREPROCESSING_OBJECT_FILE_NAME
                                                    )


class ModelTrainerConfig:
    """
    Model Training Configuration
    central place to control Model training workflow management
    
    """
    def __init__(self, training_pipeline_config:TrainingPipelineConfig, ) -> None:
        
        self.model_trainer_dir:str=os.path.join(training_pipeline_config.artifact_dir,training_pipeline.MODEL_TRAINER_DIR_NAME)
        self.model_trained_file_path:str=os.path.join(
            self.model_trainer_dir, 
            training_pipeline.MODEL_TRAINER_TRAINED_MODEL_DIR,
            training_pipeline.MODEL_TRAINER_TRAINED_MODEL_NAME)
        self.model_expected_accuracy:float=training_pipeline.MODEL_TRAINER_EXPECTED_ACCURACY
        self.model_config_file_path:str=os.path.join(self.model_trainer_dir, training_pipeline.MODEL_TRAINER_MODEL_CONFIG_FILE_PATH)
        self.best_model_detail_file_path:str=os.path.join(self.model_trainer_dir,training_pipeline.MODEL_TRAINER_BEST_MODEL_DETAIL_FILE_PATH)
        self.model_overfit_underfit_threshold:str=training_pipeline.MODEL_TRAINER_OVERFIT_UNDERFIT_THRESHOLD



class ModelEvaluationConfig:

    def __init__(self,training_pipeline_config:TrainingPipelineConfig) -> None:
       
        self.model_eval_dir=os.path.join(training_pipeline_config.artifact_dir,
                                                training_pipeline.MODEL_EVALUATION_DIR_NAME
                                            )
            
        self.report_File_path = os.path.join(self.model_eval_dir, training_pipeline.MODEL_EVALUATION_REPORT_FILE)     
        self.eval_threshold = training_pipeline.MODEL_EVALUATION_CHANGE_THRESHOLD_SCORE



class ModelPusherConfig:

    def __init__(self, training_pipeline_config:TrainingPipelineConfig) -> None:
        self.model_pusher_saved_model_dir:str = os.path.join(training_pipeline_config.artifact_dir,training_pipeline.MODEL_PUSHER_DIR_NAME)
        self.model_file_path:str = os.path.join(self.model_eval_dir, training_pipeline.MODEL_FILE_NAME)
        timestamp = round(datetime.now().timestamp())
        self.saved_model_path=os.path.join(
            training_pipeline.SAVED_MODEL_DIR,
            f"{timestamp}",
            training_pipeline.MODEL_FILE_NAME)