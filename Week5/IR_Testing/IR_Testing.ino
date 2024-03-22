#define LED 13

#define IR1 32
#define IR2 34
#define IR3 36
#define IR4 38
#define IR5 40

#define Cur 0

int currentIR[5] = {32, 34, 36, 38, 40};

void setup(){

  pinMode(LED, OUTPUT);

  pinMode(IR1, INPUT);
  pinMode(IR2, INPUT);
  pinMode(IR3, INPUT);
  pinMode(IR4, INPUT);
  pinMode(IR5, INPUT);

}

void loop(){
  
  if(digitalRead(currentIR[Cur]) == LOW) digitalWrite(LED, HIGH);
  else digitalWrite(LED, LOW);

  delay(500);

}
