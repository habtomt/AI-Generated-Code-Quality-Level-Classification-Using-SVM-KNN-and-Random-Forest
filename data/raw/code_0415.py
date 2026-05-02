"""
Auto-generated Python code
Scenario : Data Visualization
Prompt   : response_003.txt
Run      : 1
"""

# Import necessary libraries
import pandas as pd
from textblob import TextBlob
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# Example data with 'date' and 'text' columns
data = {
    'date': ['2023-09-01', '2023-09-02', '2023-09-03'],
    'text': [
        'I love the new product! It\'s amazing.',
        'The product is okay, nothing special.',
        'I had a terrible experience with the product.'
    ]
}

def main():
    # Create DataFrame
    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date'])

    # Define function for sentiment analysis
    def analyze_sentiment(text):
        # Create TextBlob object
        blob = TextBlob(text)
        # Return sentiment polarity
        return blob.sentiment.polarity

    # Apply sentiment analysis to 'text' column
    df['sentiment'] = df['text'].apply(analyze_sentiment)

    # Define function to classify sentiments
    def classify_sentiment(polarity):
        # Classify sentiment based on polarity score
        if polarity > 0.1:
            return 'Positive'
        elif polarity < -0.1:
            return 'Negative'
        else:
            return 'Neutral'

    # Classify sentiments
    df['sentiment_category'] = df['sentiment'].apply(classify_sentiment)

    try:
        # Group by date and sentiment category
        trend = df.groupby([df['date'], 'sentiment_category']).size().unstack().fillna(0)

        # Plot sentiment trends over time
        trend.plot(kind='line', stacked=False, figsize=(10, 6))
        plt.title('Sentiment Trend Over Time')
        plt.xlabel('Date')
        plt.ylabel('Number of Posts')
        plt.show()

        # Define function to plot wordcloud
        def plot_wordcloud(category):
            # Get text for the category
            text = ' '.join(df[df['sentiment_category'] == category]['text'])
            # Create wordcloud
            wordcloud = WordCloud(width=800, height=400, max_words=100, background_color='white').generate(text)

            # Plot wordcloud
            plt.figure(figsize=(10, 6))
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis('off')
            plt.title(f'Most Common Words in {category} Comments')
            plt.show()

        # Plot wordclouds for each sentiment category
        plot_wordcloud('Positive')
        plot_wordcloud('Negative')
        plot_wordcloud('Neutral')
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()