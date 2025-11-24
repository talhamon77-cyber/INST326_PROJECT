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

## System Architecture - Danieshia Maragh

### Inheritence Hierarchies

##### Participant Hierarchy
```
ParticipantAnonymizer (Abstract Base Class)
├── StudentParticipant
├── ChildParticipant 
└── ElderParticipant 
```

#### TextClean Hierarchy
```
Textclean (Abstract Base Class)
├── Characters 
├── Punctuation 
└── Stripped 
```
### Composition Relationships
```
- **Cleaning** contains:
  - Collection of letters (has-many)
  - Removal of white/extra spaces (has-many)
  - Lowercase letters (has-many)

  - **Limit** contains:
  - Child participant age (has-a)
  - Senior participant age (has-a)
  - Student participant age (has-a)
```
  ## Key Features

### 1. Polymorphic Behavior
Same method calls produce different results based on object type:
- `calculate_student()` - need to have a student email
- `calculate_child()` - must have parents with them
- `calculate_elder()`  - has to show id
- `get_age_requirement()` - different requirements based on age (except for students)

### 2. Abstract Base Classes
Enforce consistent interfaces across implementations:
- **ParticipantAnonymizer** - Requires age, person, and email methods
- **TextClean** - Requires punctuation, lowercase, and stripping methods

### 3. Composition Over Inheritance
- Cleaning coordinates multiple object types
- Limit links participants and age without inheritance
- Flexible "has-a" relationships enable system scalability

### Usage Examples

## Creating Participant Anonymizer
```
participants = [
    StudentParticipant("Danieshia", 20, "dmaragh1@terpmail.umd.edu", "University of Maryland"),
    AdultParticipant("Ash", 35, "ashley123@email.com", "Teacher"),
    SeniorParticipant("Katie", 70, "katie@email.com", True)
]

for p in participants:
    print(p.get_info())

#Age calculation
print(StudentParticipant.calculate_age()) # 20
print(AdultParticipant.calculate_age())  # 35
print(Seniorparticipant.calculate_age()) # 70
```
