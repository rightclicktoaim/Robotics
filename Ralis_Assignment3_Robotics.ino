int RED_PIN = 12;
int GREEN_PIN = 13;
int TRIGGER_PIN = 5;
int ECHO_PIN = 4;

#define SOUND_VELOCITY 0.034
#define CM_TO_INCH 0.393701

long durationMs;
float distanceCm;
float distanceInch;

void setup() {

  Serial.begin(115200); // Starts the serial communication

  pinMode(RED_PIN, OUTPUT); // Set the Red LED pin to ouptut mode
  pinMode(GREEN_PIN, OUTPUT); // Set the Green LED pin to ouptut mode

  pinMode(TRIGGER_PIN, OUTPUT); // Set the Red LED pin to ouptut mode
  pinMode(ECHO_PIN, INPUT); // Set the Green LED pin to ouptut mode

}

void loop() {

  // Clears the trigPin
  digitalWrite(TRIGGER_PIN, LOW);
  delayMicroseconds(2);
  // Sets the trigPin on HIGH state for 10 micro seconds
  digitalWrite(TRIGGER_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIGGER_PIN, LOW);
  
  // Reads the ECHO_PIN, returns the sound wave travel time in microseconds
  durationMs = pulseIn(ECHO_PIN, HIGH);
  
  // Calculate the distance
  distanceCm = durationMs * SOUND_VELOCITY/2;
  
  // Convert to inches
  distanceInch = distanceCm * CM_TO_INCH;
  
  // Prints the distance on the Serial Monitor
  Serial.clearWriteError();
  Serial.print("Distance (cm): ");
  Serial.println(distanceCm);
  Serial.print("Distance (inch): ");
  Serial.println(distanceInch);
  Serial.println();

  // IF less than 10 inches, turn ON the Red LED
  if(distanceInch <= 10){
    digitalWrite(GREEN_PIN, LOW);
    digitalWrite(RED_PIN, HIGH);
  }

  // IF greater than 10 inches, turn ON the Green LED
  if(distanceInch > 10){
    digitalWrite(RED_PIN, LOW);
    digitalWrite(GREEN_PIN, HIGH);
  }

  // Wait for ONE second, then LOOP
  delay(100);

}