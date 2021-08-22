from flask import Flask, redirect, request, render_template
import requests
import os
import playsound
import threading
import json
import subprocess

app = Flask(__name__)

@app.route('/api/upload', methods=['POST'])
def upload():
    url = dict(request.form)['url']
    filename = dict(request.form)['filename']
    r = requests.get(url)
    f = open('songs/' + filename, 'w+')
    f.truncate(0)
    f.close()
    f = open('songs/' + filename, 'wb')
    f.write(r.content)
    f.close()
    return 'OK'

@app.route('/api/play', methods=['POST'])
def play2():
    filename = dict(request.form)['filename']
    threading.Thread(target=subprocess.Popen, args=[['ffplay', 'songs/' + filename]]).start()
    return 'OK'

@app.route('/')
def home():
    songs = []
    f = open('song_titles.json')
    json_dir = json.load(f)
    f.close()
    print(json_dir['song_titles'])
    for x in json_dir['song_titles']:
        print(x)
        songs.append(json_dir['song_titles'][x])

    return render_template('home.html', songs=songs)

@app.route('/play/<string:song>')
def play(song):
    data = {'filename': song}
    requests.post('http://192.168.3.148/api/play', data=data)
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)