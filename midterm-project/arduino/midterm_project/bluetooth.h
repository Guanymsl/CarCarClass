#ifndef _BLUETOOTH_H_
#define _BLUETOOTH_H_

BT_CMD ask_BT(){

    BT_CMD message = NOTHING;

    if(Serial1.available()){

        char cmd = Serial1.read();

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

}

void send_msg(const char& msg){ Serial1.write(msg); }

void send_byte(byte* id, byte& idSize){

    for(byte i=0; i<idSize; i++) Serial1.write(id[i]);

    #ifdef DEBUG
    Serial.print("Sent id: ");
    for (byte i=0; i<idSize; i++){
        if(id[i] < 10) Serial.print('0');
        Serial.print(id[i], HEX);
    }
    Serial.println();
    #endif

}

#endif