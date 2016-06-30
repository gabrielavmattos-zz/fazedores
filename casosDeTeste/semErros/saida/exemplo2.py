import mraa
import time

pinSom = 5
BREATH_DELAY = 1
i = 0

som5 = mraa.Pwm(pinSom)
som5.period_us(700)
som5.enable(True)

while True:
	for i in range(0, 255):
		som5.write(i/255.0)
		time.sleep(BREATH_DELAY)
	som5.write(0)
	time.sleep(10)

		


