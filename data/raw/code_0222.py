import random

def get_response(user_input):
    user_input = user_input.lower()

    responses = {
        "hello": ["Hi there!", "Hello!", "Greetings!", "Hey!"],
        "how are you": ["I'm doing well, thank you!", "I'm great! How are you?", "All systems operational."],
        "what is your name": ["I am a Python-based conversational assistant.", "You can call me PythonBot."],
        "bye": ["Goodbye!", "See you later!", "Have a great day!"],
        "default": ["That's interesting, tell me more.", "I see. How does that make you feel?", "Could you elaborate on that?"]
    }

    for key in responses:
        if key in user_input:
            return random.choice(responses[key])
    
    return random.choice(responses["default"])

def start_conversation():
    print("PythonBot: Hello! Type 'bye' to exit the conversation.")
    
    while True:
        user_input = input("You: ")
        
        if 'bye' in user_input.lower():
            print(f"PythonBot: {get_response('bye')}")
            break
            
        response = get_response(user_input)
        print(f"PythonBot: {response}")

if __name__ == "__main__":
    start_conversation()