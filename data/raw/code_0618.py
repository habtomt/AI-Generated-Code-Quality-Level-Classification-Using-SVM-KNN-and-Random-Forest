"""
Auto-generated Python code
Scenario : Speech Recognition
Prompt   : response_002.txt
Run      : 1
"""

from flask import Flask, request, jsonify
from google.cloud import dialogflow_v2 as dialogflow
from google.cloud import texttospeech
import os
import base64
import json
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set up the Flask app
app = Flask(__name__)

# Set up Google Cloud credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path/to/your/service-account-file.json"

# Initialize Dialogflow client
dialogflow_client = dialogflow.SessionsClient()
project_id = "your-dialogflow-project-id"

# Initialize Text-to-Speech client
tts_client = texttospeech.TextToSpeechClient()

def detect_intent_texts(session_id, text):
    """
    Detects intent based on user's text input.
    
    Args:
    session_id (str): Unique identifier for a session.
    text (str): Text input from the user.
    
    Returns:
    response_text (str): Fulfillment text from Dialogflow.
    """
    try:
        session = dialogflow_client.session_path(project_id, session_id)
        text_input = dialogflow.types.TextInput(text=text, language_code="en-US")
        query_input = dialogflow.types.QueryInput(text=text_input)

        response = dialogflow_client.detect_intent(session=session, query_input=query_input)
        return response.query_result.fulfillment_text
    except Exception as e:
        logger.error(f"Error detecting intent: {str(e)}")
        return "Sorry, I did not understand your request."

def synthesize_speech(text):
    """
    Synthesizes voice from text.
    
    Args:
    text (str): Text to be synthesized.
    
    Returns:
    audio_content (str): Base64 encoded audio content.
    """
    try:
        synthesis_input = texttospeech.SynthesisInput(text=text)
        voice = texttospeech.VoiceSelectionParams(language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL)
        audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)

        response = tts_client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)
        audio_content = base64.b64encode(response.audio_content).decode('utf-8')
        return audio_content
    except Exception as e:
        logger.error(f"Error synthesizing speech: {str(e)}")
        return "Sorry, I'm experiencing a technical issue."

@app.route('/webhook', methods=['POST'])
def webhook():
    """
    Responds to incoming requests from Dialogflow.
    
    Returns:
    response (dict): JSON response with response text and audio content.
    """
    try:
        session_id = request.json.get('session_id', 'default')
        user_input = request.json.get('query', '')

        # Dialogflow detects intent based on user's text input
        response_text = detect_intent_texts(session_id, user_input)

        # Synthesize voice from text
        audio_content = synthesize_speech(response_text)

        # Respond with the synthesized speech (as a base64 MP3 or similar)
        return jsonify({
            'response_text': response_text,
            'audio_content': audio_content
        })
    except Exception as e:
        logger.error(f"Error handling webhook request: {str(e)}")
        return jsonify({'error': 'Sorry, I'm experiencing a technical issue.'})

if __name__ == '__main__':
    app.run(debug=True)