#include <Wire.h>
#include "rgb_lcd.h"

rgb_lcd lcd;

const int tempo = 1000;
const int pinoLCD = 21;
float y;

String mensagem;


void setup() {
	pinMode(pinoLCD, OUTPUT);
	lcd.begin(16,2);
}

void loop() {

	lcd.setRGB(10,10,200);

	lcd.print(":D  ");
	delay(tempo);
}
