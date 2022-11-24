from dataclasses import dataclass

@dataclass
class DataIngestionArtifacts():
    train_file_path: str
    test_file_path: str

@dataclass
class DataValidationArtifacts():
    validation_status : bool
    valid_train_file_path: str
    valid_test_file_path: str
    invalid_train_file_path: str
    invalid_test_file_path: str
    drift_report_file_path: str

@dataclass
class DataTransformationArtifacts():
    transformed_train_file_path: str
    transformed_test_file_path: str
    transformed_object_file_path: str

@dataclass
class ClassificationMetricArtifacts():
    f1_score: float
    precision_score : float
    recall_score : float

@dataclass
class ModelTrainerArtifacts():
    trained_model_file_path : str
    train_metric_artifacts : ClassificationMetricArtifacts
    test_metric_artifacts : ClassificationMetricArtifacts

@dataclass
class ModelEvaluationArtifacts():
    is_model_accepted :bool
    improved_accuracy : float
    best_model_path : str
    trained_model_path : str
    train_model_metric_artifacts : ClassificationMetricArtifacts
    best_model_metric_artifacts : ClassificationMetricArtifacts

@dataclass
class ModelPusherArtifacts():
    model_file_path : str
    saved_model_path : str