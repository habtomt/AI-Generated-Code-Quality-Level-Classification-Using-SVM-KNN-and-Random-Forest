import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

class ForumModerator:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=5000)
        self.model = LogisticRegression()
        self._prepare_initial_model()

    def _prepare_initial_model(self):
        data = {
            'text': [
                "I love this discussion", "Get rich quick click here", 
                "You are an idiot", "Great point, thanks for sharing",
                "Buy cheap pills now", "This is very offensive"
            ],
            'label': [0, 1, 1, 0, 1, 1]
        }
        df = pd.DataFrame(data)
        X = self.vectorizer.fit_transform(df['text'])
        self.model.fit(X, df['label'])

    def scan_content(self, text):
        X_input = self.vectorizer.transform([text.lower()])
        prediction = self.model.predict(X_input)
        return bool(prediction[0])

if __name__ == "__main__":
    moderator = ForumModerator()
    sample_post = "Click here for free spam!"
    if moderator.scan_content(sample_post):
        print("Content Removed")