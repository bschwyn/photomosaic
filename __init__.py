import sys
from flask import Flask
app = Flask(__name__)
from photomosaic import routes
#@app.route('/')
#def hello():
#    return sys.version

if __name__=="__main__":
    app.run()
