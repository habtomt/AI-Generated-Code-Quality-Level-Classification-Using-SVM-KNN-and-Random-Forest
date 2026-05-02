import re
from collections import Counter

def summarize_text(text, num_sentences=2):
    """
    Summarizes text using a frequency-based extractive algorithm.
    """
    # Normalize and split into words to calculate frequencies
    words = re.findall(r'\w+', text.lower())
    
    # Filter common stop words (simplified list)
    stop_words = {
        'the', 'and', 'is', 'i', 'it', 'in', 'to', 'of', 'a', 'was', 'for', 
        'on', 'with', 'as', 'at', 'by', 'an', 'be', 'this', 'that', 'are'
    }
    
    word_frequencies = Counter(word for word in words if word not in stop_words)
    
    # Normalize frequencies
    if not word_frequencies:
        return text
    
    max_freq = max(word_frequencies.values())
    for word in word_frequencies:
        word_frequencies[word] /= max_freq

    # Split into sentences using basic punctuation
    sentences = re.split(r'(?<=[.!?]) +', text.strip())
    sentence_scores = {}

    for sentence in sentences:
        sentence_words = re.findall(r'\w+', sentence.lower())
        score = sum(word_frequencies.get(word, 0) for word in sentence_words)
        sentence_scores[sentence] = score

    # Sort sentences by score and pick the top N
    summary_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)[:num_sentences]
    
    # Re-order summary sentences to match original document flow
    summary = ' '.join(s for s in sentences if s in summary_sentences)
    return summary

def main():
    document = """
    Python is a high-level, interpreted programming language known for its readability and versatility. 
    It was created by Guido van Rossum and first released in 1991. 
    The design philosophy of Python emphasizes code readability with its notable use of significant whitespace. 
    Its standard library is often cited as one of its greatest strengths, providing tools suited to many tasks. 
    Python is used extensively in data science, artificial intelligence, and web development. 
    Many developers prefer Python because it allows them to express concepts in fewer lines of code than might be possible in languages such as C++ or Java.
    """

    print("--- Original Document ---")
    print(document.strip())
    
    print("\n--- Summary ---")
    summary = summarize_text(document, num_sentences=2)
    print(summary)

if __name__ == "__main__":
    main()