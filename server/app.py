from sanic import Sanic
from sanic import response

import subprocess
import time
import os
import json

app = Sanic(__name__)

ALLOWED_EXTENSIONS = set(['mp3', 'm4a', 'flac', 'wav', 'aac', 'ogg', 'wma', 'aac', '3gp'])

PATH = {
    'PATH': "/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin"
}

ERROR_CODE = {
    0: 'Success',
    1: 'Insufficient Parameters',
    2: 'Parameter is not filled',
    3: 'Invalid extensions',
    4: 'Processing error',
    5: 'Invalid Parameters',
    6: 'Too Big File',
}

@app.route('/')
async def index(request):
    return await response.file('templates/index.html')

@app.route('/api')
async def api_index(request):
    return await response.file('templates/api.html')

@app.route('/api/segscore', methods=['POST'])
async def seg_score(request):
    if 'gender' not in request.form or \
        'transcript' not in request.form or \
        'file' not in request.files:
        return error(request.path, 1)

    gender = request.form.get('gender')
    transcript = request.form.get('transcript')
    file = request.files.get('file')

    if gender == '' or transcript == '':
        return error(request.path, 2)
    if gender != 'm' and gender != 'f':
        return error(request.path, 5)

    filename = make_filename(file.name)
    if filename == '':
        return error(request.path, 3)
    
    f = open('temp/raw/' + filename, 'wb')
    f.write(file.body)
    f.close()

    filesize = get_filesize('temp/raw/' + filename)
    if filesize == -1 or filesize >= 1.0:
        return error(request.path, 6)

    print('./seg_and_audio2pron.sh {} "{}" {}'.format(gender, transcript, filename))
    subprocess.run('./seg_and_audio2pron.sh {} "{}" {}'.format(gender, transcript, filename), shell=True, cwd=os.path.abspath('..'))

    if not os.path.isfile('temp/result/{}.json'.format(filename)):
        return error(request.path, 4)

    result_file = open('temp/result/{}.json'.format(filename), 'r')
    result = json.load(result_file)
    result_file.close()

    return response.json({'request': request.path, 'status': 'Success', 'code': 0, 'score': float(result['score']), 'phone_score': float(result['phone_score']), 'speed_score': float(result['speed_score']), 'rhythm_score': float(result['rhythm_score']), 'transcript': result['transcript'], 'student_transcript': result['student_trans'], 'correct': result['correct'], 'student': result['student']})


def get_filesize(filename):
    try:
        size_bytes = os.path.getsize(filename)
        size_mb = size_bytes / 1024 / 1024
        return size_mb
    except:
        return -1

def make_filename(filename):
    millis = int(round(time.time() * 1000))
    ext = filename.rsplit('.', 1)[1]

    if ext not in ALLOWED_EXTENSIONS:
        return ''

    return '{}.{}'.format(str(millis), ext)

def error(req, err):
    return response.json({'request': req, 'status': 'Fail', 'code': err, 'message': ERROR_CODE[err]})

if __name__ == '__main__':
    app.run()
