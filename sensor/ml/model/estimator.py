
from sklearn.pipeline import Pipeline
import os
from sensor.constant.training_pipeline import MODEL_FILE_NAME, SAVED_MODEL_DIR

class TargetValueMapping:
    def __init__(self):
        self.neg: int = 0
        self.pos: int = 1

    def to_dict(self):
        return self.__dict__

    def reverse_mapping(self):
        mapping_response = self.to_dict()
        return dict(zip(mapping_response.values(), mapping_response.keys()))


class SensorModel:

    def __init__(self, preprocessor:Pipeline, model):
        try:
            self.preprocessor=preprocessor
            self.model=model
        except Exception as exp:
            raise exp
    
    def predict(self, x):
        try:
            x_transform = self.preprocessor.transform(x)
            y_hat = self.model.predict(x_transform)
            return y_hat
        except Exception as e:
            raise e


class ModelResolver:

    def __init__(self, model_dir:str=SAVED_MODEL_DIR) -> None:
        try:
            self.model_dir=model_dir
        except Exception as exp:
            raise exp
        

    def get_best_model(self)->str:
        try:
            timestamps = list(map(int,os.listdir(self.model_dir)))
            latest_timestamp = max(timestamps)
            latest_model_path= os.path.join(self.model_dir,f"{latest_timestamp}",MODEL_FILE_NAME)
            return latest_model_path
        except Exception as exp:
            raise exp
        

    def is_model_exists(self)-> bool: 
        try:
            # save model dir does not exists
            if not os.path.exists(self.model_dir):
                return False
            
            # check if saved model dir has some data in it
            timestamps  = os.listdir(self.model_dir)
            if len(timestamps) == 0:
                return False 
            
            latest_model_path = self.get_best_model()
            # check if path residing in save model dir is valid path
            if not os.path.exists(latest_model_path):
                return False

            return True
        except Exception as exp:
            raise exp
