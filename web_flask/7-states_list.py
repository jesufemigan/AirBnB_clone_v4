#!/usr/bin/python3
'''a flask web app that lists all states'''

from flask import Flask, render_template
from models import storage
from models.state import State


app = Flask(__name__)


@app.route('/states_list', strict_slashes=False)
def state_list():
    '''definition for /states_list'''
    states = storage.all(State)
    return render_template("7-states_list.html", states=states)


@app.teardown_appcontext
def close_sql(exc):
    """close file storage"""
    storage.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0')
