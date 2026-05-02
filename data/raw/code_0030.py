#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from dataclasses import dataclass
from typing import List, Dict


@dataclass
class Comment:
    comment_id: int
    user: str
    text: str


class CommentModerationSystem:
    def __init__(self):
        self.profanity_list = {
            "idiot", "stupid", "hate", "dumb", "shut up", "moron", "trash"
        }

        self.abusive_patterns = [
            r"\b(kill|die)\s+you\b",
            r"\byou\s+are\s+(useless|worthless)\b",
            r"(shut\s+up)",
            r"(go\s+to\s+hell)"
        ]

    def normalize(self, text: str) -> str:
        return text.lower().strip()

    def check_profanity(self, text: str) -> bool:
        words = set(self.normalize(text).split())
        return len(words.intersection(self.profanity_list)) > 0

    def check_patterns(self, text: str) -> bool:
        for pattern in self.abusive_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return True
        return False

    def toxicity_score(self, text: str) -> float:
        score = 0.0

        if self.check_profanity(text):
            score += 0.5

        if self.check_patterns(text):
            score += 0.5

        caps_ratio = sum(1 for c in text if c.isupper()) / (len(text) + 1)
        if caps_ratio > 0.5:
            score += 0.2

        return min(score, 1.0)

    def classify(self, comment: Comment) -> Dict:
        score = self.toxicity_score(comment.text)

        if score > 0.7:
            action = "remove"
        elif score > 0.4:
            action = "flag"
        else:
            action = "allow"

        return {
            "comment_id": comment.comment_id,
            "user": comment.user,
            "score": round(score, 3),
            "action": action,
            "text": comment.text
        }


class NewsCommentFilter:
    def __init__(self):
        self.moderator = CommentModerationSystem()
        self.comments: List[Comment] = []

    def add_comment(self, comment: Comment):
        self.comments.append(comment)

    def process_comments(self) -> List[Dict]:
        results = [self.moderator.classify(c) for c in self.comments]
        return sorted(results, key=lambda x: x["score"], reverse=True)


def main():
    system = NewsCommentFilter()

    system.add_comment(Comment(1, "alice", "This article is great, very informative"))
    system.add_comment(Comment(2, "bob", "you are stupid and this is trash"))
    system.add_comment(Comment(3, "charlie", "I completely disagree but respect your opinion"))
    system.add_comment(Comment(4, "david", "SHUT UP this is useless"))
    system.add_comment(Comment(5, "eve", "Interesting perspective, thanks for sharing"))

    results = system.process_comments()

    for r in results:
        print(r)


if __name__ == "__main__":
    main()