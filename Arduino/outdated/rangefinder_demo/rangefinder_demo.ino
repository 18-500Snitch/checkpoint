/* HC-SR04 Ping distance sensor
 * @author: Andrew Zhang (andrewzhang100@gmail.com)
 * 
 * Usage: 
 * 1) Vcc to arduino 5v
 * 2) Gnd to arduino GND
 * 3) Echo to Arduino pin 13 
 * 4) Trig to Arduino pin 12
 * 
 * Reference Code: http://www.instructables.com/id/Simple-Arduino-and-HC-SR04-Example/
 * Datasheet: https://cdn.sparkfun.com/datasheets/Sensors/Proximity/HCSR04.pdf
 */

#define BAUD_RATE 9600
 
#define RANGEFINDER_TRIG_PIN 5
#define RANGEFINDER_ECHO_PIN 4

#define RANGEFINDER_SPEED_OF_SOUND 30 // cm per us
#define RANGEFINDER_PERIOD 100 // in ms, datasheet recommends 60ms
#define RANGEFINDER_MAX_DISTANCE 400 // in cm, datasheet says 400cm
#define RANGEFINDER_PULSE_WIDTH 10 // in us, datasheet recommends 10us
#define RANGEFINDER_INITIAL_DELAY 2 // in us

void setup() {
  Serial.begin(BAUD_RATE);
  pinMode(RANGEFINDER_TRIG_PIN, OUTPUT);
  pinMode(RANGEFINDER_ECHO_PIN, INPUT);
}

void loop() {
  float distance = getDistance();
  if (distance >= RANGEFINDER_MAX_DISTANCE || distance <= 0){
    Serial.println("Out of range");
  } else {
  Serial.print(distance); Serial.println("cm");
  }
  delay(RANGEFINDER_PERIOD);
}

float getDistance(){
  static long prevTrigger;
  while (millis() < prevTrigger + RANGEFINDER_PERIOD){}
  prevTrigger = millis();
  
  digitalWrite(RANGEFINDER_TRIG_PIN, LOW); delayMicroseconds(2);
  digitalWrite(RANGEFINDER_TRIG_PIN, HIGH); delayMicroseconds(10); digitalWrite(RANGEFINDER_TRIG_PIN, LOW);
  double ttl = pulseIn(RANGEFINDER_ECHO_PIN, HIGH);
  double res = (ttl/2) / RANGEFINDER_SPEED_OF_SOUND;
  return res;
}
