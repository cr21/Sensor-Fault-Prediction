from ast import Try
import os, sys
from sensor.exception import SensorException
from sensor.logger import logging
from sensor.entity.config_entity import DataIngestionConfig
from sensor.entity.artifact_entity import DataIngestionArtifact
from pandas import DataFrame
from sensor.data_access.sensor_data import SensorData
from sklearn.model_selection import train_test_split


class DataIngestion:
    def __init__(self, data_ingestion_config:DataIngestionConfig) -> None:
        try:
            self.data_ingestion_config=data_ingestion_config
        except Exception as exp:
            raise SensorException(exp)

    
    def split_data_as_train_test(self,df:DataFrame)->None:
        """
        Take Data from Feature Store and Convert into Train test split
        """
        try:
            logging.info("Performed Test Train split on Dataframe")
            train_set, test_set=train_test_split(df, test_size=self.data_ingestion_config.train_test_split_ratio)
            logging.info(
                "Exited split_data_as_train_test method of Data_Ingestion class"
            )

            dir_path_name=os.path.dirname(self.data_ingestion_config.training_file_path)

            os.makedirs(dir_path_name, exist_ok=True)

            logging.info(f"Exporting train and test file path.")

            train_set.to_csv(
                self.data_ingestion_config.training_file_path, index=False, header=True
            )

            test_set.to_csv(
                self.data_ingestion_config.testing_file_path, index=False, header=True
            )

            logging.info(f"Exported train and test file path.")



            pass
        except Exception as exp:
            raise SensorException(exp)

    def export_data_to_feature_store(self)->DataFrame:
        """
        Export mongo db collection record as data frame into feature
        """
        try:
            logging.info("Exporting Data From mongodb To Feature Store")
            sensor_data=SensorData()
            sensor_df = sensor_data.export_collection_as_dataframe(collection_name=self.data_ingestion_config.collection_name)
            feature_store_file_path = self.data_ingestion_config.feature_store_file_path

            # CREATING FOLDER
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path, exist_ok=True)
            sensor_df.to_csv(feature_store_file_path,index=False, header=True)
    
            return sensor_df
    
        except Exception as exp:
            raise SensorException(exp)

    def initiate_date_ingestion(self)->DataIngestionArtifact:
        
        try:
            dataframe=self.export_data_to_feature_store()
            self.split_data_as_train_test(dataframe)
            data_ingestion_artifact = DataIngestionArtifact(
                trained_file_path=self.data_ingestion_config.training_file_path,
                test_file_path=self.data_ingestion_config.testing_file_path
            )

            return data_ingestion_artifact

        except Exception as exp:
            raise SensorException(exp)
