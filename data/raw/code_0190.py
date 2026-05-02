import pandas as pd
import matplotlib.pyplot as plt
from textblob import TextBlob

def analyze_sentiment(text):
    analysis = TextBlob(text)
    if analysis.sentiment.polarity > 0:
        return 'Positive'
    elif analysis.sentiment.polarity == 0:
        return 'Neutral'
    else:
        return 'Negative'

def sentiment_trends():
    data = {
        'Date': pd.date_range(start='2023-01-01', periods=10, freq='D'),
        'Post': [
            'I love this new phone!', 'The battery life is terrible.', 
            'It is an okay product.', 'Best purchase ever!', 
            'Worst service I have experienced.', 'Pretty good quality.',
            'Average experience.', 'I am so happy with the results.',
            'Disappointing performance.', 'Not what I expected but fine.'
        ]
    }
    df = pd.DataFrame(data)
    df['Sentiment'] = df['Post'].apply(analyze_sentiment)
    
    sentiment_counts = df['Sentiment'].value_counts()
    
    plt.figure(figsize=(8, 5))
    sentiment_counts.plot(kind='bar', color=['green', 'gray', 'red'])
    plt.title('Brand Sentiment Overview')
    plt.ylabel('Number of Posts')
    plt.show()
    
    print(df[['Date', 'Sentiment']])

if __name__ == "__main__":
    sentiment_trends()
