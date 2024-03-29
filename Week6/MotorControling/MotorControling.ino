#include <math.h>

#define PWMR 11
#define PWML 12

#define RIN1 2
#define RIN2 3
#define LIN1 5
#define LIN2 6

#define IRL2 32
#define IRL1 34
#define IRM 36
#define IRR1 38
#define IRR2 40

int L2 = -2, L1 = -1, M = 0, R1 = 1, R2 = 2;
int cnt = 0;

double Kp = 50, Ki = 0, Kd = 200;
double lastError = 0, dError = 0 , sumError = 0;

int motor_speed = 150;
int turn_speed = motor_speed / 2;

bool allBlack = false;

const int Step_Max = 10;
//char step[Step_Max] = {'R', 'T', 'S', 'T', 'L', 'T', 'S', 'T'};
char step[Step_Max] = {'R', 'L', 'L', 'S', 'T', 'S', 'R', 'R', 'L', 'T'};
int ind = 0;

void motorWriting(double vR, double vL){

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

void Tracing(){

  int l2 = digitalRead(IRL2);
  int l1 = digitalRead(IRL1);
  int m = digitalRead(IRM);
  int r1 = digitalRead(IRR1);
  int r2 = digitalRead(IRR2);

  cnt = 0;

  if(l2 == 1) cnt++;
  if(l1 == 1) cnt++;
  if(m == 1) cnt++;
  if(r1 == 1) cnt++;
  if(r2 == 1) cnt++;

  if(cnt == 0 && allBlack == true){

    if(ind == Step_Max) ind = 0;

    if(ind < Step_Max){

      if(step[ind] == 'R') Right_Turn();
      else if(step[ind] == 'L') Left_Turn();
      else if(step[ind] == 'T') Turn_Around();
      else allBlack = false;

      ind++;

      //Right_Turn();

    }

  }else{

    if(cnt == 5 && allBlack == false) allBlack = true;

    double Error = (L2 * l2 + L1 * l1 + M * m + R1 * r1 + R2 * r2) / cnt;

    sumError += Error;
    dError = Error - lastError;
    lastError = Error;

    double powerCorrection = Kp * Error + Ki * sumError + Kd * dError;

    int vR = max(min(motor_speed - powerCorrection, 255), -255);
    int vL = max(min(motor_speed + powerCorrection, 255), -255);

    motorWriting(vR, vL);

  }

}

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

  allBlack = false;

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

  allBlack = false; 

}

void Turn_Around(){

  motorWriting(-turn_speed, turn_speed);
  delay(turn_speed * 20);

  while(digitalRead(IRM) != HIGH && digitalRead(IRL1) != HIGH);

  allBlack = false;

}

void setup(){

  pinMode(PWMR, OUTPUT);
  pinMode(PWML, OUTPUT);

  pinMode(RIN1, OUTPUT);
  pinMode(RIN2, OUTPUT);
  pinMode(LIN1, OUTPUT);
  pinMode(LIN2, OUTPUT);

  pinMode(IRL2, INPUT);
  pinMode(IRL1, INPUT);
  pinMode(IRM, INPUT);
  pinMode(IRR1, INPUT);
  pinMode(IRR2, INPUT);

}

void loop(){

  Tracing();

}