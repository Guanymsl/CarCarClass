#include <Servo.h>
#include <math.h>

Servo mServo, sServo;
double curmAngle = 0, cursAngle = 0, curX = 0;

void motorControl(double _angleF){ mServo.write(_angleF + 90); }

double getX(double _angle){ return 15 - sqrt(225 - 400 * sin(radians(_angle))); }

void screwControl(double _angleI, double _angleF){

    double dx = getX(_angleF) - getX(_angleI);
    dx = max(min(curX + dx, 12), 0) - curX;
    curX += dx;

    if(dx > 0){
        sServo.writeMicroseconds(1750);
        delay(430 * dx / PI);
    }else{
        sServo.writeMicroseconds(1250);
        delay(380 * -dx / PI);
    }

    sServo.writeMicroseconds(1500);

}
void setup(){

    Serial.begin(9600);
    mServo.attach(9);
    sServo.attach(10);

}

void loop(){

    if(Serial.available() > 0){

        String data = Serial.readStringUntil('\n'); 
        double mAngle = int(data[2] - '0') * 10 + int(data[3] - '0');
        double sAngle = int(data[0] - '0') * 10 + int(data[1] - '0');

        motorControl(mAngle);
        screwControl(cursAngle, sAngle);

        curmAngle = mAngle;
        cursAngle = sAngle;

    }

}