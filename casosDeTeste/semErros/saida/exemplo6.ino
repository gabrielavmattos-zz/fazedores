const int tempo = 1000;
const int pinoPot = A3;
float y;


void setup() 
{
	pinMode(pinoPot, INPUT);
	Serial.begin(115200);
}

void loop() 
{
	y = analogRead(pinoPot);
	y = map(pinoPot, 0, 1023, 0, 255);
	Serial.println("O valor do potenciometro é: ");
	Serial.println(y);
	delay(tempo);
}
