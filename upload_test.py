import requests

data = {'url': r'http://192.168.3.150:8081/hello.wav', 'filename': 'hello.wav'}

requests.post('http://192.168.3.148/api/upload', data=data)