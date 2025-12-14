class Normalizer:
    def normalize(self, text: str) -> str:
        raise NotImplementedError("Subclasses must implement normalize()")

class LowercaseNormalizer(Normalizer):
    def normalize(self, text: str) -> str:
        return text.lower()

class UppercaseNormalizer(Normalizer):
    def normalize(self, text: str) -> str:
        return text.upper()

class StudentEmailNormalizer(Normalizer):
    def normalize(self, email: str) -> str:
        email = email.strip().lower()
        if not email.endswith("@terpmail.umd.edu"):
            raise ValueError("Not a valid student email")
        return email

class TextCleaner:
    def __init__(self, normalizer: Normalizer):
        self.normalizer = normalizer 

    def clean(self, text: str) -> str:
        text = text.strip()
        return self.normalizer.normalize(text)


if __name__ == "__main__":
    lower_cleaner = TextCleaner(LowercaseNormalizer())
    upper_cleaner = TextCleaner(UppercaseNormalizer())
    student_cleaner = TextCleaner(StudentEmailNormalizer())

    # Polymorphic cleaning
    print(lower_cleaner.clean("   HeLLo THERE   "))      # "hello there"
    print(upper_cleaner.clean("   HeLLo THERE   "))      # "HELLO THERE"

    # Student email cleaning
    print(student_cleaner.clean("   STUDENT123@TERPMAIL.UMD.EDU   "))
    # Output: "student123@terpmail.umd.edu"

    # Error in this one:
    print(student_cleaner.clean("notstudent@gmail.com"))


# Polymorphic example

class SimpleSalesAnalysis(AbstractAnalysis):

    def __init__(self, sales_data: List[float]):
        self.sales_data = sales_data

    def validate(self) -> bool:
        if not self.sales_data:
            raise ValueError("Sales data cannot be empty.")
        return True

    def summarize(self) -> dict:
        return {"sales_mean": statistics.mean(self.sales_data)}

    def predict(self) -> dict:
        # Simple linear trend
        x = np.arange(len(self.sales_data))
        y = np.array(self.sales_data)
        coef = np.polyfit(x, y, 1)
        trend_line = np.polyval(coef, x)
        return {"slope": coef[0], "intercept": coef[1], "trend_line": trend_line.tolist()}

# Demonstration
analyses = [
    ConsumerTrendAnalysis([100,120,150], [4.0,4.1,4.3], [19.99,20.49,20.99]),
    SimpleSalesAnalysis([100,120,150])
]

for a in analyses:
    a.validate()
    print(a.summarize())
