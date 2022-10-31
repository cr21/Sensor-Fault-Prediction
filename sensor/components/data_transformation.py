import os, sys
from sensor.exception import SensorException
from sensor.logger import logging
from sensor.constant import training_pipeline
from sensor.entity.config_entity import DataTransformationConfig
from sensor.entity.artifact_entity import DataValidationArtifact
from datetime import datetime
import pandas as pd
from sensor.utils.main_utils import read_yaml_file, write_yaml_file, save_numpy_array_data, save_object



class DataTransformation:

    def __init__(self,data_transforme_config:DataTransformationConfig, data_validation_artifact:DataValidationArtifact ) -> None:
        self.data_transforme_config = data_transforme_config
        self.data_validation_artifact = data_validation_artifact

    def initiate_data_transformation(self):
        pass

