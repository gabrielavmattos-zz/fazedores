import mraa
import time

tempo = 1

x = 0

luz = mraa.Gpio(5)
luz.dir(mraa.DIR_OUT)
botao = mraa.Gpio(4)
botao.dir(mraa.DIR_IN)

while True:
	x = botao.read()
	if (x == 1):
		luz.write(1)

	luz.write(0)
