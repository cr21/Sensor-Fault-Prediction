import pymongo
from sensor.constant.database import DATABASE_NAME
from sensor.exception import SensorException
import os
import certifi
ca = certifi.where()


class MongoDBConnector:

    def __init__(self, database_name: str = DATABASE_NAME) -> None:
        self.db_name = database_name
        try:
            if self.client is None:
                mongo_db_url=os.getenv('MONGO_DB_URL')
                MongoDBConnector.client = pymongo.MongoClient(mongo_db_url, tlsCAFile=ca)
            self.client = MongoDBConnector.client
            self.database = self.client['database_name']

        except Exception as exp:
            raise exp
            # raise SensorException(exp)
