#define TRIG_PIN 2       // Trig pin for sonar
#define ECHO_PIN 3      // Echo pin for sonar
#define THRESHOLD 3    // Distance threshold in cm

// RGB LED pins - MAKE SURE THEY'RE PWM!!
#define RED_PIN 5
#define GREEN_PIN 6
#define BLUE_PIN 9

void setup() {
  Serial.begin(9600);

  // Setup sonar pins
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);

  // Setup RGB LED pins
  pinMode(RED_PIN, OUTPUT);
  pinMode(GREEN_PIN, OUTPUT);
  pinMode(BLUE_PIN, OUTPUT);

  // setLEDColor(20, 20, 20);
}

void loop() {
  // Measure distance
  float distance = measureDistance();
  Serial.println(distance);

  // Change RGB LED color based on distance
  // if (distance > 50) {
  //   setLEDColor(0, 20, 0); // Green: Far
  // } else if (distance > 20) {
  //   setLEDColor(20, 20, 0); // Yellow: Medium
  // } else {
  //   setLEDColor(20, 0, 0); // Red: Close
  // }

  if (Serial.available()) {
        String data = Serial.readStringUntil('\n'); // Read data until newline
        int red, green, blue;
        if (sscanf(data.c_str(), "%d,%d,%d", &red, &green, &blue) == 3) {
            analogWrite(RED_PIN, red);   // Set Red intensity
            analogWrite(GREEN_PIN, green); // Set Green intensity
            analogWrite(BLUE_PIN, blue);  // Set Blue intensity
        }
    }

  delay(100); // Loop delay
}

// Function to measure distance
float measureDistance() {
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);

  long duration = pulseIn(ECHO_PIN, HIGH);
  return (duration / 2.0) * 0.0343; // Convert to cm
}

// Function to set RGB LED color
void setLEDColor(int red, int green, int blue) {
  analogWrite(RED_PIN, red);
  analogWrite(GREEN_PIN, green);
  analogWrite(BLUE_PIN, blue);
}
