import requests

data = {'name': 'Chill', 'img_url': 'https://ih1.redbubble.net/image.1234400278.2371/bg,f8f8f8-flat,750x,075,f-pad,750x1000,f8f8f8.jpg', 'img_filename': 'image.jpg'}

requests.post('http://192.168.3.148/api/create_playlist', data=data)