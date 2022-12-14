from datetime import datetime
import os
from sensor.constant import training_pipeline

class TrainingPipelineConfig:
    """
    Training Pipeline configuration
    This class takes timestamp as input and default is current timestamp
    """
    def __init__(self,timestamp=datetime.now()):
        timestamp = timestamp.strftime("%m_%d_%Y_%H_%M_%S")
        self.pipeline_name = training_pipeline.PIPELINE_NAME # name of the pipeline "sensor" defined in constant folder
        self.artifact_dir = os.path.join(training_pipeline.ARTIFACT_DIR, timestamp)
        self.timestamp = timestamp

class DataIngestionConfig:
    """
    Data Ingestion configuration
    In this class, we define folder and file path structure
    Input to this class is "TrainingPipelineConfig" class, which gives, pipeline and artifacts folder structure
    """
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        self.data_ingestion_dir = os.path.join(
            training_pipeline_config.artifact_dir,training_pipeline.DATA_INGESTION_DIR_NAME
            )
        self.feature_store_file_path = os.path.join(
            self.data_ingestion_dir, training_pipeline.DATA_INGESTION_FEATURE_STORE_DIR, training_pipeline.FILE_NAME
        )
        self.training_file_path = os.path.join(
            self.data_ingestion_dir, training_pipeline.DATA_INGESTION_INGESTED_DIR, training_pipeline.TRAIN_FILE_NAME
        )
        self.testing_file_path = os.path.join(
            self.data_ingestion_dir, training_pipeline.DATA_INGESTION_INGESTED_DIR, training_pipeline.TEST_FILE_NAME
        )
        self.train_test_split_ratio = training_pipeline.DATA_INGESTION_TRAIN_TEST_SPLIT_RATION
        self.collection_name = training_pipeline.DATA_INGESTION_COLLECTION_NAME

class DataValidationConfig:
    """
    Data Validation configuration
    In this class, we define folder and file path structure for data validation
    Input to this class is "TrainingPipelineConfig" class, which gives, pipeline and artifacts folder structure
    """
    def __init__(self, training_pipeline_config:TrainingPipelineConfig):
        self.data_validation_dir = os.path.join(
            training_pipeline_config.artifact_dir, training_pipeline.DATA_VALIDATION_DIR_NAME
        )
        self.valid_data_dir = os.path.join(
            self.data_validation_dir, training_pipeline.DATA_VALIDATION_VALID_DIR
        )
        self.invalid_data_dir = os.path.join(
            self.data_validation_dir, training_pipeline.DATA_VALIDATION_INVALID_DIR
        )
        self.valid_train_file_path = os.path.join(self.valid_data_dir, training_pipeline.TRAIN_FILE_NAME)
        self.valid_test_file_path = os.path.join(self.valid_data_dir, training_pipeline.TEST_FILE_NAME)
        self.invalid_train_file_path = os.path.join(self.invalid_data_dir, training_pipeline.TRAIN_FILE_NAME)
        self.invalid_test_file_path = os.path.join(self.invalid_data_dir, training_pipeline.TEST_FILE_NAME)
        self.drift_report_file_path = os.path.join(
            self.data_validation_dir,
            training_pipeline.DATA_VALIDATION_DRIFT_REPORT_DIR,
            training_pipeline.DATA_VALIDATION_DRIFT_REPORT_FILE_NAME
        )

class DataTransformationConfig:
    """
    Data Transformation configuration
    In this class, we define folder and file path structure for data transformation
    Input to this class is "TrainingPipelineConfig" class, which gives, pipeline and artifacts folder structure
    """
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        self.data_transformation_dir = os.path.join(training_pipeline_config.artifact_dir, training_pipeline.DATA_TRANSFORMATION_DIR_NAME)
        #self.data_transformation_transformed_data_dir = os.path.join(self.data_transformation_dir,
        #training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR)
        #self.data_transformation_transformed_object_dir = os.path.join(self.data_transformation_dir,
        #training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR)
        self.transformed_train_file_path= os.path.join(self.data_transformation_dir,
        training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR, 
        training_pipeline.TRAIN_FILE_NAME.replace("csv", "npy"))

        self.transformed_test_file_path= os.path.join(self.data_transformation_dir,
        training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR, 
        training_pipeline.TEST_FILE_NAME.replace("csv", "npy"))

        self.transformed_object_file_path= os.path.join(self.data_transformation_dir,
        training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR, 
        training_pipeline.PREPROCESSING_OBJECT_FILE_NAME)

class ModelTrainerConfig:
    """
    Model Trainer configuration
    In this class, we define folder and file path structure for model trainer
    Input to this class is "TrainingPipelineConfig" class, which gives, pipeline and artifacts folder structure
    """
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        self.model_trainer_dir = os.path.join(training_pipeline_config.artifact_dir,
        training_pipeline.MODEL_TRAINER_DIR_NAME)
        self.trained_model_file_path = os.path.join(self.model_trainer_dir,
        training_pipeline.MODEL_TRAINER_TRAINED_MODEL_DIR, training_pipeline.MODEL_TRAINER_TRAINED_MODEL_NAME)
        self.expected_accuracy = training_pipeline.MODEL_TRAINER_EXPECTED_SCORE
        self.overfitting_underfitting_threshold = training_pipeline.MODEL_TRAINER_OVERFITTING_UNDERFITTING_THRESHOLD

class ModelEvaluationConfig:
    def __init__(self,training_pipeline_config):
        self.model_evaluation_dir = os.path.join(training_pipeline_config.artifact_dir,
        training_pipeline.MODEL_EVALUATION_DIR_NAME)
        self.model_evaluation_report_file_path = os.path.join(self.model_evaluation_dir,
        training_pipeline.MODEL_EVALUATION_REPORT_NAME)
        self.change_threshold = training_pipeline.MODEL_EVALUATION_CHANGED_THRESHOLD_SCORE

class ModelPusherConfig:
    def __init__(self,training_pipeline_config):
        self.model_pusher_dir = os.path.join(training_pipeline_config.artifact_dir,
        training_pipeline.MODEL_PUSHER_DIR_NAME)
        self.model_file_path = os.path.join(self.model_pusher_dir, training_pipeline.MODEL_FILE_NAME)
        

        #directory to save all the models
        timestamp = round(datetime.now().timestamp())
        self.saved_model_path = os.path.join(
            training_pipeline.SAVED_MODEL_DIR,
            f"{timestamp}",
            training_pipeline.MODEL_FILE_NAME
        )

        