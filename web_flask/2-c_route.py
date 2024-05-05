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


@app.route('/c/<string:text>', strict_slashes=False)
def c_route(text):
    '''defintion for /c/<text>'''
    text = text.replace('_', ' ')
    return f"C {text}"


if __name__ == "__main__":
    app.run(host='0.0.0.0')
