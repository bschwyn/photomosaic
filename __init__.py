import sys
import logging
from flask import Flask
app = Flask(__name__)
from photomosaic import routes
#@app.route('/')
#def hello():
#    log = logging.getLogger("ex")
#    try:
#        import bladlfkjadslkjf
#    except Exeption as e:
#        log.exception(e)
#    return "hello the try thing happened"

if __name__=="__main__":
    app.run()
