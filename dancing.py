import pyaudio
import numpy as np
from aubio import tempo, source, float_type
import aubio

# PyAudio configuration
FORMAT = pyaudio.paFloat32
CHANNELS = 1
RATE = 44100
CHUNK = 1024  # Size of each audio chunk

# Initialize PyAudio
p = pyaudio.PyAudio()

# Function to process audio chunks with Aubio
def process_audio_chunk(in_data, frame_count, time_info, status):
    samples = np.frombuffer(in_data, dtype=aubio.float_type).reshape((-1, CHANNELS))
    beat = o(samples)
    if beat[0] != 0:
        # A beat was detected, do something here
        print("Beat detected!")
    return (in_data, pyaudio.paContinue)

# Setup Aubio's tempo detection
o = tempo("default", CHUNK, CHANNELS, RATE)

# Open stream using PyAudio
stream = p.open(format=pyaudio.get_format_from_width(p.get_sample_size(FORMAT)),
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK,
                stream_callback=process_audio_chunk)

# Start the stream
stream.start_stream()

# Keep the stream open and processing audio until you decide to stop
try:
    while stream.is_active():
        # You could do additional processing here
        pass
except KeyboardInterrupt:
    # Stop and close the stream and PyAudio
    stream.stop_stream()
    stream.close()
    p.terminate()
    print("Stream stopped")
