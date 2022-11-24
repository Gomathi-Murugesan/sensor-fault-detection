from sensor.entity.artifacts_entity import ClassificationMetricArtifacts
from sensor.exception import SensorException
from sensor.logger import logging
import sys
from sklearn.metrics import f1_score, recall_score, precision_score

def get_classification_metrics_score(y_true, y_pred) -> ClassificationMetricArtifacts:
    try:
        model_f1_score = f1_score(y_true, y_pred)
        model_precision_score = precision_score(y_true, y_pred)
        model_recall_score = recall_score(y_true, y_pred)

        classification_metric_artifacts = ClassificationMetricArtifacts(
            f1_score = model_f1_score,
            precision_score= model_precision_score,
            recall_score= model_recall_score
        )
        logging.info(f"Classification Metrics Artifacts: {classification_metric_artifacts}")
        return classification_metric_artifacts
    except Exception as e:
        raise SensorException(e,sys)