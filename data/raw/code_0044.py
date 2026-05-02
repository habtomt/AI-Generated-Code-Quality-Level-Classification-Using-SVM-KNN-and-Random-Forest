#!/usr/bin/env python3

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


positive_words = {
    "good", "great", "excellent", "amazing", "love", "awesome", "fantastic",
    "happy", "satisfied", "perfect", "nice", "positive", "wonderful"
}

negative_words = {
    "bad", "terrible", "awful", "hate", "worst", "poor", "disappointed",
    "sad", "angry", "problem", "negative", "horrible", "ugly"
}


def generate_synthetic_posts(n=500):
    np.random.seed(42)

    timestamps = pd.date_range("2025-01-01", periods=n, freq="H")

    base_texts = [
        "I love this product it is amazing",
        "This is the worst experience I hate it",
        "It is okay not good not bad",
        "Absolutely fantastic and awesome service",
        "Very disappointing and horrible support",
        "Nice and satisfying experience overall",
        "Bad quality and terrible design",
        "Great value and excellent performance",
        "I am happy with this purchase",
        "Not satisfied with the product"
    ]

    texts = np.random.choice(base_texts, size=n)

    df = pd.DataFrame({
        "timestamp": timestamps,
        "text": texts
    })

    return df


def compute_sentiment(text):
    words = text.lower().split()

    score = 0
    for w in words:
        if w in positive_words:
            score += 1
        elif w in negative_words:
            score -= 1

    if score > 0:
        return score, "positive"
    elif score < 0:
        return score, "negative"
    else:
        return score, "neutral"


def analyze_sentiment(df):
    sentiments = df["text"].apply(lambda x: compute_sentiment(x))

    df["score"] = sentiments.apply(lambda x: x[0])
    df["label"] = sentiments.apply(lambda x: x[1])

    return df


def plot_sentiment_distribution(df):
    counts = df["label"].value_counts()

    plt.figure()
    plt.bar(counts.index, counts.values)
    plt.title("Sentiment Distribution")
    plt.xlabel("Sentiment")
    plt.ylabel("Count")
    plt.show()


def plot_sentiment_trend(df):
    df["date"] = df["timestamp"].dt.date
    trend = df.groupby("date")["score"].mean()

    plt.figure()
    plt.plot(trend.index, trend.values)
    plt.title("Sentiment Trend Over Time")
    plt.xlabel("Date")
    plt.ylabel("Average Sentiment Score")
    plt.xticks(rotation=45)
    plt.show()


def main():
    df = generate_synthetic_posts()

    df = analyze_sentiment(df)

    plot_sentiment_distribution(df)
    plot_sentiment_trend(df)

    print(df.head())


if __name__ == "__main__":
    main()