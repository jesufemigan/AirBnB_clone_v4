#!/usr/bin/python3

'''A flask web app'''
from flask import Flask
app = Flask(__name__)


@app.route('/', strict_slashes=False)
def index():
    '''definition for route /'''
    return "Hello, HBNB!"


@app.route('/hbnb', strict_slashes=False)
def home():
    '''definition for /hbnb'''
    return "HBNB"


if __name__ == "__main__":
    app.run(host='0.0.0.0')
