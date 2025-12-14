import unittest

from src.trend_integration_engine import TrendIntegrationEngine
from src.analyses.consumer_trend_analysis import ConsumerTrendAnalysis
from src.products.product import PhysicalProduct, DigitalProduct


class TestTrendIntegrationEngine(unittest.TestCase):

    def test_end_to_end_trend_integration(self):
        analysis = ConsumerTrendAnalysis(
            sales_data=[100, 120, 150],
            satisfaction_data=[4.0, 4.2, 4.5],
            price_data=[20.0, 21.0, 22.0]
        )

        products = [
            PhysicalProduct("Laptop", trend_score=0, weight_kg=2.3),
            DigitalProduct("E-Book", trend_score=0, file_size_mb=15),
        ]

        engine = TrendIntegrationEngine([analysis])

        # Validate
        self.assertTrue(engine.run_validation())

        # Attach trend scores
        engine.attach_trend_scores(products)

        # Ensure products were updated
        for product in products:
            self.assertNotEqual(product.trend_score, 0)

        # Generate report
        report = engine.generate_market_report(products)
        summary = report.summary()

        self.assertEqual(summary["total_products"], 2)
        self.assertIsNotNone(summary["top_product"])


if __name__ == "__main__":
    unittest.main()
