import pymongo
from sensor.constant.database import DATABASE_NAME
from sensor.constant.env_variables import MONGODB_URL_KEY
import os
import certifi
ca=certifi.where()

class MongoDBClient:
    client = None
    
    def __init__(self, database_name=DATABASE_NAME) -> None:
        try:
            if MongoDBClient.client is None:
                #print("url:",MONGODB_URL_KEY)
                mongo_db_url = os.getenv(MONGODB_URL_KEY)
                if mongo_db_url is None:
                    raise Exception(f"Environment key: {MONGODB_URL_KEY} is not set.")
                #mongo_db_url = "mongodb+srv://ineuron:Ecevlsi31@cluster0.zmhcemj.mongodb.net/?retryWrites=true&w=majority"
                MongoDBClient.client = pymongo.MongoClient(mongo_db_url, tlsCAFile=ca)
            self.client = MongoDBClient.client
            self.database = self.client[database_name]
            self.database_name = database_name
        except Exception as e:
            raise e
