/* 
*/

#include <Servo.h> 

#define CHANNEL_1 2
#define CHANNEL_2 3
#define CHANNEL_3 4
#define CHANNEL_4 5

#define DELIM ","

#define BATTERY_PIN A0

Servo channelAil;
Servo channelEle;
Servo channelThr;
Servo channelRud;
 
void setup() 
{ 
  channelAil.attach(CHANNEL_1);
  channelEle.attach(CHANNEL_2);
  channelThr.attach(CHANNEL_3);
  channelRud.attach(CHANNEL_4);
  
  pinMode(BATTERY_PIN, INPUT);
  
  Serial.begin(9600);
  Serial.println("begin");
  
  channelAil.write(0);
  channelEle.write(0);
  channelThr.write(0);
  channelRud.write(0);
}

int mapToCtrl(int n){
  return n;
  // TODO: make real mapping
}

// currently: bbbb\n
// need: 123,023,003,232\n
void loop() {
  int count = 0;
  
  char in[32]; // an array to store the received data
  int index = 0;

  while (Serial.available() > 0) {
    char c = Serial.read();
    if (c != '\n') {
      index += 1;
      if (index == 1){
        channelAil.write(c);  Serial.print("1:"); Serial.println((int)c);
      } else if (index == 2){
        channelEle.write(c);  Serial.print("2:"); Serial.println((int)c);
      } else if (index == 3){
        channelThr.write(c);  Serial.print("3:"); Serial.println((int)c);
      } else if (index == 4){
        channelRuds.write(c);  Serial.print("4:"); Serial.println((int)c);
      }
    }
  }
}

