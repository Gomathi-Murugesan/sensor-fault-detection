import os
from sensor.constant.s3_bucket import TRANING_BUCKET_NAME

"""
Defining constant variables for training pipeline like artifact name, csv file name, etc.
"""
SAVED_MODEL_DIR = os.path.join("saved_models")
TARGET_COLUMN = "class"
PIPELINE_NAME: str = "sensor"
ARTIFACT_DIR: str = "artifact"
FILE_NAME: str = "sensor.csv"

TRAIN_FILE_NAME: str = "train.csv"
TEST_FILE_NAME: str = "test.csv"

# Defining pickle file names of training pipeling
PREPROCESSING_OBJECT_FILE_NAME = "preprocessing.pkl"
MODEL_FILE_NAME = "model.pkl"
# Defining schema.yaml file names where schema related info is stored
SCHEMA_FILE_PATH = os.path.join("config", "schema.yaml")
SCHEMA_DROP_COLS = "drop_columns"

"""
Data Ingestion related constant - starts with "DATA_INGESTION"
"""

DATA_INGESTION_COLLECTION_NAME: str = "car"
DATA_INGESTION_DIR_NAME: str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store"
DATA_INGESTION_INGESTED_DIR: str = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATION: float = 0.2

"""
Data Validation related constant - starts with "DATA VALIDATION"
"""

DATA_VALIDATION_DIR_NAME = "data_validation"
DATA_VALIDATION_VALID_DIR = "validated"
DATA_VALIDATION_INVALID_DIR = "invalid"
DATA_VALIDATION_DRIFT_REPORT_DIR = "dirft_report"
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME = "report.yaml"

"""
Data Transformation related constant - starts with "DATA TRANSFORMATION"
"""

DATA_TRANSFORMATION_DIR_NAME = "data_transformation"
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR = "transformed"
DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR = "transformed_object"
#DATA_TRANSFORMATION_TRANFORMED_TRAIN_FILE_PATH = "train.npy"
#DATA_TRANSFORMATION_TRANFORMED_TEST_FILE_PATH = "test.npy"
#DATA_TRANSFORMATION_TRANFORMED_OBJECT_FILE_PATH = "pre_processing.pkl"

"""
Model Trainer related constant - starts with "MODEL TRAINER"
"""

MODEL_TRAINER_DIR_NAME:str = "model_trainer"
MODEL_TRAINER_TRAINED_MODEL_DIR:str = "trained_model"
MODEL_TRAINER_TRAINED_MODEL_NAME:str = "model.pkl"
MODEL_TRAINER_EXPECTED_SCORE:float= 0.6
MODEL_TRAINER_OVERFITTING_UNDERFITTING_THRESHOLD:float= 0.05

"""
Model Evaluation related constant - starts with "MODEL EVALUATION"
"""
MODEL_EVALUATION_DIR_NAME = "model_evaluation"
MODEL_EVALUATION_CHANGED_THRESHOLD_SCORE:float= 0.02
MODEL_EVALUATION_REPORT_NAME = "report.yaml"

"""
Model Pusher related constant - starts with "MODEL PUSHER"
"""
MODEL_PUSHER_DIR_NAME = "model_pusher"
MODEL_PUSHER_SAVED_MODEL_DIR = SAVED_MODEL_DIR