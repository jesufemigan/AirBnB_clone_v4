#!/usr/bin/python3
'''flask web app '''
from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.route('/cities_by_states', strict_slashes=False)
def cities_by_state():
    """definition for /cities_by_state"""
    states = storage.all(State)
    return render_template("8-cities_by_states.html", states=states)


@app.teardown_appcontext
def close_storage(exc):
    """Close file storage"""
    storage.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0')
