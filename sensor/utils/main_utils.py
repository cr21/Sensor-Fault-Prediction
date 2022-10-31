
import yaml
from sensor.exception import SensorException
from sensor.logger import logging
import os,sys
import numpy as np
import dill

def read_yaml_file(file_path: str) -> dict:
    try:
        with open(file_path, "rb") as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise SensorException(e, sys) from e


def write_yaml_file(file_path: str, content: object, replace: bool = False) -> None:
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as file:
            yaml.dump(content, file)
    except Exception as e:
        raise SensorException(e, sys)


def save_numpy_array_data(file_path:str, data:np.array):
    """
    Utility Function to save numpy array data to file
    @param file_path : filename in string format
    @param data : numpy array

    """

    try:
        dir_path=os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(dir_path,'wb') as file_obj:
            np.save(file_obj, data)

    except Exception as exp:
        raise SensorException(exp) from exp


def load_numpy_array(file_path:str)->np.array:
    """
    Load numpy array from file
    @param file_path: file path in string format
    @returns : numpy array
    """
    try:
        
        with open(file_path,'rb') as file_obj:
            return np.load(file_obj)

    except Exception as exp:
        raise SensorException(exp) from exp

def save_object(file_path: str, obj: object) -> None:
    try:
        logging.info("Entered the save_object method of MainUtils class")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as file_obj:
            dill.dump(obj, file_obj)
        logging.info("Exited the save_object method of MainUtils class")
    except Exception as e:
        raise SensorException(e, sys) from e
