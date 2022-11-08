from sensor.configuration.mongo_db_connection import MongoDBConnector
from sensor.constant.database import DATABASE_NAME
from sensor.exception import SensorException
from sensor.logger import logging
import os, sys
from io import BytesIO
from sensor.ml.model.estimator import SensorModel
from sensor.entity.config_entity import TrainingPipelineConfig
from sensor.pipeline.training_pipeline import TrainPipeline
from fastapi import FastAPI,UploadFile
from sensor.utils.main_utils import read_yaml_file
from sensor.constant.application import APP_HOST, APP_PORT
from starlette.responses import RedirectResponse
from sensor.constant.training_pipeline import SAVED_MODEL_DIR
from uvicorn import run as app_run
from fastapi.responses import Response
from sensor.ml.model.estimator import ModelResolver,TargetValueMapping
from sensor.utils.main_utils import load_object
from fastapi.middleware.cors import CORSMiddleware
from sensor.utils.main_utils import read_yaml_file
from sensor.constant.training_pipeline import TARGET_COLUMN,SCHEMA_FILE_PATH
import pandas as pd


env_file_path=os.path.join(os.getcwd(),"env.yaml")

def set_env_variable(env_file_path):

    if os.getenv('MONGO_DB_URL',None) is None:
        env_config = read_yaml_file(env_file_path)
        os.environ['MONGO_DB_URL']=env_config['MONGO_DB_URL']



app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")

@app.get("/train")
async def train_route():
    try:

        train_pipeline = TrainPipeline()
        if train_pipeline.is_pipeline_running:
            return Response("Training pipeline is already running.")
        train_pipeline.run_pipeline()
        return Response("Training successful !!")
    except Exception as e:
        return Response(f"Error Occurred! {e}")





@app.post("/predict")
async def predict_route(file:UploadFile):
    try:
        #get data from user csv file
        #conver csv file to dataframe
        if not file.filename.endswith(".csv"):
            raise Response(f"Please upload csv file {e}")
        file_contents = await file.read()

        buffer = BytesIO(file_contents)
        df = pd.read_csv(buffer)
        buffer.close()
        file.file.close()
        logging.info(type(df), df.shape)


        
        model_resolver = ModelResolver(model_dir=SAVED_MODEL_DIR)
        if not model_resolver.is_model_exists():
            return Response("Model is not available")
        
        # drop target column
        df.drop(TARGET_COLUMN, axis=1, inplace=True)
        # drop uncessary columns
        dropped_columns = read_yaml_file(SCHEMA_FILE_PATH)

        best_model_path = model_resolver.get_best_model()
        model:SensorModel = load_object(file_path=best_model_path)
        y_pred = model.predict(df)
        df['predicted_column'] = y_pred
        df['predicted_column'].replace(TargetValueMapping().reverse_mapping(),inplace=True)
        
        #decide how to return file to user.
    except Exception as e:
        raise Response(f"Error Occured! {e}")



def main():
    try:
        
        train_pipeline=TrainPipeline()
        train_pipeline.run_pipeline()
        
        
    except Exception as e:
        print(e)
        logging.exception(e)
        raise SensorException(e)
        


if __name__ == '__main__':
   main()
#    set_env_variable(env_file_path=env_file_path)
#    app_run(app, host=APP_HOST, port=APP_PORT)
