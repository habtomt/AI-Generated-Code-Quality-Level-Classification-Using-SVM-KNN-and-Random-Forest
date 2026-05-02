#!/usr/bin/env python3

import sys
import re
from collections import Counter

def tokenize_sentences(text):
    return re.split(r'(?<=[.!?])\s+', text.strip())

def tokenize_words(text):
    return re.findall(r'\b[a-zA-Z]+\b', text.lower())

def build_word_frequencies(words):
    stopwords = {
        "the","is","in","and","to","a","of","it","for","on","with","as","this",
        "that","was","are","at","by","an","be","or","from","which","but","not"
    }
    filtered = [w for w in words if w not in stopwords]
    return Counter(filtered)

def score_sentences(sentences, freq):
    scores = []
    for sentence in sentences:
        words = tokenize_words(sentence)
        if not words:
            continue
        score = sum(freq[w] for w in words)
        scores.append((score, sentence))
    return scores

def summarize(text, max_sentences=3):
    sentences = tokenize_sentences(text)
    words = tokenize_words(text)
    freq = build_word_frequencies(words)
    ranked = score_sentences(sentences, freq)
    ranked.sort(reverse=True, key=lambda x: x[0])
    top = [s for _, s in ranked[:max_sentences]]
    return " ".join(top)

def main():
    if len(sys.argv) > 1:
        text = " ".join(sys.argv[1:])
    else:
        text = input("Enter text: ")

    summary = summarize(text)
    print(summary)

if __name__ == "__main__":
    main()