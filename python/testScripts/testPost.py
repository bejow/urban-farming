import requests
import time
import random

oxygenData = {
    'time': str(time.time()),
    'value': str(random.randint(50,70))
    }

postReq = requests.post('http://localhost:3000/oxygen', data=oxygenData)
print(postReq)
