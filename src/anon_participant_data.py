from abc import ABC, abstractmethod
# inheritance test suite
# Base class
class Participant(ABC):
    def __init__(self, name, age, email):
        self.name = name
        self.age = age
        self.email = email

    @abstractmethod
    def get_info(self):
        pass

    def anonymize(self):
        return {"age": self.age}

# StudentParticipant 
class StudentParticipant(Participant):
    def __init__(self, name, age, email, school):
        super().__init__(name, age, email)
        self.school = school

    def get_info(self):
        return f"Student: {self.name}, Age: {self.age}, School: {self.school}"

    def anonymize(self):
        data = super().anonymize()
        data["role"] = "student"
        return data
    def participant_from_email(name, age, email):
        if email.lower().endswith(".edu"):
            return StudentParticipant(name, age, email)
        else:
            return AdultParticipant(name, age, email)
# AdultParticipant
class AdultParticipant(Participant):
    def __init__(self, name, age, email, occupation):
        super().__init__(name, age, email)
        self.occupation = occupation

    def get_info(self):
        return f"Adult: {self.name}, Age: {self.age}, Occupation: {self.occupation}"

    def anonymize(self):
        data = super().anonymize()
        data["role"] = "adult"
        return data

# Seniorparticipant
class SeniorParticipant(Participant):
    def __init__(self, name, age, email, retirement_status):
        super().__init__(name, age, email)
        self.retirement_status = retirement_status

    def get_info(self):
        return f"Senior: {self.name}, Age: {self.age}, Retired: {self.retirement_status}"

    def anonymize(self):
        data = super().anonymize()
        data["role"] = "senior"
        return data

# Anonymizing for participant data
def anonymize_participant_data(participants):
    return [p.anonymize() for p in participants]

# Example usage
participants = [
    StudentParticipant("Danieshia", 20, "dmaragh1@terpmail.umd.edu", "University of Maryland"),
    AdultParticipant("Ash", 35, "ashley123@email.com", "Teacher"),
    SeniorParticipant("Katie", 70, "katie@email.com", True)
]

for p in participants:
    print(p.get_info())

print("\nAnonymized data:")
print(anonymize_participant_data(participants))

# Data validation, statistical summaries, and trend prediction
# Project 3

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


