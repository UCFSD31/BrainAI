import serial
import time

# Open the serial port (change the port and baudrate as per your ESP32 configuration)
ser = serial.Serial('/dev/ttyUSB0', 115200)

binary_data = bytes([0b01011010, 0b01011010])
binary_data2 = bytes([0b11011010, 0b11011010])

ser.write(binary_data)


# Main loop to continuously read data from serial and display it
while True:
    # Read a line of data from the serial port
    if ser.in_waiting > 0:

        data = ser.readline()

        print(data.decode().strip())  # Decode the bytes to string and strip newline characters
    else:

        ser.write(binary_data)

    time.sleep(0.1)
# Close the serial port when done (uncomment if needed)
# ser.close()
