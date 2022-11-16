from sensor.configuration.mongo_db_connection import MongoDBClient
from sensor.constant.database import DATABASE_NAME, COLLECTION_NAME
from sensor.exception import SensorException
import sys
import pandas as pd
from typing import Optional
import numpy as np

class SensorData:
    """
    This class connects with mongodb database and exports data from collection as dataframe
    """

    def __init__(self):
        """
        connects with mongo db through MongoDBClient configuration
        """
        try:
            self.mongodb_client = MongoDBClient(database_name=DATABASE_NAME)
        except Exception as e:
            raise SensorException(e,sys)

    
    def exportdata_from_collection_as_dataframe(
        self, collection_name, database_name: Optional[str] =None) -> pd.DataFrame:
        """
        export data from collection as dataframe
        """
        try:  
            #print("collection_name:",collection_name)
            # if database name is not specified, then get the database name from mongodb client 
            if database_name is None:
                collection = self.mongodb_client.database[collection_name]
            else:
                collection = self.mongodb_client[database_name][collection_name]
            #print("collection:", collection)
            #print("collection_find:", list(collection.find()))

            df = pd.DataFrame(list(collection.find()))

            if "_id" in df.columns.to_list():
                df = df.drop(columns=["_id"], axis=1)

            df.replace({"na":np.nan}, inplace=True)

            return df

        except Exception as e:
            raise SensorException(e,sys)
