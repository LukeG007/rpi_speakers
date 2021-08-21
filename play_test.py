import requests

data = {'filename': 'hello.wav'}

requests.post('http://192.168.3.148/api/play', data=data)