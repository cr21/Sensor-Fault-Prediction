from sensor.logger import logging
from sensor.exception import SensorException
from sensor.entity.config_entity import ModelEvaluationConfig
from sensor.entity.artifact_entity import ModelTrainerArtifact, DataValidationArtifact, DataIngestionArtifact, ModelEvaluationArtifact
import os
from sensor.ml.metric.classification_metric import get_classifiaction_score
from sensor.ml.model.estimator import SensorModel
from sensor.utils.main_utils import save_object,load_object, write_yaml_file
from sensor.ml.model.estimator import ModelResolver
import pandas as pd
from sensor.constant.training_pipeline import TARGET_COLUMN
from sensor.ml.model.estimator import TargetValueMapping

class ModelEvalution:
    def __init__(self, model_evaluation_config:ModelEvaluationConfig, model_trainer_artifact:ModelTrainerArtifact,data_validation_artifact:DataValidationArtifact) -> None:
        self.model_evaluation_config = model_evaluation_config
        self.model_trainer_artifact= model_trainer_artifact
        self.data_validation_artifact=data_validation_artifact


    def initiate_model_evaluation(self, model_trainer_artifact:ModelTrainerArtifact)->ModelEvaluationArtifact:
        try:
            logging.info("Model Evaluation starts")
            valid_train_file_path = self.data_validation_artifact.valid_train_file_path
            valid_test_file_path=self.data_validation_artifact.valid_test_file_path

            train_df = pd.read_csv(valid_train_file_path)
            test_df = pd.read_csv(valid_test_file_path)

            df = pd.concat([train_df, test_df], axis=0)

            model_resolver = ModelResolver()
            is_model_accepted = True
            trained_model_path:str = self.model_trainer_artifact.trained_model_file_path
            if not model_resolver.is_model_exists():
                
                model_eval_artifact = ModelEvaluationArtifact(
                    is_model_accepted= is_model_accepted,
                    improved_accuracy=None,
                    best_model_path=None,
                    best_model_metric_artifact= None,
                    train_model_metric_artifact=self.model_trainer_artifact.test_metric_artifact,
                    trained_model_path=trained_model_path
                )
                logging.info(f"Best Model Not Availabel, returning Current Model details {model_eval_artifact}")
                return model_eval_artifact

            latest_model_file_path = model_resolver.get_best_model()
            latest_model:SensorModel = load_object(file_path=latest_model_file_path)
            logging.info(f"latestmodel type {type(latest_model)}")
            trained_model:SensorModel= load_object(file_path=trained_model_path)

            y_true = df[TARGET_COLUMN]
            # transform target string label to int label
            y_true.replace(TargetValueMapping().to_dict(), inplace=True)
            # drop target column
            df.drop(TARGET_COLUMN,axis=1, inplace=True)
            
            y_trained_pred = trained_model.predict(df)
            y_latest_pred = latest_model.predict(df)

            # get trained model metric

            trained_metric = get_classifiaction_score(y_true, y_trained_pred)
            latest_metric = get_classifiaction_score(y_true, y_latest_pred)

            improved_metric_score =  trained_metric.f1_score  - latest_metric.f1_score
            if  improved_metric_score > self.model_evaluation_config.eval_threshold:
                is_model_accepted = True
            else:
                is_model_accepted = False

            model_eval_artifact = ModelEvaluationArtifact(
                    is_model_accepted= is_model_accepted,
                    improved_accuracy=improved_metric_score,
                    best_model_path=latest_model_file_path,
                    best_model_metric_artifact= latest_metric,
                    train_model_metric_artifact=trained_metric,
                    trained_model_path=trained_model_path
                )

            model_eval_report = model_eval_artifact.__dict__
            logging.info(f"Model evaluation artifact generated: {model_eval_artifact}")
            write_yaml_file(self.model_evaluation_config.report_File_path, model_eval_report, True)
            return model_eval_artifact

        except Exception as exp:
            raise SensorException(exp)
        


