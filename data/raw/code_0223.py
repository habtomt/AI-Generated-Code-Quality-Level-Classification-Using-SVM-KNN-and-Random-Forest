import re

def extract_entities(text):
    """
    Identifies and classifies basic entities using pattern matching.
    """
    # Regex patterns for basic entity classification
    patterns = {
        "DATE": r'\b(?:\d{1,2}[/-]\d{1,2}[/-]\d{2,4})|(?:\d{4}[/-]\d{1,2}[/-]\d{1,2})|(?:(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{1,2},? \d{4})\b',
        "ORGANIZATION": r'\b[A-Z][a-z]+ (?:Inc\.|Corp\.|Group|LLC|Solutions|University|Association)\b',
        "NAME": r'\b[A-Z][a-z]+ [A-Z][a-z]+\b'
    }

    results = []
    
    for label, pattern in patterns.items():
        matches = re.finditer(pattern, text)
        for match in matches:
            results.append({
                "entity": match.group(),
                "label": label,
                "start": match.start(),
                "end": match.end()
            })
            
    # Sort results by their position in the text
    return sorted(results, key=lambda x: x['start'])

def main():
    sample_text = """
    John Smith joined Acme Corp. on January 15, 2023. 
    Previously, he worked at Global Solutions LLC until 12/31/2022. 
    Alice Johnson is the lead developer at Tech University.
    """

    print(f"{'Entity':<25} | {'Type':<15} | {'Position':<10}")
    print("-" * 55)

    entities = extract_entities(sample_text)
    
    for item in entities:
        print(f"{item['entity']:<25} | {item['label']:<15} | {item['start']}-{item['end']}")

if __name__ == "__main__":
    main()