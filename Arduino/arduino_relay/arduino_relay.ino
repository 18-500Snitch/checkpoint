#include <NewPing.h>
//

//==========PPM STUFF================
//////////////////////CONFIGURATION///////////////////////////////
#define CHANNEL_NUMBER 12  //set the number of chanels
#define CHANNEL_DEFAULT_VALUE 1500  //set the default servo value
#define FRAME_LENGTH 22500  //set the PPM frame length in microseconds (1ms = 1000µs)
#define PULSE_LENGTH 300  //set the pulse length
#define onState 1  //set polarity of the pulses: 1 is positive, 0 is negative
#define sigPin 10  //set PPM signal output pin on the arduino

/*this array holds the servo values for the ppm signal
  change theese values in your code (usually servo values move between 1000 and 2000)*/
int ppm[CHANNEL_NUMBER];

#define BUF_SIZE 25
char buf[BUF_SIZE];

//================rangefinder stuff==============
#define TRIGGER_PIN   12
#define ECHO_PIN      11
#define MAX_DISTANCE  200

NewPing sonar(TRIGGER_PIN, ECHO_PIN, MAX_DISTANCE);
unsigned int pingSpeed = 50;
unsigned long pingTimer;
unsigned int pingDist = 0;

//Parse from iiii,iiii,iiii,iiii\n to ints
void parseToInts(char *ints,int *out)
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

void parseSerialToPPM(){
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
    parseToInts(buf,ppm);
  
    //Serial.print("parsed:"); 
    //Serial.print((int)ppm[0]); Serial.print(",");
    //Serial.print((int)ppm[1]); Serial.print(","); 
    //Serial.print((int)ppm[2]); Serial.print(",");
    //Serial.print((int)ppm[3]); Serial.print("\n");
    for (int j=0; j<BUF_SIZE; j++){
      buf[j] = 0;
    }
  }
}

void ppmSetup(){
  //initiallize default ppm values
  for (int i = 0; i < CHANNEL_NUMBER; i++) {
    ppm[i] = CHANNEL_DEFAULT_VALUE;
  }

  pinMode(sigPin, OUTPUT);
  digitalWrite(sigPin, !onState);  //set the PPM signal pin to the default state (off)

  cli();
  TCCR1A = 0; // set entire TCCR1 register to 0
  TCCR1B = 0;

  OCR1A = 100;  // compare match register, change this
  TCCR1B |= (1 << WGM12);  // turn on CTC mode
  TCCR1B |= (1 << CS11);  // 8 prescaler: 0,5 microseconds at 16mhz
  TIMSK1 |= (1 << OCIE1A); // enable timer compare interrupt
  sei();
}

void rangefinderSetup(){
  pingTimer = millis();
}

void sendRangefinder(){
  static float oldDistance;
  if(oldDistance == pingDist)
  {
    return;
  }
  oldDistance = pingDist;
  if (oldDistance >= MAX_DISTANCE || oldDistance <= 0){
    Serial.println(">DEBUG: Out of range");
  } else {
    Serial.print(">("); Serial.print(oldDistance); Serial.print(","); Serial.print(oldDistance); Serial.print(")");
    Serial.println();
  }
}

void echoCheck () {
  if (sonar.check_timer()) {
    pingDist = sonar.ping_result / US_ROUNDTRIP_CM;
  }
}

//===============main=================

#define BAUD_RATE 9600

void setup() 
{ 
  Serial.begin(BAUD_RATE);
  Serial.println(">DEBUG: Arduino relay begin");
  ppmSetup();
  rangefinderSetup();
  Serial.println(">DEBUG: Arduino relay setup finished");
} 

void loop() 
{
  if (millis() >= pingTimer)
  {
    pingTimer += pingSpeed;
    sonar.ping_timer(echoCheck);
  }
  parseSerialToPPM();
  //sendRangefinder();
}


ISR(TIMER1_COMPA_vect) { //leave this alone
  static boolean state = true;

  TCNT1 = 0;

  if (state) {  //start pulse
    digitalWrite(sigPin, onState);
    OCR1A = PULSE_LENGTH * 2;
    state = false;
  } else { //end pulse and calculate when to start the next pulse
    static byte cur_chan_numb;
    static unsigned int calc_rest;

    digitalWrite(sigPin, !onState);
    state = true;

    if (cur_chan_numb >= CHANNEL_NUMBER) {
      cur_chan_numb = 0;
      calc_rest = calc_rest + PULSE_LENGTH;//
      OCR1A = (FRAME_LENGTH - calc_rest) * 2;
      calc_rest = 0;
    }
    else {
      OCR1A = (ppm[cur_chan_numb] - PULSE_LENGTH) * 2;
      calc_rest = calc_rest + ppm[cur_chan_numb];
      cur_chan_numb++;
    }
  }
}
