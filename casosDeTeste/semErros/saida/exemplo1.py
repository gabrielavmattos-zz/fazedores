import mraa
import time

som5 = mraa.Pwm(5)
som5.period_us(700)
som5.enable(True)

while True:
	som5.write(1)
    	time.sleep(1)
    	som5.write(0)	
    	time.sleep(1)



