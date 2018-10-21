from flask import Flask, request, send_file, redirect, url_for, send_from_directory
import os
import time
from copykey import copykey
from threading import Thread
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = './tmp/'
ALLOWED_EXTENSIONS = set(['mp4'])
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        # check if the post request has the file part
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        type = request.form['type']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            return 'No selected file'
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            copykey.copykey(os.path.join(app.config['UPLOAD_FOLDER'], filename), os.path.join(app.config['UPLOAD_FOLDER'], filename + '.scad'), type)
            time.sleep(10)
        return redirect(url_for('get_file', filename=filename + '.scad'))
    except:
        return 'Failure'

@app.route('/get/<filename>')
def get_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/')
def index():
    with open("index.html", "r") as f:
        return f.read()
