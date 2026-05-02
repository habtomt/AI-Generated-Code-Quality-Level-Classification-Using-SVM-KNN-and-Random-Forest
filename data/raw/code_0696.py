"""
Auto-generated Python code
Scenario : Voice & Video Communication
Prompt   : response_001.txt
Run      : 2
"""

import pyaudio
import wave
import threading
import socket
import pydub
import numpy as np
from pydub import AudioSegment
from pydub.playback import play

class VoiceCommunicationSystem:
    def __init__(self, host='localhost', port=12345):
        self.host = host
        self.port = port
        self.server_socket = None
        self.client_socket = None
        self.p2p = False
        self.push_to_talk = False
        self.background_noise_suppression = False

        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(format=pyaudio.paInt16, channels=2, rate=44100, input=True, frames_per_buffer=1024)

    def start_server(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print('Server started. Waiting for incoming connections...')

        while True:
            client_socket, address = self.server_socket.accept()
            print(f'Connected to {address}')

            if self.p2p:
                self.client_socket = client_socket
                threading.Thread(target=self.handle_client_connection).start()
            else:
                threading.Thread(target=self.handle_client_connection).start()

    def handle_client_connection(self):
        if self.p2p:
            self.client_socket.sendall(b'connected')
            while True:
                try:
                    data = self.client_socket.recv(1024)
                    if data:
                        self.stream.write(data)
                        print('Received data from client')
                except Exception as e:
                    print(f'Error handling client connection: {e}')
                    break
        else:
            while True:
                try:
                    data = self.stream.read(1024)
                    self.client_socket.sendall(data)
                    print('Sent data to client')
                except Exception as e:
                    print(f'Error handling client connection: {e}')
                    break

    def start_client(self, host='localhost', port=12345):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((host, port))
        print('Connected to server')

        self.client_socket.sendall(b'connected')

        while True:
            try:
                data = self.stream.read(1024)
                self.client_socket.sendall(data)
                print('Sent data to server')
            except Exception as e:
                print(f'Error handling client connection: {e}')
                break

    def push_to_talk(self):
        self.push_to_talk = True
        print('Push-to-talk enabled')

    def disable_push_to_talk(self):
        self.push_to_talk = False
        print('Push-to-talk disabled')

    def enable_background_noise_suppression(self):
        self.background_noise_suppression = True
        print('Background noise suppression enabled')

    def disable_background_noise_suppression(self):
        self.background_noise_suppression = False
        print('Background noise suppression disabled')

    def stop(self):
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()
        if self.server_socket:
            self.server_socket.close()
        if self.client_socket:
            self.client_socket.close()
        print('Voice communication system stopped')

def main():
    system = VoiceCommunicationSystem()

    threading.Thread(target=system.start_server).start()

    # Client code
    # client = VoiceCommunicationSystem()
    # client.start_client()

    # Push-to-talk
    # system.push_to_talk()

    # Background noise suppression
    # system.enable_background_noise_suppression()

    # Stop the system
    # system.stop()

if __name__ == '__main__':
    main()