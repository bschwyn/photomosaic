from app import app
from flask import Flask, request, render_template, send_from_directory, redirect, url_for
from werkzeug import secure_filename

import os

from PIL import Image

from .photomosaics2 import Photomosaic



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
    <head>
    <title>Photomosaic Image Upload </title>
    <meta name ="description"
    conent="TinEye is a reverse image search engine. Search by image: Give it an image and it will tell you where the image appears on the web."> 
    </head>
    <body>
    
    <form action = "http://localhost:5000/uploader" method = "POST"
    enctype = "multipart/form-data">
    <input type = "file" name = "file" />
    <input type = "submit"/>
    </form >
    
    <div class="forms ">
        <form id="upload_form" method="post" action="http://localhost:5000/uploader" enctype="multipart/form-data">
              <label for="upload_box" id="upload-button"></label>
              <input id="upload_box" name="image" onchange="display_throbber(); this.form.submit()" title="Upload an image" type="file"  />
              <input style="display: none;" id="file_submit" value="Upload Image" class="submit" type="submit"  />
            </form>
            <form id="url_form" method="post" action="https://www.tineye.com/search" onsubmit="display_throbber();">
              <div class="input-container">
                <input class="image-url" id="url_box" name="url" maxlength="100000" placeholder="Upload or enter Image URL"  onfocus="this.form.search_button.disabled=false" type="text"  />
              </div>
              <input class="submit-button" id="url_submit" name="search_button" value=""  type="submit" />
            </form>
        </div>
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

#possible bugs:
#what if multiple people upload the same file or make a new version of a previously uploaded photo?
    # add unique identifier to every upload, have people put in a title
#what if the parameters they upload are too big / etc
# have some directions / errors

#ways to make it better...
#different, more complicated templates


@app.route('/create_mosaic/<filename>', methods=['GET', 'POST'])
def mosaic(filename):
    photomosaic = Photomosaic("/home/ben/Projects/photomosaic/app/static/" + filename,
                              '/home/ben/Pictures/')
    x = photomosaic.construct_mosaic(10, 10, 1)
    x.save("/home/ben/Projects/photomosaic/app/static/mosaics/" + filename)
    return render_template('template3.html', filename='/mosaics/' + filename)