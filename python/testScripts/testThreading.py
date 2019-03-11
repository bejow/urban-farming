import threading
import time

def print_every_5_seconds():
    while True:
        print("I print every 5 seconds")
        time.sleep(5)

def print_every_second():
    while True:
        print("I print every second")
        time.sleep(1)

threading.Thread(target=print_every_5_seconds).start()
threading.Thread(target=print_every_second).start()
