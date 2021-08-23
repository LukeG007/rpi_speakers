import requests

data = {'name': 'hi'}

requests.post('http://192.168.3.148/api/create_playlist', data=data)