from typing import List, Dict

from abstract_analysis import AbstractAnalysis
from product import Product
from market_report import MarketReport


class TrendIntegrationEngine:
    """
    Coordinates trend analysis workflows across the application.

    Responsibilities:
    - Run validation across analysis modules
    - Execute summaries and predictions
    - Attach trend scores to Product objects
    - Generate integrated market reports

    This class represents the Trend App Integration Lead role.
    """

    def __init__(self, analyses: List[AbstractAnalysis]):
        self.analyses = analyses

    def run_validation(self) -> bool:
        """Validate all registered analysis modules."""
        for analysis in self.analyses:
            analysis.validate()
        return True

    def collect_summaries(self) -> List[Dict]:
        """Collect summaries from all analyses."""
        return [analysis.summarize() for analysis in self.analyses]

    def collect_predictions(self) -> List[Dict]:
        """Collect trend predictions from all analyses."""
        return [analysis.predict() for analysis in self.analyses]

    def attach_trend_scores(
        self,
        products: List[Product],
        trend_key: str = "sales_trend",
    ) -> None:
        """
        Assigns trend scores to products based on analysis output.

        Assumes:
        - analyses[0] is ConsumerTrendAnalysis
        - trend score is derived from slope value
        """
        predictions = self.collect_predictions()
        trend_data = predictions[0].get(trend_key, {})

        slope = trend_data.get("slope", 0)

        for product in products:
            product.trend_score = round(slope * 100, 2)

    def generate_market_report(self, products: List[Product]) -> MarketReport:
        """Generate a MarketReport using integrated trend scores."""
        return MarketReport(products)


def demo_trend_integration(
    engine: TrendIntegrationEngine,
    products: List[Product]
) -> Dict:
    """
    Demonstrates end-to-end integration:
    validation → prediction → product scoring → reporting
    """

    engine.run_validation()
    engine.attach_trend_scores(products)

    report = engine.generate_market_report(products)
    return report.summary()
