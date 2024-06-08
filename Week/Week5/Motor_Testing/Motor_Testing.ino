#define PWMA 11
#define PWMB 12

#define AIN1 2
#define AIN2 3
#define BIN1 5
#define BIN2 6

#define IR1 32
#define IR2 34
#define IR3 36
#define IR4 38
#define IR5 40

void setup() {

  pinMode(PWMA, OUTPUT);
  pinMode(PWMB, OUTPUT);

  pinMode(AIN1, OUTPUT);
  pinMode(AIN2, OUTPUT);
  pinMode(BIN1, OUTPUT);
  pinMode(BIN2, OUTPUT);

}

void loop() {

  digitalWrite(PWMA, HIGH);
  digitalWrite(PWMB, HIGH);
  //analogWrite(PWMA, 100);
  //analogWrite(PWMB, 100);

  digitalWrite(AIN1, HIGH);
  digitalWrite(AIN2, LOW);

  delay(5000);

  digitalWrite(AIN1, LOW);
  digitalWrite(AIN2, LOW);

  digitalWrite(BIN1, HIGH);
  digitalWrite(BIN2, LOW);

  delay(5000);

  digitalWrite(BIN1, LOW);
  digitalWrite(BIN2, LOW);

  digitalWrite(AIN1, LOW);
  digitalWrite(AIN2, HIGH);

  delay(5000);

  digitalWrite(AIN1, LOW);
  digitalWrite(AIN2, LOW);

  digitalWrite(BIN1, LOW);
  digitalWrite(BIN2, HIGH);

  delay(5000);

  digitalWrite(BIN1, LOW);
  digitalWrite(BIN2, LOW);

  digitalWrite(PWMA, LOW);
  digitalWrite(PWMB, LOW);

  delay(5000);

}
