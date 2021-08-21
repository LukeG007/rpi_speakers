import requests

data = {'url': r'http://192.168.3.199:8081/01%20-%20Ace%20of%20Spades.mp3', 'filename': 'ace_of_spades.mp3'}

requests.post('http://192.168.3.148/api/upload', data=data)