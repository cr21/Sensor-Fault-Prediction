import pymongo
from sensor.constant.database import DATABASE_NAME, MONGO_DB_URL
# from sensor.exception import SensorException
import os
import certifi

ca = certifi.where()


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
            raise exp

    def to_dict(self):
        return self.__dict__
