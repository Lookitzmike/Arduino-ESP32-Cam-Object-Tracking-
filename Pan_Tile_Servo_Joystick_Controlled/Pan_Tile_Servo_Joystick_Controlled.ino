#include <Servo.h>

Servo servoX;
Servo servoY;
int pan_X;
int tilt_Y;

void setup() {
  Serial.begin(9600);
  servoX.attach(3);
  servoY.attach(4);
}

void loop() {
  pan_X = analogRead(A1);
  pan_X = map(pan_X, 0, 1023, 30, 150);
  servoX.write(pan_X);
  delay(25);
  Serial.print("Pan Deg =  ");
  Serial.print(pan_X);
  
  tilt_Y = analogRead(A2);
  tilt_Y = map(tilt_Y, 0, 1023, 50, 130);
  servoY.write(tilt_Y);
  delay(25);
  Serial.print(" || Tilt Deg =  ");
  Serial.println(tilt_Y);
  
}
