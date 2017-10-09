/* Sensor Pod Firmware
 * @author: Andrew Zhang (andrewzhang100@gmail.com)
 *  
 * HC-SR04 Ping distance sensor
 * 
 * Usage: 
 * 1) Vcc to arduino 5v
 * 2) Gnd to arduino GND
 * 3) Echo to Arduino pin 13 
 * 4) Trig to Arduino pin 12
 * 
 * Reference Code: http://www.instructables.com/id/Simple-Arduino-and-HC-SR04-Example/
 * Datasheet: https://cdn.sparkfun.com/datasheets/Sensors/Proximity/HCSR04.pdf
 * 
 * IMU not selected yet
 */

#define BAUD_RATE 9600

#define RANGEFINDER_VCC_PIN 3
#define RANGEFINDER_TRIG_PIN A3
#define RANGEFINDER_ECHO_PIN A2
#define RANGEFINDER_GND_PIN 6

#define RANGEFINDER_SPEED_OF_SOUND 30 // cm per us
#define RANGEFINDER_PERIOD 100 // in ms, datasheet recommends 60ms
#define RANGEFINDER_MAX_DISTANCE 400 // in cm, datasheet says 400cm
#define RANGEFINDER_PULSE_WIDTH 10 // in us, datasheet recommends 10us
#define RANGEFINDER_INITIAL_DELAY 2 // in us

//=============declare all functions=======

void imuSetup();
void sendIMUData();
void getIMU(int* accl_x, int* accl_y, int* accl_z,
            int* gyro_x, int* gyro_y, int* gyro_z,
            int* hall_x, int* hall_y, int* hall_z);

void rangeFinderSetup();
void sendRangeFinderData();
float getRangeFinder();

//=============main functions=============

void setup() {
  Serial.begin(BAUD_RATE);
  rangeFinderSetup();
  imuSetup();
}

void loop() {
  // sendImuData();
  sendRangeFinderData();
}

//=====================IMU========================

void imuSetup(){}

void sendImuData(){
  int accl_x, accl_y, accl_z;
  int gyro_x, gyro_y, gyro_z;
  int hall_x, hall_y, hall_z;
  getImu(&accl_x, &accl_y, &accl_z,
          &gyro_x, &gyro_y, &gyro_z,
          &hall_x, &hall_y, &hall_z);
  Serial.print("{accl_x:"); Serial.print(accl_x);
  Serial.print(", accl_y:"); Serial.print(accl_y);
  Serial.print(", accl_z:"); Serial.print(accl_z);
  Serial.print(", gyro_x:"); Serial.print(gyro_x);
  Serial.print(", gyro_y:"); Serial.print(gyro_y);
  Serial.print(", gyro_z:"); Serial.print(gyro_z);
  Serial.print(", hall_x:"); Serial.print(hall_x);
  Serial.print(", hall_y:"); Serial.print(hall_y);
  Serial.print(", hall_z:"); Serial.print(hall_z);
  Serial.println("}");
}

void getImu(int* accl_x, int* accl_y, int* accl_z,
             int* gyro_x, int* gyro_y, int* gyro_z,
             int* hall_x, int* hall_y, int* hall_z){
  *accl_x = 4;
  *accl_y = 12;
  *accl_z = 54;
  *gyro_x = 5;
  *gyro_x = 76;
  *gyro_x = 12;
  *hall_x = 43;
  *hall_x = 67;
  *hall_x = 2;
}

//==================RANGEFINDER==============

void rangeFinderSetup() {
  Serial.begin(BAUD_RATE);
  pinMode(RANGEFINDER_TRIG_PIN, OUTPUT);
  pinMode(RANGEFINDER_ECHO_PIN, INPUT);
  
  pinMode(RANGEFINDER_VCC_PIN, OUTPUT);
  pinMode(RANGEFINDER_GND_PIN, OUTPUT);
  digitalWrite(RANGEFINDER_GND_PIN, LOW);
  digitalWrite(RANGEFINDER_VCC_PIN, HIGH);
}

void sendRangeFinderData(){
  float distance = getRangeFinder();
  if (distance >= RANGEFINDER_MAX_DISTANCE || distance <= 0){
    Serial.println("Out of range");
  } else {
    Serial.print("[");
    Serial.print(distance);
    Serial.println("]"); // in cm
  }
}

float getRangeFinder(){
  static long prevTrigger;
  while (millis() < prevTrigger + RANGEFINDER_PERIOD){}
  prevTrigger = millis();
  
  digitalWrite(RANGEFINDER_TRIG_PIN, LOW); delayMicroseconds(2);
  digitalWrite(RANGEFINDER_TRIG_PIN, HIGH); delayMicroseconds(10); digitalWrite(RANGEFINDER_TRIG_PIN, LOW);
  double ttl = pulseIn(RANGEFINDER_ECHO_PIN, HIGH);
  double res = (ttl/2) / RANGEFINDER_SPEED_OF_SOUND;
  return res;
}
