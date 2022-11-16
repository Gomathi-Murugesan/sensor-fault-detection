from sensor.configuration.mongo_db_connection import MongoDBClient
from sensor.exception import SensorException
import sys
from sensor.logger import logging
#from sensor.entity.config_entity import TrainingPipelineConfig, DataIngestionConfig
from sensor.pipeline.training_pipeline import TrainingPipeline
import os

def test_exception():
    try:
        logging.info("We are dividing 1 by zero")
        x=1/0
    except Exception as e:
        logging.error("Error occurred")
        raise SensorException(e, sys)
        #raise e


if __name__ == '__main__':
    #mongo_db_client = MongoDBClient()
    #print(os.environ["TMP"])
    #print(os.environ["APPDATA"])
    #print(os.environ["MONGO_DB_URL"])
    #print(os.getenv("MONGO_DB_URL"))
    #print('client:', mongo_db_client.client)
    #print('db:',mongo_db_client.database)
    #for coll in mongo_db_client.database.list_collection_names():
     #   print(coll)
    #print('db_name:',mongo_db_client.database_name)
    #print(mongo_db_client.database.list_collection_names)
    #try:
    #    test_exception()
    #except Exception as e:
    #    print(e)
    #training_pipeline_config = TrainingPipelineConfig()
    #data_ingestion_config = DataIngestionConfig(training_pipeline_config)
    #print(data_ingestion_config.__dict__)
    # written the above training_pipeline_config, data_ingestion_config in TrainingPipeline class after testing here
    training_pipeline = TrainingPipeline()
    training_pipeline.run_training_pipeline()