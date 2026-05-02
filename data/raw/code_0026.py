#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from typing import List, Dict
from dataclasses import dataclass

@dataclass
class Post:
    id: int
    user: str
    content: str

class SimpleNLPModerationEngine:
    def __init__(self):
        self.offensive_keywords = {
            "badword1", "badword2", "idiot", "stupid", "hate"
        }
        
        self.spam_patterns = [
            r"(buy\s+now)",
            r"(free\s+money)",
            r"(click\s+here)",
            r"(http[s]?://\S+)",
            r"(\b\w+\b)(\s+\1){3,}"
        ]

    def normalize_text(self, text: str) -> str:
        return text.lower().strip()

    def contains_offensive_language(self, text: str) -> bool:
        words = set(self.normalize_text(text).split())
        return len(words.intersection(self.offensive_keywords)) > 0

    def is_spam(self, text: str) -> bool:
        for pattern in self.spam_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return True
        return False

    def is_violation(self, text: str) -> Dict[str, bool]:
        return {
            "offensive": self.contains_offensive_language(text),
            "spam": self.is_spam(text)
        }

    def moderate_post(self, post: Post) -> Dict:
        violations = self.is_violation(post.content)

        if violations["offensive"] or violations["spam"]:
            return {
                "post_id": post.id,
                "user": post.user,
                "action": "removed",
                "reason": violations
            }

        return {
            "post_id": post.id,
            "user": post.user,
            "action": "approved",
            "reason": violations
        }


class ForumModerationSystem:
    def __init__(self):
        self.engine = SimpleNLPModerationEngine()
        self.posts: List[Post] = []

    def add_post(self, post: Post):
        self.posts.append(post)

    def moderate_all(self) -> List[Dict]:
        results = []
        for post in self.posts:
            result = self.engine.moderate_post(post)
            results.append(result)
        return results

    def get_clean_posts(self) -> List[Post]:
        clean_posts = []
        for post in self.posts:
            result = self.engine.moderate_post(post)
            if result["action"] == "approved":
                clean_posts.append(post)
        return clean_posts


def main():
    forum = ForumModerationSystem()

    forum.add_post(Post(1, "alice", "Hello everyone, welcome to the forum!"))
    forum.add_post(Post(2, "bob", "buy now cheap products click here http://spam.com"))
    forum.add_post(Post(3, "charlie", "You are so stupid and hate this community"))
    forum.add_post(Post(4, "david", "This is a normal discussion post"))

    results = forum.moderate_all()

    print("Moderation Results:")
    for r in results:
        print(r)

    print("\nClean Posts:")
    for p in forum.get_clean_posts():
        print(f"{p.id}: {p.content}")


if __name__ == "__main__":
    main()