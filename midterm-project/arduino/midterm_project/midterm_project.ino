#include "function.h"

int motor_speed = 180;
int turn_speed = motor_speed / 2;
char step;
bool reading = false;

MFRC522 mfrc522(SS, RST);
STATE state = STOP;
BT_CMD _cmd = NOTHING;

#include "RFID.h"
#include "bluetooth.h"
#include "node.h"
#include "track.h"

void setup(){

    Serial1.begin(9600);
    Serial.begin(9600);

    SPI.begin();
    mfrc522.PCD_Init();

    pinMode(PWMR, OUTPUT);
    pinMode(PWML, OUTPUT);
    pinMode(RIN1, OUTPUT);
    pinMode(RIN2, OUTPUT);
    pinMode(LIN1, OUTPUT);
    pinMode(LIN2, OUTPUT);

    pinMode(IRL2, INPUT);
    pinMode(IRL1, INPUT);
    pinMode(IRM, INPUT);
    pinMode(IRR1, INPUT);
    pinMode(IRR2, INPUT);

    #ifdef DEBUG
    Serial.println("Start!");
    #endif

}

void loop(){

    if(state == STOP) MotorWriting(0, 0);
    if(state != SEARCH) SetState();
    if(state == SEARCH) Search();

}

void SetState(){

    _cmd = ask_BT();

    if(_cmd == START) reading = true;
    else if(_cmd == END) reading = false, state = STOP;
    else if(reading && _cmd != NOTHING){

        if(_cmd == FORWARD) step = 'f';
        else if(_cmd == RIGHT) step = 'r';
        else if(_cmd == LEFT) step = 'l';
        else if(_cmd == TURN) step = 'b';
        else if(_cmd == HALT) step = 'h';

        state = SEARCH;

    }

}

void Search(){

    tracking();
    detecting();

}