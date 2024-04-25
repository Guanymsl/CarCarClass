#ifndef _RFID_H_
#define _RFID_H_

byte* rfid(byte& idSize){

    if (mfrc522.PICC_IsNewCardPresent() && mfrc522.PICC_ReadCardSerial()){

        byte* id = mfrc522.uid.uidByte;
        idSize = mfrc522.uid.size;

        #ifdef DEBUG
        Serial.print("UID Size: ");\
        Serial.println(idSize);
        for (byte i=0; i<idSize; i++) {
            Serial.print("id[");
            Serial.print(i);
            Serial.print("]: ");
            Serial.println(id[i], HEX);
        }
        Serial.println();
        #endif

        mfrc522.PICC_HaltA();
        return id;

    }

    return 0;

}

void detecting(){

    byte _idSize;
    byte* _id = rfid(_idSize);
    if(_id != 0){
        send_byte(_id, _idSize);
        Turn_Around();
        send_msg('g');
        state = RECEIVE;
    }

}

#endif