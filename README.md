# Consumer Market Trend Analysis System

## Project Overview
This project is a complete Information Science application designed to help businesses
analyze consumer and product data in order to identify patterns and predict future market trends.
The system integrates object-oriented design, data persistence, testing, and reporting
into a cohesive, end-to-end solution.

The application supports physical and digital products, calculates trend scores using
polymorphic behavior, generates market reports, and persists data between sessions.

This project serves as the capstone for INST326 and demonstrates professional software
development practices.

---

## Team Members
 Talha Muhammad - Product performance and insights functions
- Alexandra Rodriguez - Text and data processing utilities including keyword extraction, CSV parsing, and URL validation
- Anneliese Leo - formatting search results, generating data reports, and calculating relevance scores
- Danieshia Maragh - Anonymized participant data, cleaned content, and generated returned report information
- Ariana Saenz - Data validation, statistical summaries, and trend prediction

---

## Domain Problem
Businesses often collect large amounts of sales and customer engagement data but lack
tools to transform that data into actionable insights.  
This system retrieves product data, analyzes performance metrics, and produces ranked
reports to support decision-making and trend prediction.

---

## Key Features
- Object-oriented product hierarchy with inheritance and polymorphism
- Trend score analysis for physical and digital products
- Data persistence using JSON
- Import products from JSON or CSV
- Export market reports to JSON
- Unit, integration, and system testing
- Modular, maintainable architecture

---

Running the Application

From the repository root:

python trend_app.py


The application will:

Load saved products (if they exist)

Add sample products if none are found

Generate a market report

Export the report

Save system state

Running Tests
python -m unittest discover


All tests must pass before submission.

Video Presentation

📽️ Video link:

AI Collaboration

AI tools were used to assist with:

Code scaffolding

Debugging

Documentation structure

All AI-generated content was reviewed, modified, and validated by the team.
Final responsibility for correctness and design decisions rests with the team.
