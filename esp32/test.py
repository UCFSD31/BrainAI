import serial
import time

#Alphabetically lists the ports by name
def comslist():
    ports = []
    for i in serial.tools.list_ports.comports():
        try:
            ser = serial.Serial(i.name)
            ser.close()
        except serial.SerialException as e:
            print(e)
        else:
            ports.append(i.name)
    ports.sort()
    return ports

#Finds the desired port using the name eg COM1
def selectcom(port):
    try :
        ser = serial.Serial(port)
    except serial.SerialException as e:
        print(e)
    else:
        return ser

print(comslist)

# Open the serial port (change the port and baudrate as per your ESP32 configuration)
#ser = serial.Serial('COM4',115200)

# Sample binary data (6 bytes)
binary_data = bytes([0b01011010, 0b01011010])
binary_data2 = bytes([0b11011010, 0b11011010])

# Main loop to continuously read and write data
#while True:
    # Check if there is data available to be read
   #if ser.in_waiting > 0:
        # Read a line of data from the serial port
    #    data = ser.readline()
        
     #   # Print the data to the screen
      #  print(data.decode().strip())  # Decode the bytes to string and strip newline characters
    #else:
        # If no data is available, write some data to the serial port
    #    ser.write(binary_data)
    
    # Add a small delay to avoid excessive polling
    #time.sleep(0.1)

# Close the serial port when done (uncomment if needed)
#ser.close()
