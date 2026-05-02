"""
Auto-generated Python code
Scenario : Natural Language Processing
Prompt   : response_002.txt
Run      : 1
"""

import spacy

# Load the pre-trained model
nlp = spacy.load("en_core_web_sm")

def extract_entities(text):
    # Process the input text
    doc = nlp(text)
    
    # Define a dictionary to hold entities
    entities = {"PERSON": [], "DATE": [], "ORG": []}

    # Iterate over the entities
    for ent in doc.ents:
        if ent.label_ in entities:
            entities[ent.label_].append(ent.text)

    return entities

# Example text
text = """
Apple Inc. was founded by Steve Jobs, Steve Wozniak, and Ronald Wayne on April 1, 1976. 
The company was later incorporated as Apple Computer, Inc. on January 3, 1977. 
In 2021, Tim Cook is the CEO of the company.
"""

# Extract and print entities
entities = extract_entities(text)
for entity_type, values in entities.items():
    print(f"{entity_type}: {values}")


# Example usage with user input
def main():
    text = input("Enter a text: ")
    entities = extract_entities(text)
    
    print("\nExtracted entities:")
    for entity_type, values in entities.items():
        print(f"{entity_type}: {values}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"An error occurred: {str(e)}")