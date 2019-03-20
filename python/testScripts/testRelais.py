import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)

#setting up the pins
RELAIS_1_PIN = 13

GPIO.setup(RELAIS_1_PIN, GPIO.OUT)

#logic

while True:
	GPIO.output(RELAIS_1_PIN, GPIO.LOW)
	time.sleep(0.5)
	GPIO.output(RELAIS_1_PIN, GPIO.HIGH)
	time.sleep(0.5)
