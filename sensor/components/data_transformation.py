import sys
from sensor.exception import SensorException
from sensor.logger import logging
from sensor.entity.config_entity import DataTransformationConfig
from sensor.entity.artifacts_entity import DataValidationArtifacts, DataTransformationArtifacts
import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import RobustScaler
from imblearn.combine import SMOTETomek
from sensor.constant.training_pipeline import TARGET_COLUMN
from sensor.utils.main_utils import save_numpy_array_data, load_numpy_array_data, save_object
from sensor.ml.model.estimator import TargetValueMapping


class DataTransformation:

    def __init__(self, data_validation_artifacts:DataValidationArtifacts,
                data_transmission_config:DataTransformationConfig):
        try:
            self.data_validation_artifacts = data_validation_artifacts
            self.data_transmission_config = data_transmission_config
        except Exception as e:
            raise SensorException(e, sys)

    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise SensorException(e, sys)          

    @classmethod
    def get_data_transfomer_object(cls)-> Pipeline:
        try:
            # strategy can be constant, mean, median,etc..
            # here we use constant to replace all the missing values with constant zero
            simple_imputer = SimpleImputer(strategy="constant", fill_value=0)
            robust_scaler = RobustScaler()
            preprocessor_pipeline = Pipeline(
                steps=[
                    ('imputer', simple_imputer), #replaces missing values with zero
                    ('robust_scaler', robust_scaler) #keeps all features in the same range and handles the outliers
                ]
            )
            return preprocessor_pipeline
        except Exception as e:
            raise SensorException(e, sys)

    def initiate_data_transmission(self) -> DataTransformationArtifacts:
        try:
            logging.info('Starting initiate data transmission')
            train_df = self.read_data(self.data_validation_artifacts.valid_train_file_path)
            test_df = self.read_data(self.data_validation_artifacts.valid_test_file_path)
            
            #Preparing train df
            # prepare the input train df by dropping target column
            input_feature_train_df = train_df.drop(columns=[TARGET_COLUMN], axis=1)
            # select the target column from train df
            target_feature_train_df = train_df[TARGET_COLUMN]
            # encode the categorical target feature using TargetValueMapping
            target_feature_train_df = target_feature_train_df.replace(TargetValueMapping().to_dict())

            #Preparing test df
            input_feature_test_df = test_df.drop(columns=[TARGET_COLUMN], axis=1)
            target_feature_test_df = test_df[TARGET_COLUMN]
            target_feature_test_df = target_feature_test_df.replace(TargetValueMapping().to_dict())

            #Preprocessor Pipeline to transfrom input features of train and test df using same fit
            preprocessor_pipeline = self.get_data_transfomer_object()
            preprocessor_object = preprocessor_pipeline.fit(input_feature_train_df)

            transformed_input_feature_train = preprocessor_object.transform(input_feature_train_df)
            transformed_input_feature_test = preprocessor_object.transform(input_feature_test_df)

            #Balance the dataset using SMOTETomek
            smt = SMOTETomek(sampling_strategy="minority")

            input_feature_train_final, target_feature_train_final = smt.fit_resample(
                transformed_input_feature_train, target_feature_train_df
            )
            input_feature_test_final, target_feature_test_final = smt.fit_resample(
                transformed_input_feature_test, target_feature_test_df
            )

            #Concatenate the input features and target feature into np.array
            train_array = np.c_[input_feature_train_final, np.array(target_feature_train_final)]
            test_array = np.c_[input_feature_test_final, np.array(target_feature_test_final)]

            #save train and test numpy arrays in a file path using save_numpy_array_data method
            save_numpy_array_data(self.data_transmission_config.transformed_train_file_path, train_array)
            save_numpy_array_data(self.data_transmission_config.transformed_test_file_path, test_array)

            #save the preprocessor object to a file path using save_object
            save_object(self.data_transmission_config.transformed_object_file_path, preprocessor_object)

            # Prepare and return DataTransformationArtifacts
            data_transformation_artifacts = DataTransformationArtifacts(
                    transformed_train_file_path = self.data_transmission_config.transformed_train_file_path,
                    transformed_test_file_path = self.data_transmission_config.transformed_test_file_path,
                    transformed_object_file_path = self.data_transmission_config.transformed_object_file_path
            )
            logging.info(f"Data Transformation Artifacts: {data_transformation_artifacts}")
            return data_transformation_artifacts
        except Exception as e:
            raise SensorException(e, sys)



