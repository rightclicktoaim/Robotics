/* @copyright Rui Santos
 * Complete project details at https://RandomNerdTutorials.com/esp8266-nodemcu-hc-sr04-ultrasonic-arduino/
  
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files.
 *   
 *   @author Stephen A Ralis
 *   Help Received: In-class presentations, Tutorial by Rui Santos
 */

// Initializes the data pins at the following GPIO pin addresses
int RED_PIN = 12;
int GREEN_PIN = 13;
int TRIGGER_PIN = 5;
int ECHO_PIN = 4;

// Predefined constants - required for distance calculations
#define SOUND_VELOCITY 0.034
#define CM_TO_INCH 0.393701

// Duration in Milliseconds - directly from the audio sensor and received by the ECHO_PIN
long durationMs;

// These will be derived from the above three values and computed in the loop()
float distanceCm;
float distanceInch;

void setup() {

  // Opens the serial listener at the given frequency
  Serial.begin(115200);

  // Set the LEDs and TRIGGER_PIN for the audio sensor as OUTPUT pin-types
  pinMode(RED_PIN, OUTPUT);
  pinMode(GREEN_PIN, OUTPUT);
  pinMode(TRIGGER_PIN, OUTPUT);

  // Set the ECHO_PIN for the audio sensor as an INPUT pin-type
  pinMode(ECHO_PIN, INPUT);

}

void loop() {

  // Resets the TRIGGER_PIN 
  digitalWrite(TRIGGER_PIN, LOW);
  delayMicroseconds(2);

  // Brings the TRIGGER_PIN HIGH for 10 micro seconds - audio is transmitted
  digitalWrite(TRIGGER_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIGGER_PIN, LOW);
  
  // Times how long the ECHO_PIN is HIGH - audio is received
  durationMs = pulseIn(ECHO_PIN, HIGH);
  
  // Calculate the distance in Centimeters
  distanceCm = durationMs * SOUND_VELOCITY/2;
  
  // Convert the distance to inches
  distanceInch = distanceCm * CM_TO_INCH;
  
  // Prints the distance on the Serial Monitor
  Serial.clearWriteError();
  Serial.print("Distance (cm): ");
  Serial.println(distanceCm);
  Serial.print("Distance (inch): ");
  Serial.println(distanceInch);
  Serial.println();

  // IF less than 10 inches, turn ON the Red LED
  if( distanceInch <= 10 ){
    digitalWrite(GREEN_PIN, LOW);
    digitalWrite(RED_PIN, HIGH);
  }

  // IF greater than 10 inches, turn ON the Green LED
  if( distanceInch > 10 ){
    digitalWrite(RED_PIN, LOW);
    digitalWrite(GREEN_PIN, HIGH);
  }

  // Loop 10 times per second - delay in milliseconds
  delay( 100 );

}