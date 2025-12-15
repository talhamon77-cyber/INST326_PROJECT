class Product:
    def __init__(self, name: str):
        self.name = name
        self.trend_score = None

    def __repr__(self):
        return f"Product(name={self.name}, trend_score={self.trend_score})"
