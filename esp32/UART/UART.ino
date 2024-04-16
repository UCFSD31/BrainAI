#include <ESP32Servo.h>

#define SERIAL_BAUDRATE 115200
#define WORD_SIZE 3   // number of bytes to expect from pc
#define NUMSERVOS 4   // total servos used
#define STARTUP 90   // starting position 
#define MASK 0b01111111 
#define OFFSET 90
#define MSB 7 
#define FLIP 180

// Pin numbers for the servos 
// These are all GPIO pins on the ESP32
// Recommended pins include 2,4,12-19,21-23,25-27,32-33
// for the ESP32-C3 the GPIO pins are 1-10,18-21

#define SERVO_1_PIN 18
#define SERVO_2_PIN 22
#define SERVO_3_PIN 19
#define SERVO_4_PIN 2

// functions declartions 
void printData(byte data[WORD_SIZE], int len); // displays the bits received through UART 
int getDistance(int servoIndex); // gets the distance from current angle to target angle 
bool checkAllEqual();  // checks to see if all servos are at the target angle before reading the next set of inputs
int getMaxDistance(); // gets the max distance any servo has to get to 
void reset(); //  resets to starting position
void targetCheck(); // checks to see if the angles are within 0-180
void returnAngles();  // sends to the pc angles current position in HEX
void clearBuffer();

// global variables
Servo servos[NUMSERVOS];
byte servoBits[WORD_SIZE]; // store the 3 bytes of data from pc thorugh UAR 
int target[NUMSERVOS]; // stores the target angles
int pinNums[NUMSERVOS] = {SERVO_1_PIN,SERVO_2_PIN,SERVO_3_PIN,SERVO_4_PIN}; 

void setup() 
{
  Serial.begin(SERIAL_BAUDRATE);

  // initlized the servos to their pins
  for(int i = 0; i < NUMSERVOS; i++)
  {
    servos[i].attach(pinNums[i]);
  }
  // sets the starting postions for each servo 
  for(int i = 0; i < NUMSERVOS; i++)
  {
    servos[i].write(STARTUP);
  }
}

void loop() 
{
  if (Serial.available()) 
  {
    // reads in 3 bytes of data from the pc through UART and saves them in servoBits array
    int BytesRead = Serial.readBytes(servoBits, WORD_SIZE);

    // clears the buffer
    clearBuffer();
    
    // set the target valus for each servo
    // first bit determines if the angles is positvie or negative 
    // the rest of the bits (7) deteremine the angle from 0 - 90 
    // servo 1 and servo 2 are combined as one servo. meaning the angle for servo 1 is flipped for servo 2. 
    int index = 0;
    for(int i = 0; i < WORD_SIZE; i++)
    { 
      if(bitRead(servoBits[i], MSB) == 0)
      {
        if(index == 1)
        {
          target[index++] = (servoBits[i] & MASK) + OFFSET;
          target[index++] = FLIP - ((servoBits[i] & MASK) + OFFSET);
        }
        else
          target[index++] = (servoBits[i] & MASK) + OFFSET;
        
      }
      else if (bitRead(servoBits[i], MSB) == 1)
      {
        if(index == 1)
        {
          target[index++] = (((servoBits[i] & MASK) * -1) + OFFSET);
          target[index++] = FLIP - (((servoBits[i] & MASK) * -1) + OFFSET);
        }
        else
          target[index++] = (((servoBits[i] & MASK) * -1) + OFFSET);
      }
    }

    targetCheck();
    //moveInc();

    while(!checkAllEqual())
    {
      // if (Serial.available())
      //   break;

      int max = getMaxDistance();

      for(int i = 0; i < NUMSERVOS; i++)
      {
        int distance = getDistance(i);
        int move = 0;

        // if the distance if less than or equal to 3. set it to the target angle
        //  this helps with servos being up to +- 3 degrees off 
        if(distance <= 3)
          servos[i].write(target[i]);

        // finds the distance to move based on a ratio of the distance and the max distance.
        move = ((double)distance / (double)max) * (double)distance;

        // checks current angle and adds to subtracts to get to the target angle 
        int current = servos[i].read();

        if(current > target[i])
          servos[i].write(current - move);
        else if(current < target[i])
          servos[i].write(current + move);
        else
          servos[i].write(target[i]);

        //delayMicroseconds(500);
      }
    }

    //send back to pc current angles 
    returnAngles();
  }
}

void moveInc()
{

  while(!checkAllEqual())
    {
      if (Serial.available())
        break;
      
      for(int i = 0; i < NUMSERVOS; i++)
      {
        servos[i].write(target[i]);
        //delayMicroseconds(1000);
      }
    }


}
void clearBuffer()
{
  while(Serial.available() > 0)
    Serial.read();
}
void returnAngles()
{ 
  for(int i = 0; i < NUMSERVOS; i++)
  {
    if(i == 2)
      continue;

    Serial.println(servos[i].read());
  }
}
void targetCheck()
{
  if(target[1] >= 125 || target[2] <= 55)
  {
    target[1] = 125;
    target[2] = 55;
  }

  for(int i = 0; i < NUMSERVOS; i++)
  {

    if (target[i] > 180)
      target[i] = 180;
    else if(target[i] < 0)
      target[i] = 0;
  }
}
void reset()
{
  for(int i = 0; i < NUMSERVOS; i++)
    servos[i].write(STARTUP);
}
int getDistance(int servoIndex)
{
  int rawValue = servos[servoIndex].read() - target[servoIndex];

  int value = abs(rawValue);

  return value;
}
int getMaxDistance()
{
  int maxValue = 0;
  
  for (int i = 0; i < NUMSERVOS; i++)
  {
    int value = servos[i].read() - target[i];
    value = abs(value);

    if(value > maxValue)
      maxValue = value;
  }

  return maxValue;
}
bool checkAllEqual()
{
  for (int i = 0; i < NUMSERVOS; i++) 
  {
    int difference = servos[i].read() - target[i];
    
    // if the distance is less than 3 its close enough target range.
    // servos are 3 degrees off  
    if (abs(difference) > 3) 
      return false; // Return false if any element is not equal to the desired value
  }

  return true;
}
void printData(byte data[WORD_SIZE], int len)
{
    // Display the received byte
    Serial.println("Numbers of bytes: ");
    Serial.println(len);
    Serial.println("Received byte in HEX: ");

    for(int i = 0; i < len; i++)
    {
      Serial.print(data[i],HEX);
      Serial.print(" ");
    }
    Serial.println();
}
