/***************************************************************************/
// File			  [track.h]
// Author		  [Erik Kuo]
// Synopsis		  [Code used for tracking]
// Functions      [MotorWriting, MotorInverter, tracking]
// Modify		  [2020/03/27 Erik Kuo]
/***************************************************************************/

/*if you have no idea how to start*/
/*check out what you have learned from week 1 & 6*/
/*feel free to add your own function for convenience*/

#ifndef _TRACK_H_
#define _TRACK_H_

/*===========================import variable===========================*/
int extern motor_speed;
char extern step;
int extern state;
/*===========================import variable===========================*/

int L2 = -2, L1 = -1, M = 0, R1 = 1, R2 = 2;
double Kp = 50, Ki = 0, Kd = 200;
double lastError = 0, dError = 0 , sumError = 0;

bool allBlack = false;

// Write the voltage to motor.
void MotorWriting(double vL, double vR) {
    // TODO: use TB6612 to control motor voltage & direction

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

}  // MotorWriting

// Handle negative motor_PWMR value.
void MotorInverter(int motor, bool& dir) {
    // Hint: the value of motor_PWMR must between 0~255, cannot write negative value.
    return;
}  // MotorInverter

// P/PID control Tracking
void tracking() {
    // TODO: find your own parameters!

    // TODO: complete your P/PID tracking code

    int l1 = digitalRead(IRL1), l2 = digitalRead(IRL2);
    int m = digitalRead(IRM);
    int r1 = digitalRead(IRR1), r2 = digitalRead(IRR2);

    int cnt = l2 + l1 + m + r1 + r2;

    if(allBlack == true && cnt < 5){

        if(step == 'r') Right_Turn();
        else if(step == 'l') Left_Turn();
        else if(step == 'b') Turn_Around();
        else if (step == 's') Halt();

        allBlack = false;
        send_msg('g');
        state = 1;

    }else{

        if(cnt == 5 && allBlack == false) allBlack = true;

        double Error = (L2 * l2 + L1 * l1 + M * m + R1 * r1 + R2 * r2) / cnt;

        sumError += Error;
        dError = Error - lastError;
        lastError = Error;

        double powerCorrection = Kp * Error + Ki * sumError + Kd * dError;

        double vR = max(min(motor_speed - powerCorrection, 255), -255);
        double vL = max(min(motor_speed + powerCorrection, 255), -255);

        MotorWriting(vL, vR);

    }
    // end TODO

}  // tracking

#endif