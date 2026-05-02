"""
Auto-generated Python code
Scenario : Natural Language Processing
Prompt   : response_001.txt
Run      : 1
"""

# Import necessary libraries
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import os

# Set up the chatbot's directory
chatbot_dir = os.path.dirname(__file__)

# Create a new chatbot instance
chatbot = ChatBot(
    'InteractiveBot',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    database_uri='sqlite:///database.sqlite3'
)

# Set up the trainer and load training data
trainer = ChatterBotCorpusTrainer(chatbot)

# Train the chatbot using the English language corpus
trainer.train(
    'chatterbot.corpus.english',
    'chatterbot.corpus.english.greetings',
    'chatterbot.corpus.english.conversations',
    'chatterbot.corpus.english.phrases',
)

# Interactive conversation
def chat_with_bot():
    print("Type 'exit' to end the conversation.")
    while True:
        try:
            user_input = input("You: ")
            if user_input.lower() == 'exit':
                print("Goodbye!")
                break
            
            response = chatbot.get_response(user_input)
            print("Bot:", response)

        except (KeyboardInterrupt, EOFError, SystemExit):
            print("Goodbye!")
            break

if __name__ == "__main__":
    print("Hello! I am your interactive chatbot. How can I assist you today?")
    chat_with_bot()