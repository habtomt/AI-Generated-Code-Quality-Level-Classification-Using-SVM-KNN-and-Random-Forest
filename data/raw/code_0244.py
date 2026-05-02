import json
from flask import Flask, request, jsonify
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

app = Flask(__name__)

# Load a lightweight open-source model and tokenizer
MODEL_NAME = "microsoft/DialoGPT-medium"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)

@app.route('/chat', methods=['POST'])
def chat():
    """
    Backend endpoint to handle chatbot requests.
    Expects JSON input: {"message": "User text here"}
    """
    data = request.get_json()
    user_input = data.get("message", "")

    if not user_input:
        return jsonify({"error": "No message provided"}), 400

    try:
        # Encode user input and append end-of-string token
        new_user_input_ids = tokenizer.encode(user_input + tokenizer.eos_token, return_tensors='pt')

        # Generate a response from the model
        chat_history_ids = model.generate(
            new_user_input_ids, 
            max_length=1000, 
            pad_token_id=tokenizer.eos_token_id,
            no_repeat_ngram_size=3,       
            do_sample=True, 
            top_k=100, 
            top_p=0.7,
            temperature=0.8
        )

        # Decode the response
        bot_response = tokenizer.decode(
            chat_history_ids[:, new_user_input_ids.shape[-1]:][0], 
            skip_special_tokens=True
        )

        return jsonify({
            "reply": bot_response,
            "status": "success"
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Start the server
    app.run(host='0.0.0.0', port=5000)