/*
 * basic_demo.ino
 * Example for MCP9600
 *  
 * Copyright (c) 2018 Seeed Technology Co., Ltd.
 * Website    : www.seeed.cc
 * Author     : downey
 * Create Time: May 2018
 * Change Log :
 *
 * The MIT License (MIT)
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 */


 

#include "Seeed_SHT35.h"
#include <Wire.h>

//This is Arduino 1
char ArdName[] = "--Ard1";
int sensor2 = 44, sensor1 = 45; //Default address is actually 45.

/*SAMD core*/
#ifdef ARDUINO_SAMD_VARIANT_COMPLIANCE
  #define SDAPIN  20
  #define SCLPIN  21
  #define RSTPIN  7
  #define SERIAL SerialUSB
#else
  #define SDAPIN  A4
  #define SCLPIN  A5
  #define RSTPIN  2
  #define SERIAL Serial
#endif

SHT35 sensor(SCLPIN);

int dataCollectionInterval = 50; //In miliseconds


void setup()
{
    pinMode(LED_BUILTIN, OUTPUT);
    SERIAL.begin(9600);
    SERIAL.println("--Arduino #, Sensor Addr, Time Start (s),Temp (c),Humidity(RH)");
    //Sensor initialization process
    if(sensor.init())
    {
      SERIAL.println("sensor init failed!!!");
    }
}

//Function to read the sensor and output its value. Argument allows us to set which sensor to read. 2 is 44, 1 is 43.
void sensorRead(int senseSelect)
{
  u16 value=0;
    u8 data[6]={0};
    float temp, hum, temp2,hum2;
    if(NO_ERROR!=sensor.read_meas_data_single_shot(HIGH_REP_WITH_STRCH,&temp2,&hum2))
    {
      SERIAL.println("read temp failed!!\n\n\n");
    }
    else
    {
      //First print the arduino name into the terminal
      SERIAL.print(ArdName);
      SERIAL.print(",");
      //Then print the sensor address that is read
      if (senseSelect == 2){
        SERIAL.print(sensor2);
      }
      else if (senseSelect == 1)
      {
        SERIAL.print(sensor1);
      }
      //This prints the time that the progarm was started
      SERIAL.print(",");
      SERIAL.print(floor(millis()/1000));
      SERIAL.print(',');
      //This prints the temperature of which sensor is selected
      if (senseSelect == 2){
        SERIAL.print(temp2);
      }
      else if (senseSelect == 1){
        SERIAL.print(temp);
      }
      //This prints the humidity of the selected sensor
      SERIAL.print(',');
      if (senseSelect == 2){
        SERIAL.println(hum2);
      }
      else if (senseSelect == 1){
        SERIAL.println(hum);
      }
    }
}

//This function will blink the onboard LED to tell us if something is happening. We can set it to do whatever.
void ledBlink()
{
    digitalWrite(LED_BUILTIN, HIGH);
    delay(dataCollectionInterval/4);
    digitalWrite(LED_BUILTIN, LOW);
    delay(dataCollectionInterval/4);
    digitalWrite(LED_BUILTIN, HIGH);
    delay(dataCollectionInterval/4);
    digitalWrite(LED_BUILTIN, LOW);
    delay(dataCollectionInterval/4);
}

//This function will run if the arduino detects a data transfer from the computer.
void recieveCommand()
{ 
      //R=82 1=49 2=50
      int commandRead = Serial.read();
      if (commandRead == 50){
        sensorRead(2); //Arguments are (sensor select,)
      }
      else if (commandRead == 49){
        sensorRead(1);
      }      
}

//Main program loop
void loop()
{
    int commandRead = Serial.read();
    if (commandRead > 10)
    {
      recieveCommand();
    }  
    
    ledBlink();
}
