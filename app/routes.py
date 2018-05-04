from app import app
from flask import Flask, request, render_template, send_from_directory, redirect, url_for
from werkzeug import secure_filename
import urllib.request
import ntpath
import sys
import os
import time
from PIL import Image
import itertools
import tempfile
import uuid

from .photomosaics2 import Photomosaic

def uniquify(filename):
    head, tail = filename.split('.')
    uniquifier = str(uuid.uuid4().hex)
    return head + uniquifier +'.' + tail


TESTBLA_FOLDER = os.path.join('static', 'testbla')
app.config['UPLOAD_FOLDER'] = TESTBLA_FOLDER

@app.route('/')
@app.route('/')
@app.route('/index')
def index():
    return "this is the index"


@app.route('/test1/')
def send_file():
    return render_template('test.html')


@app.route('/testmosaictime')
def timeing():
    start = time.time()
    print('start', file=sys.stderr)
    photomosaic = Photomosaic("/home/ben/Pictures/heroes/1518057175453-D4FA2544-E96B-4B0D-84F0-43EB61AAC8DD.jpeg",
                              '/home/ben/Pictures/')
    x = photomosaic.construct_mosaic(15, 15, 1)
    #x.save('/home/ben/Documents/aphotomosaic15.jpg')
    end = time.time()
    print("total time", end - start, file=sys.stderr)
    print('end', file=sys.stderr)
    return end-start


@app.route('/upload/')
def upload():
    return render_template("upload_picture_template.html")

@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        target = os.path.join(app.root_path, 'static')
        print(os.path.join(target, f.filename), file=sys.stderr)
        #check if file with same name
        if not os.path.isfile(os.path.join(target, f.filename)):
            filename = f.filename
            f.save(os.path.join(target, filename))
        else:
            #not guaranteed to save a unique file, just highly likely
            filename = uniquify(f.filename)
            f.save(os.path.join(target, filename))

    return render_template('mosaic_parameters_template.html', filename=filename)

@app.route('/uploader_url', methods=['GET', 'POST'])
def download_url_and_upload():
    if request.method == 'POST':
        url = request.form['url']

        head, tail = ntpath.split(url)
        local_filename = "/home/ben/Projects/photomosaic/app/static/" + tail
        urllib.request.urlretrieve(url, local_filename)
        return render_template('mosaic_parameters_template.html', filename = tail)
    if request.method == 'GET':
        return 'get'
    return "not post"

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


@app.route('/create_mosaic/<filename>/', methods=['GET', 'POST'])
def mosaic(filename):
    width = int(request.form['width'])
    height = int(request.form['height'])
    scale = int(request.form['scale'])
    print(width, height, scale, file=sys.stderr)
    photomosaic = Photomosaic("/home/ben/Projects/photomosaic/app/static/" + filename, '/home/ben/Pictures/')
    #if width, height, scale out of bounds, add form validation
    x = photomosaic.construct_mosaic(width, height, scale)

    data_to_string = str(width)

    x.save("/home/ben/Projects/photomosaic/app/static/mosaics/" + "mosaic_"+ filename)

    print("saving to", "/home/ben/Projects/photomosaic/app/static/mosaics/" + "mosaic_"+ filename, file=sys.stderr)
    #
    return render_template('show_final_template.html', filename='/mosaics/' + "mosaic_" + filename)
