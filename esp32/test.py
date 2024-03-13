import serial

# Open the serial port (change the port and baudrate as per your ESP32 configuration)
ser = serial.Serial('/dev/ttyUSB0', 115200)

# Sample binary data (6 bytes)
binary_data = bytes([0b01011010, 0b01011010])
binary_data2 = bytes([0b11011010, 0b11011010])

# Send binary data with a delay between commands
#while 1:
ser.write(binary_data)

#ser.write(binary_data2)

# Close the serial port when done
ser.close()
