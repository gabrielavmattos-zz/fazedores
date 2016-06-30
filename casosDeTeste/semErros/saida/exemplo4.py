import mraa
import time

tempo = 10
pinoSensor = 3
pinoSom = 4

y = 0

sensortoque3 = mraa.Gpio(pinoSensor)
sensortoque3.dir(mraa.DIR_IN)

som4 = mraa.Gpio(pinSom)
som4.dir(mraa.DIR_OUT)

while True:
	y = sensortoque3.read()
	if (y == 1):
		som4.write(1)
	som4.write(0)
