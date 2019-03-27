import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
#setting up the pins
temp_sensor_pin = 7

GPIO.setup(temp_sensor_pin, GPIO.IN)

#logic

while True:
	temperature = GPIO.input(temp_sensor_pin)
    print(temperature)
	time.sleep(0.5)

