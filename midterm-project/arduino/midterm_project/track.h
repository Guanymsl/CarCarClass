#ifndef _TRACK_H_
#define _TRACK_H_

int L2 = -2, L1 = -1, M = 0, R1 = 1, R2 = 2;
double Kp = 50, Ki = 0, Kd = 100;
double lastError = 0, dError = 0 , sumError = 0;
bool allBlack = false;

void MotorWriting(double vR, double vL){

    if(vR >= 0){

        digitalWrite(RIN1, LOW);
        digitalWrite(RIN2, HIGH);

    }else{

        digitalWrite(RIN1, HIGH);
        digitalWrite(RIN2, LOW);

    }

    if(vL >= 0){

        digitalWrite(LIN1, LOW);
        digitalWrite(LIN2, HIGH);

    }else{

        digitalWrite(LIN1, HIGH);
        digitalWrite(LIN2, LOW);

    }

    analogWrite(PWMR, abs(vR));
    analogWrite(PWML, abs(vL));

}

void tracking(){

    int l1 = digitalRead(IRL1), l2 = digitalRead(IRL2);
    int m = digitalRead(IRM);
    int r1 = digitalRead(IRR1), r2 = digitalRead(IRR2);

    int cnt = l2 + l1 + m + r1 + r2;

    if(allBlack == true && cnt <= 1){

        if(step == 'r') Turn('r');
        else if(step == 'l') Turn('l');
        else if(step == 'f') delay(22500 / motor_speed * 0.3);
        else if(step == 'b') Turn_Around();
        else if(step == 'h') Halt();

        delay(22500 / motor_speed * 0.1);

        lastError = dError = sumError = 0;

        allBlack = false;
        get_command();

    }else if(allBlack == true){

        MotorWriting(motor_speed + 10, motor_speed);

    }else if(cnt != 0){

        if(cnt >= 4 && allBlack == false) allBlack = true;

        double Error = (L2 * l2 + L1 * l1 + M * m + R1 * r1 + R2 * r2) / cnt;

        sumError += Error;
        dError = Error - lastError;
        lastError = Error;

        double powerCorrection = Kp * Error + Ki * sumError + Kd * dError;

        double vR = max(min(motor_speed + 10 - powerCorrection, 255), -255);
        double vL = max(min(motor_speed + powerCorrection, 255), -255);

        MotorWriting(vR, vL);

    }

}

#endif