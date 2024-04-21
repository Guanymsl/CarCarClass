#ifndef _FUNCTION_H_
#define _FUNCTION_H_

//RFID.h
byte* rfid(byte&);

//bluetooth.h
enum BT_CMD{

    NOTHING,
    // TODO: add your own command type here

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
//void MotorInverter(int, bool&);
void tracking();

#endif