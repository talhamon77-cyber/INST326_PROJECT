#test
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
