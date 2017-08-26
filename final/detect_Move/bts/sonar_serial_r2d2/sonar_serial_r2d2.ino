int tr = 10;
int er = 6;
int trr = A2;
int err = A3;
int tl = A5;
int el = A4;
int tll = A0;
int ell = A1;
int tf = 9;
int ef = 8;
int tfr = A11;
int efr = A10;
int tfl = A14;
int efl = A13;
int fdistance1,fdistance2,fdistance,ldistance,rdistance,lldistance,rrdistance,frdistance,fldistance;
long duration;
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
pinMode(tr,OUTPUT);
pinMode(er,INPUT);
pinMode(tl,OUTPUT);
pinMode(el,INPUT);
pinMode(tf,OUTPUT);
pinMode(ef,INPUT);
pinMode(tll,OUTPUT);
pinMode(ell,INPUT);
pinMode(trr,OUTPUT);
pinMode(err,INPUT);
pinMode(tfr,OUTPUT);
pinMode(efr,INPUT);
pinMode(tfl,OUTPUT);
pinMode(efl,INPUT);
Serial.begin(9600);
Serial.println("Enter direction :");
}

void loop() {
digitalWrite(22,HIGH);
digitalWrite(23,HIGH);
digitalWrite(24,HIGH);
digitalWrite(25,HIGH);

  fd();
  Serial.print("Forward Distance: ");
  Serial.println(fdistance);
  //delay(100);
  /*fld();
  Serial.print("Forward left Distance: ");
  Serial.println(fldistance);
  //delay(100);
  frd();
  Serial.print("Forward right Distance: ");
  Serial.println(frdistance);
  //delay(100);
  ld();
  Serial.print("Left Distance: ");
  Serial.println(ldistance);
  //delay(100);
  rd();
  Serial.print("Right Distance: ");
  Serial.println(rdistance);
  //delay(100);*/
  rrd();
  Serial.print("RR Distance: ");
  Serial.println(rrdistance);
  //delay(100);
  lld();
  Serial.print("LL Distance: ");
  Serial.println(lldistance);
  //delay(100);

if (Serial.available())
{
  char ch=Serial.read();
  while(ch=='w'){
      fd();
  Serial.print("Forward Distance: ");
  Serial.println(fdistance);
  rrd();
  Serial.print("RR Distance: ");
  Serial.println(rrdistance);
  //delay(100);
  lld();
  Serial.print("LL Distance: ");
  Serial.println(lldistance);
    sonar();
    if (Serial.available())
  {
  ch=Serial.read();
  }
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

  /*if (fdistance <= 80)
  {
    if(rrdistance > lldistance)
    {
      mf();
      delay(4000);
      mr();
      delay(3200);
      mf();
      delay(5000);
      ml();
      delay(2500);
      mf();
      delay(8000);
      ml();
      delay(2500);
      mf();
      delay(5000);
      mr();
      delay(3200);
      mf();
      delay(2000);
    }
    else
    {
      mf();
      delay(4000);
      ml();
      delay(2500);
      mf();
      delay(5000);
      mr();
      delay(3200);
      mf();
      delay(8000);
      mr();
      delay(3200);
      mf();
      delay(5000);
      ml();
      delay(2500);
      mf();
      delay(2000);
    }
  }*/
}
void sonar(){
    if(fdistance < 60)
  {
    Serial.println("Forward Less----------------");
    if(rrdistance > 90)
    {
      mr();
      delay(3200);
      mf();
      delay(4000);
      if(lldistance > 90)
      {
        ml();
        delay(2500);
      }
      else
      {
        ms();
      }
    }
    else if(lldistance > 90)
    {
      ml();
      delay(2540);
      mf();
      delay(4000);
    }
    if(lldistance > 90)
      {
        mr();
        delay(3200);
      }
      else
      {
        ms();
      }
  }
  else
  {
    Serial.println("Forward++++++++++++++++++++++++++++++");
    mf();
  }
}

/*void fd() {
digitalWrite(tf, LOW);
delayMicroseconds(2);
digitalWrite(tf, HIGH);
delayMicroseconds(10);
digitalWrite(tf, LOW);
duration = pulseIn(ef, HIGH);
fdistance1= duration*0.0344/2;
delay(2);
digitalWrite(tf, LOW);
delayMicroseconds(2);
digitalWrite(tf, HIGH);
delayMicroseconds(10);
digitalWrite(tf, LOW);
duration = pulseIn(ef, HIGH);
fdistance2= duration*0.0344/2;
fdistance=abs(fdistance1-fdistance2);
if (fdistance > 20)
{
  fd();
}
fdistance=(fdistance1+fdistance2)/2;
}*/
void fd() {
digitalWrite(tf, LOW);
delayMicroseconds(2);
digitalWrite(tf, HIGH);
delayMicroseconds(10);
digitalWrite(tf, LOW);
duration = pulseIn(ef, HIGH);
fdistance= duration*0.0344/2;
}
void frd() {
digitalWrite(tfr, LOW);
delayMicroseconds(2);
digitalWrite(tfr, HIGH);
delayMicroseconds(10);
digitalWrite(tfr, LOW);
duration = pulseIn(efr, HIGH);
frdistance= duration*0.0344/2;
}
void fld() {
digitalWrite(tfl, LOW);
delayMicroseconds(2);
digitalWrite(tfl, HIGH);
delayMicroseconds(10);
digitalWrite(tfl, LOW);
duration = pulseIn(efl, HIGH);
fldistance= duration*0.0344/2;
}
void ld() {
digitalWrite(tl, LOW);
delayMicroseconds(2);
digitalWrite(tl, HIGH);
delayMicroseconds(10);
digitalWrite(tl, LOW);
duration = pulseIn(el, HIGH);
ldistance= duration*0.0344/2;
/*if (ldistance>=350)
{
  ld();
}*/
}
void lld() {
digitalWrite(tll, LOW);
delayMicroseconds(2);
digitalWrite(tll, HIGH);
delayMicroseconds(10);
digitalWrite(tll, LOW);
duration = pulseIn(ell, HIGH);
lldistance= duration*0.0344/2;
}
void rd() {
digitalWrite(tr, LOW);
delayMicroseconds(2);
digitalWrite(tr, HIGH);
delayMicroseconds(10);
digitalWrite(tr, LOW);
duration = pulseIn(er, HIGH);
rdistance= duration*0.0344/2;
}
void rrd() {
digitalWrite(trr, LOW);
delayMicroseconds(2);
digitalWrite(trr, HIGH);
delayMicroseconds(10);
digitalWrite(trr, LOW);
duration = pulseIn(err, HIGH);
rrdistance= duration*0.0344/2;
}
void mf(){
analogWrite(2,0);  //left motor
analogWrite(3,180);//left motor
analogWrite(4,0);  //right motor
analogWrite(5,180);//right motor
}
void mb(){
analogWrite(2,180);
analogWrite(3,0);
analogWrite(4,180);
analogWrite(5,0);
}
void ml(){
analogWrite(2,210);
analogWrite(3,0);
analogWrite(4,0);
analogWrite(5,230);
}
void mr(){
analogWrite(2,0);
analogWrite(3,210);
analogWrite(4,230);
analogWrite(5,0);
}
void ms(){ //motor stop
analogWrite(2,0);
analogWrite(3,0);
analogWrite(4,0);
analogWrite(5,0);
Serial.println("Motor At Rest}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}");
}
void hmc(){
digitalWrite(28,HIGH);
digitalWrite(29,LOW);
analogWrite(7,250);
  }//clockwise head motor rotation
void hmac(){
digitalWrite(28,LOW);
digitalWrite(29,HIGH);
analogWrite(7,250);
}//anti-clockwise headmotor rotation
void hms(){
digitalWrite(28,LOW);
digitalWrite(29,LOW);
analogWrite(7,0);
}
