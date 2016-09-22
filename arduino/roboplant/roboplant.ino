int ledRed = 13;
int ledYellow = 12;
int ledGreen = 11;

void setup() {
  // initialize the digital pin as an output.
  pinMode(ledRed, OUTPUT);
  pinMode(ledYellow, OUTPUT);
  pinMode(ledGreen, OUTPUT); 
  
  // initialize serial communication at 9600 bits per second:
  Serial.begin(9600);
}


void loop() {
  // read the input on analog pin 0, which is moisture sensor:
  int sensorValue = analogRead(A0); 
  
  Serial.println(sensorValue);
  
  // hand calibrated
  if (sensorValue > 710) {
    digitalWrite(ledGreen, HIGH);
    digitalWrite(ledYellow, LOW);
    digitalWrite(ledRed, LOW);
  } else if (sensorValue > 670 && sensorValue <= 710) {
    digitalWrite(ledGreen, LOW);
    digitalWrite(ledYellow, HIGH);
    digitalWrite(ledRed, LOW);
  } else {
    digitalWrite(ledGreen, LOW);
    digitalWrite(ledYellow, LOW);
    digitalWrite(ledRed, HIGH);
  }
  
  delay(1000);
}
