import threading
import time
import requests
import RPi.GPIO as GPIO
import sys
import json
import traceback
from w1thermsensor import W1ThermSensor

import settings

def startThreads(threads):
    for thread in threads:
        thread.start()

def stopThreads(threads):
    for thread in threads:
        thread.do_run = False

def get_settings(interval):
    global token
    headers= {
        "Authorization": "Bearer " + token
    }
    global current_settings
    t = threading.currentThread()
    while getattr(t, "do_run", True):
        req = requests.get(settings.api_url + settings.settings_endpoint, headers=headers)
        current_settings = json.loads(req.text)
        time.sleep(interval)
    print("stop fetching settings..")

def update_ph(interval):
    #periodically gets the sensor value of PH and sends it to the server
    global token
    t = threading.currentThread()
    while getattr(t, "do_run", True):
        ph_data = {
            'time': str(time.time()),
            'value': str("fake sensor ph data")
        }
        headers= {
            "Authorization": "Bearer " + token
        }
        postReq = requests.post(settings.api_url + settings.ph_endpoint, data=ph_data, headers=headers)
        print("Update PH:\n{}\n\n".format(ph_data))
        time.sleep(interval)
    print("stop updating ph..")

def update_oxygen(interval):
    #periodically gets the sensor value of oxygen and sends it to the server                     
    global token
    t = threading.currentThread()
    while getattr(t, "do_run", True):
        oxygen_data = {
            'time': str(time.time()),
            'value': str("fake sensor oxygen data")
        }
        headers= {
            "Authorization": "Bearer " + token
        }
        postReq = requests.post(settings.api_url + settings.oxygen_endpoint, data=oxygen_data, headers=headers)
        print("Update Oxygen:\n{}\n\n".format(oxygen_data))
        time.sleep(interval)
    print("stop updating oxygen..")
        

def update_temperature(interval):
    #periodically gets the sensor value of temperature and send it to the server                     
    global token
    sensor = W1ThermSensor()
    t = threading.currentThread()
    while getattr(t, "do_run", True):
        temperature_data = {
            'time': str(time.time()),
            'value': str(sensor.get_temperature())
        }
        headers= {
            "Authorization": "Bearer " + token
        }
        postReq = requests.post(settings.api_url + settings.temperature_endpoint, data=temperature_data, headers=headers)
        print("Update Temperature:\n{}\n\n".format(temperature_data))
        time.sleep(interval)
    print("stop updating temperature")

def water_loop(pin):
    global current_settings
    t = threading.currentThread()
    while getattr(t, "do_run", True):
        print(current_settings)
        GPIO.output(pin, GPIO.LOW)
        time.sleep(float(current_settings["water_time"]))
        GPIO.output(pin, GPIO.HIGH)
        time.sleep(float(current_settings["no_water_time"]))
    print("Stopping Water on Pin", pin)

def light_loop(pin):
    global current_settings
    t = threading.currentThread()
    while getattr(t, "do_run", True):
        print(current_settings)
        GPIO.output(pin, GPIO.LOW)
        time.sleep(float(current_settings["light_time"]))
        GPIO.output(pin, GPIO.HIGH)
        time.sleep(float(current_settings["no_light_time"]))
    print("Stopping Light on pin", pin)

def authenticate():
    global token
    headers = {
        "content-type" : "application/x-www-form-urlencoded"
    }
    auth_data = {
        "deviceIdentifier": settings.uuid,
        "deviceSecret": settings.secret
    }
    auth_req = requests.post(settings.api_url + settings.auth_endpoint, headers=headers, data=auth_data)
    new_token = json.loads(auth_req.text)
    token = new_token
    return token

try:
    #GPIO Setup
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(settings.water_relais_pin, GPIO.OUT)
    GPIO.setup(settings.light_relais_pin, GPIO.OUT)
    #load settings
    current_settings = settings.system_settings
    
    #authenticate
    token = authenticate()
    print("#token: " + str(token))


    #create separate Threads for the diffrent jobs
    ph_thread = threading.Thread(target=update_ph, args=[settings.update_ph_frequency])
    oxygen_thread = threading.Thread(target=update_oxygen, args=[settings.update_oxygen_frequency])
    temperature_thread = threading.Thread(target=update_temperature, args=[settings.update_temperature_frequency])
    water_thread = threading.Thread(target=water_loop, args=[settings.water_relais_pin])
    light_thread = threading.Thread(target=light_loop, args=[settings.light_relais_pin])
    settings_thread = threading.Thread(target=get_settings, args=[settings.fetch_settings_frequency])
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
    
