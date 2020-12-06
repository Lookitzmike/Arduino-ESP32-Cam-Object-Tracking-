#include <Servo.h>
#define DELAY 30

Servo servoX;
char InBytes = ' ';
int var;

void setup() {
  Serial.begin(9600);
  servoX.attach(3);
  servoX.write(90);

}

void loop() {
  receive();
}

void receive() {
  if (Serial.available() > 0) {
    char InBytes = Serial.read();
    Serial.println("Outside");
    Serial.println(InBytes);
    if (InBytes == '1') { // Right
      for (var = 0; var >= 90; var -= 10) {
        servoX.write(var);
        delay(DELAY);
        Serial.println("In 1");
        Serial.println(InBytes);
      }
    }
    else if (InBytes == '2') { // Left
      for (var = 0; var <= 90; var += 10) {
        servoX.write(var);
        delay(DELAY);
        Serial.println("In 2");
        Serial.println(InBytes);
      }
    }
    else if (InBytes == '3') { // Center
      servoX.write(90);
      delay(DELAY);
      Serial.println("In 3");
      Serial.println(InBytes);
    }
  }
}
