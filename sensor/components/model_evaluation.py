from sensor.exception import SensorException
from sensor.logger import logging
from sensor.entity.artifacts_entity import DataValidationArtifacts, ModelTrainerArtifacts, ModelEvaluationArtifacts
from sensor.entity.config_entity import ModelEvaluationConfig
import os, sys
from sensor.utils.main_utils import load_object, save_object, write_yaml_file
from sensor.ml.metrics.classification_metric import get_classification_metrics_score
from sensor.ml.model.estimator import SensorModel, ModelResolver
import pandas as pd
from sensor.constant.training_pipeline import TARGET_COLUMN
from sensor.ml.model.estimator import TargetValueMapping

class ModelEvaluation:

    def __init__(self, data_validation_artifacts:DataValidationArtifacts, 
    model_trainer_artifacts:ModelTrainerArtifacts, model_evaluation_config:ModelEvaluationConfig):
        try:
            self.data_validation_artifacts = data_validation_artifacts
            self.model_trainer_artifacts = model_trainer_artifacts
            self.model_evaluation_config = model_evaluation_config
        except Exception as e:
            raise SensorException(e, sys)

    def initiate_model_evaluation(self) -> ModelEvaluationArtifacts:
        """ This method is to check whether the new trained model is best than the previous best model saved in the saved model folder
            Accept the new trained model, if no other model is available
            Compare the metrics and performance of both the new trained model and the previous saved model
            Accept the new trained model, if the performance of the new trained model is good
        """
        try:
            # load the valid train and test file paths 
            valid_train_file_path = self.data_validation_artifacts.valid_train_file_path
            valid_test_file_path = self.data_validation_artifacts.valid_test_file_path

            # load the train and test df
            train_df = pd.read_csv(valid_train_file_path)
            test_df = pd.read_csv(valid_test_file_path)

            #concatenate the train and test df into one df
            df = pd.concat([train_df, test_df], axis=0)

            # Get the current trained modle from model_trainer_artifacts
            trained_model_file_path = self.model_trainer_artifacts.trained_model_file_path
            # load the model object using load_object method
            new_trained_model = load_object(trained_model_file_path)
            
            # create modelresolver object to load the saved models from the saved_model directory
            model_resolver = ModelResolver()
            is_model_accepted = True
            # check whether we have any previous model saved, if not accpet the new trained model
            if not model_resolver.is_model_exists():
                model_evaluation_artifacts = ModelEvaluationArtifacts(
                    is_model_accepted = is_model_accepted,
                    improved_accuracy = None,
                    best_model_path = None,
                    trained_model_path = trained_model_file_path,
                    train_model_metric_artifacts = self.model_trainer_artifacts.train_metric_artifacts,
                    best_model_metric_artifacts = None
                )
                logging.info(f"Model evaluation artifacts: {model_evaluation_artifacts}")
                return model_evaluation_artifacts
            
            # if we have any other previous saved model, then compare the performance of current trained model and previous saved model
            #get the latest best model from the saved model in order to compare
            best_model_file_path = model_resolver.get_latest_best_model_path()
            # load the model object using load_object method
            best_saved_model = load_object(best_model_file_path)

            # take the original true y value from the df(class column)
            y_true = df[TARGET_COLUMN]
            y_true.replace(TargetValueMapping().to_dict(), inplace=True)
            #predict the output y using both the new trained model and the previous best saved model
            input_df = df.drop(columns=[TARGET_COLUMN], axis=1)
            y_predict_new_trained = new_trained_model.predict(input_df)
            y_predict_best_saved = best_saved_model.predict(input_df)

            #calculate the performance metrics for both the new_trained_model and best_saved_model with y_true
            new_trained_metric = get_classification_metrics_score(y_true, y_predict_new_trained)
            best_saved_metric = get_classification_metrics_score(y_true, y_predict_best_saved)

            #calculte the improved_accuracy between new trained model and best saved model
            improved_accuracy = new_trained_metric.f1_score-best_saved_metric.f1_score

            if improved_accuracy < self.model_evaluation_config.change_threshold:
                is_model_accepted = False
            model_evaluation_artifacts = ModelEvaluationArtifacts(
                    is_model_accepted = is_model_accepted,
                    improved_accuracy = improved_accuracy,
                    best_model_path = best_model_file_path,
                    trained_model_path = trained_model_file_path,
                    train_model_metric_artifacts = new_trained_metric,
                    best_model_metric_artifacts = best_saved_metric
                )
            #print(model_evaluation_artifacts)
            # write the model evaluation report in yaml file using write_yaml_file
            #model_evaluation_report = model_evaluation_artifacts.__dict__()
            model_evaluation_report_file_path = self.model_evaluation_config.model_evaluation_report_file_path
            os.makedirs(os.path.dirname(model_evaluation_report_file_path), exist_ok=True)
            write_yaml_file(model_evaluation_report_file_path,model_evaluation_artifacts)
            
            logging.info(f"Model evaluation artifacts: {model_evaluation_artifacts}")
            return model_evaluation_artifacts

        except Exception as e:
            raise SensorException(e, sys)