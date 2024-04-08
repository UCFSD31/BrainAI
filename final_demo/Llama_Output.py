import csv
import pandas as pd
import serial
import time
import serial.tools.list_ports

servo_degrees = [0,0,0]

def decode_bits(servo_bytes):
    directions = []
    angles = []
    for bytes in servo_bytes:
        directions.append((bytes & 0x80) >> 7)
        angles.append((bytes & 0x7F))
    return directions, angles

def move_servos(directions, angles):
    output_degrees = []
    for servo_degree, angle, direction in zip(servo_degrees, angles, directions):
        direction_value = 1 - 2 * direction
        degrees = angle * direction_value
        degrees_capped = max(min(degrees, 90), -90)
        output_degrees.append(servo_degree + degrees_capped)
    return output_degrees

def read_pandas_entry(panda_row):
    angles = []
    directions = []
    for i in range(3):
        if i == panda_row[2]:
            angles.append(panda_row[1])
            directions.append(panda_row[3])
        else:
            angles.append(0)
            directions.append(0)

    return angles, directions

def compare(panda_row, predicted_directions, predicted_angles):
    true_directions, true_angles = read_pandas_entry(panda_row)
    return (true_directions == predicted_directions).all() and (true_angles == predicted_angles).all()

def sendLlama(bytes, ser):
    ser.write(bytes)

def output(bytes, ser, panda_row, training = False):
    if(training == False):
        predicted_directions, predicted_angles = decode_bits(bytes)
        move_servos(predicted_directions, predicted_angles)
        return compare(panda_row, predicted_directions, predicted_angles)
    else:
        sendLlama(bytes, ser)