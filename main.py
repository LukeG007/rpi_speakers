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
audio_requests = []
audio_playing_object = None
def play_audio(wave_obj):
    global audio_playing_object
    audio_playing_object = wave_obj.play()
    audio_playing_object.wait_done()
    del audio_requests[0]

def audio_sys():
    global audio_requests
    global audio_playing_object
    while True:
        if len(audio_requests) == 1:
            filename = audio_requests[0]
            filetype = filename.split('.')[len(filename.split('.')) - 1]
            if filetype.lower() == 'wav':
                wave_obj = sa.WaveObject.from_wave_file('songs/' + filename)
                threading.Thread(target=play_audio, args=[wave_obj]).start()
        if len(audio_requests) == 2:
            audio_playing_object.stop()
            filename = audio_requests[0]
            filetype = filename.split('.')[len(filename.split('.')) - 1]
            if filetype.lower() == 'wav':
                wave_obj = sa.WaveObject.from_wave_file('songs/' + filename)
                threading.Thread(target=play_audio, args=[wave_obj]).start()


@app.route('/api/upload', methods=['POST'])
def upload():
    url = dict(request.form)['url']
    filename = dict(request.form)['filename']
    playlist = dict(request.form)['playlist']
    filename = filename.lower()
    filetype = filename.split('.')[len(filename.split('.')) - 1]
    title = dict(request.form)['title']
    r = requests.get(url)
    f = open('playlists/{}/songs/'.format(playlist) + filename, 'w+')
    f.truncate(0)
    f.close()
    f = open('playlists/{}/songs/'.format(playlist) + filename, 'wb')
    f.write(r.content)
    f.close()
    if filetype == 'mp3':
        sound = AudioSegment.from_mp3('songs/' + filename)
        sound.export('playlists/{}/songs/'.format(playlist) + filename.replace('.mp3', '.wav'), format="wav")
        filename = filename.replace('.mp3', '.wav')
    f = open('song_titles.json', 'r')
    json_dir = json.load(f)
    json_dir['song_titles'][filename] = title
    json_str = json.dumps(json_dir)
    f.close()
    os.system('rm playlists/{}/song_titles.json'.format(playlist))
    os.system('touch playlists/{}/song_titles.json'.format(playlist))
    f = open('playlists/{}/song_titles.json'.format(playlist), 'w')
    f.write(json_str)
    f.close()
    return 'OK'

@app.route('/api/play', methods=['POST'])
def play2():
    filename = dict(request.form)['filename']
    playlist = dict(request.form)['playlist']
    filetype = filename.split('.')[len(filename.split('.')) - 1]
    if filetype.lower() == 'wav':
        wave_obj = sa.WaveObject.from_wave_file('playlists/{}/songs/'.format(playlist) + filename)
        play_obj = wave_obj.play()
        play_obj.wait_done()
    return 'OK'

@app.route('/playlists')
def playlists():
    all_playlists = os.listdir('playlists')
    return render_template('playlists.html', playlists=all_playlists)

@app.route('/playlists/<string:playlist>')
def playlist_view(playlist):
    f = open('playlists/{}/song_titles.json'.format(playlist))
    json_dir = json.load(f)
    f.close()
    for song in json_dir['song_titles']:
        title = json_dir[song]
        print(song)
        del json_dir['song_titles'][song]
        song = 'playlists/{}/'.format(playlist) + song
        json_dir['song_titles'][song] = title
    return render_template('home.html', songs=json_dir['song_titles'])

@app.route('/api/autoplay', methods=['POST'])
def autoplay():
    playlist = dict(request.form)['playlist']
    for filename in os.listdir('playlists/{}/songs'.format(playlist)):
        filetype = filename.split('.')[len(filename.split('.')) - 1]
        if filetype.lower() == 'wav':
            wave_obj = sa.WaveObject.from_wave_file('playlists/{}/songs/'.format(playlist) + filename)
            play_obj = wave_obj.play()
            play_obj.wait_done()
    return 'OK'

@app.route('/play/<string:song>')
def play(song):
    data = {'filename': song}
    requests.post('http://192.168.3.148/api/play', data=data)
    return redirect('/')

if __name__ == '__main__':
    threading.Thread(target=audio_sys).start()
    app.run(host='0.0.0.0', port=80)