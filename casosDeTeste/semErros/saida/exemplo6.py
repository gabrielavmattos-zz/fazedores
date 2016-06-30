import mraa
import pyupm_i2clcd as lcd
import time

tempo = 10
pinoPot = 0
pinoLCD = 21

y = 0.0

potenciometro = mraa.Aio(pinoPot)
mylcd = lcd.Jhd1313m1(1, 0x3E, 0x62)
mylcd.setCursor(0,0)

while True:
	y = potenciometro.readFloat()
	mylcd.write(""+str(y))
	time.sleep(tempo)
