
from sklearn.pipeline import Pipeline
class TargetValueMapping:
    def __init__(self):
        self.neg: int = 0
        self.pos: int = 1

    def to_dict(self):
        return self.__dict__

    def reverse_mapping(self):
        mapping_response = self.to_dict()
        return dict(zip(mapping_response.values(), mapping_response.keys()))


class SensorModel:

    def __init__(self, preproessor:Pipeline, model):
        try:
            self.preproessor=preproessor
            self.model=model
        except Exception as exp:
            raise exp
    
    def predict(self, X):
        try:
            X_transform=self.preproessor.transform(X)
            y_pred = self.model.predict(X_transform)
            return y_pred
        except Exception as exp:
            raise exp