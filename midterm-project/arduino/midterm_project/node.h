#ifndef _NODE_H_
#define _NODE_H_

void Turn(char dir){

    int sign = 0;

    if(dir == 'r') sign = -1;
    else sign = 1;

    delay(22500 / motor_speed * 0.5);
    MotorWriting(sign * turn_speed, -sign * turn_speed);
    delay(5625 / turn_speed * 6);

    int t = 0;
    while(digitalRead(IRM) != HIGH && digitalRead(IRR1) != HIGH && digitalRead(IRL1) != HIGH){

        delay(1);
        t++;
        if(t >= 5625 / turn_speed * 10) break;

    }  

    if(t == 5625 / turn_speed * 10){

        while(digitalRead(IRM) != HIGH && digitalRead(IRR1) != HIGH && digitalRead(IRL1) != HIGH){

            MotorWriting(-sign * turn_speed / 1.5, sign * turn_speed / 1.5);

        }

    }

}

void Turn_Around(){

    MotorWriting(-turn_speed, turn_speed);
    delay(5625 / turn_speed * 20);

    int t = 0;
    while(digitalRead(IRM) != HIGH && digitalRead(IRR1) != HIGH && digitalRead(IRL1) != HIGH){

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