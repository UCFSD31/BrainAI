import serial
import time
import serial.tools.list_ports

angle1 = 0
angle2 = 0
angle3 = 0

direction_one = 0
direction_two = 0
direction_three = 0

def sendCompVision(angle1, angle2, angle3, ser):
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

    ser.write(binary_data)

def sendLlama(bytes):
    ser.write(bytes)
