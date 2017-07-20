void setup() {
  pinMode(22,OUTPUT);
  pinMode(23,OUTPUT);
  pinMode(24,OUTPUT);
  pinMode(25,OUTPUT);
  pinMode(2,OUTPUT);
  pinMode(3,OUTPUT);
  pinMode(4,OUTPUT);
  pinMode(5,OUTPUT);
  pinMode(28,OUTPUT);
  pinMode(29,OUTPUT);
  pinMode(7,OUTPUT);
  Serial.begin(9600);
  Serial.println("Enter direction :");
}

void loop() {
digitalWrite(22,HIGH);
digitalWrite(23,HIGH);
digitalWrite(24,HIGH);
digitalWrite(25,HIGH);
//mf();
//delay(2000);
//mb();
//delay(2000);
//mr();
//delay(5000);
//ml();
//delay(5000);
//ms();
//delay(7000);
//hmc();
//delay(5000);
//hmac();
//delay(5000);
if (Serial.available())
{
  char ch=Serial.read();
  if(ch=='w'){
    mf();
  }
    if(ch=='a'){
    ml();
  }
    if(ch=='d'){
    mr();
  }
    if(ch=='x'){
    ms();
    hms();
  }
    if(ch=='s'){
    mb();
  }
  if(ch=='r'){
    hmc();
  }
  if(ch=='l'){
    hmac();
  }
}
}

void mf(){
analogWrite(2,0);  //left motor
analogWrite(3,180);//left motor
analogWrite(4,0);  //right motor
analogWrite(5,180);//right motor
Serial.println("R2D2 Move Forward");
}
void mb(){
analogWrite(2,180);
analogWrite(3,0);
analogWrite(4,180);
analogWrite(5,0);
Serial.println("R2D2 Move Back");
}
void ml(){
analogWrite(2,210);
analogWrite(3,0);
analogWrite(4,0);
analogWrite(5,230);
Serial.println("R2D2 Move Left");
}
void mr(){
analogWrite(2,0);
analogWrite(3,210);
analogWrite(4,230);
analogWrite(5,0);
Serial.println("R2D2 Move Right");
}
void ms(){ //motor stop
analogWrite(2,0);
analogWrite(3,0);
analogWrite(4,0);
analogWrite(5,0);
Serial.println("R2D2 Move Right");
}
void hmc(){
digitalWrite(28,HIGH);
digitalWrite(29,LOW);
analogWrite(8,250);
Serial.println("Move Head Clockwise");
}//clockwise head motor rotation
void hmac(){
digitalWrite(28,LOW);
digitalWrite(29,HIGH);
analogWrite(8,250);
Serial.println("Move Head Anit-Clockwise");
}//anti-clockwise headmotor rotation
void hms(){
digitalWrite(28,LOW);
digitalWrite(29,LOW);
analogWrite(8,0);
Serial.println("Stop Head Movement");
}
