const int tempo = 10;
int x;


void setup() {
	pinMode(3, OUTPUT);
	pinMode(5, INPUT);
}

void loop() {
	x = digitalRead(5);
	if (x == 1) 
	{
		digitalWrite(3, HIGH);
		delay(tempo);
		digitalWrite(3, LOW);
	}
}
