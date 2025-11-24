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
