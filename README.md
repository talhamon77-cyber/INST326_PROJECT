# Consumer Trend Analysis Library

## Team Members
- Talha Muhammad - Product performance and insights functions
- Alexandra Rodriguez - Text and data processing utilities including keyword extraction, CSV parsing, and URL validation
- Anneliese Leo - formatting search results, generating data reports, and calculating relevance scores
- Danieshia Maragh - Anonymized participant data, cleaned content, and generated returned report information
- Ariana Saenz - Data validation, statistical summaries, and trend prediction

## Domain 
Information retrieval and data management for market trend prediction.

## Course 
INST326-0301 - Object-Oriented Programming for Information Science  

## Project Overview
A Python library to help businesses identify, analyze, and predict future trends in the consumer market based on sales and customer engagement data.

## Problem Statement
- Seeing what was trending in prior years
- Why are certain products more popular than others
- If certain products are more popular at specific times (seasonal)
- Specific pattern to these trends
- Pricing and how it affects consumer rates
- Possible trending topics

## Installation and Setup
1. Clone this repository:
   ```bash
   https://github.com/talhamon77-cyber/INST326_PROJECT.git
   ```

2. No external dependencies required - uses Python standard library only

## Quick Usage Examples

#For Anonymizing data

data = ParticipantData()

data.add_participant("Alice")

data.add_participant("Bob")

print(data.anonymize_participant_data())

#For Cleaning Content

report = ReturnReport()

#Add sales

report.add_sales("P1", 200)

report.add_sales("P2", 50)

report.add_sales("P3", 120)

#Add returns

report.add_return("P1", 4)

report.add_return("P2", 2)

report.add_return("P3", 10)

#Show only the formatted report

report.display_report()

#For cleaning text

#Sample data

data = [
"Apple pie recipe",

"Banana smoothie",

"Python tutorial",

"Cherry tart",

"Learn Java",

"Random note"

]

#Functions to check categories

def is_fruit(text):
    
   return any(fruit in text for fruit in ["apple", "banana", "cherry"])

def is_programming(text):
    
   return any(lang in text for lang in ["python", "java"])

#Define category rules

categories = {
    
   "fruits": is_fruit,
    
   "programming": is_programming
   
}

#Create organizer

organizer = TextOrganizer()

organizer.clean_text_content(data, categories)

#Display only the formatted report
