void setup() {

  Serial.begin(9600);
  Serial2.begin(9600);

}

void loop() {

  char temp;

  while(Serial2.available() > 0){

    Serial.print("Here");

    temp = Serial2.read();
    Serial.print(temp);

  }

  while(Serial.available() > 0){

    Serial.print("Here");

    temp = Serial.read();
    Serial2.write(temp);

  }

}
