import threading
import time
import sensors
import requests
import controller
import RPi.GPIO as GPIO

#GPIO.setmode(GPIO.BOARD)
WATER_RELAIS_PIN = 11
LIGHT_RELAIS_PIN = 13
#GPIO.setup(WATER_RELAIS_PIN, GPIO.OUT)
#GPIO.setup(LIGHT_RELAIS_PIN, GPIO.OUT)
#GPIO.output(WATER_RELAIS_PIN, GPIO.HIGH)
def main():
    #create separate Threads for the diffrent jobs
    ph_thread = threading.Thread(target=update_ph, args=[20])
    oxygen_thread = threading.Thread(target=update_oxygen, args=[30])
    temperature_thread = threading.Thread(target=update_temperature, args=[15])
    water_thread = threading.Thread(target=controller.loop, args=[WATER_RELAIS_PIN, 5, 2])
    light_thread = threading.Thread(target=controller.loop, args=[LIGHT_RELAIS_PIN, 2, 1])

    water_thread.start()
    #light_thread.start()
    #starting threads
    #ph_thread.start()
    
    #oxygen_thread.start()
    #temperature_thread.start()

    #starting threads
    #ph_thread.start()
    #oxygen_thread.start()
    #temperature_thread.start()
   
def update_ph(interval):
    #periodically gets the sensor value of PH and sends it to the server
    while True:
        ph_data = {
            'time': str(time.time()),
            'value': str(sensors.read_ph_sensor())
        }
        postReq = requests.post('http://localhost:3000/ph', data=ph_data)
        print("Update PH:\n{}\n\n".format(ph_data))
        time.sleep(interval)

def update_oxygen(interval):
    #periodically gets the sensor value of oxygen and sends it to the server                     
    while True:
        oxygen_data = {
            'time': str(time.time()),
            'value': str(sensors.read_oxygen_sensor())
        }
        postReq = requests.post('http://localhost:3000/oxygen', data=oxygen_data)
        print("Update Oxygen:\n{}\n\n".format(oxygen_data))
        time.sleep(interval)
        

def update_temperature(interval):
    #periodically gets the sensor value of temperature and send it to the server                     
    while True:
        temperature_data = {
            'time': str(time.time()),
            'value': str(sensors.read_temperature_sensor())
        }
        postReq = requests.post('http://localhost:3000/temperature', data=temperature_data)
        print("Update Temperature:\n{}\n\n".format(temperature_data))
        time.sleep(interval)


try:

    
    main()
    input("press key to exit")
except KeyboardInterrupt:
    GPIO.cleanup()
    print("Handling Keyboard Interrupt")
finally:
    print("finally")
    GPIO.cleanup()

