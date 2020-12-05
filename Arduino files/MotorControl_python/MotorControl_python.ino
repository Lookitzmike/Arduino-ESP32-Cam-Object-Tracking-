#include <Servo.h>
#define DELAY 100

Servo servoX;
String InBytes;
String var;

void setup() {
  Serial.begin(9600);
  servoX.attach(3);
  servoX.write(90);

}

void loop() {
  if (Serial.available() > 0) {
    InBytes = Serial.readStringUntil('\n');
    var = InBytes;
    if (InBytes == "right") {
      servoX.write(0);
      delay(DELAY);
    }
    else if (InBytes == "left") {
      servoX.write(180);      
      delay(DELAY);
    }
    else if (InBytes == "middle") {
      servoX.write(90);      
      delay(DELAY);
    }
  }
}
