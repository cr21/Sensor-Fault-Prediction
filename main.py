from sensor.configuration.mongo_db_connection import MongoDBConnector
from sensor.constant.database import DATABASE_NAME
from sensor.exception import SensorException
from sensor.logger import logging
import os, sys
from sensor.entity.config_entity import TrainingPipelineConfig
from sensor.pipeline.training_pipeline import TrainPipeline
if __name__ == '__main__':
    try:
        train_pipeline_config=TrainingPipelineConfig()
        train_pipeline=TrainPipeline(train_pipeline_config)
        train_pipeline.run_pipeline()
        
        
    except Exception as e:
        raise SensorException(e)
