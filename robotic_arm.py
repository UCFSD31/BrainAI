import pyaudio
import aubio
import numpy as np
from time import sleep
import serial
import time
import serial.tools.list_ports
import dancing
import send_bytes




def main():
    mode = "Dancing"

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

if __name__ == "__main__":
    main()