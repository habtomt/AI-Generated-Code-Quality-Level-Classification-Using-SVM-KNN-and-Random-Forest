#!/usr/bin/env python3

import re
import sys

DATE_PATTERNS = [
    r"\b\d{1,2}/\d{1,2}/\d{2,4}\b",
    r"\b\d{1,2}-\d{1,2}-\d{2,4}\b",
    r"\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{1,2}, \d{4}\b"
]

ORG_KEYWORDS = [
    "inc", "ltd", "llc", "corp", "corporation", "university",
    "institute", "company", "co", "agency", "organization"
]

def extract_dates(text):
    dates = []
    for pattern in DATE_PATTERNS:
        dates.extend(re.findall(pattern, text, flags=re.IGNORECASE))
    return list(set(dates))

def extract_orgs(text):
    sentences = re.split(r"[.?!]", text)
    orgs = set()

    for sentence in sentences:
        words = sentence.strip().split()
        for i, word in enumerate(words):
            clean_word = word.lower().strip(",")
            if clean_word in ORG_KEYWORDS:
                orgs.add(sentence.strip())
            if word.endswith(("Inc", "Ltd", "LLC", "Corp", "University", "Institute")):
                orgs.add(sentence.strip())

    return list(orgs)

def extract_names(text):
    words = re.findall(r"\b[A-Z][a-z]+\b", text)
    return list(set(words))

def classify_entities(text):
    return {
        "names": extract_names(text),
        "dates": extract_dates(text),
        "organizations": extract_orgs(text)
    }

def main():
    if len(sys.argv) > 1:
        text = " ".join(sys.argv[1:])
    else:
        text = input("Enter text: ")

    result = classify_entities(text)

    print("\nNamed Entities:")
    print("Names:", result["names"])
    print("Dates:", result["dates"])
    print("Organizations:", result["organizations"])

if __name__ == "__main__":
    main()