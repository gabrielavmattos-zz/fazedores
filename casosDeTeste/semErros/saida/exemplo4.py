import mraa
import time

tempo = 10
pinoSensor = 3
pinoSom = 4

y = 0

sensortoque = mraa.Gpio(pinoSensor)
sensortoque.dir(mraa.DIR_IN)

som = mraa.Gpio(pinSom)
som.dir(mraa.DIR_OUT)

while True:
	y = sensortoque.read()
	if (y == 1):
		som.write(1)
	som.write(0)
