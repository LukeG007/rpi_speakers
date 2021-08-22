import requests

data = {'url': r'http://192.168.3.150:8081/how_r_u.wav', 'filename': 'how_r_u.wav', 'title': 'How are you?'}

requests.post('http://192.168.3.148/api/upload', data=data)