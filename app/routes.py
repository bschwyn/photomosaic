from app import app
from flask import Flask, request, render_template, send_from_directory, redirect, url_for
from werkzeug import secure_filename
import os

from PIL import Image

TESTBLA_FOLDER = os.path.join('static', 'testbla')
app.config['UPLOAD_FOLDER'] = TESTBLA_FOLDER

@app.route('/')
@app.route('/')
@app.route('/index')
def index():
    return app.root_path


@app.route('/upload/')
def upload():
    return """
<html>
    <body>
    <!-- send form data to uploader w/ post method upon submit -->
    <form action = "http://localhost:5000/uploader" method = "POST"
    enctype = "multipart/form-data">
    <input type = "file" name = "file" />
    <input type = "submit"/>
    </form >
    </body>
</html>"""

@app.route('/test1/')
def send_file():
    filename = 'picture.jpg'
    path = os.path.join(app.root_path, 'static')
    return send_from_directory(directory=path, filename=filename)

@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        target = os.path.join(app.root_path, 'static')
        f.save(os.path.join(target, f.filename))
    #do stuff with uploaded image
    filename = f.filename
    return render_template('template.html', filename=filename)

@app.route('/rotate/<filename>', methods=['GET', 'POST'])
def rotate(filename):
    img = Image.open("/home/ben/Projects/photomosaic/app/static/" + filename)
    img2 = img.rotate(90)
    img2.save("/home/ben/Projects/photomosaic/app/static/rotated/" + filename)
    rotated = "/rotated/" + filename
    return render_template('template2.html', filename=rotated)

