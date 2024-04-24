#ifndef _FUNCTION_H_
#define _FUNCTION_H_

#define DEBUG

#define PWMR 11
#define PWML 12
#define RIN1 2
#define RIN2 3
#define LIN1 5
#define LIN2 6

#define IRL2 32
#define IRL1 34
#define IRM 36
#define IRR1 38
#define IRR2 40

#define RST 9
#define SS 53

#include <MFRC522.h>
#include <SPI.h>
#include <math.h>

//midterm_project.ino
enum STATE{

  STOP,
  RECEIVE,
  SEARCH

};
void Search();
void SetState();

//RFID.h
byte* rfid(byte&);
void detecting();

//bluetooth.h
enum BT_CMD{

    NOTHING,

    START,
    END,

    FORWARD,
    RIGHT,
    LEFT,
    TURN,
    HALT

};
BT_CMD ask_BT();
void send_msg(const char&);
void send_byte(byte*, byte&);

//node.h
void Right_Turn();
void Left_Turn();
void Turn_Around();
void Halt();

//track.h
void MotorWriting(double, double);
void tracking();

#endif