from sensor.entity.artifact_entity import ClassficationMetricArtifact
from sensor.exception import SensorException
import os, sys
import numpy as np
from sklearn.metrics import f1_score, accuracy_score, precision_score, recall_score
from sensor.logger import logging
def get_classifiaction_score(y_true:np.array, y_pred:np.array)-> ClassficationMetricArtifact:
    try:
        model_f1_score = f1_score(y_true, y_pred)
        model_recall_Score = recall_score(y_true, y_pred)
        model_accuracy_score = accuracy_score(y_true, y_pred)
        model_precision_score = precision_score(y_true, y_pred)

        classification_metric= ClassficationMetricArtifact(
                                model_accuracy_score,
                                model_precision_score,
                                model_recall_Score,
                                model_accuracy_score
            )

        logging.info(f"writing Classification Metric {classification_metric}")
        return classification_metric
    except Exception as exp:
        raise SensorException(exp)