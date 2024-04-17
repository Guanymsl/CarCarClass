/***************************************************************************/
// File			  [node.h]
// Author		  [Erik Kuo, Joshua Lin]
// Synopsis		[Code for managing car movement when encounter a node]
// Functions  [/* add on your own! */]
// Modify		  [2020/03/027 Erik Kuo]
/***************************************************************************/

#ifndef _NODE_H_
#define _NODE_H_

#include "track.h"

/*===========================import variable===========================*/
int extern motor_speed;
int extern turn_speed;
/*===========================import variable===========================*/

// TODO: add some function to control your car when encounter a node
// here are something you can try: left_turn, right_turn... etc.

void Right_Turn(){

    motorWriting(-turn_speed, turn_speed);
    delay(turn_speed * 8);

    int t = 0;

    while(digitalRead(IRM) != HIGH && digitalRead(IRL1) != HIGH){

        delay(1);
        t++;
        if(t >= turn_speed * 12) break;

    }

    if(t>=turn_speed * 12){

        while(digitalRead(IRM) != HIGH && digitalRead(IRR1) != HIGH) motorWriting(turn_speed / 1.5, -turn_speed / 1.5);

    }

}

void Left_Turn(){

    motorWriting(turn_speed, -turn_speed);
    delay(turn_speed * 8);

    int t = 0;

    while(digitalRead(IRM) != HIGH && digitalRead(IRR1) != HIGH){

        delay(1);
        t++;
        if(t >= turn_speed * 12) break;

    }

    if(t>=turn_speed * 12){

        while(digitalRead(IRM) != HIGH && digitalRead(IRL1) != HIGH) motorWriting(-turn_speed / 1.5, turn_speed / 1.5);

    }

}

void Turn_Around(){

    motorWriting(-turn_speed, turn_speed);
    delay(turn_speed * 20);

    while(digitalRead(IRM) != HIGH && digitalRead(IRL1) != HIGH);

}

void Halt(){ motorWriting (0, 0); }

#endif