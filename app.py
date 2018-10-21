from flask import Flask, request, send_file, redirect, url_for, send_from_directory, render_template
import os
import time
from copykey import copykey
from werkzeug.utils import secure_filename
import cv2
from base64 import b64encode

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
    # check if the post request has the file part
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    type = request.form['type']
    # if user does not select file, browser also
    # submit a empty part without filename
    if file.filename == '':
        return 'No file selected'
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'video.mp4'))
        img1, img2 = copykey.copykey(
            os.path.join(app.config['UPLOAD_FOLDER'], 'video.mp4'),
            os.path.join(app.config['UPLOAD_FOLDER'], filename + '.scad'),
            type,
            cool_video_output=os.path.join(app.config['UPLOAD_FOLDER'], 'cool_video.mp4')
        )
        return render_template("index.html", result=True, filename=".".join(filename.split(".")[:-1]) + '.scad', img1=b64encode(cv2.imencode('.jpg', img1)[1]).decode('utf-8'), img2=b64encode(cv2.imencode('.jpg', img2)[1]).decode('utf-8'), time=time.time())
        cv2.imshow(img1)
        cv2.waitKey(0)
    # return redirect(url_for('get_file', filename=filename + '.scad'))
    return render_template("index.html")

@app.route('/get/<filename>')
def get_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/')
def index():
    return render_template("index.html")

@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r
