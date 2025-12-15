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
