"""
Auto-generated Python code
Scenario : Content Moderation & Filtering
Prompt   : response_001.txt
Run      : 1
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
from sklearn import metrics

# Load dataset
def load_dataset(file_path):
    try:
        # Assume data.csv with columns ['text', 'label'] where label=1 is harmful and label=0 is safe.
        data = pd.read_csv(file_path)
        return data
    except Exception as e:
        print(f"Error loading dataset: {e}")
        return None

# Text preprocessing and model training
def train_model(data):
    try:
        # Text preprocessing, usually beneficial but might differ based on dataset specifics
        # Here, using a Tfidf Vectorizer pipeline for simplicity
        X = data['text']
        y = data['label']

        # Split data into train and test
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Create a pipeline that transforms data using TF-IDF and then classifies with Naive Bayes
        model = make_pipeline(TfidfVectorizer(), MultinomialNB())

        # Train the model
        model.fit(X_train, y_train)

        # Predict
        predicted = model.predict(X_test)

        # Evaluate the model
        report = metrics.classification_report(y_test, predicted)
        print(report)
        return model
    except Exception as e:
        print(f"Error training model: {e}")
        return None

# Example function to predict severity based on multiple metrics
def predict_severity(content, model, threshold=0.8):
    """Predict severity of harmful content."""
    try:
        prediction_probas = model.predict_proba([content])[0]
        harmful_prob = prediction_probas[1]  # Probability of harmful content
        severity = "low"
        
        if harmful_prob > threshold:
            severity = "high"
        elif harmful_prob > threshold / 2:
            severity = "medium"
        
        return severity, harmful_prob
    except Exception as e:
        print(f"Error predicting severity: {e}")
        return None, None

# Implement basic priority sorting based on severity
def prioritize_content_for_review(contents, user_reports, model, threshold=0.8):
    """Prioritize content for review based on severity and user reports."""
    try:
        prioritized_content = []
        
        for content, user_report in zip(contents, user_reports):
            severity, harmful_prob = predict_severity(content, model, threshold)
            
            # Combining harmful probability and user reports
            priority = (harmful_prob * 0.7) + (user_report * 0.3)
            
            prioritized_content.append((content, severity, priority))
        
        # Sort by priority (descending)
        prioritized_content.sort(key=lambda x: x[2], reverse=True)
        
        return prioritized_content
    except Exception as e:
        print(f"Error prioritizing content: {e}")
        return None

# Main function
def main():
    # Load dataset
    data = load_dataset('data.csv')
    
    if data is not None:
        # Train model
        model = train_model(data)
        
        if model is not None:
            # Example usage
            sample_contents = ["Example of content", "Another example"]
            user_reports = [0, 1]  # User reported the second content as potentially harmful
            prioritized_results = prioritize_content_for_review(sample_contents, user_reports, model)
            
            if prioritized_results is not None:
                for content, severity, priority in prioritized_results:
                    print(f"Content: {content}, Severity: {severity}, Priority: {priority}")

if __name__ == "__main__":
    main()