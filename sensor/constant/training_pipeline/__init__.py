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


"""
Data Ingestion related constant starts here:
Prefix :  DATA_INGESTION 
"""

DATA_INGESTION_COLLECTION_NAME:str="sensor"
DATA_INGESTION_DIR_NAME:str="data_ingestion"
DATA_INGESTION_FEATUER_STORE_DIR:str="feature_store"
DATA_INGESTION_INGESTED_DIR:str="ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO:float=0.2

