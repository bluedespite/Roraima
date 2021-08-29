#include <TinyGPS++.h>
#include <SoftwareSerial.h>
#include <TimeLib.h>


static const int RXPin = 3, TXPin = 2;
static const uint32_t GPSBaud = 9600;
static const int UTC_offset = -5; 
static byte prevSec = 0;
int Analogica0=0;
int Analogica1=0;
int Analogica2=0;
int Analogica3=0;
int Analogica4=0;
int Analogica5=0;
float Velocity=0;
double Longitude=0;
double Latitude=0;

TinyGPSPlus gps;

// The serial connection to the GPS device
SoftwareSerial ss(RXPin, TXPin);

void setup()
{
  Serial.begin(9600);
  ss.begin(GPSBaud);
   
}

void loop()
{  
  while (ss.available() > 0)
    if (gps.encode(ss.read()))
    {
    int Year = gps.date.year();
    byte Month = gps.date.month();
    byte Day = gps.date.day();
    byte Hour = gps.time.hour();
    byte Minute = gps.time.minute();
    byte Second = gps.time.second();
    if (gps.time.second() !=prevSec) 
    { //update the display only if the time has changed
    setTime(Hour, Minute, Second, Day, Month, Year);
    adjustTime(UTC_offset * SECS_PER_HOUR);  
    prevSec=Second;
    Analogica0 = analogRead(0);
    Analogica1 = analogRead(1);
    Analogica2 = analogRead(2);
    Analogica3 = analogRead(3);
    Analogica4 = analogRead(4);
    Analogica5 = analogRead(5);
    if (gps.speed.isValid())
    {Velocity=gps.speed.kmph();}
    if (gps.location.isValid())
    {
    Latitude=gps.location.lat();
    Longitude=gps.location.lng();
    }
 
  if (millis() > 5000 && gps.charsProcessed() < 10)
  {   
      Serial.println(F("ERROR:No GPS detected: check wiring."));
  }
}}}

void displayInfo()
{
  Serial.print(F("Latitude=")); 
  Serial.print(Latitude, 6);
  Serial.print(F("|Longitude=")); 
  Serial.print(Longitude, 6);
  Serial.print(F("|Velocity="));
  Serial.print(Velocity); // Speed in kilometers per hour (double)

  Serial.print(F("|DateTime="));
  if (gps.date.isValid() && gps.time.isValid())
  {
    Serial.print(year());
    Serial.print(F("-"));
    if (month() < 10) Serial.print(F("0"));
    Serial.print(month());
    Serial.print(F("-"));
    if (day() < 10) Serial.print(F("0"));
    Serial.print(day());
    Serial.print(F(" "));
    if (hour() < 10) Serial.print(F("0"));
    Serial.print(hour());
    Serial.print(F(":"));
    if (minute() < 10) Serial.print(F("0"));
    Serial.print(minute());
    Serial.print(F(":"));
    if (second() < 10) Serial.print(F("0"));
    Serial.print(second());

  }
  else
  {
    Serial.print(F("INVALID DATETIME"));
  }

  Serial.print(F("|0="));
  Serial.print(String(Analogica0, DEC));
  Serial.print(F("|1="));
  Serial.print(String(Analogica1, DEC));
  Serial.print(F("|2="));
  Serial.print(String(Analogica2, DEC));
  Serial.print(F("|3="));
  Serial.print(String(Analogica3, DEC));
  Serial.print(F("|4="));
  Serial.print(String(Analogica4, DEC));
  Serial.print(F("|5="));
  Serial.print(String(Analogica5, DEC));
  Serial.println();
}

void serialEvent(){
  //recepcion Serial
  String CadenaEntrada="";
  while(Serial.available()){
    char CaracterEntrada=Serial.read();
    CadenaEntrada+=CaracterEntrada;
    if (CaracterEntrada =='\n'){
      displayInfo();
      CadenaEntrada="";
      }}      
}
