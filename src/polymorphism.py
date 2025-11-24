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
