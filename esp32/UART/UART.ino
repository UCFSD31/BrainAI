#include <ESP32Servo.h>

#define SERIAL_BAUDRATE 115200
#define WORD_SIZE 6   // word length 
#define LINEFEED 10   // "enter" ascii
#define NUMSERVOS 6   // totla servos used
#define STARTUP 90   // starting position 

// functions declartions 
void printData(byte data[WORD_SIZE], int len);


byte servoBits[WORD_SIZE]; // store the 6 bytes of data from pc
int target[WORD_SIZE]; // store the 6 bytes of data from pc
Servo servos[NUMSERVOS]; // arays of servo objects
int pinNums[NUMSERVOS] = {2,22,4,10,18,21}; // declares the pins for the servos 



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
 
    for(int i = 0; i < NUMSERVOS; i++)
    {
      
      if(bitRead(servoBits[i], 7) == 0 )
      {
        target[i] = (servoBits[i] & 0b01111111) + 90;

        if(i == 1)
          servos[i].write(180 - ((servoBits[i] & 0b01111111) + 90));
        else
          servos[i].write((servoBits[i] & 0b01111111) + 90);

        

      }
      else if (bitRead(servoBits[i], 7) == 1)
      {
        target[i] = ((servoBits[i] & 0b01111111) * -1) + 90;
        if(i == 1)
          servos[i].write(180 - (((servoBits[i] & 0b01111111) * -1) + 90));

        else
          servos[i].write(((servoBits[i] & 0b01111111) * -1) + 90);

      }
    }

    //delay(2000);

    // while(!checkAllEqual(target))
    // {
      
    // }

    //Serial.println("finshed ");
  }

}

bool checkAllEqual(int target[])
{
  for (int i = 0; i < NUMSERVOS; i++) 
  {
    int difference = servos[i].read() - target[i];
    
    if (abs(servos[i].read() - target[i]) >= 3) 
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
