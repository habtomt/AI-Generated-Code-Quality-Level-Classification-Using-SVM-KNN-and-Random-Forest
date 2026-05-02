"""
Auto-generated Python code
Scenario : Text-to-Speech
Prompt   : response_001.txt
Run      : 1
"""

# Import necessary libraries
from google.cloud import speech
from google.cloud import dialogflow_v2 as dialogflow
from google.cloud import texttospeech
import pyaudio
import wave

# Set up credentials
# Replace with your own credentials
GOOGLE_APPLICATION_CREDENTIALS = "path_to_your_service_account_key.json"

# Set up audio parameters
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "output.wav"

# Step 1: Convert speech to text
def speech_to_text(audio_file_path):
    # Set up Speech-to-Text client
    client = speech.SpeechClient()
    
    # Open audio file
    with open(audio_file_path, "rb") as audio_file:
        content = audio_file.read()
        
    # Create a RecognitionAudio object
    audio = speech.RecognitionAudio(content=content)
    
    # Set up RecognitionConfig
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        language_code="en-US",
    )
    
    # Recognize speech
    response = client.recognize(config=config, audio=audio)

    # Return the first transcript
    for result in response.results:
        return result.alternatives[0].transcript

# Step 2: Process text through Dialogflow
def get_dialogflow_response(project_id, session_id, text_input, language_code='en'):
    # Set up Dialogflow client
    session_client = dialogflow.SessionsClient()
    
    # Get session path
    session = session_client.session_path(project_id, session_id)
    
    # Create TextInput object
    text_input = dialogflow.TextInput(text=text_input, language_code=language_code)
    
    # Create QueryInput object
    query_input = dialogflow.QueryInput(text=text_input)
    
    # Detect intent
    response = session_client.detect_intent(session=session, query_input=query_input)
    
    # Return the fulfillment text
    return response.query_result.fulfillment_text

# Step 3: Convert text response to speech
def text_to_speech(text, output_audio_path):
    # Set up Text-to-Speech client
    client = texttospeech.TextToSpeechClient()
    
    # Create SynthesisInput object
    synthesis_input = texttospeech.SynthesisInput(text=text)
    
    # Create VoiceSelectionParams object
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
    )
    
    # Create AudioConfig object
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )
    
    # Synthesize speech
    response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)
    
    # Write audio content to file
    with open(output_audio_path, "wb") as out_file:
        out_file.write(response.audio_content)

    # Print a message to confirm the audio was saved
    print(f'Audio content written to file {output_audio_path}')

# Record audio input
def record_audio():
    # Set up PyAudio
    p = pyaudio.PyAudio()
    
    # Open stream
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
    
    # Initialize frames list
    frames = []
    
    # Record audio
    print("Recording...")
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    print("Finished recording")
    
    # Close stream
    stream.stop_stream()
    stream.close()
    
    # Terminate PyAudio
    p.terminate()
    
    # Save audio to file
    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(p.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()

def main():
    # Record audio input
    record_audio()
    
    # Step 1: Convert speech to text
    customer_query = speech_to_text(WAVE_OUTPUT_FILENAME)
    
    # Step 2: Process text through Dialogflow
    project_id = "your-dialogflow-project-id"
    session_id = "unique-session-id"
    response_text = get_dialogflow_response(project_id, session_id, customer_query)
    
    # Step 3: Convert text response to speech
    text_to_speech(response_text, "response.mp3")

if __name__ == "__main__":
    main()