from sensor.configuration.mongo_db_connection import MongoDBConnector
from sensor.constant.database import DATABASE_NAME
from sensor.exception import SensorException
import os
import sys
if __name__ == '__main__':
    try:
        connector = MongoDBConnector(DATABASE_NAME)
        print(f"collection_name: {connector.database.list_collection_names()}")
    except Exception as e:
        raise SensorException(e,sys)
