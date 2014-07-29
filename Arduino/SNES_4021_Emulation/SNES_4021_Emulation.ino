/*
 * Copyright (c) 2014 GhostSonic
 * Licensed under the MIT License
 * See LICENSE.txt for details
 
 * MAGIC SKETCH THAT EMULATES A 4021 SHIFT REGISTER FOR A SNES WITH INPUT VIA SERIAL
 * This sketch has only been tested on a MEGA 2560, since that's all I have.
 * You will NEED to modify part of this sketch if you want it to have any chance of working on another board, info about that is further below.
 * You should hook the following arduino pins to subsequent SNES Controller port's pins directly.
 * PIN 2 (interrupt 0): Clock 
 * PIN 3 (interrupt 1): Latch
 * PIN 4: Data
 * Ground: Ground
 * You can look up a picture of the controller port pinout. Or you can try to interpret this crappy ascii thing I made up. I recommend looking it up.
(ooo|oooo]
 |   |||_Clock
 |   ||_Latch
 |   |_Data
 |_Ground
*/

//The onboard LED connected to Pin 13 should light up once the Arduino and the Python are ready for the console to be turned on.
#define Status_LED 13
//We make use of port manipulation due to the substantially faster speeed compared to digitalWrite.
//If we didn't, it doesn't work at all
#define WRITE_DATA_HIGH PORTG |= B00100000 //Pin 4 is on PORTG on the Mega2560
#define WRITE_DATA_LOW PORTG &= B11011111
/* The following two lines should replace the above two lines if you want to test this on an Uno board. I have no idea if this actually works. If it does, then awesome.
#define WRITE_DATA_HIGH PORTD |= B00010000
#define WRITE_DATA_LOW PORTD &= B11101111
The rest of the code shouldn't need any changes */

int saveddata = 0xffff;
byte serialData1 = 0;
byte serialData2 = 0;
byte clocks = 0;

void setup(){
  Serial.begin(115200);
  attachInterrupt(0, clocking, RISING);
  attachInterrupt(1, latching, RISING);
  pinMode(4, OUTPUT);
  pinMode(Status_LED, 13);
  
  digitalWrite(Status_LED, LOW);
  while(Serial.read() != 0x10); //Wait for a a Serial ping from Python
  delay(3);
  Serial.write(0x12);
  digitalWrite(Status_LED, HIGH);
}

void loop(){
  if(Serial.available() > 1){
    serialData1 = Serial.read();
    serialData2 = Serial.read();
  }
}

void latching(){
    saveddata = ~(serialData1 << 8| serialData2);
    if(saveddata & 1) WRITE_DATA_HIGH;
    else WRITE_DATA_LOW;
    saveddata = saveddata >> 1;
    Serial.write(0x12); //Send a byte to request input data 
    clocks = 0;
}

void clocking(){ //This is somehow fast enough for a lot of games.
  //Write the least significant bit to the data line, then shift it.
  if(saveddata & 1) WRITE_DATA_HIGH;
  else WRITE_DATA_LOW;
  saveddata = saveddata >> 1;
  clocks++;
  if (clocks > 15) WRITE_DATA_LOW; //Write data low after the end of the 16th cycle, some games hate it when you don't.
  //That might have something to do with SNES detecting if a controller is plugged in or not.
}
