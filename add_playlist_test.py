import requests

data = {'name': 'Chill', 'img_url': 'http://192.168.3.150:8081/chill_cover.jpg', 'img_filename': 'cover.jpg'}

requests.post('http://192.168.3.148/api/create_playlist', data=data)