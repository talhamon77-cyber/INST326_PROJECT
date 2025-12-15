"""
demo.py
Run with: python demo.py

Demonstrates:
- AbstractProduct + Physical/Digital products
- MarketReport analysis
- Trend integration
"""

from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from market_report import MarketReport
from trend_integration_engine import TrendIntegrationEngine


def main():
    print("=== MARKET REPORT DEMO ===\n")

    # Create products using your real classes
    products = [
        PhysicalProduct(
            name="Laptop",
            sales=120,
            returns=10,
            satisfaction=4.6,
            weight=2.3
        ),
        DigitalProduct(
            name="E-Book",
            sales=300,
            returns=5,
            satisfaction=4.9,
            file_size=15
        ),
        PhysicalProduct(
            name="Headphones",
            sales=80,
            returns=8,
            satisfaction=4.2,
            weight=0.4
        ),
    ]

    # Show individual trend scores
    print("Products & Trend Scores:")
    for p in products:
        print(f"- {p.name} ({p.__class__.__name__}) → {p.calculate_trend_score():.2f}")

    # Market report
    report = MarketReport(products)

    print("\nMarket Report Summary:")
    summary = report.summary()
    for k, v in summary.items():
        print(f"{k}: {v}")

    # Ranked products
    print("\nRanked Products (Best → Worst):")
    ranked = report.ranked_products()
    for i, p in enumerate(ranked, 1):
        print(f"{i}. {p.name} → {p.calculate_trend_score():.2f}")

    # Trend integration demo
    engine = TrendIntegrationEngine(products)
    integrated = engine.integrate_trends()

    print("\nIntegrated Trend Scores:")
    for name, score in integrated.items():
        print(f"{name}: {score:.2f}")

    print("\n=== DEMO COMPLETE ===")


if __name__ == "__main__":
    main()
