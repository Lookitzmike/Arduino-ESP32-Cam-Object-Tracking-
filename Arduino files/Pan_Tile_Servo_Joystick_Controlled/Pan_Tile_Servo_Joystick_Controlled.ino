#include <Servo.h>
#define DELAY 0.5
#define buttonPin 2
#define LED1 6
#define LED2 7

Servo servoX;
Servo servoY;
int pan_X;
int tilt_Y;
int InByte;

int buttonCounter = 0;    // Counter for number of button press
int currentState = 0;     // Current state of button
int previousState = 0;    // Past state of button

void setup() {
  pinMode(buttonPin, INPUT);
  pinMode(LED1, OUTPUT);    // LED indicator that manual is selected
  pinMode(LED2, OUTPUT);    // LED indicator that Auto is selected
  servoX.attach(3);
  servoY.attach(4);
  Serial.begin(9600);
}

void loop() {
  currentState = digitalRead(buttonPin);    // Read button press
  if (currentState != previousState){       // If detect button press by comparing the current state with previous
    if (currentState == HIGH){
      buttonCounter++;                      // Increment 1 
    }
    delay(100);                             // Delay to avoid spamming button
  }
  previousState = currentState;             // Save current state to previous state
  if (buttonCounter % 2 == 0){              // If the buttonCounter value divided by 2 gives no remainder
    serialComm();
    digitalWrite(LED2, HIGH);
    digitalWrite(LED1, LOW);
  } else {
    joystickControl();
    digitalWrite(LED2, LOW);
    digitalWrite(LED1, HIGH);
  }
}

void serialComm(){  
  if (Serial.available()) {
    InByte = Serial.parseInt();
    servoX.write(InByte);
    delay(DELAY);
  }  
}

void joystickControl(){
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
