import pymongo
from sensor.constant.database import DATABASE_NAME
from sensor.exception import SensorException
from sensor.constant.env_variable import MONGODB_URL_KEY
import os
import certifi
ca = certifi.where()
MONGO_DB_URL = os.getenv(MONGODB_URL_KEY)

class MongoDBConnector:
    client = None

    def __init__(self, database_name: str = DATABASE_NAME, database_url: str = MONGO_DB_URL) -> None:
        self.db_name = database_name
        try:
            if MongoDBConnector.client is None:
                MongoDBConnector.client = pymongo.MongoClient(MONGO_DB_URL, tlsCAFile=ca)
            self.client = MongoDBConnector.client
            self.database = self.client[self.db_name]

        except Exception as exp:
            raise SensorException(exp)


    def to_dict(self):
        return self.__dict__
