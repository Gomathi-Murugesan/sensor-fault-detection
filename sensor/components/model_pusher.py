from sensor.exception import SensorException
from sensor.logger import logging
from sensor.entity.config_entity import ModelPusherConfig
from sensor.entity.artifacts_entity import ModelEvaluationArtifacts, ModelPusherArtifacts
import sys, os
from sensor.utils.main_utils import save_object
import shutil

class ModelPusher:

    def __init__(self,model_evaluation_artifacts:ModelEvaluationArtifacts, 
        model_pusher_config:ModelPusherConfig):
        try:
            self.model_evaluation_artifacts = model_evaluation_artifacts
            self.model_pusher_config = model_pusher_config
        except Exception as e:
            raise SensorException(e, sys)

    def initiate_model_pusher(self) -> ModelPusherArtifacts:
        """Save the trained model inside the model pusher folder and saved models folder"""
        try:
            trained_model_path = self.model_evaluation_artifacts.trained_model_path

            #Creating model pusher folder and saving model
            model_file_path = self.model_pusher_config.model_file_path
            os.makedirs(os.path.dirname(model_file_path), exist_ok=True)
            shutil.copy(src=trained_model_path,dst=model_file_path)

            #creating the saved models folder and saving the models
            saved_model_path = self.model_pusher_config.saved_model_path
            os.makedirs(os.path.dirname(saved_model_path), exist_ok=True)
            shutil.copy(src=trained_model_path,dst=saved_model_path)

            model_pusher_artifacts = ModelPusherArtifacts(
                model_file_path=model_file_path,
                saved_model_path=saved_model_path)
            
            return model_pusher_artifacts

        except Exception as e:
            raise SensorException(e, sys)