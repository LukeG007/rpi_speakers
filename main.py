from flask import Flask, redirect, request
import requests

app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)