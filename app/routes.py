from app import app
from flask import Flask, request, render_template, send_from_directory, redirect, url_for
from werkzeug import secure_filename
import os

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

#@app.route('/test/')
#def test():
#    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'picture.jpg')
#    return render_template('test.html', bla = full_filename)

@app.route('/test1/')
def send_file():
    filename = 'picture.jpg'
    path = os.path.join(app.root_path, 'static')
    return send_from_directory(directory=path, filename=filename)

#@app.route('<fname>')
#def legacy_images(fname):
#    return redirect(url_for('static', filename='static/' + fname), code=301)

@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        target = os.path.join(app.root_path, 'static')
        f.save(os.path.join(target, f.filename))
    #do stuff with uploaded image
    return render_template('template.html', filename='picture.jpg')

#figure out what request.files['file'] means
#figure out where save file goes --- to project root!

#how do I have the the app call a function
#what is a simple thing that I can do with the image?
#display the image.
#have the image be available for download