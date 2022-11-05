
from sensor.entity.config_entity import ModelTrainerConfig
from sensor.entity.artifact_entity import DataTransformationArtifact
import numpy as np
from sensor.logger import logging
from sensor.exception import SensorException
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score, roc_auc_score
from sensor.utils.main_utils import write_yaml_file



class ModelTrainer:
    def __init__(self, model_training_config:ModelTrainerConfig, data_transformation_artifact:DataTransformationArtifact) -> None:
        self.model_training_config = model_training_config
        self.data_transformation_artifact= data_transformation_artifact


    def load_transformed_data(self):
        try:
            transformed_train_file_path:str =self.data_transformation_artifact.transformed_train_file_path
            transformed_test_file_path:str =self.data_transformation_artifact.transformed_test_file_path
            # transformed_object_file_path:str=self.data_transformation_artifact.transformed_object_file_path
            train_array=np.load(transformed_train_file_path)
            test_array=np.load(transformed_test_file_path)
            return (train_array, test_array)
        except Exception as exp:
            raise SensorException(exp)

    def get_best_model(self, X_train, y_train):
        try:
            clf = DecisionTreeClassifier(random_state=0)
            # clf = LogisticRegression(solver='saga', max_iter=200)
            clf.fit(X_train, y_train)
            return clf
        except Exception as exp:
            raise SensorException(exp)

    def calculate_metric(self,model, X_test, y_test):
        try:
            accuracy= model.score(X_test, y_test)
            y_pred = model.predict(X_test)
            f1 = f1_score(y_test, y_pred)
            y_prob = model.predict_proba(X_test)[:,1]
            roc_auc = roc_auc_score(y_test,y_prob)
            model_performance={
                                "F1":float(f1),
                                "roc_auc":float(roc_auc),
                                "accuracy":float(accuracy)}
            model_report = {
                "Model": {
                    "name":"LogisticRegression",
                    "metric":model_performance
                }
            }
            
            write_yaml_file(self.model_training_config.best_model_detail_file_path,model_report, replace=True )
            logging.info(f"[F1 => {f1}, roc_auc => {roc_auc} accuracy => {accuracy}")
        except Exception as exp:
            raise SensorException(exp)

    def initiate_model_training(self):
        try:
            # read transformed numpy file
            train_array, test_array =self.load_transformed_data()
            # last column is Target column
            X_train_features = train_array[:,:-1]
            Y_train = train_array[:,-1]
            X_test_features = test_array[:,:-1]
            Y_test=test_array[:,-1]

            # model training
            clf = self.get_best_model(X_train_features, Y_train)
            self.calculate_metric(clf, X_test_features,Y_test)
        except Exception as exp:
            raise SensorException(exp)
        






