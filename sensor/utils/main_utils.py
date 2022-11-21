from sensor.exception import SensorException
from sensor.logger import logging
import yaml, sys, os
import numpy as np
import dill

def read_yaml_file(file_path) -> dict:
    """
        function to read the yaml file from the given file path
    """
    try:
        with open(file_path, 'rb') as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise SensorException(e, sys)

def write_yaml_file(file_path:str, content:object, replace:bool = False) -> None:
    """
        Function to write a given content into a YAML file in the given file_path
    """
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as file:
            yaml.dump(content, file)
        
    except Exception as e:
        raise SensorException(e, sys)

def save_numpy_array_data(file_path:str, numpy_array:np.array):
    """
    Function to save a given numpy array data in a given file path
    """
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, 'wb') as file_obj:
            np.save(file_obj, numpy_array)
    except Exception as e:
        raise SensorException(e, sys)

def load_numpy_array_data(file_path:str) -> np.array:
    """
    Function to load a numpy array data from a given file path and return the numpy array
    """
    try:
        with open(file_path, 'rb') as file_obj:
            return np.load(file_obj)
    except Exception as e:
        raise SensorException(e, sys)

def save_object(file_path:str, obj: object):
    """ Function to save a given preprocessing object file in a given file path"""
    try:
        logging.info('Entering save_object method of MainUtils file')
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'wb') as file_obj:
            dill.dump(obj, file_obj)
        logging.info("Saved a given preprocessing object in a given file path")
    except Exception as e:
        raise SensorException(e, sys)
