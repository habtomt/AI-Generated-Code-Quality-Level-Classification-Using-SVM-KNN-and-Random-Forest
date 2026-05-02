"""
Auto-generated Python code
Scenario : Natural Language Processing
Prompt   : response_001.txt
Run      : 3
"""

import random

# Define a list of possible responses to user input
responses = {
    'hello': ['Hi!', 'Hey there!', 'Hello!'],
    'how are you': ['I\'m doing great, thanks!', 'I\'m good.', 'I\'m doing well.'],
    'what is your name': ['My name is Chatty.', 'I\'m Chatty, nice to meet you.', 'I\'m an AI chatbot.'],
    'exit': ['Goodbye!', 'See you later.', 'Have a great day!']
}

# Define a function to process user input
def process_input(user_input):
    # Convert user input to lowercase for easier comparison
    user_input = user_input.lower()

    # Check if the user wants to exit the conversation
    if user_input in ['exit', 'bye', 'goodbye']:
        return responses['exit'][random.randint(0, len(responses['exit']) - 1)]

    # Check if the user has entered a specific question or phrase
    for question, answers in responses.items():
        if question in user_input:
            # Return a random response based on the user's input
            return answers[random.randint(0, len(answers) - 1)]

    # If the user's input is not recognized, try to respond conversationally
    try:
        # Use the NLTK library to analyze the user's input
        import nltk
        from nltk.sentiment import SentimentIntensityAnalyzer

        nltk.download('vader_lexicon')
        sia = SentimentIntensityAnalyzer()
        sentiment = sia.polarity_scores(user_input)['compound']

        # If the user's input is positive, respond positively
        if sentiment > 0:
            return f"That's great to hear! {random.choice(['I\'m glad you\'re happy.', 'That\'s awesome!', 'That\'s terrific!'])}"
        # If the user's input is negative, respond sympathetically
        elif sentiment < 0:
            return f"I'm sorry to hear that. {random.choice(['Try not to worry.', 'It\'s okay, things will get better.', 'I\'m here to help.'])}"
        # If the user's input is neutral, respond neutrally
        else:
            return f"Okay, {random.choice(['That\'s interesting.', 'I see.', 'Okay.'])}"
    except Exception as e:
        # If an error occurs, return a default response
        return f"Sorry, I didn't understand that. {random.choice(['Please try again.', 'I\'m not sure what you mean.', 'I\'m still learning.'])}"

# Main function to start the conversation
def main():
    print("Welcome to Chatty! I'm here to chat with you.")
    while True:
        # Get user input
        user_input = input("You: ")

        # Process user input and print the response
        print("Chatty:", process_input(user_input))

        # Check if the user wants to exit the conversation
        if user_input.lower() in ['exit', 'bye', 'goodbye']:
            break

# Run the main function
if __name__ == "__main__":
    main()