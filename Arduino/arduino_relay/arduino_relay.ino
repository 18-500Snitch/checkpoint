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

#define BUF_SIZE 16
char buf[BUF_SIZE];

#define SIGNED_GAIN     2.52 // nominally 2.52
#define SIGNED_OFFSET   93
#define UNSIGNED_GAIN   1.30 // nominally 1.30
#define UNSIGNED_OFFSET 59

char* parseToBytes(char *ints)    //Parse from iii,iii,iii,iii\n to bbbb
{
    if(strlen(ints) > 16){
        return ">DEBUG: TOO LARGE";
    }
    char split[4][4];
    char *int_literal, *num;
    static char out[32];
    int_literal = strdup(ints);

    int i = 0;
    while( (num = strsep(&int_literal, ",")) != NULL )
    {
        out[i] = strtol(num, NULL, 10);
        i++;
    }
    
    // Serial.print("Parsed to: "); Serial.println(out);
    return out;
}

void parseSerialToPWM(){  int used = false;
  int i=0;
  while (Serial.available()){
    char c = Serial.read();
    if (c == '\n'){
      break;
    }
    buf[i] = c;
    i++;
    used = true;
  }
  
  if (used){
    // Serial.print("buf:"); Serial.println(buf);
    char* res = parseToBytes(buf);
  
    // Serial.print("parsed:"); 
    // Serial.print((int)res[0]); Serial.print(",");
    // Serial.print((int)res[1]); Serial.print(","); 
    // Serial.print((int)res[2]); Serial.print(",");
    // Serial.print((int)res[3]); Serial.print("\n");
  
    res[0] = res[0]/  SIGNED_GAIN +   SIGNED_OFFSET;
    res[1] = res[1]/  SIGNED_GAIN +   SIGNED_OFFSET;
    res[2] = res[2]/UNSIGNED_GAIN + UNSIGNED_OFFSET;
    res[3] = res[3]/  SIGNED_GAIN +   SIGNED_OFFSET;
  
    // Serial.print("final:"); 
    // Serial.print((byte)res[0]); Serial.print(",");
    // Serial.print((byte)res[1]); Serial.print(","); 
    // Serial.print((byte)res[2]); Serial.print(",");
    // Serial.print((byte)res[3]); Serial.print("\n");
  
    axis1.write((byte)res[0]);
    axis2.write((byte)res[1]);
    axis3.write((byte)res[2]);
    axis4.write((byte)res[3]);
    
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
 
#define RANGEFINDER_TRIG_PIN 6
#define RANGEFINDER_ECHO_PIN 7

#define RANGEFINDER_SPEED_OF_SOUND 30 // cm per us
#define RANGEFINDER_PERIOD 100 // in ms, datasheet recommends 60ms
#define RANGEFINDER_MAX_DISTANCE 400 // in cm, datasheet says 400cm
#define RANGEFINDER_PULSE_WIDTH 10 // in us, datasheet recommends 10us
#define RANGEFINDER_INITIAL_DELAY 2 // in us
#define RANGEFINDER_TIMEOUT 250
float getDistance(){
  static long prevTrigger;
  while (millis() < prevTrigger + RANGEFINDER_PERIOD){}
  prevTrigger = millis();
  
  digitalWrite(RANGEFINDER_TRIG_PIN, LOW); delayMicroseconds(2);
  digitalWrite(RANGEFINDER_TRIG_PIN, HIGH); delayMicroseconds(10); digitalWrite(RANGEFINDER_TRIG_PIN, LOW);
  double ttl = pulseIn(RANGEFINDER_ECHO_PIN, HIGH, RANGEFINDER_TIMEOUT);
  double res = (ttl/2) / RANGEFINDER_SPEED_OF_SOUND;
  return res;
}

void rangefinderSetup(){ 
  pinMode(RANGEFINDER_TRIG_PIN, OUTPUT);
  pinMode(RANGEFINDER_ECHO_PIN, INPUT);
}

void sendRangefinder(){
  float distance = getDistance();
  if (distance >= RANGEFINDER_MAX_DISTANCE || distance <= 0){
    Serial.println(">DEBUG: Out of range");
  } else {
    Serial.print(">("); Serial.print(distance); Serial.print(","); Serial.print(distance); Serial.print(")");
    Serial.println();
    // Serial.println("cm");
  }
  delay(RANGEFINDER_PERIOD);
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
}
