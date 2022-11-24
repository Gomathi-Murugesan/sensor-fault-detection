from sensor.exception import SensorException
from sensor.logger import logging
from sensor.entity.artifacts_entity import DataTransformationArtifacts, ModelTrainerArtifacts
from sensor.entity.config_entity import ModelTrainerConfig
import os, sys
from sensor.utils.main_utils import load_numpy_array_data, load_object, save_object
from xgboost import XGBClassifier
from sensor.ml.metrics.classification_metric import get_classification_metrics_score
from sensor.ml.model.estimator import SensorModel
class ModelTrainer:

    def __init__(self,data_transformation_artifacts:DataTransformationArtifacts,
     model_trainer_config:ModelTrainerConfig):
        try:
            self.data_transformation_artifacts = data_transformation_artifacts
            self.model_trainer_config = model_trainer_config
        except Exception as e:
            raise SensorException(e, sys)

    def perform_hyperparameter_tuning(self):
        pass

    def train_model(self,x_train,y_train):
        try:
            xgb_clf = XGBClassifier()
            xgb_clf.fit(x_train,y_train)
            return xgb_clf
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
            #train the model with x_train and y_train
            model = self.train_model(x_train,y_train)

            # predict y values for x_train with the model
            y_train_pred = model.predict(x_train)
            # calculate the classification metrics for y_train and y_train predicted
            classification_train_metrics = get_classification_metrics_score(y_train, y_train_pred)

            if classification_train_metrics.f1_score <= self.model_trainer_config.expected_accuracy:
                raise Exception("Trained Model doesnot meet the expected accuracy")

            y_test_pred = model.predict(x_test)
            classification_test_metrics = get_classification_metrics_score(y_test, y_test_pred)

            # check overfitting and underfitting--- USE DIFFERENT METHOD -- EXPLORE
            difference = abs(classification_train_metrics.f1_score - classification_test_metrics.f1_score)

            if difference>self.model_trainer_config.overfitting_underfitting_threshold:
                raise Exception("Model is not effective, try more experiments")
            
            # combine the model and the preprocessor together using SensorModel method, inorder to predict the output for new x input
            # load the preprocessor pipeline object from the data tranformation artifacts
            preprocessor = load_object(self.data_transformation_artifacts.transformed_object_file_path)
            # combine both model and preprocessor
            sensor_model = SensorModel(preprocessor, model)
            # save the final sensor_model inside model trainer
            model_dir_path = os.path.dirname(self.model_trainer_config.trained_model_file_path)
            os.makedirs(model_dir_path, exist_ok=True)
            save_object(file_path=self.model_trainer_config.trained_model_file_path, obj=sensor_model)

            # Model Trainer Artifacts
            model_trainer_artifacts = ModelTrainerArtifacts(
                trained_model_file_path = self.model_trainer_config.trained_model_file_path,
                train_metric_artifacts = classification_train_metrics,
                test_metric_artifacts = classification_test_metrics
            )
            logging.info(f"Model Trainer Artifacts: {model_trainer_artifacts}")
            return model_trainer_artifacts
        except Exception as e:
            raise SensorException(e, sys)