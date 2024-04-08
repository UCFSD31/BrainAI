import pyaudio
import aubio
import numpy as np
from time import sleep
import serial
import time
import serial.tools.list_ports
import dancing
import send_bytes
import speech_to_text as stt
import media_pipe_hands as mp

print("Speech recognition application started. Speak into the microphone.")
while True:
    text = stt.listen_and_recognize()
    if text == "stop":
        print("Exiting the application.")
        break

def main():

    # TODO: Wrap with speech to text 
    while True:
        mode = stt.listen_and_recognize()

        # try:
        #     serial_connection = serial.Serial('/dev/ttyUSB1', 115200)
        #     send_bytes.set_serial_device(serial_connection)
        # except serial.SerialException:
        #     try:
        #         # If connection to /dev/ttyUSB1 fails, try connecting to /dev/ttyUSB0
        #         serial_connection = serial.Serial('/dev/ttyUSB0', 115200)
        #         send_bytes.set_serial_device(serial_connection)
        #     except serial.SerialException:
        #         print("\nRobotic arm microcontroller not connected - robotic_arm.py")
        #         return

        if(mode == "Dancing"):
            dancing.dance()
            print("Starting PyAudio and Aubio Model")
        if(mode == "Speech"):
            while True:
                mode = stt.listen_and_recognize()
                if mode == "Training":
                    # TODO: Instantiate LlaMa Model for Training
                    print("Starting LlaMa Model for Training")
                if mode == "Testing":
                    # TODO: Instantiate LlaMa Model for Testing
                    print("Starting LlaMa Model for Testing")
                if mode == "Exit":
                    break
            print("Starting Llama Model")
        if(mode == "Vision"):
            # TODO: Instantiate MediaPipe Model
            print("Starting MediaPipe Model")
        if(mode == "Quit"):
            break

if __name__ == "__main__":
    main()