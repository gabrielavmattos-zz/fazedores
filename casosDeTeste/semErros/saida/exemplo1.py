import mraa
import time

som = mraa.Gpio(5)
som.dir(mraa.DIR_OUT)

while True:
	som.write(1)
    	time.sleep(1)
    	som.write(0)	
    	time.sleep(1)



