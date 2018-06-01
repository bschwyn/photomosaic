#import app
#from photomosaic import app
from photomosaic import app

@app.route('/')
def hello():
    return "hello this is a route"
