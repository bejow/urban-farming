import threading
import time
import requests
import RPi.GPIO as GPIO
import sys
import json
import traceback

import controller
import sensors
import settings

def startThreads(threads):
    for thread in threads:
        thread.start()

def stopThreads(threads):
    for thread in threads:
        thread.do_run = False

def get_settings(interval):
    global current_settings
    t = threading.currentThread()
    while getattr(t, "do_run", True):
        req = requests.get(settings.api_url + settings.settings_endpoint)
        current_settings = json.loads(req.text)
        time.sleep(interval)
    print("stop fetching settings..")

def update_ph(interval):
    #periodically gets the sensor value of PH and sends it to the server
    t = threading.currentThread()
    while getattr(t, "do_run", True):
        ph_data = {
            'time': str(time.time()),
            'value': str(sensors.read_ph_sensor())
        }
        postReq = requests.post(settings.api_url + settings.ph_endpoint, data=ph_data)
        print("Update PH:\n{}\n\n".format(ph_data))
        time.sleep(interval)
    print("stop updating ph..")

def update_oxygen(interval):
    #periodically gets the sensor value of oxygen and sends it to the server                     
    t = threading.currentThread()
    while getattr(t, "do_run", True):
        oxygen_data = {
            'time': str(time.time()),
            'value': str(sensors.read_oxygen_sensor())
        }
        postReq = requests.post(settings.api_url + settings.oxygen_endpoint, data=oxygen_data)
        print("Update Oxygen:\n{}\n\n".format(oxygen_data))
        time.sleep(interval)
    print("stop updating oxygen..")    
        

def update_temperature(interval):
    #periodically gets the sensor value of temperature and send it to the server                     
    t = threading.currentThread()
    while getattr(t, "do_run", True):
        temperature_data = {
            'time': str(time.time()),
            'value': str(sensors.read_temperature_sensor())
        }
        postReq = requests.post(settings.api_url + settings.temperature_endpoint, data=temperature_data)
        print("Update Temperature:\n{}\n\n".format(temperature_data))
        time.sleep(interval)
    print("stop updating temperature..")

def loop(pin, time_on, time_off):
    global current_settings
    t = threading.currentThread()
    while getattr(t, "do_run", True):
        print(current_settings)
        GPIO.output(pin, GPIO.LOW)
        time.sleep(int(current_settings["water_time"]))
        GPIO.output(pin, GPIO.HIGH)
        time.sleep(int(current_settings["no_water_time"])
    print("stop looping pin", pin)

try:
    #GPIO Setup
    GPIO.setmode(GPIO.BOARD)
    WATER_RELAIS_PIN = 13
    LIGHT_RELAIS_PIN = 11
    GPIO.setup(WATER_RELAIS_PIN, GPIO.OUT)
    GPIO.setup(LIGHT_RELAIS_PIN, GPIO.OUT)

    #load settings
    current_settings = settings.default_settings
    print(current_settings)
    #create separate Threads for the diffrent jobs
    ph_thread = threading.Thread(target=update_ph, args=[20])
    oxygen_thread = threading.Thread(target=update_oxygen, args=[30])
    temperature_thread = threading.Thread(target=update_temperature, args=[15])
    water_thread = threading.Thread(target=loop, args=[WATER_RELAIS_PIN, current_settings["water_time"], current_settings["no_water_time"]])
    light_thread = threading.Thread(target=loop, args=[LIGHT_RELAIS_PIN, 2, 1])
    settings_thread = threading.Thread(target=get_settings, args=[5])
    myThreads = [ph_thread, oxygen_thread, temperature_thread, water_thread, light_thread, settings_thread]

    startThreads(myThreads)
    input("press key to exit")
except KeyboardInterrupt:
    print("Handling Keyboard Interrupt")
except SystemExit:
    print("Handling System Exit")
except Exception:
    traceback.print_exc()
finally:
    print("error or end of programm")
    GPIO.cleanup()
    stopThreads(myThreads)
    sys.exit()

