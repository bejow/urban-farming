import threading
import time
import requests
import RPi.GPIO as GPIO
import sys
import json

import controller
import sensors
import settings

GPIO.setmode(GPIO.BOARD)
WATER_RELAIS_PIN = 13
LIGHT_RELAIS_PIN = 11
GPIO.setup(WATER_RELAIS_PIN, GPIO.OUT)
GPIO.setup(LIGHT_RELAIS_PIN, GPIO.OUT)

global settings
settings = settings.default_settings

def main():
    #create separate Threads for the diffrent jobs
    ph_thread = threading.Thread(target=update_ph, args=[20])
    oxygen_thread = threading.Thread(target=update_oxygen, args=[30])
    temperature_thread = threading.Thread(target=update_temperature, args=[15])
    water_thread = threading.Thread(target=controller.loop, args=[WATER_RELAIS_PIN, 2, 1])
    light_thread = threading.Thread(target=controller.loop, args=[LIGHT_RELAIS_PIN, 2, 1])

    get_settings(3)
    #starting threads
    #ph_thread.start()
    #oxygen_thread.start()
    #temperature_thread.start()
    #water_thread.start()
    #light_thread.start()

def get_settings(interval):
    global settings
    #while True:
    req = requests.get(settings.api_url + settings.settings_endpoint)
    settings = json.loads(req.text)
    print(settings)

def update_ph(interval):
    #periodically gets the sensor value of PH and sends it to the server
    while True:
        ph_data = {
            'time': str(time.time()),
            'value': str(sensors.read_ph_sensor())
        }
        postReq = requests.post(settings.api_url + settings.ph_endpoint, data=ph_data)
        print("Update PH:\n{}\n\n".format(ph_data))
        time.sleep(interval)

def update_oxygen(interval):
    #periodically gets the sensor value of oxygen and sends it to the server                     
    while True:
        oxygen_data = {
            'time': str(time.time()),
            'value': str(sensors.read_oxygen_sensor())
        }
        postReq = requests.post(settings.api_url + settings.oxygen_endpoint, data=oxygen_data)
        print("Update Oxygen:\n{}\n\n".format(oxygen_data))
        time.sleep(interval)
        

def update_temperature(interval):
    #periodically gets the sensor value of temperature and send it to the server                     
    while True:
        temperature_data = {
            'time': str(time.time()),
            'value': str(sensors.read_temperature_sensor())
        }
        postReq = requests.post(settings.api_url + settings.temperature_endpoint, data=temperature_data)
        print("Update Temperature:\n{}\n\n".format(temperature_data))
        time.sleep(interval)


try:
    main()
    input("press key to exit")
except KeyboardInterrupt:
    print("Handling Keyboard Interrupt")
except SystemExit:
    print("Handling System Exit")
finally:
    print("finally")
    GPIO.cleanup()
    sys.exit()

