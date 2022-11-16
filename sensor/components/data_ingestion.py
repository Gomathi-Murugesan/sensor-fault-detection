from sensor.exception import SensorException
from sensor.logger import logging
from sensor.entity.config_entity import DataIngestionConfig
from sensor.entity.artifacts_entity import DataIngestionArtifacts
import os, sys
from pandas import DataFrame
from sensor.data_access.sensor_data import SensorData
from sklearn.model_selection import train_test_split

class DataIngestion:

    def __init__(self, data_ingestion_config:DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise SensorException(e, sys)

    def export_data_into_feature_store(self) -> DataFrame:
        """
        Export data from MongoDB and load them into the feature store dir inside Data Ingestion directory
        """
        try:
            logging.info("Exporting data from MongoDB into feature store")
            sensor_data = SensorData()
            #print("config.collection_name:",self.data_ingestion_config.collection_name)
            dataframe = sensor_data.exportdata_from_collection_as_dataframe(self.data_ingestion_config.collection_name)
            #get the feature store file path from dataingestion_config
            feature_store_file_path = self.data_ingestion_config.feature_store_file_path
            
            #create folder for the feature store
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path,exist_ok=True) #creates directory if it doesn't exist

            #store dataframe as csv file in feature store
            dataframe.to_csv(feature_store_file_path,index=False,header=True)
            return dataframe
        except Exception as e:
            raise SensorException(e, sys)

    def split_data_into_train_test(self, dataframe:DataFrame) -> None:
        """
        Split the dataframe into train and test file 
        """
        try:
            train_set, test_set = train_test_split(
                dataframe, test_size=self.data_ingestion_config.train_test_split_ratio
            )
            logging.info("Perforemd train test split on the dataframe")

            dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(dir_path, exist_ok=True)
            logging.info("Exported Train and test file path")

            train_set.to_csv(
                self.data_ingestion_config.training_file_path, index=False, header=True)
            test_set.to_csv(
                self.data_ingestion_config.testing_file_path, index=False, header=True)

            logging.info("Exported Train and Test files as csv files")
        except Exception as e:
            raise SensorException(e, sys)


    def initiate_data_ingestion(self) -> DataIngestionArtifacts:
        try:
            dataframe = self.export_data_into_feature_store()
            self.split_data_into_train_test(dataframe)
            data_ingestion_artifacts = DataIngestionArtifacts(
                self.data_ingestion_config.training_file_path, self.data_ingestion_config.testing_file_path)
            return data_ingestion_artifacts
        except Exception as e:
            raise SensorException(e, sys)
