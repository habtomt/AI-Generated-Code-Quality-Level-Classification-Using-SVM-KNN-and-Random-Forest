from flask import Flask, request, jsonify
from datetime import datetime
import random

app = Flask(__name__)

class SimpleMLModel:
    def __init__(self):
        self.responses = [
            "Hello! How can I help you today?",
            "I'm here to assist you.",
            "Can you please elaborate?",
            "That's interesting, tell me more.",
            "I'm a simple model, but I'm learning!"
        ]

    def generate_response(self, user_input: str) -> str:
        user_input = user_input.lower()

        if "hello" in user_input:
            return "Hello! Nice to meet you."
        if "time" in user_input:
            return f"The current time is {datetime.now().strftime('%H:%M:%S')}."
        if "name" in user_input:
            return "I am a Python-based chatbot."
        if "help" in user_input:
            return "Sure, tell me what you need help with."

        return random.choice(self.responses)

model = SimpleMLModel()

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json(force=True)
        user_message = data.get("message", "")

        if not user_message:
            return jsonify({"error": "Empty message"}), 400

        response = model.generate_response(user_message)

        return jsonify({
            "response": response,
            "timestamp": datetime.utcnow().isoformat()
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)