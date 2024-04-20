/***************************************************************************/
// File			  [bluetooth.h]
// Author		  [Erik Kuo]
// Synopsis		  [Code for bluetooth communication]
// Functions      [ask_BT, send_msg, send_byte]
// Modify		  [2020/03/27 Erik Kuo]
/***************************************************************************/

/*if you have no idea how to start*/
/*check out what you have learned from week 2*/

#ifndef _BLUETOOTH_H_
#define _BLUETOOTH_H_

BT_CMD ask_BT(){

    BT_CMD message = NOTHING;
    char cmd;

    if(Serial1.available()){
        // TODO:
        // 1. get cmd from Serial1(bluetooth serial)
        // 2. link bluetooth message to your own command type

        cmd = Serial1.read();

        #ifdef DEBUG
        Serial.print("cmd : ");
        Serial.println(cmd);
        #endif

        if(cmd == 's') message = START;
        else if(cmd == 'e') message = END;
        else if(cmd == 'f') message = FORWARD;
        else if(cmd == 'r') message = RIGHT;
        else if(cmd == 'l') message = LEFT;
        else if(cmd == 'b') message = TURN;
        else if(cmd == 'h') message = HALT;

    }

    return message;

}  // ask_BT

// send msg back through Serial1(bluetooth serial)
// can use send_byte alternatively to send msg back
// (but need to convert to byte type)

void send_msg(const char& msg){
    // TODO:

    Serial1.write(msg);

}  // send_msg

// send UID back through Serial1(bluetooth serial)
void send_byte(byte* id, byte& idSize){

    for (byte i = 0; i < idSize; i++){  // Send UID consequently.
        Serial1.write(id[i]);
    }

    #ifdef DEBUG
    Serial.print("Sent id: ");
    for (byte i = 0; i < idSize; i++){  // Show UID consequently.
        if(id[i] < 10) Serial.print('0');
        Serial.print(id[i], HEX);
    }
    Serial.println();
    #endif

}  // send_byte

#endif