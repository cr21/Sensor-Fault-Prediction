from sensor.config.mongo_db_connection import MongoDBConnector
from sensor.constant.database import  DATABASE_NAME


if __name__=='__main__':
    connector = MongoDBConnector(DATABASE_NAME)
    print(f"collection_name: {connector.database.list_collection_names()}")
