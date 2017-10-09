//

//==========PWM STUFF================

#include <Servo.h>

Servo axis1;
Servo axis2;
Servo axis3;
Servo axis4;

#define BUF_SIZE 16
char buf[BUF_SIZE];

#define SIGNED_GAIN     2.52 // nominally 2.52
#define SIGNED_OFFSET   93
#define UNSIGNED_GAIN   1.30 // nominally 1.30
#define UNSIGNED_OFFSET 59

//================rangefinder stuff==============



char * parseToBytes(char *ints)    //Parse from iii,iii,iii,iii\n to bbbb
{
    if(strlen(ints) > 16){
        return "TOO LARGE";
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
    
    Serial.print("Parsed to: "); Serial.println(out);
    return out;
}
 
void setup() 
{ 
  axis1.attach(2);  // attaches the servo on pin 9 to the servo object 
  axis2.attach(3);  // attaches the servo on pin 9 to the servo object 
  axis3.attach(4);  // attaches the servo on pin 9 to the servo object 
  axis4.attach(5);  // attaches the servo on pin 9 to the servo object 
  Serial.begin(9600);
  Serial.println("Quad relay begin");
} 

void loop() 
{
  int used = false;
  int i=0;
  while (true){
    if (Serial.available()){
      char c = Serial.read();
      if (c == '\n'){
        break;
      }
      buf[i] = c;
      i++;
      used = true;
    }
  }
  
  if (used){
    Serial.print("buf:"); Serial.println(buf);
    char* res = parseToBytes(buf);
  
    Serial.print("parsed:"); 
    Serial.print((int)res[0]); Serial.print(",");
    Serial.print((int)res[1]); Serial.print(","); 
    Serial.print((int)res[2]); Serial.print(",");
    Serial.print((int)res[3]); Serial.print("\n");
  
    res[0] = res[0]/  SIGNED_GAIN +   SIGNED_OFFSET;
    res[1] = res[1]/  SIGNED_GAIN +   SIGNED_OFFSET;
    res[2] = res[2]/UNSIGNED_GAIN + UNSIGNED_OFFSET;
    res[3] = res[3]/  SIGNED_GAIN +   SIGNED_OFFSET;
  
    Serial.print("final:"); 
    Serial.print((byte)res[0]); Serial.print(",");
    Serial.print((byte)res[1]); Serial.print(","); 
    Serial.print((byte)res[2]); Serial.print(",");
    Serial.print((byte)res[3]); Serial.print("\n");
  
    axis1.write((byte)res[0]);
    axis2.write((byte)res[1]);
    axis3.write((byte)res[2]);
    axis4.write((byte)res[3]);
    
        for (int j=0; j<BUF_SIZE; j++){
          buf[j] = 0;
        }
  }
} 
