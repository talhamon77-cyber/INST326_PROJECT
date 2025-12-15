import unittest

from trend_integration_engine import TrendIntegrationEngine
from abstract_analysis import AbstractAnalysis
from product import Product


class FakeAnalysis(AbstractAnalysis):
    """Concrete test implementation of AbstractAnalysis."""

    def validate(self) -> bool:
        return True

    def summarize(self):
        return {"status": "ok"}

    def predict(self):
        return {
            "sales_trend": {
                "slope": 0.25
            }
        }


class TestTrendIntegrationEngine(unittest.TestCase):

    def test_engine_end_to_end_with_real_dependencies(self):
        # Arrange
        analysis = FakeAnalysis()
        engine = TrendIntegrationEngine([analysis])

        products = [
            Product("Product A"),
            Product("Product B"),
        ]

        # Act
        valid = engine.run_validation()
        engine.attach_trend_scores(products)
        report = engine.generate_market_report(products)
        summary = report.summary()

        # Assert
        self.assertTrue(valid)

        for product in products:
            self.assertEqual(product.trend_score, 25.0)

        self.assertIn("total_products", summary)
        self.assertEqual(summary["total_products"], 2)


if __name__ == "__main__":
    unittest.main()
