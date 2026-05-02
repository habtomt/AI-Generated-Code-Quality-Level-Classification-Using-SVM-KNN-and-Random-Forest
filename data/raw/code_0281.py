import sounddevice as sd
import numpy as np
import socket
import threading
import keyboard
import noisereduce as nr

# --- Configuration ---
CHUNK_SIZE = 1024
CHANNELS = 1
RATE = 44100
SERVER_IP = '127.0.0.1'
PORT = 5555
PTT_KEY = 'v'

# --- Networking ---
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('0.0.0.0', PORT))

def receive_audio():
    while True:
        data, addr = sock.recvfrom(CHUNK_SIZE * 4)
        audio_data = np.frombuffer(data, dtype=np.float32)
        sd.play(audio_data, RATE)

def send_audio():
    with sd.InputStream(samplerate=RATE, channels=CHANNELS, blocksize=CHUNK_SIZE, dtype='float32') as stream:
        while True:
            if keyboard.is_pressed(PTT_KEY):
                data, overflowed = stream.read(CHUNK_SIZE)
                if overflowed:
                    continue
                
                # Background Noise Suppression
                reduced_noise = nr.reduce_noise(
                    y=data.flatten(), 
                    sr=RATE, 
                    prop_decrease=0.7, 
                    stationary=True
                )
                
                sock.sendto(reduced_noise.tobytes(), (SERVER_IP, PORT))

# --- Main ---
if __name__ == "__main__":
    print(f"Voice System Active. Hold '{PTT_KEY}' to talk.")
    
    receiver_thread = threading.Thread(target=receive_audio, daemon=True)
    sender_thread = threading.Thread(target=send_audio, daemon=True)
    
    receiver_thread.start()
    sender_thread.start()
    
    receiver_thread.join()
    sender_thread.join()