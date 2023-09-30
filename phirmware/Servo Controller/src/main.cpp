#include <Arduino.h>
#include <Servo.h>


// Create servo objects
Servo servo1;
Servo servo2;
Servo servo3;
Servo servo4;
Servo servo5;
Servo servo6;

void setup() {
  // put your setup code here, to run once:
  pinMode(LED_BUILTIN, OUTPUT);

  Serial.begin(9600);

  // Attach servo objects to pins
  servo1.attach(3);
  servo2.attach(5);
  servo3.attach(6);
  servo4.attach(9);
  servo5.attach(10);
  servo6.attach(11);

}

int inputArray[6];

void loop() {
  // put your main code here, to run repeatedly:

  // Read serial input
  // In the format: "N,N,N,N,N,N"
  // Where N is a number between 0 and 180 with leading zeros
  // Each number represents the angle of a servo

  if (Serial.available()) {
    String line = Serial.readStringUntil('\n');

    // extract motor speeds from string
    inputArray[0] = line.substring(0, 3).toInt();
    inputArray[1] = line.substring(4, 7).toInt();
    inputArray[2] = line.substring(8, 11).toInt();
    inputArray[3] = line.substring(12, 15).toInt();
    inputArray[4] = line.substring(16, 19).toInt();
    inputArray[5] = line.substring(20, 23).toInt();
  }

  // Set servo angles
  servo1.write(inputArray[0]);
  servo2.write(inputArray[1]);
  servo3.write(inputArray[2]);
  servo4.write(inputArray[3]);
  servo5.write(inputArray[4]);
  servo6.write(inputArray[5]);

  Serial.print(inputArray[0]);
  Serial.print(" ");
  Serial.print(inputArray[1]);
  Serial.print(" ");
  Serial.print(inputArray[2]);
  Serial.print(" ");
  Serial.print(inputArray[3]);
  Serial.print(" ");
  Serial.print(inputArray[4]);
  Serial.print(" ");
  Serial.println(inputArray[5]);

}