import threading
import time
import sensors
import requests

def main():
    #create separate Threads for the diffrent jobs
    ph_thread = threading.Thread(target=update_ph, args=[20])
    oxygen_thread = threading.Thread(target=update_oxygen, args=[30])
    temperature_thread = threading.Thread(target=update_temperature, args=[15])

    #starting threads
    ph_thread.start()
    oxygen_thread.start()
    temperature_thread.start()

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

main()

