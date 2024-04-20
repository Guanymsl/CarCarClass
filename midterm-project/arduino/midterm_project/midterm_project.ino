/***************************************************************************/
// File       [final_project.ino]
// Author     [Erik Kuo]
// Synopsis   [Code for managing main process]
// Functions  [setup, loop, Search_Mode, Hault_Mode, SetState]
// Modify     [2020/03/27 Erik Kuo]
/***************************************************************************/

#define DEBUG  // debug flag

// for RFID
#include <MFRC522.h>
#include <SPI.h>

#include <math.h>

/*===========================define pin & create module object================================*/
// BlueTooth
// BT connect to Serial1 (Hardware Serial)
// Mega               HC05
// Pin  (Function)    Pin
// 18    TX       ->  RX
// 19    RX       <-  TX

// TB6612, 請按照自己車上的接線寫入腳位(左右不一定要跟註解寫的一樣)
// TODO: 請將腳位寫入下方
#define PWMR 11     // 定義 ENA (PWM調速) 接腳
#define PWML 12     // 定義 ENB (PWM調速) 接腳
#define RIN1 2      // 定義 A1 接腳（右）
#define RIN2 3      // 定義 A2 接腳（右）
#define LIN1 5      // 定義 B1 接腳（左）
#define LIN2 6      // 定義 B2 接腳（左）

// 循線模組, 請按照自己車上的接線寫入腳位
#define IRL2 32
#define IRL1 34
#define IRM 36
#define IRR1 38
#define IRR2 40

// RFID, 請按照自己車上的接線寫入腳位
#define RST 9        // 讀卡機的重置腳位
#define SS 53        // 晶片選擇腳位
MFRC522 mfrc522(SS, RST);  // 建立MFRC522物件
/*===========================define pin & create module object===========================*/

/*============setup============*/
void setup(){
    // bluetooth initialization
    Serial1.begin(9600);
    // Serial window
    Serial.begin(9600);

    // RFID initial
    SPI.begin();
    mfrc522.PCD_Init();

    // TB6612 pin
    pinMode(PWMR, OUTPUT);
    pinMode(PWML, OUTPUT);
    pinMode(RIN1, OUTPUT);
    pinMode(RIN2, OUTPUT);
    pinMode(LIN1, OUTPUT);
    pinMode(LIN2, OUTPUT);

    // tracking pin
    pinMode(IRL2, INPUT);
    pinMode(IRL1, INPUT);
    pinMode(IRM, INPUT);
    pinMode(IRR1, INPUT);
    pinMode(IRR2, INPUT);

    #ifdef DEBUG
    Serial.println("Start!");
    #endif

}
/*============setup============*/

/*=====Import header files=====*/
#include "function.h"
#include "RFID.h"
#include "bluetooth.h"
#include "node.h"
#include "track.h"
/*=====Import header files=====*/

/*===========================initialize variables===========================*/
int motor_speed = 150;  // set your own value for motor power
int turn_speed = motor_speed / 2;
int state = 0;          // set state to false to halt the car, set state to true to activate the car
BT_CMD _cmd = NOTHING;  // enum for bluetooth message, reference in bluetooth.h line 2
char step = NULL;
bool reading = false;
/*===========================initialize variables===========================*/

/*===========================declare function prototypes===========================*/
void Search();    // search graph
void SetState();  // switch the state
/*===========================declare function prototypes===========================*/

/*===========================define function===========================*/
void loop(){

    if(state == 0) MotorWriting(0, 0);
    if(state != 2) SetState();
    if(state == 2) Search();

}

void SetState(){
    // TODO:
    // 1. Get command from bluetooth
    // 2. Change state if need

    _cmd = ask_BT();

    if(_cmd == END) reading = false, state = 0;

    while(reading && _cmd != NOTHING){

        if(_cmd == FORWARD) step = 'f';
        else if(_cmd == RIGHT) step = 'r';
        else if(_cmd == LEFT) step = 'l';
        else if(_cmd == TURN) step = 'b';
        else if(_cmd == HALT) step = 's';

        state = 2;

    }

    if(_cmd == START) reading = true;

}

void Search() {
    // TODO: let your car search graph(maze) according to bluetooth command from computer(python
    // code)

    tracking();

    byte _idSize;
    byte* _id = rfid(_idSize);
    if(_id != 0) send_byte(_id, _idSize);

}
/*===========================define function===========================*/