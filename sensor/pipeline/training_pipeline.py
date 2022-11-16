from sensor.entity.config_entity import TrainingPipelineConfig, DataIngestionConfig
from sensor.entity.artifacts_entity import DataIngestionArtifacts
from sensor.exception import SensorException
from sensor.logger import logging
import sys
from sensor.components.data_ingestion import DataIngestion

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
            logging.info(f"Data Ingestion completed and artifacts: {data_ingestion_artifacts}")
            return data_ingestion_artifacts
        except Exception as e:
            raise SensorException(e, sys)

    def start_data_validation(self):
        try:
            pass
        except Exception as e:
            raise SensorException(e, sys)

    def start_data_transformation(self):
        try:
            pass
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
        except Exception as e:
            raise SensorException(e, sys)