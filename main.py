from sensor.configuration.mongo_db_connection import MongoDBClient
from sensor.exception import SensorException
import sys,os
from sensor.logger import logging
#from sensor.entity.config_entity import TrainingPipelineConfig, DataIngestionConfig
from sensor.pipeline.training_pipeline import TrainingPipeline
from fastapi import FastAPI
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from sensor.constant.application import APP_HOST, APP_PORT
from starlette.responses import RedirectResponse
from uvicorn import run as app_run 
from sensor.ml.model.estimator import ModelResolver, TargetValueMapping
from sensor.utils.main_utils import load_object
from sensor.constant.training_pipeline import SAVED_MODEL_DIR

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")

@app.get("/train")
async def train_route():
    try:
        training_pipeline = TrainingPipeline()
        if training_pipeline.is_pipeline_running:
            return Response("Training pipeline is already running.")
        training_pipeline.run_training_pipeline()
        return Response("Training Successful !!")
    except Exception as e:
        return Response(f"Error occurred!, {e}")

@app.get("/predict")
async def predict_route():
    try:
        #get csv file from the user
        #convert csv file into a dataframe
        df=None
        model_resolver = ModelResolver(model_dir=SAVED_MODEL_DIR)
        if not model_resolver.is_model_exists():
            return Response("Model is not available")
        best_model_path = model_resolver.get_latest_best_model_path()
        model = load_object(best_model_path)
        y_pred = model.predict(df)
        df['predicted_column'] = y_pred
        df['predicted_column'].replace(TargetValueMapping().reverse_mapping(), inplace=True)
        #return the y_predict to the user
    except Exception as e:
        return Response(f"Error occurred!, {e}")

def main():
    try:
        training_pipeline = TrainingPipeline()
        training_pipeline.run_training_pipeline()
    except Exception as e:
        print(e)
        logging.exception(e)

if __name__ == '__main__':
    app_run(app, host=APP_HOST, port=APP_PORT)

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
    #training_pipeline = TrainingPipeline()
    #training_pipeline.run_training_pipeline()