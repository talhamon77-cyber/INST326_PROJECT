#----------------------------------------
import tempfile
import csv
import json
from pathlib import Path
from anon_participant_data import StudentParticipant, AdultParticipant, SeniorParticipant, anonymize_participant_data
from data_manager import DataManager

def test_import_json_csv_anonymize_and_save():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)
        dm = DataManager(tmpdir)
        
        # 1. Create test JSON file
        json_data = [
            {"type": "student", "name": "Danieshia", "age": 20, "email": "dmaragh1@terpmail.umd.edu", "school": "University of Maryland"},
            {"type": "adult", "name": "Ash", "age": 35, "email": "ashley123@email.com", "occupation": "Teacher"}
        ]
        json_file = tmpdir / "test_input.json"
        with json_file.open("w") as f:
            json.dump(json_data, f)
        
        # 2. Import from JSON
        json_participants, msg = dm.import_participants(json_file)
        print(f"JSON Import: {msg}")
        assert len(json_participants) == 2
        assert json_participants[0].name == "Danieshia"
        assert json_participants[1].occupation == "Teacher"
        
        # 3. Create test CSV file
        csv_file = tmpdir / "test_input.csv"
        with csv_file.open("w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["type", "name", "age", "email", "school", "occupation", "retirement_status"])
            writer.writeheader()
            writer.writerow({"type": "senior", "name": "Katie", "age": 70, "email": "katie@email.com", "retirement_status": "true", "school": "", "occupation": ""})
            writer.writerow({"type": "student", "name": "John", "age": 22, "email": "john@college.edu", "school": "MIT", "occupation": "", "retirement_status": ""})
        
        # 4. Import from CSV
        csv_participants, msg = dm.import_participants(csv_file)
        print(f"CSV Import: {msg}")
        assert len(csv_participants) == 2
        assert csv_participants[0].name == "Katie"
        assert csv_participants[0].retirement_status == True
        assert csv_participants[1].school == "MIT"
        
        # 5. Combine all participants
        all_participants = json_participants + csv_participants
        
        # 6. Load and verify combined data
        print(f"\nAll participants ({len(all_participants)}):")
        for p in all_participants:
            print(f"  {p.get_info()}")
        
        # 7. Anonymize the data
        anonymized = anonymize_participant_data(all_participants)
        print(f"\nAnonymized data:")
        for anon in anonymized:
            print(f"  {anon}")
        
        # 8. Save original participants to JSON
        success, msg = dm.save_participants_to_json(all_participants, "all_participants.json")
        assert success
        print(f"\n{msg}")
        
        # 9. Save anonymized data to JSON
        success, msg = dm.export_report_to_json(
            {"anonymized_participants": anonymized},
            "anonymized_report.json"
        )
        assert success
        print(f"{msg}")
        
        # 10. Verify files exist
        assert (tmpdir / "all_participants.json").exists()
        assert (tmpdir / "anonymized_report.json").exists()
        
        # 11. Load back and verify
        loaded, msg = dm.load_participants_from_json("all_participants.json")
        assert len(loaded) == 4
        print(f"\n{msg}")

if __name__ == "__main__":
    test_import_json_csv_anonymize_and_save()

   # -------------------------------------
  # Data validation, statistical summaries, and trend prediction

from abc import ABC, abstractmethod
from typing import List, Union
import statistics

# Abstract Base Class
class AbstractAnalysis(ABC):
    
    @abstractmethod
    def validate(self) -> bool:
        pass

    @abstractmethod
    def summarize(self) -> dict:
        pass

    @abstractmethod
    def predict(self) -> dict:
        pass

# Implementation
class ConsumerTrendAnalysis(AbstractAnalysis):

    def __init__(self, sales_data: List[float], satisfaction_data: List[float], price_data: List[float]):
        self.sales_data = sales_data
        self.satisfaction_data = satisfaction_data
        self.price_data = price_data

    def validate(self) -> bool:
        for name, data in [("sales", self.sales_data), ("satisfaction", self.satisfaction_data), ("price", self.price_data)]:
            if not data:
                raise ValueError(f"{name} data cannot be empty.")
            if not all(isinstance(x, (int, float)) for x in data):
                raise TypeError(f"{name} data must be numeric.")
            if any(x < 0 for x in data):
                raise ValueError(f"{name} data cannot contain negative values.")
        return True
    
    # Statistical summary
    def summarize(self) -> dict:
        return {
            "sales": self._calc_summary(self.sales_data),
            "satisfaction": self._calc_summary(self.satisfaction_data),
            "price": self._calc_summary(self.price_data)
        }

    def _calc_summary(self, data: List[float]) -> dict:
        return {
            "mean": statistics.mean(data),
            "median": statistics.median(data),
            "stdev": statistics.stdev(data) if len(data) > 1 else 0.0
        }
    
    # Trend prediction
    def predict(self) -> dict:
        return {
            "sales_trend": self._predict_trend(self.sales_data),
            "satisfaction_trend": self._predict_trend(self.satisfaction_data),
            "price_trend": self._predict_trend(self.price_data)
        }

    def _predict_trend(self, data: List[float]) -> dict:
        n = len(data)
        x = list(range(n))
        
        # Calculate means
        x_mean = sum(x) / n
        y_mean = sum(data) / n
        
        # Calculate slope using least squares formula
        numerator = sum((x[i] - x_mean) * (data[i] - y_mean) for i in range(n))
        denominator = sum((x[i] - x_mean) ** 2 for i in range(n))
        
        slope = numerator / denominator if denominator != 0 else 0
        intercept = y_mean - slope * x_mean
        
        # Calculate trend line values
        trend_line = [slope * i + intercept for i in x]
        
        return {
            "slope": slope,
            "intercept": intercept,
            "trend_line": trend_line
        }
sales_data = [100, 120, 140, 160, 180]
satisfaction_data = [7.0, 7.5, 8.0, 8.5, 9.0]
price_data = [50, 52, 54, 56, 58]

# Create analysis object
analysis = ConsumerTrendAnalysis(sales_data, satisfaction_data, price_data)

# Validate
print("Valid:", analysis.validate())

# Get summary
print("\nSummary:")
print(analysis.summarize())

# Get predictions
print("\nPredictions:")
print(analysis.predict())

#----------------------------------------
import unittest
from abstract_product import AbstractProduct


class SimpleProduct(AbstractProduct):
    """Concrete implementation for testing."""
    
    def calculate_trend_score(self) -> float:
        """Simple trend score: sales minus returns times satisfaction."""
        return (self.sales - self.returns) * self.satisfaction


class TestAbstractProduct(unittest.TestCase):
    
    def test_valid_product_creation(self):
        """Test creating a product with valid parameters."""
        print("\n=== Test: Valid Product Creation ===")
        product = SimpleProduct("Test Item", 100, 5, 4.5)
        
        print(f"Created product: {product}")
        print(f"Name: {product.name}")
        print(f"Sales: {product.sales}")
        print(f"Returns: {product.returns}")
        print(f"Satisfaction: {product.satisfaction}")
        
        self.assertEqual(product.name, "Test Item")
        self.assertEqual(product.sales, 100)
        self.assertEqual(product.returns, 5)
        self.assertEqual(product.satisfaction, 4.5)
    
    def test_trend_score_calculation(self):
        """Test that trend score is calculated."""
        print("\n=== Test: Trend Score Calculation ===")
        product = SimpleProduct("Trending Product", 200, 10, 4.0)
        expected = (200 - 10) * 4.0
        
        print(f"Product: {product.name}")
        print(f"Trend score: {product.calculate_trend_score()}")
        
        self.assertEqual(product.calculate_trend_score(), expected)
    
    def test_invalid_name(self):
        """Test that empty name raises ValueError."""
        print("\n=== Test: Invalid Name (Empty String) ===")
        print("Attempting to create product with empty name...")
        
        with self.assertRaises(ValueError):
            SimpleProduct("", 100, 5, 4.5)
    
    def test_invalid_sales(self):
        """Test that zero sales raises ValueError."""
        print("\n=== Test: Invalid Sales (Zero) ===")
        print("Attempting to create product with 0 sales...")
        
        with self.assertRaises(ValueError):
            SimpleProduct("Product", 0, 5, 4.5)
    
    def test_to_dict(self):
        """Test dictionary conversion."""
        print("\n=== Test: Dictionary Conversion ===")
        product = SimpleProduct("Dict Test", 50, 2, 3.5)
        result = product.to_dict()
        
        print(f"Product: {product.name}")
        print(f"Dictionary output: {result}")
        
        self.assertEqual(result["name"], "Dict Test")
        self.assertEqual(result["sales"], 50)
        self.assertEqual(result["returns"], 2)
        self.assertEqual(result["satisfaction"], 3.5)


if __name__ == "__main__":
    unittest.main()

    #-----------------------------------------

from typing import Any, Dict, Type, TypeVar

from abstract_product import AbstractProduct

PhysicalProductType = TypeVar("PhysicalProductType", bound="PhysicalProduct")


class PhysicalProduct(AbstractProduct):
    """
    Product representing a physical good in the marketplace.

    Adds a weight attribute and calculates trend score by penalizing
    return rate and weight (shipping/handling cost proxy).
    """

    def __init__(
        self,
        name: str,
        sales: int,
        returns: int,
        satisfaction: float,
        weight: float,
    ) -> None:
        super().__init__(name=name, sales=sales, returns=returns, satisfaction=satisfaction)

        if not isinstance(weight, (int, float)):
            raise TypeError("weight must be a number")
        if float(weight) <= 0.0:
            raise ValueError("weight must be greater than 0")

        self._weight = float(weight)

    @property
    def weight(self) -> float:
        """float: Product weight in kilograms."""
        return self._weight

    def calculate_trend_score(self) -> float:
        """
        Calculate the trend score for a physical product.

        This is part of the market report.

        Rewards sales and satisfaction; penalizes return rate and weight.

        Returns
        -------
        float
            Trend score (non-negative).
        """
        return_rate = self._returns / self._sales
        base_score = self._sales * 0.1 + self._satisfaction * 20.0
        penalty = return_rate * 50.0 + self._weight * 0.5
        return max(base_score - penalty, 0.0)

    def to_dict(self) -> Dict[str, Any]:
        """Convert this product into a serializable dictionary."""
        data = super().to_dict()
        data.update({"type": "physical", "weight": self._weight})
        return data

    @classmethod
    def from_dict(cls: Type[PhysicalProductType], data: Dict[str, Any]) -> PhysicalProductType:
        """
        Create a PhysicalProduct from a dictionary.

        Required keys: name, sales, returns, satisfaction, weight
        """
        return cls(
            name=data["name"],
            sales=data["sales"],
            returns=data["returns"],
            satisfaction=data["satisfaction"],
            weight=data["weight"],
        )
    
    #test
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

#test
import unittest
from typing import List

# Test PhysicalProduct
class TestPhysicalProduct(unittest.TestCase):
    def test_physical_product_initialization(self):
        product = PhysicalProduct("Laptop", 85.0, 2.5)
        print(f"Physical Product Created: {product.name}")
        print(f"  - Trend Score: {product.trend_score}")
        print(f"  - Weight: {product.weight_kg} kg")
        self.assertEqual(product.name, "Laptop")
        self.assertEqual(product.trend_score, 85.0)
        self.assertEqual(product.weight_kg, 2.5)
    
    def test_physical_product_type(self):
        product = PhysicalProduct("Smartphone", 90.0, 0.2)
        print(f"Product Type: {product.product_type()}")
        self.assertEqual(product.product_type(), "physical")


# Test DigitalProduct
class TestDigitalProduct(unittest.TestCase):
    def test_digital_product_initialization(self):
        product = DigitalProduct("E-Book", 91.0, 15.0)
        print(f"Digital Product Created: {product.name}")
        print(f"  - Trend Score: {product.trend_score}")
        print(f"  - File Size: {product.file_size_mb} MB")
        self.assertEqual(product.name, "E-Book")
        self.assertEqual(product.trend_score, 91.0)
        self.assertEqual(product.file_size_mb, 15.0)
    
    def test_digital_product_type(self):
        product = DigitalProduct("Software", 88.0, 250.0)
        print(f"Product Type: {product.product_type()}")
        self.assertEqual(product.product_type(), "digital")


# Test MarketReport
class TestMarketReport(unittest.TestCase):
    def test_empty_report_average_trend_score(self):
        report = MarketReport([])
        avg = report.average_trend_score()
        print(f"Empty Report Average: {avg}")
        self.assertEqual(avg, 0.0)
    
    def test_empty_report_top_product(self):
        report = MarketReport([])
        top = report.top_product()
        print(f"Empty Report Top Product: {top}")
        self.assertIsNone(top)
    
    def test_empty_report_summary(self):
        report = MarketReport([])
        summary = report.summary()
        print(f"Empty Report Summary:")
        print(f"  - Total Products: {summary['total_products']}")
        print(f"  - Average Score: {summary['average_trend_score']}")
        print(f"  - Top Product: {summary['top_product']}")
        self.assertEqual(summary["total_products"], 0)
        self.assertEqual(summary["average_trend_score"], 0.0)
        self.assertIsNone(summary["top_product"])
    
    def test_single_product_average(self):
        products = [PhysicalProduct("Laptop", 82.5, 2.3)]
        report = MarketReport(products)
        avg = report.average_trend_score()
        print(f"Single Product Report Average: {avg}")
        self.assertEqual(avg, 82.5)
    
    def test_single_product_top(self):
        products = [DigitalProduct("E-Book", 91.0, 15)]
        report = MarketReport(products)
        top = report.top_product()
        print(f"Single Product Top: {top.name} (Score: {top.trend_score})")
        self.assertEqual(top.name, "E-Book")
        self.assertEqual(top.trend_score, 91.0)
    
    def test_multiple_products_average(self):
        products = [
            PhysicalProduct("Laptop", 80.0, 2.0),
            DigitalProduct("E-Book", 90.0, 15),
            PhysicalProduct("Mouse", 70.0, 0.1),
        ]
        report = MarketReport(products)
        avg = report.average_trend_score()
        expected = (80.0 + 90.0 + 70.0) / 3
        print(f"Multiple Products Report:")
        print(f"  - Products: Laptop (80.0), E-Book (90.0), Mouse (70.0)")
        print(f"  - Average Score: {avg:.2f}")
        print(f"  - Expected: {expected:.2f}")
        self.assertEqual(avg, expected)
    
    def test_top_product_selection(self):
        products = [
            PhysicalProduct("Laptop", 82.5, 2.3),
            DigitalProduct("E-Book", 91.0, 15),
            PhysicalProduct("Headphones", 76.0, 0.4),
        ]
        report = MarketReport(products)
        top = report.top_product()
        print(f"Top Product from Mixed Products:")
        print(f"  - Winner: {top.name}")
        print(f"  - Score: {top.trend_score}")
        print(f"  - Type: {top.product_type()}")
        self.assertEqual(top.name, "E-Book")
        self.assertEqual(top.trend_score, 91.0)
    
    def test_top_product_with_ties(self):
        products = [
            PhysicalProduct("Product A", 85.0, 1.0),
            DigitalProduct("Product B", 85.0, 10),
        ]
        report = MarketReport(products)
        top = report.top_product()
        print(f"Top Product with Tie:")
        print(f"  - Winner: {top.name}")
        print(f"  - Score: {top.trend_score}")
        self.assertEqual(top.trend_score, 85.0)
    
    def test_summary_complete(self):
        products = [
            PhysicalProduct("Laptop", 82.5, 2.3),
            DigitalProduct("E-Book", 91.0, 15),
            PhysicalProduct("Headphones", 76.0, 0.4),
        ]
        report = MarketReport(products)
        summary = report.summary()
        
        print(f"Complete Market Report Summary:")
        print(f"  - Total Products: {summary['total_products']}")
        print(f"  - Average Trend Score: {summary['average_trend_score']:.2f}")
        print(f"  - Top Product: {summary['top_product']}")
        
        self.assertEqual(summary["total_products"], 3)
        self.assertEqual(summary["average_trend_score"], (82.5 + 91.0 + 76.0) / 3)
        self.assertEqual(summary["top_product"], "E-Book")
    
    def test_ranked_products_default_descending(self):
        products = [
            PhysicalProduct("C", 70.0, 1.0),
            DigitalProduct("A", 90.0, 10),
            PhysicalProduct("B", 80.0, 2.0),
        ]
        report = MarketReport(products)
        ranked = report.ranked_products()
        
        print(f"Ranked Products (Descending by Trend Score):")
        for i, p in enumerate(ranked, 1):
            print(f"  {i}. {p.name} - Score: {p.trend_score}")
        
        self.assertEqual(ranked[0].trend_score, 90.0)
        self.assertEqual(ranked[1].trend_score, 80.0)
        self.assertEqual(ranked[2].trend_score, 70.0)
    
    def test_ranked_products_ascending(self):
        products = [
            PhysicalProduct("C", 70.0, 1.0),
            DigitalProduct("A", 90.0, 10),
            PhysicalProduct("B", 80.0, 2.0),
        ]
        report = MarketReport(products)
        ranked = report.ranked_products(descending=False)
        
        print(f"Ranked Products (Ascending by Trend Score):")
        for i, p in enumerate(ranked, 1):
            print(f"  {i}. {p.name} - Score: {p.trend_score}")
        
        self.assertEqual(ranked[0].trend_score, 70.0)
        self.assertEqual(ranked[1].trend_score, 80.0)
        self.assertEqual(ranked[2].trend_score, 90.0)
    
    def test_ranked_products_custom_key(self):
        products = [
            PhysicalProduct("Heavy", 70.0, 5.0),
            PhysicalProduct("Light", 90.0, 0.5),
            PhysicalProduct("Medium", 80.0, 2.0),
        ]
        report = MarketReport(products)
        ranked = report.ranked_products(key=lambda p: p.weight_kg)
        
        print(f"Ranked Products (By Weight - Descending):")
        for i, p in enumerate(ranked, 1):
            print(f"  {i}. {p.name} - Weight: {p.weight_kg} kg")
        
        self.assertEqual(ranked[0].weight_kg, 5.0)
        self.assertEqual(ranked[1].weight_kg, 2.0)
        self.assertEqual(ranked[2].weight_kg, 0.5)
    
    def test_ranked_products_custom_key_ascending(self):
        products = [
            PhysicalProduct("Heavy", 70.0, 5.0),
            PhysicalProduct("Light", 90.0, 0.5),
            PhysicalProduct("Medium", 80.0, 2.0),
        ]
        report = MarketReport(products)
        ranked = report.ranked_products(key=lambda p: p.weight_kg, descending=False)
        
        print(f"Ranked Products (By Weight - Ascending):")
        for i, p in enumerate(ranked, 1):
            print(f"  {i}. {p.name} - Weight: {p.weight_kg} kg")
        
        self.assertEqual(ranked[0].weight_kg, 0.5)
        self.assertEqual(ranked[1].weight_kg, 2.0)
        self.assertEqual(ranked[2].weight_kg, 5.0)


# Test Polymorphism
class TestPolymorphism(unittest.TestCase):
    def test_product_type_polymorphism(self):
        products = [
            PhysicalProduct("Laptop", 82.5, 2.3),
            DigitalProduct("E-Book", 91.0, 15),
        ]
        report = MarketReport(products)
        
        print(f"Polymorphism Test:")
        print(f"  - Product 1: {report.products[0].name} is {report.products[0].product_type()}")
        print(f"  - Product 2: {report.products[1].name} is {report.products[1].product_type()}")
        
        self.assertEqual(report.products[0].product_type(), "physical")
        self.assertEqual(report.products[1].product_type(), "digital")
    
    def test_top_product_polymorphism(self):
        products = [
            PhysicalProduct("Laptop", 82.5, 2.3),
            DigitalProduct("E-Book", 91.0, 15),
        ]
        report = MarketReport(products)
        top = report.top_product()
        
        print(f"Top Product Statistics:")
        print(f"  - Top Product: {top.name}")
        print(f"  - Type: {type(top).__name__}")
        print(f"  - Product Type Method Returns: {top.product_type()}")
        
        self.assertIsInstance(top, DigitalProduct)
        self.assertEqual(top.product_type(), "digital")


if __name__ == '__main__':
    unittest.main(verbosity=0)
