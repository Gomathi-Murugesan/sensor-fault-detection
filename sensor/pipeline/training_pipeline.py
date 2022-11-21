from sensor.entity.config_entity import TrainingPipelineConfig, DataIngestionConfig, DataValidationConfig, DataTransformationConfig
from sensor.entity.artifacts_entity import DataIngestionArtifacts, DataValidationArtifacts, DataTransformationArtifacts
from sensor.exception import SensorException
from sensor.logger import logging
import sys
from sensor.components.data_ingestion import DataIngestion
from sensor.components.data_validation import DataValidation
from sensor.components.data_transformation import DataTransformation
class TrainingPipeline:
    """
    Training pipeline class with various compenents
    """

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
            logging.info(f"Data Ingestion is completed and artifacts: {data_ingestion_artifacts}")
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
            logging.info(f"Data Validation is completed and artifacts: {data_validation_artifacts}")
            return data_validation_artifacts
        except Exception as e:
            raise SensorException(e, sys)

    def start_data_transformation(self, data_validation_artifacts) -> DataTransformationArtifacts:
        try:
            logging.info("starting data transformation")
            data_transformation_config = DataTransformationConfig(self.training_pipeline_config)
            data_transformation = DataTransformation(data_validation_artifacts, data_transformation_config)
            data_transformation_artifacts = data_transformation.initiate_data_transmission()
            logging.info(f"Data Transformation is completed and artifacts: {data_transformation_artifacts}")
            return data_transformation_artifacts        
        except Exception as e:
            raise SensorException(e, sys)

    def start_model_trainer(self):
        try:
            pass
        except Exception as e:
            raise SensorException(e, sys)

    def start_model_evaluation(self):
        try:
            pass
        except Exception as e:
            raise SensorException(e, sys)

    def start_model_pusher(self):
        try:
            pass
        except Exception as e:
            raise SensorException(e, sys)

    def run_training_pipeline(self):
        try:
            data_ingestion_artifacts: DataIngestionArtifacts = self.start_data_ingestion()
            data_validation_artifacts= self.start_data_validation(data_ingestion_artifacts)
            data_tranformation_artifacts= self.start_data_transformation(data_validation_artifacts)
            model_trainer_artifacts= self.start_model_trainer(data_tranformation_artifacts)

        except Exception as e:
            raise SensorException(e, sys)