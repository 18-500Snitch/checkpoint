//

//==========PWM STUFF================

#include <Servo.h>

Servo axis1;
Servo axis2;
Servo axis3;
Servo axis4;

#define AXIS_1_PIN 2
#define AXIS_2_PIN 3
#define AXIS_3_PIN 4
#define AXIS_4_PIN 5

#define BUF_SIZE 21
char buf[BUF_SIZE];
int speedBuf[4];
#define SIGNED_GAIN     2.52 // nominally 2.52
#define SIGNED_OFFSET   93
#define UNSIGNED_GAIN   1.30 // nominally 1.30
#define UNSIGNED_OFFSET 59
void parseToBytes(char *ints,int *out)    //Parse from iii,iii,iii,iii\n to bbbb
{
    if(strlen(ints) > 21){
        Serial.println(">DEBUG: TOO LARGE");
    }
    char *tokens[4];
    char *ptr = strtok(ints,",");
    byte index = 0;
    while(ptr != NULL)
    {
      tokens[index] = ptr;
      ptr = strtok(NULL,",");
      index++;
    }
    if(index != 4) return;
    for( int i = 0; i < 4; i++)
    {
      out[i] = atoi(tokens[i]);
    }
}

void parseSerialToPWM(){
  static int messageRec = false;
  static int i=0;
  if (Serial.available()){
    char c = Serial.read();
    if (c == '\n'){
      messageRec = true;
    } else {
      buf[i] = c;
      i++;
    }
  }
  
  if (messageRec){
    messageRec = false;
    i = 0;
    //Serial.print("buf:"); Serial.println(buf);
    parseToBytes(buf,speedBuf);
  
    //Serial.print("parsed:"); 
    //Serial.print((int)speedBuf[0]); Serial.print(",");
    //Serial.print((int)speedBuf[1]); Serial.print(","); 
    //Serial.print((int)speedBuf[2]); Serial.print(",");
    //Serial.print((int)speedBuf[3]); Serial.print("\n");
  
    speedBuf[0] = speedBuf[0]/  SIGNED_GAIN +   SIGNED_OFFSET;
    speedBuf[1] = speedBuf[1]/  SIGNED_GAIN +   SIGNED_OFFSET;
    speedBuf[2] = speedBuf[2]/UNSIGNED_GAIN + UNSIGNED_OFFSET;
    speedBuf[3] = speedBuf[3]/  SIGNED_GAIN +   SIGNED_OFFSET;
  
    //Serial.print("final:"); 
    //Serial.print((int)speedBuf[0]); Serial.print(",");
    //Serial.print((int)speedBuf[1]); Serial.print(","); 
    //Serial.print((int)speedBuf[2]); Serial.print(",");
    //Serial.print((int)speedBuf[3]); Serial.print("\n");
  
    axis1.write(speedBuf[0]);
    axis2.write(speedBuf[1]);
    axis3.write(speedBuf[2]);
    axis4.write(speedBuf[3]);
    
    for (int j=0; j<BUF_SIZE; j++){
      buf[j] = 0;
    }
  }
}

void pwmSetup(){
  axis1.attach(AXIS_1_PIN);  // attaches the servo on pin 9 to the servo object 
  axis2.attach(AXIS_2_PIN);  // attaches the servo on pin 9 to the servo object 
  axis3.attach(AXIS_3_PIN);  // attaches the servo on pin 9 to the servo object 
  axis4.attach(AXIS_4_PIN);  // attaches the servo on pin 9 to the servo object 
}

//================rangefinder stuff==============
 
#define RANGEFINDER_TRIG_PIN 7
#define RANGEFINDER_ECHO_PIN 6

#define RANGEFINDER_SPEED_OF_SOUND 30 // cm per us
#define RANGEFINDER_PERIOD 100 // in ms, datasheet recommends 60ms
#define RANGEFINDER_MAX_DISTANCE 400 // in cm, datasheet says 400cm
#define RANGEFINDER_PULSE_WIDTH 10 // in us, datasheet recommends 10us
#define RANGEFINDER_INITIAL_DELAY 2 // in us
#define RANGEFINDER_TIMEOUT 250000
float getDistance(){
  static double res;
  static long prevTrigger;
  if(millis() < prevTrigger + RANGEFINDER_PERIOD){return res;}
  prevTrigger = millis();
  
  digitalWrite(RANGEFINDER_TRIG_PIN, LOW); delayMicroseconds(2);
  digitalWrite(RANGEFINDER_TRIG_PIN, HIGH); delayMicroseconds(10); digitalWrite(RANGEFINDER_TRIG_PIN, LOW);
  double ttl = pulseIn(RANGEFINDER_ECHO_PIN, HIGH, RANGEFINDER_TIMEOUT);
  res = (ttl/2) / RANGEFINDER_SPEED_OF_SOUND;
  return res;
}

void rangefinderSetup(){ 
  pinMode(RANGEFINDER_TRIG_PIN, OUTPUT);
  pinMode(RANGEFINDER_ECHO_PIN, INPUT);
}

void sendRangefinder(){
  static float oldDistance;
  float distance = getDistance();
  if(oldDistance == distance)
  {
    return;
  }
  oldDistance = distance;
  if (distance >= RANGEFINDER_MAX_DISTANCE || distance <= 0){
    Serial.println(">DEBUG: Out of range");
  } else {
    Serial.print(">("); Serial.print(distance); Serial.print(","); Serial.print(distance); Serial.print(")");
    Serial.println();
    // Serial.println("cm");
  }
}

//===============main=================

#define BAUD_RATE 9600

void setup() 
{ 
  Serial.begin(BAUD_RATE);
  Serial.println(">DEBUG: Arduino relay begin");
  pwmSetup();
  rangefinderSetup();
  Serial.println(">DEBUG: Arduino relay setup finished");
} 

void loop() 
{
  parseSerialToPWM();
  sendRangefinder();
  delayMicroseconds(2);
}
