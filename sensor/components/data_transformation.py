from sensor.exception import SensorException
from sensor.logger import logging
from imblearn.combine import SMOTETomek
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import RobustScaler
from sklearn.pipeline import Pipeline
from sensor.constant import training_pipeline
from sensor.entity.config_entity import DataTransformationConfig
from sensor.entity.artifact_entity import DataValidationArtifact, DataTransformationArtifact
import pandas as pd
import numpy as np
from sensor.utils.main_utils import save_numpy_array_data, save_object
from sensor.ml.model.estimator import  TargetValueMapping

class DataTransformation:

    def __init__(self,data_transformation_config:DataTransformationConfig, data_validation_artifact:DataValidationArtifact ) -> None:
       
        try:
            self.data_transformation_config = data_transformation_config
            self.data_validation_artifact = data_validation_artifact
        except Exception as exp:
            raise SensorException(exp)


    @staticmethod
    def read_data(csv_file_path:str)->pd.DataFrame:
        try:
            # don't do this if file is very large, read in chunk
            return pd.read_csv(csv_file_path)
        except Exception as exp:
            raise SensorException(exp)

    @classmethod
    def get_data_transform_object(cls)-> Pipeline:
        try:
            robust_scaler=RobustScaler()
            simple_imputer=SimpleImputer(strategy="constant", fill_value=0)

            # apply missing imputed value followed by robust scalar, handle outliers
            preprocessing_pipeline=Pipeline(steps=
                [
                    ("Imputer",simple_imputer),
                    ("RobustScaler",robust_scaler)
                ]
            )
            return preprocessing_pipeline
        except Exception as exp:
            raise SensorException(exp)

    def initate_data_transformation(self)-> DataTransformationArtifact:
        try:    
            train_dataframe= DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path)
            test_datafrane=DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)
            
            # drop target column from train_data_frame and create target train, train feature objects
            TARGET_COLUMN  = training_pipeline.TARGET_COLUMN
            #training dataframe
            input_feature_train_df = train_dataframe.drop(columns=[TARGET_COLUMN], axis=1)
            target_feature_train_df = train_dataframe[TARGET_COLUMN]
            target_feature_train_df = target_feature_train_df.replace( TargetValueMapping().to_dict())

            #testing dataframe
            input_feature_test_df = test_datafrane.drop(columns=[TARGET_COLUMN], axis=1)
            target_feature_test_df = test_datafrane[TARGET_COLUMN]
            target_feature_test_df = target_feature_test_df.replace(TargetValueMapping().to_dict())

            
            preprocessing_pipeline= DataTransformation.get_data_transform_object()
            
            proprocessor_object=preprocessing_pipeline.fit(input_feature_train_df)
            transformed_input_train_Features = proprocessor_object.transform(input_feature_train_df)
            transformed_input_test_Features = proprocessor_object.transform(input_feature_test_df)

            smt = SMOTETomek(sampling_strategy="minority")

            input_feature_train_final, target_feature_train_final = smt.fit_resample(
                transformed_input_train_Features, target_feature_train_df
            )

            input_feature_test_final, target_feature_test_final = smt.fit_resample(
                transformed_input_test_Features, target_feature_test_df
            )

            train_arr = np.c_[input_feature_train_final, np.array(target_feature_train_final) ]
            test_arr = np.c_[ input_feature_test_final, np.array(target_feature_test_final) ]

            #save numpy array data
            save_numpy_array_data( self.data_transformation_config.transformed_train_file_path, data=train_arr, )
            save_numpy_array_data( self.data_transformation_config.transformed_test_file_path,data==test_arr,)
            save_object( self.data_transformation_config.transformed_object_file_path, proprocessor_object)
            
            data_transformation_artifact = DataTransformationArtifact(
                transformed_object_file_path= self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path = self.data_transformation_config.transformed_test_file_path
            )
            logging.info(f"Data Transformation Artifact : {data_transformation_artifact}")
            return data_transformation_artifact
        except Exception as exp:
            raise SensorException(exp)
