import mraa
import pyupm_i2clcd as lcd
import time

tempo = 10
pinoLCD = 21

mylcd = lcd.Jhd1313m1(1, 0x3E, 0x62)
mylcd.setCursor(0,0)

while True:
	mylcd.setColor(10, 10, 200)
	mylcd.write(":D   ")
	time.sleep(tempo)
