#!/usr/bin/python

import pyaudio
import aubio
import numpy as np
import wave
from time import sleep

seconds = 30  # how long this script should run

bufferSize = 512
windowSizeMultiple = 2  # or 4 for higher accuracy, but more computational cost

audioInputDeviceIndex = 0  # use 'arecord -l' to check available audio devices
audioInputChannels = 1

# Create and start the input stream
pa = pyaudio.PyAudio()
audioInputDevice = pa.get_device_info_by_index(audioInputDeviceIndex)
audioInputSampleRate = int(audioInputDevice['defaultSampleRate'])

# Create the aubio tempo detection:
hopSize = bufferSize
winSize = hopSize * windowSizeMultiple
tempoDetection = aubio.tempo('default', winSize, hopSize, audioInputSampleRate)

# Open a WAV file for writing
wavOutputFilename = 'output.wav'
wavFile = wave.open(wavOutputFilename, 'wb')
wavFile.setnchannels(audioInputChannels)
wavFile.setsampwidth(pa.get_sample_size(pyaudio.paFloat32))
wavFile.setframerate(audioInputSampleRate)

# This function gets called by the input stream, as soon as enough samples are collected from the audio input:
def readAudioFrames(in_data, frame_count, time_info, status):
    signal = np.frombuffer(in_data, dtype=np.float32)

    beat = tempoDetection(signal)
    if np.sum(beat) > 0:  # Check if any beat was detected
        bpm = tempoDetection.get_bpm()
        print("beat! (running with "+str(bpm)+" bpm)")

    # Write audio frames to WAV file
    wavFile.writeframes(in_data)

    return (in_data, pyaudio.paContinue)

# Configure the input stream
inputStream = pa.open(format=pyaudio.paFloat32,
                      input=True,
                      channels=audioInputChannels,
                      input_device_index=audioInputDeviceIndex,
                      frames_per_buffer=bufferSize,
                      rate=audioInputSampleRate,
                      stream_callback=readAudioFrames)

# Because the input stream runs asynchronously, we just wait for a few seconds here before stopping the script:
sleep(seconds)

# Clean up
inputStream.stop_stream()
inputStream.close()
pa.terminate()
wavFile.close()
