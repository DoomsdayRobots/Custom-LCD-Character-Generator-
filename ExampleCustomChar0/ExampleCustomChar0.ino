#include <LiquidCrystal.h> 
LiquidCrystal lcd(12, 11, 5, 4, 3, 2); 
byte customChar[8] = { 
  B01010,
  B10101,
  B10001,
  B01010,
  B00100,
  B00110,
  B00100,
  B00110,
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