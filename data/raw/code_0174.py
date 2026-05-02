import re

class ReviewAuditor:
    def detect_deception(self, review_text, user_metadata):
        features = {
            "caps_ratio": len(re.findall(r'[A-Z]', review_text)) / len(review_text),
            "is_short": len(review_text.split()) < 5,
            "high_frequency_user": user_metadata.get('daily_reviews', 0) > 20
        }
        
        if features["caps_ratio"] > 0.5 or (features["is_short"] and features["high_frequency_user"]):
            return "Flagged for Deception"
        return "Verified"

if __name__ == "__main__":
    auditor = ReviewAuditor()
    status = auditor.detect_deception(
        "BEST PRODUCT EVER BUY IT NOW", 
        {"daily_reviews": 50}
    )
    print(status)