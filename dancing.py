import numpy as np
import pyaudio
import queue
import soundfile as sf

# Constants
FORMAT = pyaudio.paFloat32
CHANNELS = 1
RATE = 48000  # Sample rate
CHUNK = 1024  # Buffer size

# Initialize PyAudio
p = pyaudio.PyAudio()

# Queue to hold audio data
audio_queue = queue.Queue()

def callback(in_data, frame_count, time_info, status):
    audio_queue.put(in_data)
    return (in_data, pyaudio.paContinue)

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK,
                stream_callback=callback)

# Start the stream
stream.start_stream()

# Capture audio for a few seconds
import time
print("Capturing audio for analysis...")
time.sleep(10)  # Adjust this for how long you want to capture audio

# Stop stream
stream.stop_stream()
stream.close()
p.terminate()

# Process audio data
audio_data = b''.join(list(audio_queue.queue))
audio_signal = np.frombuffer(audio_data, dtype=np.float32)

# Beat detection (optional, remove if not needed)
# import librosa
# tempo, beats = librosa.beat.beat_track(y=audio_signal, sr=RATE)
# print(f"Estimated tempo: {tempo} beats per minute.")

# Save the audio signal to a file
filename = "captured_audio.wav"
sf.write(filename, audio_signal, RATE)
print(f"Audio saved to {filename}")
