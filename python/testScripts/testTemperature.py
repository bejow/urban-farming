from w1thermsensor import W1ThermSensor
import time

sensor = W1ThermSensor()

while True:
	temperature = sensor.get_temperature()
    print("The temperature is %s celsius" % temperature)
	time.sleep(1)

