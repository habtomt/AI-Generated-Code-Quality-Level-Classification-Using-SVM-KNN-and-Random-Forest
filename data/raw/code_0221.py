import re

def analyze_sentiment(text):
    """
    Analyzes the sentiment of a text based on a predefined word lexicon.
    """
    # Lexicon of positive and negative indicators
    positive_words = {
        'love', 'great', 'excellent', 'helpful', 'happy', 'good', 'amazing', 
        'wonderful', 'fantastic', 'best', 'brilliant', 'awesome', 'positive', 
        'impressive', 'success', 'enjoy', 'like', 'perfectly', 'superb'
    }
    
    negative_words = {
        'bad', 'terrible', 'awful', 'disappointed', 'hate', 'worst', 'poor', 
        'fail', 'failure', 'useless', 'broken', 'wrong', 'negative', 'annoying',
        'frustrating', 'boring', 'mistake', 'slow', 'hard', 'difficult'
    }
    
    # Clean and tokenize the text into lowercase words
    words = re.findall(r'\w+', text.lower())
    
    # Calculate counts
    pos_count = sum(1 for word in words if word in positive_words)
    neg_count = sum(1 for word in words if word in negative_words)
    
    # Logic to determine overall sentiment
    if pos_count > neg_count:
        return "Positive"
    elif neg_count > pos_count:
        return "Negative"
    else:
        return "Neutral"

def main():
    # List of sample texts to analyze
    samples = [
        "I love this tool, it is absolutely amazing and helpful!",
        "This is a terrible mistake and I am very disappointed.",
        "The package arrived on Tuesday at four in the afternoon.",
        "The service was good, but the food was bad.",
        "Everything is working perfectly, what a great success!"
    ]
    
    print(f"{'Text':<60} | {'Sentiment':<10}")
    print("-" * 75)
    
    for text in samples:
        sentiment = analyze_sentiment(text)
        print(f"{text[:58]:<60} | {sentiment:<10}")

if __name__ == "__main__":
    main()