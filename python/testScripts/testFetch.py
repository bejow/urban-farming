import requests
#download and install it http://docs.python-requests.org/en/latest/user/install/#install
req = requests.get('http://localhost:3000/oxygen')
print(req.text)
