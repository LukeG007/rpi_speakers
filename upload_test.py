import requests

data = {'url': r'http://192.168.3.150:8081/good.mp3', 'filename': 'good.mp3', 'title': 'Good'}

requests.post('http://192.168.3.148/api/upload', data=data)