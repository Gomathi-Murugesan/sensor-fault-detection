from sensor.exception import SensorException
import os, sys
from sensor.constant.training_pipeline import MODEL_FILE_NAME, SAVED_MODEL_DIR
from sensor.logger import logging
class TargetValueMapping:
    """ 
    Custom code to encode the categorical column by assigning 1 for pos class and 0 for neg class
    """
    def __init__(self):
        self.pos = 1
        self.neg = 0
    
    def to_dict(self):
        """ Function to return self as dictionary """
        return self.__dict__

    def reverse_mapping(self):
        """ Reverse mapping the dictionary"""
        mapping_response = self.to_dict()
        return dict(zip(mapping_response.values(), mapping_response.keys()))

class SensorModel:
    """ Class to predict the output(y_predict) for the given input x
    using preprocessor object and model files"""
    def __init__(self, preprocessor, model):
        try:
            self.preprocessor = preprocessor
            self.model = model
        except Exception as e:
            raise SensorException(e, sys)

    def predict(self, x):
        try:
            x_transformed = self.preprocessor.transform(x)
            y_predict = self.model.predict(x_transformed)
            return y_predict
        except Exception as e:
            raise SensorException(e,sys)

class ModelResolver:
    """ This class is used to get the latest model from all the saved models from the folder "SAVED_MODEL_DIR"
    """
    def __init__(self, model_dir=SAVED_MODEL_DIR):
        try:
            self.model_dir = model_dir
        except Exception as e:
            raise SensorException(e, sys)

    
    def get_latest_best_model_path(self):
        """ Saved model folder contains different timestamp folders with model.pkl files.
        get the latest timestamp folder and the model.pkl file inside that folder is the best model"""
        try:
            #list all the timestamps folder in integer
            timestamps = list(map(int,os.listdir(self.model_dir))) 
            latest_timestamp = max(timestamps) #get the latest timestamp
            # get the path of the model.pkl file inside the latest timestamp folder
            latest_model_path = os.path.join(self.model_dir, f"{latest_timestamp}",MODEL_FILE_NAME)
            return latest_model_path
        except Exception as e:
            raise SensorException(e, sys)

    def is_model_exists(self) -> bool:
        try:
            if not os.path.exists(self.model_dir): #check for saved model folder
                return False
            timestamps = os.listdir(self.model_dir)
            if len(timestamps)==0: # check for timestamps folder
                return False
            latest_model_path = self.get_latest_best_model_path()

            if not os.path.exists(latest_model_path): # check for model.pkl file
                return False
            
            return True
        except Exception as e:
            raise SensorException(e, sys)