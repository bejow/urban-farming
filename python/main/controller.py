import RPi.GPIO as GPIO
import time

#GPIO.setmode(GPIO.BOARD)

#setting up the pins
WATER_RELAIS_PIN = 11
LIGHT_RELAIS_PIN = 13

#GPIO.setup(WATER_RELAIS_PIN, GPIO.OUT)
#GPIO.setup(LIGHT_RELAIS_PIN, GPIO.OUT)

def loop(pin, time_on, time_off):
    while True:
        print(GPIO.getmode())
        GPIO.output(pin, GPIO.LOW)
        time.sleep(time_on)
        GPIO.output(pin, GPIO.HIGH)
        time.sleep(time_off)

def turn_off(pin):
	GPIO.output(pin, GPIO.LOW)

def turn_on(pin):
	GPIO.output(pin, GPIO.HIGH)

