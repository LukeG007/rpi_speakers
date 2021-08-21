import requests

data = {'filename': 'ace_of_spades.mp3'}

requests.post('http://192.168.3.148/api/play', data=data)