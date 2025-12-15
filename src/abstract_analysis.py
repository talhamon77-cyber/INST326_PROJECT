from abc import ABC, abstractmethod
from typing import Dict

class AbstractAnalysis(ABC):

    @abstractmethod
    def validate(self) -> bool:
        pass

    @abstractmethod
    def summarize(self) -> Dict:
        pass

    @abstractmethod
    def predict(self) -> Dict:
        pass
