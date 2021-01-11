# define THRESH 1
#define MAX 150     //maximum posible reading. TWEAK THIS VALUE!!

#include <Wire.h>
//#include "Adafruit_DRV2605.h"         // feedback

Adafruit_DRV2605 drv;
//const int analogOutPin = 6;                // feedback

float outputValue = 0; 
int feedback;
int readings[10];
int finalReading;
byte multiplier = 1;

void setup(){
  Serial.begin(9600); //Serial communication baud rate (alt. 115200)

//  pinMode(3, OUTPUT);
//  Serial.println("DRV test");
  drv.begin();
  drv.selectLibrary(1);
  
//  drv.setMode(DRV2605_MODE_PWMANALOG);
  drv.setMode(DRV2605_MODE_INTTRIG);
}

float map_float(float x, float in_min, float in_max, float out_min, float out_max)
{
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}

void loop(){
//  for(int i = 0; i < 10; i++){    //take ten readings in ~0.02 seconds
//    readings[i] = analogRead(A0) * multiplier;
//    delay(2);                   // default value was 2
//  }
//  for(int i = 0; i < 10; i++){   //average the ten readings
//    finalReading += readings[i];
//  }
//  finalReading /= 10;

//  Serial.print(finalReading);
//  Serial.print("\t");
//  finalReading = constrain(finalReading, 0, MAX);
//  Serial.print(finalReading);
//  Serial.print("\t");
//  outputValue = map_float(finalReading, 0, MAX, -1, THRESH);

  while (!Serial) ;
//  Serial.println(outputValue);
//  feedback = map(finalReading, 0, MAX , 0 , 255);
  feedback = Serial.read();
//  Serial.print("\t");
  Serial.println(feedback);
  if (feedback > 0){
    drv.setWaveform(0, feedback);  // ramp up medium 1, see datasheet part 11.2
//  drv.setWaveform(1, 1);  // strong click 100%, see datasheet part 11.2
//  drv.setWaveform(2, 0);  // end of waveforms
    drv.go(); }
}
    
