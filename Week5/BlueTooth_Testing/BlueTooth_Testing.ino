void setup() {

  Serial.begin(9600);
  Serial3.begin(9600);

}

void loop() {

  char temp;

  while(Serial3.available() > 0){

    temp = Serial3.read();
    Serial.print(temp);

  }

  while(Serial.available() > 0){

    temp = Serial.read();
    Serial3.write(temp);

  }

}
