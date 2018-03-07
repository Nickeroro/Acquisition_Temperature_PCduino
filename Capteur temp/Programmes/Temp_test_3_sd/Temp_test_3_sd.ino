#include <SD.h>
const int sdPin = 4;
 
// Temperature pin set to analog 0
const int temPin = 2;
 
// Delay time. How often to take a temperature reading, in miliseconds
// 20 minutes = 1200000 milliseconds
const int delayTime = 10000;
 
// File variable
File tempsFile;
 
 
 
void setup() {
  // Serial output for when connected to computer
  Serial.begin(9600);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }
 
  Serial.print("Initializing SD card...");
  if(!SD.begin(sdPin)) {
    Serial.println("initialization failed!");
    return;
  }
  Serial.println("Initialization done.");
 
  tempsFile = SD.open("temps.txt", FILE_WRITE);
 
  if (tempsFile) {
    Serial.println("Printing temperatures");
    tempsFile.println("Printing temperatures:");
    tempsFile.close();
    Serial.println("Done.");
  } else {
    Serial.println("Error opening file in setup.");
  }
 
}
 
void loop() {
  /********************/
  // Open SD card for writing
  tempsFile = SD.open("temps.txt", FILE_WRITE);
 
  if (tempsFile) {
    // Temperature readings
    float voltage, degreesC,
    voltage = getVoltage(temPin);
    degreesC = (voltage - 0.5) * 100.0;
 
    // write temps to Serial
    Serial.print("Celsius: ");
    Serial.print(degreesC);
 
    // write temps to SD card
    tempsFile.print("Celsius: ");
    tempsFile.print(degreesC);
 
    // close the file
    tempsFile.close();
  } else {
    Serial.println("Error opening file in loop.");
  }
 
 
  delay(delayTime);
 
}
 
float getVoltage(int pin)
{
  return (analogRead(pin) * 0.0008056640625);
}
