from flask import Flask, redirect, request, render_template
import requests
import os
import psutil
import simpleaudio as sa
import threading
import json
from pydub import AudioSegment
import subprocess

app = Flask(__name__)

@app.route('/api/upload', methods=['POST'])
def upload():
    url = dict(request.form)['url']
    filename = dict(request.form)['filename']
    filename = filename.lower()
    filetype = filename.split('.')[len(filename.split('.')) - 1]
    title = dict(request.form)['title']
    r = requests.get(url)
    f = open('songs/' + filename, 'w+')
    f.truncate(0)
    f.close()
    f = open('songs/' + filename, 'wb')
    f.write(r.content)
    f.close()
    if filetype == 'mp3':
        sound = AudioSegment.from_mp3('song/' + filename)
        sound.export(filename.replace('.mp3', '.wav'), format="wav")
        filename = filename.replace('.wav', '.mp3')
    f = open('song_titles.json', 'r')
    json_dir = json.load(f)
    json_dir['song_titles'][filename] = title
    json_str = json.dumps(json_dir)
    f.close()
    os.system('rm song_titles.json')
    os.system('touch song_titles.json')
    f = open('song_titles.json', 'w')
    f.write(json_str)
    f.close()
    return 'OK'

@app.route('/api/play', methods=['POST'])
def play2():
    filename = dict(request.form)['filename']
    threading.Thread(target=subprocess.Popen, args=[['ffplay', 'songs/' + filename]]).start()
    print(dir(psutil.Process().children(recursive=True)[0]))
    return 'OK'

@app.route('/api/autoplay')
def autoplay():
    #threading.Thread(target=subprocess.Popen, args=[['ffplay', 'songs/' + filename]]).start()
    for filename in os.listdir('songs'):
        filetype = filename.split('.')[len(filename.split('.')) - 1]
        if filetype.lower() == 'wav':
            wave_obj = sa.WaveObject.from_wave_file('songs/' + filename)
            play_obj = wave_obj.play()
            play_obj.wait_done()
    return 'OK'

@app.route('/')
def home():
    songs = []
    f = open('song_titles.json')
    json_dir = json.load(f)
    f.close()
    return render_template('home.html', songs=json_dir['song_titles'])

@app.route('/play/<string:song>')
def play(song):
    data = {'filename': song}
    requests.post('http://192.168.3.148/api/play', data=data)
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)