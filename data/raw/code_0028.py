#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import math
from dataclasses import dataclass
from typing import List, Dict
from collections import defaultdict, Counter


@dataclass
class Review:
    review_id: int
    user_id: str
    product_id: str
    text: str
    rating: int
    user_total_reviews: int
    user_negative_ratio: float
    user_avg_rating: float


class FakeReviewDetector:
    def __init__(self):
        self.spam_patterns = [
            r"http[s]?://",
            r"buy\s+now",
            r"click\s+here",
            r"free\s+money"
        ]

        self.fake_keywords = {
            "amazing", "best", "perfect", "worst", "terrible", "unbelievable"
        }

    def text_features(self, text: str) -> Dict[str, float]:
        text_clean = text.strip()

        caps_ratio = sum(1 for c in text_clean if c.isupper()) / (len(text_clean) + 1)
        exclamation_count = text_clean.count("!")
        word_counts = Counter(text_clean.lower().split())

        repeated_words = sum(1 for _, c in word_counts.items() if c > 2)

        return {
            "caps_ratio": caps_ratio,
            "exclamations": exclamation_count,
            "repeated_words": repeated_words,
            "length": len(text_clean)
        }

    def check_spam_patterns(self, text: str) -> float:
        score = 0.0
        for pattern in self.spam_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                score += 0.4
        return min(score, 1.0)

    def keyword_score(self, text: str) -> float:
        words = text.lower().split()
        matches = sum(1 for w in words if w in self.fake_keywords)
        return min(matches / 5, 1.0)

    def behavior_score(self, review: Review) -> float:
        score = 0.0

        if review.user_total_reviews < 3:
            score += 0.3

        if review.user_negative_ratio < 0.1:
            score += 0.2

        if review.user_avg_rating > 4.8 or review.user_avg_rating < 1.5:
            score += 0.2

        return min(score, 1.0)

    def text_anomaly_score(self, text: str) -> float:
        features = self.text_features(text)

        score = 0.0

        if features["caps_ratio"] > 0.3:
            score += 0.3

        if features["exclamations"] > 3:
            score += 0.2

        if features["repeated_words"] > 2:
            score += 0.3

        if features["length"] < 20:
            score += 0.2

        return min(score, 1.0)

    def overall_score(self, review: Review) -> float:
        text = review.text

        text_score = (
            self.check_spam_patterns(text) * 0.3 +
            self.keyword_score(text) * 0.3 +
            self.text_anomaly_score(text) * 0.4
        )

        behavior_score = self.behavior_score(review)

        return 0.6 * text_score + 0.4 * behavior_score

    def classify(self, review: Review) -> Dict:
        score = self.overall_score(review)

        if score > 0.75:
            label = "fake"
        elif score > 0.45:
            label = "suspicious"
        else:
            label = "genuine"

        return {
            "review_id": review.review_id,
            "user_id": review.user_id,
            "product_id": review.product_id,
            "score": round(score, 3),
            "label": label,
            "rating": review.rating
        }


class ReviewModerationSystem:
    def __init__(self):
        self.detector = FakeReviewDetector()
        self.reviews: List[Review] = []

    def add_review(self, review: Review):
        self.reviews.append(review)

    def process(self) -> List[Dict]:
        results = [self.detector.classify(r) for r in self.reviews]
        return sorted(results, key=lambda x: x["score"], reverse=True)


def main():
    system = ReviewModerationSystem()

    system.add_review(Review(1, "u1", "p1", "BEST PRODUCT EVER!!! AMAZING!!!", 5, 1, 0.0, 5.0))
    system.add_review(Review(2, "u2", "p1", "ok", 5, 1, 0.0, 5.0))
    system.add_review(Review(3, "u3", "p2", "This product is good and I like it", 4, 10, 0.2, 3.8))
    system.add_review(Review(4, "u4", "p3", "buy now click here http://spam.com", 1, 1, 0.0, 5.0))
    system.add_review(Review(5, "u5", "p2", "Worst worst worst worst worst!!!", 1, 2, 0.0, 1.0))

    results = system.process()

    for r in results:
        print(r)


if __name__ == "__main__":
    main()