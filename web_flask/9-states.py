#!/usr/bin/python3
'''flask web app '''
from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.route('/states', strict_slashes=False)
def cities_by_state():
    """definition for /cities_by_state"""
    states = storage.all(State)
    return render_template("7-states_list.html", states=states)


@app.route('/states/<string:id>', strict_slashes=False)
def states(id):
    """defintion for /states/id"""
    all_states = storage.all(State)
    full_id = 'State.' + id
    for id, state in all_states.items():
        if id == full_id:
            return render_template("9-states.html", state=state)
    return render_template("9-states.html")


@app.teardown_appcontext
def close_storage(exc):
    """Close file storage"""
    storage.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0')
