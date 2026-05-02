"""
Auto-generated Python code
Scenario : Content Moderation & Filtering
Prompt   : response_004.txt
Run      : 1
"""

# Import necessary libraries
import nltk
from nltk.tokenize import word_tokenize
from textblob import TextBlob

# Download required NLTK data if not already downloaded
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
try:
    nltk.data.find('taggers/averaged_perceptron_tagger')
except LookupError:
    nltk.download('averaged_perceptron_tagger')

# Sample list of inflammatory or abusive words
banned_words = {'abuse', 'dumb', 'stupid', 'hate'}

def filter_comment(comment):
    """
    Check if the comment contains banned words or has negative sentiment.
    
    Parameters:
    comment (str): The comment to be filtered.
    
    Returns:
    bool: True if the comment is acceptable, False otherwise.
    """
    # Tokenize the comment
    words = word_tokenize(comment.lower())
    
    # Check for banned words
    for word in words:
        if word in banned_words:
            return False  # Comment is not allowed
    
    # Sentiment analysis for additional checks
    analysis = TextBlob(comment)
    if analysis.sentiment.polarity < -0.5:
        return False  # Comment is likely negative/inflammatory
    
    return True  # Comment is acceptable

# Example usage
comments = [
    "I think this article is stupid and dumb.",
    "I disagree with the points made here, but respect your opinion.",
    "What a wonderful article, very insightful!"
]

filtered_comments = [comment for comment in comments if filter_comment(comment)]

print("Filtered Comments:")
for comment in filtered_comments:
    print("-", comment)

# Extending the filter with a machine learning model
# For this example, we'll use a basic sentiment analysis model
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score

# Sample dataset for training the model
train_comments = [
    ("This is a great article!", 1),  # Positive sentiment
    ("I hate this article.", -1),  # Negative sentiment
    ("The article is okay, I guess.", 0),  # Neutral sentiment
    # Add more samples here...
]

# Separate comments and labels
train_comments_text = [comment for comment, _ in train_comments]
train_comments_labels = [label for _, label in train_comments]

# Split the data into training and test sets
train_text, test_text, train_labels, test_labels = train_test_split(train_comments_text, train_comments_labels, test_size=0.2, random_state=42)

# Create a TF-IDF vectorizer
vectorizer = TfidfVectorizer()

# Fit the vectorizer to the training data and transform both the training and test data
X_train = vectorizer.fit_transform(train_text)
y_train = train_labels
X_test = vectorizer.transform(test_text)

# Train a Naive Bayes classifier
clf = MultinomialNB()
clf.fit(X_train, y_train)

# Make predictions on the test data
y_pred = clf.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(test_labels, y_pred)
print(f"Model Accuracy: {accuracy:.2f}")

# Now you can use this model to enhance the filtering mechanism
def enhanced_filter_comment(comment):
    """
    Check if the comment contains banned words, has negative sentiment, or is classified as negative by the model.
    
    Parameters:
    comment (str): The comment to be filtered.
    
    Returns:
    bool: True if the comment is acceptable, False otherwise.
    """
    # Tokenize the comment
    words = word_tokenize(comment.lower())
    
    # Check for banned words
    for word in words:
        if word in banned_words:
            return False  # Comment is not allowed
    
    # Sentiment analysis for additional checks
    analysis = TextBlob(comment)
    if analysis.sentiment.polarity < -0.5:
        return False  # Comment is likely negative/inflammatory
    
    # Use the machine learning model for classification
    comment_vector = vectorizer.transform([comment])
    prediction = clf.predict(comment_vector)
    if prediction[0] == -1:
        return False  # Comment is classified as negative
    
    return True  # Comment is acceptable

# Example usage with the enhanced filter
enhanced_filtered_comments = [comment for comment in comments if enhanced_filter_comment(comment)]

print("Enhanced Filtered Comments:")
for comment in enhanced_filtered_comments:
    print("-", comment)