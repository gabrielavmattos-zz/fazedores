const int pinSom = 5;
const int BREATH_DELAY = 5;
int i;


void setup() {
	pinMode(pinSom, OUTPUT);
}

void loop() {
	for (i = 0; i <= 256; i++) {
	analogWrite(pinSom, i);
	delay(BREATH_DELAY);
}
	delay(100);
}
