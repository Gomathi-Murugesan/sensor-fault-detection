from sensor.constant.training_pipeline import SCHEMA_FILE_PATH
from sensor.entity.config_entity import DataValidationConfig
from sensor.entity.artifacts_entity import DataIngestionArtifacts, DataValidationArtifacts
from sensor.exception import SensorException
from sensor.logger import logging
from sensor.utils.main_utils import read_yaml_file, write_yaml_file
import pandas as pd
import sys, os
from scipy.stats import ks_2samp


class DataValidation:

    def __init__(self, data_ingestion_artifacts: DataIngestionArtifacts, data_validation_config: DataValidationConfig):
        try:
            logging.info('Data validation init function called')
            self.data_ingestion_artifacts = data_ingestion_artifacts
            self.data_validation_config = data_validation_config
            # read schema.yaml file from config folder using read_yaml_file method
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise SensorException(e, sys)

    def validate_number_of_columns(self, dataframe: pd.DataFrame) -> bool:
        try:
            """
            calculate the number of columns in the schema file
            and if number of coulmns is equal to the number of columns in the dataframe, then return True
            by default return False
            """
            number_of_columns = len(self._schema_config["columns"])
            logging.info(f"Number of columns in schema {number_of_columns}")
            logging.info(f"Dataframe columns: {len(dataframe.columns)}")
            if len(dataframe.columns) == number_of_columns:
                return True
            return False
        except Exception as e:
            raise SensorException(e, sys)

    def is_numerical_column_exist(self, dataframe: pd.DataFrame) -> bool:
        try:
            """ 
            Check whether all the numerical columns in schema file exist in dataframe columns
            """
            numerical_columns = self._schema_config["numerical_columns"]
            dataframe_columns = dataframe.columns
            all_numerical_columns_present = True
            missing_numerical_columns = []
            for num_column in numerical_columns:
                if not num_column in dataframe_columns:
                    all_numerical_columns_present = False
                    missing_numerical_columns.append(num_column)

            logging.info(
                f"Missing numerical columns are [{missing_numerical_columns}]")
            return all_numerical_columns_present

        except Exception as e:
            raise SensorException(e, sys)

    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise SensorException(e, sys)



    def detect_dataset_drift(self,base_df, current_df, threshold=0.5):
        """
        This function is to calculate dirft report for each and every columns
        we can set the threshold p-value, 50% distribution will be better our for model training
        """
        try:
            status= True
            report = {}
            for column in base_df.columns:
                d1 = base_df[column]
                d2 = current_df[column]
                distribution_p_value = ks_2samp(d1, d2)
                if distribution_p_value.pvalue >= threshold:
                    is_drift_found = False
                else:
                    is_drift_found = True
                    status = False
                report.update({
                    column: {
                        'p-value': float(distribution_p_value.pvalue),
                        'drift_status': is_drift_found
                    }
                })
            
            drift_report_file_path = self.data_validation_config.drift_report_file_path

            #create a directory
            dir_path = os.path.dirname(drift_report_file_path)
            os.makedirs(dir_path, exist_ok=True)
            write_yaml_file(file_path=drift_report_file_path, content=report)

            return status
        
        except Exception as e:
            raise SensorException(e, sys)



    def drop_zero_std_dev_columns(self, dataframe):
        pass

    def initiate_data_validation(self) -> DataValidationArtifacts:
        try:
            logging.info('Starting data validation artifacts')
            error_message = {}
            # get the train and test file paths from data ingestion artifacts
            train_file_path = self.data_ingestion_artifacts.train_file_path
            test_file_path = self.data_ingestion_artifacts.test_file_path

            # read the data from the train and test file paths into a dataframe using read_data function
            train_dataframe = DataValidation.read_data(train_file_path)
            test_dataframe = DataValidation.read_data(test_file_path)

            # validate number of columns in train and test dataframe
            status = self.validate_number_of_columns(train_dataframe)
            if not status:
                error_message = f"{error_message} Train dataframe does not contain all the columns \n"
            status = self.validate_number_of_columns(test_dataframe)
            if not status:
                error_message = f"{error_message} Test dataframe does not contain all the columns \n"

            # validate whether all the numerical columns are present in the train and test datframes

            status = self.is_numerical_column_exist(train_dataframe)
            if not status:
                error_message = f"{error_message} Train dataframe does not contain all the numerical columns \n"
            status = self.is_numerical_column_exist(test_dataframe)
            if not status:
                error_message = f"{error_message} Test dataframe does not contain all the numerical columns \n"

            if len(error_message) > 0:  # when atleast one error_message is generated
                raise Exception(error_message)

            # if there are any missing columns, we will raise Exception
            # we will run the pipeline even if there are data drift but will update False in validation_status, 
            

            # Let's check the data drift
            status = self.detect_dataset_drift(base_df=train_dataframe, current_df=test_dataframe)

            # we are not writing valid and invaild files in the data validation folder
            # instead for next stage component, we can refer the train and test file paths from data ingestion artifacts
            data_validation_artifacts = DataValidationArtifacts(
                validation_status = status,
                valid_train_file_path = self.data_ingestion_artifacts.train_file_path,
                valid_test_file_path = self.data_ingestion_artifacts.test_file_path,
                #invalid_train_file_path = self.data_validation_config.invalid_train_file_path,
                #invalid_test_file_path = self.data_validation_config.invalid_test_file_path,
                invalid_train_file_path = None,
                invalid_test_file_path = None,
                drift_report_file_path = self.data_validation_config.drift_report_file_path
                )
            return data_validation_artifacts
        except Exception as e:
            raise SensorException(e, sys)
