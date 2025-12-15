# Data validation, statistical summaries, and trend prediction

from abc import ABC, abstractmethod
from typing import List, Union
import statistics
 # Abstract Base Class
class AbstractAnalysis(ABC):
    
    @abstractmethod
    def validate(self) -> bool:
        pass

    @abstractmethod
    def summarize(self) -> dict:
        pass

    @abstractmethod
    def predict(self) -> dict:
        pass

# Implementation
class ConsumerTrendAnalysis(AbstractAnalysis):

    def __init__(self, sales_data: List[float], satisfaction_data: List[float], price_data: List[float]):
        self.sales_data = sales_data
        self.satisfaction_data = satisfaction_data
        self.price_data = price_data

    def validate(self) -> bool:
        for name, data in [("sales", self.sales_data), ("satisfaction", self.satisfaction_data), ("price", self.price_data)]:
            if not data:
                raise ValueError(f"{name} data cannot be empty.")
            if not all(isinstance(x, (int, float)) for x in data):
                raise TypeError(f"{name} data must be numeric.")
            if any(x < 0 for x in data):
                raise ValueError(f"{name} data cannot contain negative values.")
        return True
# Statistical summary
    def summarize(self) -> dict:
        return {
            "sales": self._calc_summary(self.sales_data),
            "satisfaction": self._calc_summary(self.satisfaction_data),
            "price": self._calc_summary(self.price_data)
        }

    def _calc_summary(self, data: List[float]) -> dict:
        return {
            "mean": statistics.mean(data),
            "median": statistics.median(data),
            "stdev": statistics.stdev(data) if len(data) > 1 else 0.0
        }
    
# Trend prediction
    def predict(self) -> dict:
        return {
            "sales_trend": self._predict_trend(self.sales_data),
            "satisfaction_trend": self._predict_trend(self.satisfaction_data),
            "price_trend": self._predict_trend(self.price_data)
        }

    def _predict_trend(self, data: List[float]) -> dict:
        x = np.arange(len(data))
        y = np.array(data)
        coef = np.polyfit(x, y, 1)
        trend_line = np.polyval(coef, x)
        return {"slope": coef[0], "intercept": coef[1], "trend_line": trend_line.tolist()}
