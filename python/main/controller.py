import RPi.GPIO as GPIO
import time
import threading
#GPIO.setmode(GPIO.BOARD)

#setting up the pins
WATER_RELAIS_PIN = 11
LIGHT_RELAIS_PIN = 13

#GPIO.setup(WATER_RELAIS_PIN, GPIO.OUT)
#GPIO.setup(LIGHT_RELAIS_PIN, GPIO.OUT)

def loop(pin, time_on, time_off):
    print("Pin", pin, "\ntime on:", time_on, "\ntime off:", time_off)
    t = threading.currentThread()
    while getattr(t, "do_run", True):
        GPIO.output(pin, GPIO.LOW)
        time.sleep(time_on)
        GPIO.output(pin, GPIO.HIGH)
        time.sleep(time_off)
    print("stop looping pin", pin)

def turn_off(pin):
	GPIO.output(pin, GPIO.LOW)

def turn_on(pin):
	GPIO.output(pin, GPIO.HIGH)

