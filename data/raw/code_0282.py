import os
import time
import threading
import queue
import wave
import numpy as np
import sounddevice as sd

# --- Configuration ---
SAMPLE_RATE = 16000
CHANNELS = 1
RECORDINGS_DIR = "call_recordings"

if not os.path.exists(RECORDINGS_DIR):
    os.makedirs(RECORDINGS_DIR)

class SupportCallSession:
    def __init__(self):
        self.audio_queue = queue.Queue()
        self.is_calling = False
        self.stream = None
        self.filename = f"{RECORDINGS_DIR}/call_{int(time.time())}.wav"

    def audio_callback(self, indata, outdata, frames, time_info, status):
        """Handle real-time audio pass-through and queuing."""
        if status:
            print(status)
        # Simulate voice communication (loopback for local demo)
        outdata[:] = indata
        # Put audio in queue for recording/analysis
        self.audio_queue.put(indata.copy())

    def start_call(self):
        self.is_calling = True
        print(f"--- Call Started: Recording to {self.filename} ---")
        
        # Audio Analytics Thread
        threading.Thread(target=self._run_analytics, daemon=True).start()
        # Recording Thread
        threading.Thread(target=self._record_session, daemon=True).start()

        with sd.Stream(samplerate=SAMPLE_RATE, channels=CHANNELS, 
                       callback=self.audio_callback):
            while self.is_calling:
                time.sleep(0.1)

    def stop_call(self):
        self.is_calling = False
        print("\n--- Call Ended ---")

    def _record_session(self):
        with wave.open(self.filename, 'wb') as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(2) # 16-bit
            wf.setframerate(SAMPLE_RATE)
            
            while self.is_calling or not self.audio_queue.empty():
                try:
                    data = self.audio_queue.get(timeout=1)
                    # Convert float32 to int16 for WAV storage
                    audio_int16 = (data * 32767).astype(np.int16)
                    wf.writeframes(audio_int16.tobytes())
                except queue.Empty:
                    continue

    def _run_analytics(self):
        """Simulate real-time voice analytics (Volume/Sentiment)."""
        while self.is_calling:
            if not self.audio_queue.empty():
                data = self.audio_queue.queue[-1]
                rms = np.sqrt(np.mean(data**2))
                db = 20 * np.log10(rms) if rms > 0 else -60
                
                # Logic for "Silence" or "High Emotion" detection
                status = "Normal"
                if db > -20: status = "Agent/Customer Raised Voice"
                elif db < -45: status = "Silence Detected"
                
                print(f"[Analytics] Level: {db:.2f} dB | Status: {status}", end='\r')
            time.sleep(0.5)

if __name__ == "__main__":
    session = SupportCallSession()
    
    # Run the call for a fixed duration or user interrupt
    try:
        call_thread = threading.Thread(target=session.start_call)
        call_thread.start()
        
        # Simulate a 10 second support call
        time.sleep(10)
        session.stop_call()
        call_thread.join()
        
    except KeyboardInterrupt:
        session.stop_call()