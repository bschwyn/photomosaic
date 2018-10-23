
from photomosaic import app
from flask import Flask, request, render_template
import urllib.request
import ntpath
import sys
import os
import time
from PIL import Image
import uuid
import tempfile
import itertools
from .photomosaic_model import Photomosaic
import logging


def uniquify(filename):
    head, tail = filename.split('.')
    uniquifier = str(uuid.uuid4().hex)
    return head + uniquifier +'.' + tail


TESTBLA_FOLDER = os.path.join('static', 'testbla')
app.config['UPLOAD_FOLDER'] = TESTBLA_FOLDER


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


@app.route('/mosaic/')
def upload():
    return render_template("upload_picture_template.html")

@app.route('/mosaic/uploader', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        target = os.path.join(app.root_path, 'static')
        if not os.path.isfile(os.path.join(target, f.filename)):
            filename = f.filename
            log = logging.getLogger("ex")
            f.save(os.path.join(target,filename))
#            return os.path.join(target, filename)
        else:
            filename =uniquify(f.filename)
            f.save(os.path.join(target, filename))
        #check if file with same name
        defaultpic="defaultpic.jpg"
        print(filename, file=sys.stderr)

    return render_template('mosaic_parameters_template.html', filename=filename, defaultpic=defaultpic)

@app.route('/mosaic/uploader_url', methods=['GET', 'POST'])
def download_url_and_upload():
    if request.method == 'POST':
        url = request.form['url']

        head, tail = ntpath.split(url)
        local_filename = "/var/www/photomosaic/photomosaic/static/" + tail
        urllib.request.urlretrieve(url, local_filename)
        return render_template('mosaic_parameters_template.html', filename = tail)
    if request.method == 'GET':
        return 'get'
    return "not post"

@app.route('/rotate/<filename>', methods=['GET', 'POST'])
def rotate(filename):
    img = Image.open("/var/www/photomosaic/photomosaic/static/" + filename)
    img2 = img.rotate(90)
    img2.save("/var/www/photomosaic/photomosaic/static/rotated/" + filename)
    rotated = "/rotated/" + filename
    return render_template('template2.html', filename=rotated)

#possible bugs:
#what if multiple people upload the same file or make a new version of a previously uploaded photo?
    # add unique identifier to every upload, have people put in a title
#what if the parameters they upload are too big / etc
# have some directions / errors

#ways to make it better...
#different, more complicated templates


@app.route('/mosaic/<filename>/', methods=['GET', 'POST'])
def mosaic(filename):
    width = int(request.form['width'])
    height = int(request.form['height'])
    scale = int(request.form['scale'])
    print(width, height, scale, file=sys.stderr)
    photomosaic = Photomosaic("/var/www/photomosaic/photomosaic/static/" + filename, '/home/ben/Pictures/mosaicsourcephotos/')
    #if width, height, scale out of bounds, add form validation
    x = photomosaic.construct_mosaic(width, height, scale)

    data_to_string = str(width)

    x.save("/var/www/photomosaic/photomosaic/static/mosaics/" + "mosaic_"+ filename)

    print("saving to", "/var/www/photomosaic/photomosaic/static/mosaics/" + "mosaic_"+ filename, file=sys.stderr)
    #
    return render_template('show_final_template.html', filename='/mosaics/' + "mosaic_" + filename)

