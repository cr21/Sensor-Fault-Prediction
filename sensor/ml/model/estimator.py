

class TargetValueMapping:
    def __init__(self) -> None:
        self.neg:int=0
        self.pos:int=1


    def to__dict(self):
        retirn self.__dict__


    def reverse_mapping(self):
        mapping_response=self.to__dict
        return dict(zip(mapping_response.values(), mapping_response.keys()))