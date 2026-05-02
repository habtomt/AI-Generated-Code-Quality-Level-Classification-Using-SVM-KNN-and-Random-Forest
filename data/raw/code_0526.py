"""
Auto-generated Python code
Scenario : Natural Language Processing
Prompt   : response_002.txt
Run      : 3
"""

# Import required libraries
import spacy
from spacy import displacy
from spacy.matcher import Matcher
from spacy.tokens import Span
import datetime

# Load the spaCy model for entity recognition
nlp = spacy.load("en_core_web_sm")  # Use a language model of your choice

# Define a function to identify and classify key entities in text
def identify_entities(text):
    try:
        # Process the text using spaCy
        doc = nlp(text)

        # Define a function to match entities (e.g., names, dates, organizations)
        def match_entities(doc, label):
            # Create a matcher for the entities
            matcher = Matcher(nlp.vocab)
            pattern = [{"ENT_TYPE": label}]
            matcher.add(label, [pattern])
            matches = matcher(doc)
            entities = []
            for match_id, start, end in matches:
                span = doc[start:end]
                entities.append((span.text, span.label_))
            return entities

        # Identify and classify key entities (e.g., names, dates, organizations)
        entities = []
        entities.extend(match_entities(doc, "PERSON"))  # Names
        entities.extend(match_entities(doc, "DATE"))  # Dates
        entities.extend(match_entities(doc, "ORG"))  # Organizations

        # Print the identified entities
        for entity in entities:
            print(f"{entity[0]}: {entity[1]}")

    except Exception as e:
        print(f"Error: {str(e)}")

# Test the function with a sample text
text = "Apple is a global technology company founded on April 1, 1976, by Steve Jobs and Steve Wozniak."
identify_entities(text)