import re

class ParticipantAnonymizer:
    def __init__(self):
        self.counter = 0

    def _anonymize_contact(self, value: str) -> str:
        if not value:

        email_pattern = r'\S+@\S+\.\S+'
        phone_pattern = r'\+?\d[\d\s\-]{7,}\d'
        value = re.sub(email_pattern, '[HIDDEN]', value)
        value = re.sub(phone_pattern, '[HIDDEN]', value)
        return value

    def anonymize(self, participants: list[dict]) -> list[dict]:
        anonymized = []
        for participant in participants:
            self.counter += 1
            new_participant = {}
            for key, value in participant.items():
                if key.lower() == 'name':
                    new_participant['id'] = f"participant_{self.counter}"
                elif key.lower() in ('email', 'phone'):
                    new_participant[key] = '[HIDDEN]'
                else:
                    new_participant[key] = value
            anonymized.append(new_participant)
        return anonymized

participants = [
    {"name": "Meow", "age": 25, "email": "meow@example.com", "phone": "+1234567890"},
    {"name": "Meowie", "age": 30, "email": "meowie@example.com", "phone": "555-1234-9191"}
]

anonymizer = ParticipantAnonymizer()
anonymized_data = anonymizer.anonymize(participants)
print(anonymized_data)

