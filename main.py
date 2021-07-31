from flask import Flask, redirect, request
import requests
import playsound
import threading
import pygame
pygame.mixer.init()

app = Flask(__name__)

def play(filename):
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()

@app.route('/api/upload', methods=['POST'])
def upload():
    url = dict(request.form)['url']
    filename = dict(request.form)['filename']
    r = requests.get(url)
    f = open(filename, 'w+')
    f.truncate(0)
    f.close()
    f = open(filename, 'wb')
    f.write(r.content)
    f.close()
    return 'OK'

@app.route('/api/play', methods=['POST'])
def play2():
    filename = dict(request.form)['filename']
    threading.Thread(target=play, args=[filename]).start()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)