#define LED 2
String InBytes;

void setup() {
  Serial.begin(9600);
  pinMode(LED, OUTPUT);
}

void loop() {
  if (Serial.available() > 0) {
    InBytes = Serial.readStringUntil('\n');
    if (InBytes == "on") {
      digitalWrite(LED, HIGH);
      Serial.println("LED ON");
    }
    if (InBytes == "off") {
      digitalWrite(LED, LOW);
      Serial.println("LED OFF");
    }
  }
}
