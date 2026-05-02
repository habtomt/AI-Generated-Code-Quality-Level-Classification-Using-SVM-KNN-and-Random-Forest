"""
Auto-generated Python code
Scenario : Voice & Video Communication
Prompt   : response_001.txt
Run      : 3
"""

# Import necessary libraries
import pyaudio
import numpy as np
import socket
import threading

# Set up audio parameters
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 48000
CHUNK = 1024

# Set up network parameters
HOST = '127.0.0.1'
PORT = 12345

# Create a PyAudio object
p = pyaudio.PyAudio()

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)

# Function to handle client connections
def handle_client(conn, addr):
    print(f'Connected to {addr}')

    # Create a stream object for the client
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    # Create a thread for receiving audio from the client
    receive_thread = threading.Thread(target=receive_audio, args=(conn, stream))
    receive_thread.start()

    # Create a thread for sending audio to the client
    send_thread = threading.Thread(target=send_audio, args=(conn, stream))
    send_thread.start()

    # Close the stream and socket
    stream.stop_stream()
    stream.close()
    conn.close()

# Function to receive audio from a client
def receive_audio(conn, stream):
    while True:
        try:
            # Read audio data from the client
            data = conn.recv(CHUNK)
            if not data:
                break
            # Play the audio data
            audio = np.frombuffer(data, dtype=np.int16)
            p.play(audio, rate=RATE)
        except Exception as e:
            print(f'Error receiving audio: {e}')
            break

# Function to send audio to a client
def send_audio(conn, stream):
    while True:
        try:
            # Read audio data from the microphone
            audio = stream.read(CHUNK)
            # Send the audio data to the client
            conn.send(audio)
        except Exception as e:
            print(f'Error sending audio: {e}')
            break

# Create a thread for accepting client connections
accept_thread = threading.Thread(target=accept_connections)
accept_thread.start()

# Function to accept client connections
def accept_connections():
    while True:
        try:
            # Accept a client connection
            conn, addr = server_socket.accept()
            # Create a thread to handle the client connection
            client_thread = threading.Thread(target=handle_client, args=(conn, addr))
            client_thread.start()
        except Exception as e:
            print(f'Error accepting connections: {e}')

# Main loop
while True:
    pass

# Close the PyAudio object
p.terminate()