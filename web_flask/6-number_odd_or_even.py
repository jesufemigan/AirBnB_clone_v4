#!/usr/bin/python3

'''A flask web app'''
from flask import Flask, render_template
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


@app.route('/python/', strict_slashes=False, defaults={'text':
           'is cool'})
@app.route('/python/<string:text>', strict_slashes=False)
def python_route(text):
    '''definition for /python/<text>'''
    text = text.replace('_', ' ')
    return f"Python {text}"


@app.route('/number/<int:n>', strict_slashes=False)
def number_route(n):
    '''definiton for /number/<n>'''
    if type(n) is int:
        return f"{n} is a number"


@app.route('/number_template/<int:n>', strict_slashes=False)
def number_template(n):
    '''definition for /number_template/n'''
    if type(n) is int:
        return render_template("5-number.html", data={'n': n})


@app.route('/number_odd_or_even/<int:n>', strict_slashes=False)
def number_odd_or_even(n):
    '''definition for /number_odd_or_even/n'''
    if type(n) is int:
        if n % 2 == 0:
            result = f"{n} is even"
        else:
            result = f"{n} is odd"
        return render_template("6-number_odd_or_even.html",
                               data={'result': result})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
