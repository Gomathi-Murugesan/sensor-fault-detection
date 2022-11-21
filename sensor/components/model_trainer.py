from sensor.exception import SensorException
from sensor.logger import logging
from sensor.entity.artifacts_entity import DataTransformationArtifacts, ModelTrainerArtifacts
from sensor.entity.config_entity import ModelTrainerConfig
import os, sys
from sensor.utils.main_utils import load_numpy_array_data

class ModelTrainer:

    def __init__(self,data_transformation_artifacts:DataTransformationArtifacts,
     model_trainer_config:ModelTrainerConfig):
        try:
            self.data_transformation_artifacts = data_transformation_artifacts
            self.model_trainer_config = model_trainer_config
        except Exception as e:
            raise SensorException(e, sys)

    def initiate_model_trainer(self) -> ModelTrainerArtifacts:
        try:
            train_file_path = self.data_transformation_artifacts.transformed_train_file_path
            test_file_path = self.data_transformation_artifacts.transformed_test_file_path

            #load the numpy array from train and test file path where arrays are stored in the file
            train_array = load_numpy_array_data(train_file_path)
            test_array = load_numpy_array_data(test_file_path)

            x_train, y_train, x_test, y_test = (
                train_array[:, :-1], #all rows, all columns except the last column
                train_array[:, -1], #all rows, only the last column
                test_array[:, :-1],
                test_array[:, -1]
            )

        except Exception as e:
            raise SensorException(e, sys)