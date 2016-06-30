import mraa
import time

pinSom = 5
BREATH_DELAY = 1

i = 0

som = mraa.Pwm(pinSom)
som.period_us(700)
som.enable(True)

while True:
	for i in range(0, 255):
		som.write(i/255.0)
		time.sleep(BREATH_DELAY)
	som.write(0)
	time.sleep(10)

		


