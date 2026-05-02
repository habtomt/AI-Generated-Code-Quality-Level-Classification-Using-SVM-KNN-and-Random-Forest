#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from dataclasses import dataclass, field
from typing import List, Dict, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression


@dataclass
class ContentItem:
    id: int
    user: str
    text: str
    user_reports: int = 0
    label: int = 0  # 0 = safe, 1 = harmful


class ContentModerationMLSystem:
    def __init__(self):
        self.vectorizer = TfidfVectorizer()
        self.model = LogisticRegression(max_iter=1000)
        self.trained = False

        self.training_data = [
            ("I hate you and you are worthless", 1),
            ("This is terrible and I will hurt you", 1),
            ("You are an idiot", 1),
            ("Buy now cheap products click here", 1),
            ("I love this community", 0),
            ("This is a helpful discussion", 0),
            ("Thank you for your support", 0),
            ("What a nice post", 0),
            ("Let’s learn programming together", 0),
            ("Good morning everyone", 0),
        ]

    def train(self):
        texts, labels = zip(*self.training_data)
        X = self.vectorizer.fit_transform(texts)
        self.model.fit(X, labels)
        self.trained = True

    def predict_harmful(self, text: str) -> float:
        if not self.trained:
            self.train()
        X = self.vectorizer.transform([text])
        return self.model.predict_proba(X)[0][1]

    def severity_score(self, text: str, user_reports: int) -> float:
        ml_score = self.predict_harmful(text)
        report_score = min(user_reports * 0.2, 1.0)
        keyword_score = self.keyword_severity(text)
        return 0.5 * ml_score + 0.3 * report_score + 0.2 * keyword_score

    def keyword_severity(self, text: str) -> float:
        severe_words = ["kill", "hate", "stupid", "idiot", "destroy", "threat"]
        text_l = text.lower()
        matches = sum(1 for w in severe_words if w in text_l)
        return min(matches / 3, 1.0)

    def classify(self, item: ContentItem) -> Dict:
        score = self.severity_score(item.text, item.user_reports)

        if score > 0.7:
            action = "remove"
        elif score > 0.4:
            action = "flag_for_review"
        else:
            action = "allow"

        return {
            "id": item.id,
            "user": item.user,
            "score": round(score, 3),
            "action": action,
            "reports": item.user_reports
        }


class ModerationQueue:
    def __init__(self, system: ContentModerationMLSystem):
        self.system = system
        self.items: List[ContentItem] = []

    def add(self, item: ContentItem):
        self.items.append(item)

    def process(self) -> List[Dict]:
        results = []
        for item in self.items:
            results.append(self.system.classify(item))
        return self.prioritize(results)

    def prioritize(self, results: List[Dict]) -> List[Dict]:
        return sorted(
            results,
            key=lambda x: (x["score"], x["reports"]),
            reverse=True
        )


def main():
    system = ContentModerationMLSystem()
    queue = ModerationQueue(system)

    queue.add(ContentItem(1, "alice", "I hate this so much", 3))
    queue.add(ContentItem(2, "bob", "Buy now click here http://spam.com", 1))
    queue.add(ContentItem(3, "charlie", "Great discussion everyone", 0))
    queue.add(ContentItem(4, "david", "You are an idiot and I will destroy you", 5))
    queue.add(ContentItem(5, "eve", "Looking forward to learning AI", 0))

    results = queue.process()

    for r in results:
        print(r)


if __name__ == "__main__":
    main()