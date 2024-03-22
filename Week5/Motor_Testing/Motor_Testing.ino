#define PWMA 11
#define PWMB 12

#define AIN1 2
#define AIN2 3
#define BIN1 5
#define BIN2 6

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
  digitalWrite(AIN1, LOW);
  digitalWrite(BIN1, HIGH);
  digitalWrite(BIN2, LOW);

  delay(5000);

  digitalWrite(PWMA, LOW);
  digitalWrite(PWMB, LOW);

  delay(5000);

}
