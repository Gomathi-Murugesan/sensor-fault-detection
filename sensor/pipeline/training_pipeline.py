from sensor.entity.config_entity import TrainingPipelineConfig, DataIngestionConfig, DataValidationConfig, DataTransformationConfig, ModelTrainerConfig, ModelEvaluationConfig, ModelPusherConfig
from sensor.entity.artifacts_entity import DataIngestionArtifacts, DataValidationArtifacts, DataTransformationArtifacts, ModelTrainerArtifacts, ModelEvaluationArtifacts, ModelPusherArtifacts
from sensor.exception import SensorException
from sensor.logger import logging
import sys
from sensor.components.data_ingestion import DataIngestion
from sensor.components.data_validation import DataValidation
from sensor.components.data_transformation import DataTransformation
from sensor.components.model_trainer import ModelTrainer
from sensor.components.model_evaluation import ModelEvaluation
from sensor.components.model_pusher import ModelPusher
class TrainingPipeline:
    """
    Training pipeline class with various compenents
    """
    is_pipeline_running = False
    def __init__(self):
        self.training_pipeline_config = TrainingPipelineConfig()
    
    def start_data_ingestion(self) -> DataIngestionArtifacts:
        """
        Defining data_ingestion compenents with input and output
        Raises:
            SensorException: custom exception created

        Returns:
            DataIngestionArtifacts: output artifacts from data ingestion component
        """
        try:
            logging.info("Starting Data Ingestion")
            self.data_ingestion_config = DataIngestionConfig(self.training_pipeline_config)
            data_ingestion = DataIngestion(self.data_ingestion_config)
            data_ingestion_artifacts = data_ingestion.initiate_data_ingestion()
            logging.info(f"Data Ingestion is completed and the artifacts are: {data_ingestion_artifacts}")
            return data_ingestion_artifacts
        except Exception as e:
            raise SensorException(e, sys)

    def start_data_validation(self, data_ingestion_artifacts:DataIngestionArtifacts) -> DataValidationArtifacts:
        """_summary_

        Args:
            data_ingestion_artifacts (DataIngestionArtifacts): output of data ingestion component

        Raises:
            SensorException: custom exception 

        Returns:
            DataValidationArtifacts: output of the data validation component
        """
        try:
            logging.info("Starting Data Validation")
            data_validation_config = DataValidationConfig(self.training_pipeline_config)
            data_validation = DataValidation(data_ingestion_artifacts=data_ingestion_artifacts,
            data_validation_config= data_validation_config
            )
            data_validation_artifacts = data_validation.initiate_data_validation()
            logging.info(f"Data Validation is completed and the artifacts are: {data_validation_artifacts}")
            return data_validation_artifacts
        except Exception as e:
            raise SensorException(e, sys)

    def start_data_transformation(self, data_validation_artifacts) -> DataTransformationArtifacts:
        try:
            logging.info("starting data transformation")
            data_transformation_config = DataTransformationConfig(self.training_pipeline_config)
            data_transformation = DataTransformation(data_validation_artifacts, data_transformation_config)
            data_transformation_artifacts = data_transformation.initiate_data_transmission()
            logging.info(f"Data Transformation is completed and the artifacts are: {data_transformation_artifacts}")
            return data_transformation_artifacts        
        except Exception as e:
            raise SensorException(e, sys)

    def start_model_trainer(self, data_transformation_artifacts) -> ModelTrainerArtifacts:
        try:
            logging.info("starting Model Trainer")
            model_trainer_config = ModelTrainerConfig(self.training_pipeline_config)
            model_trainer = ModelTrainer(data_transformation_artifacts, model_trainer_config)
            model_trainer_artifacts = model_trainer.initiate_model_trainer()
            logging.info(f"Model Trainer is completed and the artifacts are: {model_trainer_artifacts}")
            return model_trainer_artifacts
        except Exception as e:
            raise SensorException(e, sys)

    def start_model_evaluation(self, data_validation_artifacts, model_trainer_artifacts) -> ModelEvaluationArtifacts:
        try:
            logging.info("starting Model Evaluation")
            model_evaluation_config = ModelEvaluationConfig(self.training_pipeline_config)
            model_evaluation = ModelEvaluation(data_validation_artifacts, model_trainer_artifacts, model_evaluation_config)
            model_evaluation_artifacts = model_evaluation.initiate_model_evaluation()
            logging.info(f"Model Evaluation is completed and the artifacts are: {model_evaluation_artifacts}")
            return model_evaluation_artifacts
        except Exception as e:
            raise SensorException(e, sys)

    def start_model_pusher(self, model_evaluation_artifacts) -> ModelPusherArtifacts:
        try:
            logging.info("starting Model Pusher")
            model_pusher_config = ModelPusherConfig(self.training_pipeline_config)
            model_pusher = ModelPusher(model_evaluation_artifacts, model_pusher_config)
            model_pusher_artifacts = model_pusher.initiate_model_pusher()
            logging.info(f"Model Pusher is completed and the artifacts are: {model_pusher_artifacts}")
            return model_pusher_artifacts
        except Exception as e:
            raise SensorException(e, sys)

    def run_training_pipeline(self):
        try:
            TrainingPipeline.is_pipeline_running = True
            data_ingestion_artifacts: DataIngestionArtifacts = self.start_data_ingestion()
            data_validation_artifacts= self.start_data_validation(data_ingestion_artifacts)
            data_tranformation_artifacts= self.start_data_transformation(data_validation_artifacts)
            model_trainer_artifacts= self.start_model_trainer(data_tranformation_artifacts)
            model_evaluation_artifacts= self.start_model_evaluation(data_validation_artifacts, model_trainer_artifacts)
            if not model_evaluation_artifacts.is_model_accepted:
                raise Exception('Trained model is not better than the best model')
            model_pusher_artifacts= self.start_model_pusher(model_evaluation_artifacts)
            TrainingPipeline.is_pipeline_running = False
        except Exception as e:
            TrainingPipeline.is_pipeline_running = False
            raise SensorException(e, sys)