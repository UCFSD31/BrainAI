import serial
import time
import serial.tools.list_ports

def sendAngles(angle1, angle2, angle3, ser):



    angle1 = int(angle1) - 90
    angle2 = int(angle2) - 90
    angle3 = int(angle3) - 90

    sign_bit_1 = '1' if angle1 < 0 else '0'
    sign_bit_2 = '1' if angle2 < 0 else '0'
    sign_bit_3 = '1' if angle3 < 0 else '0'

    angle_bits_1 = bin(abs(angle1))[2:]
    angle_bits_2 = bin(abs(angle2))[2:]
    angle_bits_3 = bin(abs(angle3))[2:]

    #ser = serial.Serial('')


    angle_bits_1 = angle_bits_1.zfill(7)
    angle_bits_2 = angle_bits_2.zfill(7)
    angle_bits_3 = angle_bits_3.zfill(7)

    binary_data = bytes([int(sign_bit_1 + angle_bits_1, 2),
                         int(sign_bit_2 + angle_bits_2, 2),
                         int(sign_bit_3 + angle_bits_3, 2)])
    

    print("Data Computer:", binary_data)

    #ser = serial.Serial('/dev/ttyUSB0', 115200)

    ser.write(binary_data)

# # Open the serial port (change the port and baudrate as per your ESP32 configuration)
# ser = serial.Serial('/dev/ttyUSB0', 115200)


# binary_data2 = bytes([0b11011010, 0b11011010])

# ser.write(binary_data)


# # Main loop to continuously read data from serial and display it
# while True:
#     # Read a line of data from the serial port
#     if ser.in_waiting > 0:

#         data = ser.readline()

#         print(data.decode().strip())  # Decode the bytes to string and strip newline characters
#     else:

#         ser.write(binary_data)

#     time.sleep(0.1)
# # Close the serial port when done (uncomment if needed)
# # ser.close()


# Print information about each serial port

