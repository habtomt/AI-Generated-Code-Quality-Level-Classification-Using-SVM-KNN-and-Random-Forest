"""
Auto-generated Python code
Scenario : Natural Language Processing
Prompt   : response_004.txt
Run      : 2
"""

import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize, sent_tokenize
from collections import defaultdict
import string

# Download required NLTK data if not already downloaded
nltk.download('punkt')
nltk.download('stopwords')

# Function to summarize a text document
def summarize_text(text, summary_length=5):
    # Tokenize the text into sentences
    sentences = sent_tokenize(text)
    
    # Tokenize the text into words
    words = word_tokenize(text.lower())
    
    # Remove stopwords and punctuation
    stop_words = set(stopwords.words('english') + list(string.punctuation))
    filtered_words = [word for word in words if word not in stop_words]
    
    # Calculate the word frequency
    word_freq = defaultdict(int)
    for word in filtered_words:
        word_freq[word] += 1
    
    # Calculate the sentence score
    sentence_scores = defaultdict(int)
    for sentence in sentences:
        for word in word_tokenize(sentence.lower()):
            if word in word_freq:
                sentence_scores[sentence] += word_freq[word]
    
    # Sort sentences by score and select top N sentences
    sorted_sentences = sorted(sentence_scores.items(), key=lambda x: x[1], reverse=True)
    summary = ' '.join([sentence for sentence, _ in sorted_sentences[:summary_length]])
    
    return summary

# Example usage:
text = """
Lorem ipsum dolor sit amet, consectetur adipiscing elit. 
Phasellus malesuada augue eu nulla lacinia, 
sit amet vulputate ex lacinia. 
Nulla facilisi. 
Sed et nulla at tellus interdum blandit et nec arcu. 
Proin sit amet felis sit amet erat malesuada congue. 
Nulla facilisi. 
Cras ultrices ligula sed magna dictum porta. 
Sed diam donec adipiscing tristique eu tristique 
sit amet sapien. 
Nulla facilisi. 
Sed et nulla at tellus interdum blandit et nec arcu. 
Proin sit amet felis sit amet erat malesuada congue.
"""
print(summarize_text(text))