from flask import Flask

app = Flask(__name__, static_url_path='')

from app import routes

if __name__=="__main__":
    app.run()