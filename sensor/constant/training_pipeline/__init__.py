import os
from sensor.constant.s3_bucket import TRAINING_BUCKET_NAME

#defining common constant variable for training pipeline

TARGET_COLUMN:str="class"
PIPELINE_NAME:str="sensor"
ARTIFACT_DIR:str="artifact"
FILE_NAME:str="sensor.csv"
TRAIN_FILE_NAME:str="train.csv"
TEST_FILE_NAME:str="test.csv"

PREPROCESSING_OBJECT_FILE_NAME:str="preprocessing.pkl"
MODEL_FILE_NAME:str="model.pkl"
SCHEMA_FILE_PATH:str=os.path.join("config","schema.yaml")
SCHEMA_DROP_COLUMNS:str = "drop_columns"

SAVED_MODEL_DIR =os.path.join("saved_models")

"""
Data Ingestion related constant starts here:
Prefix :  DATA_INGESTION 
"""

DATA_INGESTION_COLLECTION_NAME:str="sensor"
DATA_INGESTION_DIR_NAME:str="data_ingestion"
DATA_INGESTION_FEATUER_STORE_DIR:str="feature_store"
DATA_INGESTION_INGESTED_DIR:str="ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO:float=0.2



"""
Data Validation related constant starts here:
Prefix :  DATA_VALIDATION
"""

DATA_VALIDATION_DIR_NAME:str="data_validation"
DATA_VALIDATION_VALID_DIR:str="validated"
DATA_VALIDATION_INVALID_DIR:str="invalid"
DATA_VALIDATION_DRIFT_REPORT_DIR:str="drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME:str="report.yaml"





"""
Data Transformation related constant starts here:
Prefix :  DATA_TRANSFORMATION
"""

DATA_TRANSFORMATION_DIR_NAME:str="data_transformation"
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR:str="transformed"
DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR:str="transformed_object"


"""
Model Training  related constant starts here:
Prefix :  MODEL_TRAINER
"""
MODEL_TRAINER_DIR_NAME:str="model_trainer"
MODEL_TRAINER_TRAINED_MODEL_DIR:str="trainedModel"
MODEL_TRAINER_TRAINED_MODEL_NAME:str="model.pkl"
MODEL_TRAINER_TRAINED_MODEL_FILE_PATH:str="trainedModel"
MODEL_TRAINER_EXPECTED_ACCURACY=0.9
MODEL_TRAINER_OVERFIT_UNDERFIT_THRESHOLD=0.05
MODEL_TRAINER_MODEL_CONFIG_FILE_PATH="Model_Configuration"
MODEL_TRAINER_BEST_MODEL_DETAIL_FILE_PATH="best_model_detail.yaml"



"""
Model Evaluation  related constant starts here:
Prefix :  MODEL_EVALUATION
"""
MODEL_EVALUATION_CHANGE_THRESHOLD_SCORE:float=0.02
MODEL_EVALUATION_DIR_NAME:str="model_evaluation"
MODEL_EVALUATION_REPORT_FILE:str="model_evaluation_report.yaml"

"""
Model Pusher  related constant starts here:
Prefix :  MODEL_PUSHER
"""

MODEL_PUSHER_DIR_NAME:str="model_pusher"
MODEL_PUSHER_SAVED_MODEL_DIR:str=SAVED_MODEL_DIR


