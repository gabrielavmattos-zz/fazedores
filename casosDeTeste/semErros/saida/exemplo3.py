import mraa
import time

x = 0

luz5 = mraa.Gpio(5)
luz5.dir(mraa.DIR_OUT)
botao4 = mraa.Gpio(4)
botao4.dir(mraa.DIR_IN)

while True:
	x = botao4.read()
	if (x == 1):
		luz5.write(1)

	luz5.write(0)
