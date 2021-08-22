import requests

data = {'filename': 'how_r_u.wav'}

requests.post('http://192.168.3.148/api/play', data=data)