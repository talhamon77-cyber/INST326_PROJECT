from typing import List, Dict, Callable
from abc import ABC, abstractmethod

# Abstract Product Base Class
class Product(ABC):
    """
    Abstract base class for all products.
    This defines what every Product must have:
    - a name, a trend_score, and a product_type() method
    """

    def __init__(self, name: str, trend_score: float):
        # Common attributes shared by all products
        self.name = name
        self.trend_score = trend_score

    @abstractmethod
    def product_type(self) -> str:
        """
        Must be implemented by all subclasses.
        Returns the type of product (e.g. 'physical', 'digital').
        """
        pass

# Product Implementations
class PhysicalProduct(Product):     # Represents a physical product that has weight.
    def __init__(self, name: str, trend_score: float, weight_kg: float):
        # Call the parent (Product) constructor
        super().__init__(name, trend_score)
        self.weight_kg = weight_kg

    def product_type(self) -> str:     # Required implementation of abstract method
        return "physical"

class DigitalProduct(Product):     # Represents a digital product that has a file size.
    def __init__(self, name: str, trend_score: float, file_size_mb: float):
        # Call the parent (Product) constructor
        super().__init__(name, trend_score)
        self.file_size_mb = file_size_mb

    def product_type(self) -> str:     # Required implementation of abstract method
        return "digital"

# Market Report (Composition)
class MarketReport:
    # contains a list of Product objects and performs analysis on them
    def __init__(self, products: List[Product]):
        # Store the list of products
        # This is composition (has-a relationship)
        self.products = products

    def average_trend_score(self) -> float:     # Calculate and return the average trend score of all products in the report.
        # If there are no products, avoid division by zero
        if not self.products:
            return 0.0

        # Add up all trend scores and divide by count
        total = sum(p.trend_score for p in self.products)
        return total / len(self.products)

    def top_product(self) -> Product | None:      # Return the product with the highest trend score.
        # Returns None if there are no products.
        if not self.products:
            return None

        # max() finds the item with the highest value
        # key tells Python what value to compare
        return max(self.products, key=lambda p: p.trend_score)

    def summary(self) -> Dict:      # Return a summary dictionary of the report.
        top = self.top_product()

        return {
            # Total number of products in the report
            "total_products": len(self.products),

            # Average trend score across all products
            "average_trend_score": self.average_trend_score(),

            # Name of the top product (if one exists)
            "top_product": top.name if top else None,
        }

    def ranked_products(
        self,
        key: Callable[[Product], float] = lambda p: p.trend_score,
        descending: bool = True,
    ) -> List[Product]:
        """
        Return products sorted by a given key.
        By default:
        - Sorts by trend_score & Highest score first
        """
        return sorted(
            self.products,
            key=key,
            reverse=descending
        )


def test_market_report_with_mixed_products():
    # Create a list of products with different concrete types
    # Even though they are different classes, they all inherit from Product
    products = [
        PhysicalProduct("Laptop", trend_score=82.5, weight_kg=2.3),
        DigitalProduct("E-Book", trend_score=91.0, file_size_mb=15),
        PhysicalProduct("Headphones", trend_score=76.0, weight_kg=0.4),
    ]

    # Create a MarketReport using the list of products
    report = MarketReport(products)    # MarketReport does NOT care what type of product each one is

    # Test average trend score
    expected_average = (82.5 + 91.0 + 76.0) / 3    # Calculate the expected average manually

    # Check that MarketReport calculates the same value
    assert report.average_trend_score() == expected_average

    # Test top product
    top = report.top_product()    # Get the product with the highest trend score

    # The E-Book has the highest trend score (91.0)
    assert top.name == "E-Book"

    # Polymorphism check:
    # Even though 'top' is treated as a Product,
    # the correct subclass method is called
    assert top.product_type() == "digital"

    # Test summary dictionary
    summary = report.summary()    # Generate the summary report

    # Verify the summary contains the correct values
    assert summary["total_products"] == 3
    assert summary["top_product"] == "E-Book"

    # Test optional ranking
    ranked = report.ranked_products()    # Get products ranked by trend score (highest first)

    # Ensure the list is sorted in descending order
    assert ranked[0].trend_score >= ranked[1].trend_score
