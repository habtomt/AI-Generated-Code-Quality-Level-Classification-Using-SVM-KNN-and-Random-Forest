class ContentSafetySystem:
    def __init__(self):
        self.harmful_keywords = ["hate", "harass", "fake news"]

    def analyze_severity(self, text):
        score = sum(1 for word in self.harmful_keywords if word in text.lower())
        return min(score / 5.0, 1.0)

    def prioritize_reviews(self, contents):
        results = []
        for content in contents:
            severity = self.analyze_severity(content['text'])
            priority = (severity * 0.7) + (content['reports'] * 0.3)
            results.append({**content, "priority_score": priority})
        
        return sorted(results, key=lambda x: x['priority_score'], reverse=True)

if __name__ == "__main__":
    queue = [
        {"text": "Normal post", "reports": 0},
        {"text": "Hate speech and harassment", "reports": 10}
    ]
    system = ContentSafetySystem()
    for item in system.prioritize_reviews(queue):
        print(item)