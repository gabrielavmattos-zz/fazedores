const int tempo = 10;
const int pinoSensor = 6;
const int pinoSom = 4;
int y;


void setup() {
	pinMode(pinoSensor, INPUT);
	pinMode(pinoSom, OUTPUT);
}

void loop() {
	y = digitalRead(pinoSensor);
	if (y == 1) {
	digitalWrite(pinoSom, HIGH);
	}
	digitalWrite(pinoSom, LOW);
}
