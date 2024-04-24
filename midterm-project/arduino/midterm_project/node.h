#ifndef _NODE_H_
#define _NODE_H_

void Right_Turn(){

    delay(22500 / motor_speed);
    MotorWriting(-turn_speed, turn_speed);
    delay(5625 / turn_speed * 8);

    int t = 0;
    while(digitalRead(IRM) != HIGH && digitalRead(IRR1) != HIGH){

        delay(1);
        t++;
        if(t >= 5625 / turn_speed * 12) break;

    }  

    if(t >= 5625 / turn_speed * 12){

        while(digitalRead(IRM) != HIGH && digitalRead(IRL1) != HIGH) MotorWriting(turn_speed / 1.5, -turn_speed / 1.5);

    }

}

void Left_Turn(){

    delay(22500 / motor_speed);
    MotorWriting(turn_speed, -turn_speed);
    delay(5625 / turn_speed * 8);

    int t = 0;
    while(digitalRead(IRM) != HIGH && digitalRead(IRL1) != HIGH){

        delay(1);
        t++;
        if(t >= 5625 / turn_speed * 12) break;

    }

    if(t >= 5625 / turn_speed * 12){

        while(digitalRead(IRM) != HIGH && digitalRead(IRR1) != HIGH) MotorWriting(-turn_speed / 1.5, turn_speed / 1.5);

    }

}

void Turn_Around(){

    MotorWriting(-turn_speed, turn_speed);
    delay(5625 / turn_speed * 12);

    int t = 0;
    while(digitalRead(IRM) != HIGH && digitalRead(IRR1) != HIGH){

        delay(1);
        t++;
        if(t >= 5625 / turn_speed * 24) break;

    }

    if(t >= 5625 / turn_speed * 24){

        while(digitalRead(IRM) != HIGH && digitalRead(IRL1) != HIGH) MotorWriting(turn_speed / 1.5, -turn_speed / 1.5);

    }

}

void Halt(){ MotorWriting(0, 0); }

#endif