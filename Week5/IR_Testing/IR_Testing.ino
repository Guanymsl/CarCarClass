#define LED 13

#define IR1 32
#define IR2 34
#define IR3 36
#define IR4 38
#define IR5 40

#define Cur 

int currentIR[5] = {IR1, IR2, IR3, IR4, IR5};

void setup(){

  pinMode(LED, OUTPUT);

  pinMode(IR1, INPUT);
  pinMode(IR2, INPUT);
  pinMode(IR3, INPUT);
  pinMode(IR4, INPUT);
  pinMode(IR5, INPUT);

  Serial.begin(9600);

  Serial.println("Start Testing!");

}

void loop(){
  
  for(int i=0; i<5; i++){

    /*if(digitalRead(currentIR[i]) == LOW){

      Serial.print("IR");
      Serial.print(i + 1);
      Serial.println("is good!");

    }*/

    Serial.println(analogRead(currentIR[i]));

  }

  Serial.println();

  delay(3000);

}
