#include <LiquidCrystal.h> 
LiquidCrystal lcd(12, 11, 5, 4, 3, 2); 
byte customChar[8] = { 
  B00000,
  B01110,
  B11111,
  B10101,
  B11111,
  B01110,
  B01010,
  B00000,
}; 

void setup()
{
  lcd.createChar(0,customChar);
  lcd.begin(16, 2);
  lcd.write(byte(0));
}

void loop()
{
}