#!/usr/bin/env python3

import sys
import re

POSITIVE_WORDS = {
    "good", "great", "excellent", "amazing", "happy", "love", "wonderful",
    "fantastic", "positive", "fortunate", "correct", "superior", "nice", "enjoy"
}

NEGATIVE_WORDS = {
    "bad", "terrible", "awful", "worst", "sad", "hate", "horrible",
    "poor", "negative", "unfortunate", "wrong", "inferior", "angry", "dislike"
}

def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^a-z\s]", "", text)
    return text

def analyze_sentiment(text):
    words = clean_text(text).split()

    pos_count = sum(1 for w in words if w in POSITIVE_WORDS)
    neg_count = sum(1 for w in words if w in NEGATIVE_WORDS)

    if pos_count > neg_count:
        return "positive"
    elif neg_count > pos_count:
        return "negative"
    else:
        return "neutral"

def main():
    if len(sys.argv) > 1:
        text = " ".join(sys.argv[1:])
    else:
        text = input("Enter text: ")

    result = analyze_sentiment(text)
    print(result)

if __name__ == "__main__":
    main()