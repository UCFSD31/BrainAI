#include <ESP32Servo.h>

#define SERIAL_BAUDRATE 115200
#define WORD_SIZE 3   // word length 
#define LINEFEED 10   // "enter" ascii
#define NUMSERVOS 4   // totla servos used
#define STARTUP 90   // starting position 

// functions declartions 
void printData(byte data[WORD_SIZE], int len);


byte servoBits[WORD_SIZE]; // store the 3 bytes of data from pc
int target[NUMSERVOS]; // store the 3 bytes of data from pc
Servo servos[NUMSERVOS]; // arays of servo objects
int pinNums[NUMSERVOS] = {14,35,25,19}; // declares the pins for the servos 



void setup() 
{
  Serial.begin(SERIAL_BAUDRATE);

  // initlized the servos to their pins
  for(int i = 0; i < NUMSERVOS; i++)
  {
    servos[i].attach(pinNums[i]);
  }
  for(int i = 0; i < NUMSERVOS; i++)
  {
    servos[i].write(STARTUP);
  }

}

void loop() 
{
  if (Serial.available()) 
  {
    int BytesRead = Serial.readBytes(servoBits, WORD_SIZE);
    int index = 0;

    for(int i = 0; i < WORD_SIZE; i++)
    {
      
      if(bitRead(servoBits[i], 7) == 0 )
      {
        if(index == 0)
        {
          target[index++] = (servoBits[i] & 0b01111111) + 90;

          target[index++] = 180 - ((servoBits[i] & 0b01111111) + 90);
        }
        else
          target[index++] = (servoBits[i] & 0b01111111) + 90;
        
      }
      else if (bitRead(servoBits[i], 7) == 1)
      {
        if(index == 0)
        {
          target[index++] = (((servoBits[i] & 0b01111111) * -1) + 90);
          
          target[index++] = 180 - (((servoBits[i] & 0b01111111) * -1) + 90);
        }
        else
          target[index++] = (((servoBits[i] & 0b01111111) * -1) + 90);
        
      }
      //servos[i].write(target[i]);
    }

    //delay(2000);
  }

}

void moveInc()
{
    while(!checkAllEqual())
    {
      int max = getMaxDistance();
      // if(max <= 10)
      // {
      //   servos[i].write(target[i]);
      //   continue;
      // }

      // if(max == 0)
      //   break;
      for(int i = 0; i < NUMSERVOS; i++)
      {
        int distance = getDistance(i);
        int move = 0;

        if(distance <= 10 )
        {
          servos[i].write(target[i]);
          continue;
        }

        
          

        move = (double)(distance / max) * distance;
        int current = servos[i].read();

        if(current > target[i])
          servos[i].write(current - move);
        else if(current < target[i])
          servos[i].write(current + move);

        //delay(200);
      }
    }
}
int getDistance(int servoIndex)
{
  int rawValue = servos[servoIndex].read() - target[servoIndex];

  int value = abs(rawValue);

  // check if angle read is accurate
  // if (value <= 3)
  //   return 0;

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
  // check if angle read is accurate
  // if(maxValue <= 3)
  //   return 0;

  return maxValue;
}
bool checkAllEqual()
{
  for (int i = 0; i < NUMSERVOS; i++) 
  {
    int difference = servos[i].read() - target[i];
    
    if (abs(difference) > 3) 
    {
      Serial.println("this is what is reading: ");

      Serial.println(servos[i].read());

      Serial.println("this is the target: ");
      
      Serial.println(target[i]);
      Serial.println("this is the dfiifernce: ");

      Serial.println(difference);


      return false; // Return false if any element is not equal to the desired value
    }
  }

  Serial.println("finshed ");
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
