import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

#setting up the pins
WATER_RELAIS_PIN = 11
LIGHT_RELAIS_PIN = 13

GPIO.setup(WATER_RELAIS_PIN, GPIO.OUT)
GPIO.setup(LIGHT_RELAIS_PIN, GPIO.OUT)

#logic
def turn_of(pin):
	GPIO.output(pin, GPIO.LOW)

def turn_on(pin):
	GPIO.output(pin, GPIO.HIGH)

