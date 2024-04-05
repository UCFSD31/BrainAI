import pyaudio
import aubio
import numpy as np
from time import sleep
import send_bytes  # Assuming this module has a function `send_data` to send the moves

dance_move_1 = [[0, 90, 0], [0, -90, 0]]

seconds = 10
bufferSize = 512
windowSizeMultiple = 2
audioInputDeviceIndex = 0
audioInputChannels = 1
hopSize = bufferSize
winSize = hopSize * windowSizeMultiple

pa = pyaudio.PyAudio()
audioInputDevice = pa.get_device_info_by_index(audioInputDeviceIndex)
audioInputSampleRate = int(audioInputDevice['defaultSampleRate'])
tempoDetection = aubio.tempo('default', winSize, hopSize, audioInputSampleRate)

current_move = 0
half_time_skip = 0

def readAudioFrames(in_data, frame_count, time_info, status):
    global current_move
    global half_time_skip
    signal = np.frombuffer(in_data, dtype=np.float32)
    beat = tempoDetection(signal)       
    if np.sum(beat) > 0:
        bpm = tempoDetection.get_bpm()
        print("beat! (running with "+str(bpm)+" bpm)")
        #send_bytes.sendAngles(dance_move_1[current_move])
        current_move = 1 - current_move

    return (in_data, pyaudio.paContinue)

def dance():
    inputStream = pa.open(format=pyaudio.paFloat32,
                          input=True,
                          channels=audioInputChannels,
                          input_device_index=audioInputDeviceIndex,
                          frames_per_buffer=bufferSize,
                          rate=audioInputSampleRate,
                          stream_callback=readAudioFrames)

    sleep(seconds)

    inputStream.stop_stream()
    inputStream.close()
    pa.terminate()