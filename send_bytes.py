import serial
import time
import serial.tools.list_ports

serial_connection = None

def sendAngles(angles):
    angle1 = int(angles[0]) - 90
    angle2 = int(angles[1]) - 90
    angle3 = int(angles[2]) - 90

    sign_bit_1 = '1' if angles[0] < 0 else '0'
    sign_bit_2 = '1' if angles[1] < 0 else '0'
    sign_bit_3 = '1' if angles[2] < 0 else '0'

    angle_bits_1 = bin(abs(angles[0]))[2:]
    angle_bits_2 = bin(abs(angles[1]))[2:]
    angle_bits_3 = bin(abs(angles[2]))[2:]

    angle_bits_1 = angle_bits_1.zfill(7)
    angle_bits_2 = angle_bits_2.zfill(7)
    angle_bits_3 = angle_bits_3.zfill(7)

    binary_data = bytes([int(sign_bit_1 + angle_bits_1, 2),
                         int(sign_bit_2 + angle_bits_2, 2),
                         int(sign_bit_3 + angle_bits_3, 2)])
    

    print("Data Computer:", binary_data)

    serial_connection.write(binary_data)

def set_serial_device(new_serial_connection):
    global serial_connection
    serial_connection = new_serial_connection