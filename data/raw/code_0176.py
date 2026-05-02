class CommentFilter:
    def __init__(self):
        self.abusive_list = ["inflammatory", "abusive", "toxic"]

    def is_clean(self, comment):
        comment_lower = comment.lower()
        if any(word in comment_lower for word in self.abusive_list):
            return False
        
        # Simple length and punctuation check for constructive behavior
        if len(comment) < 10 or comment.count('!') > 3:
            return False
            
        return True

if __name__ == "__main__":
    filter_engine = CommentFilter()
    user_comment = "This is a very inflammatory and abusive comment!!!"
    if not filter_engine.is_clean(user_comment):
        print("Comment Hidden")