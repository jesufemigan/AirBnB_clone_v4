#!/usr/bin/python3

'''a flask web app'''

from flask import Flask, render_template
from models import storage
from models.amenity import Amenity
from models.state import State
from models.place import Place
import uuid


app = Flask(__name__)


@app.route('/4-hbnb', strict_slashes=False)
def hbnb():
    '''route for /hbnb'''
    states = storage.all(State)
    amenities = storage.all(Amenity)
    places = storage.all(Place)

    return render_template("4-hbnb.html", states=states,
                           amenities=amenities, places=places,
                           cache_id=uuid.uuid4())


@app.teardown_appcontext
def close_db(exc):
    '''close db'''
    storage.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0')
