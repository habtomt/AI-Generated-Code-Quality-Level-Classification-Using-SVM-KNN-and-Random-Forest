"""
Auto-generated Python code
Scenario : Natural Language Processing
Prompt   : response_002.txt
Run      : 2
"""

# Required libraries for entity recognition
from spacy import displacy
import spacy
from spacy import displacy
import en_core_web_sm
import re

# Load the English language model
nlp = en_core_web_sm.load()

# Sample text to perform entity recognition
text = """
Apple is a technology company founded on April 1, 1976, by Steve Jobs and Steve Wozniak. 
It is headquartered in Cupertino, California, and is one of the world's largest technology companies.
"""

# Process the text using the language model
doc = nlp(text)

# Print the recognized entities
for entity in doc.ents:
    print(f"{entity.text}: {entity.label_}")

# Function to classify entities
def classify_entities(text):
    try:
        # Process the text using the language model
        doc = nlp(text)
        
        # Initialize an empty dictionary to store the entities
        entities = {}
        
        # Iterate over the recognized entities
        for entity in doc.ents:
            # Get the entity text and label
            entity_text = entity.text
            entity_label = entity.label_
            
            # Classify the entity based on its label
            if entity_label == "PERSON":
                entities['name'] = entity_text
            elif entity_label == "DATE":
                entities['date'] = entity_text
            elif entity_label == "ORG":
                entities['organization'] = entity_text
            elif entity_label == "GPE":
                entities['location'] = entity_text
            else:
                entities['other'] = entity_text
        
        # Return the classified entities
        return entities
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return None

# Test the function
print(classify_entities(text))