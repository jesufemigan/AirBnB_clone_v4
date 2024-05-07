#!/usr/bin/python3
""" Create a new view for Place object that handles
all default RESTFul API actions"""
from models.place import Place
from models.user import User
from models.city import City
from models.amenity import Amenity
from models.state import State
from models import storage
from flask import abort, jsonify, make_response, request
from api.v1.views import app_views
# from api.v1.views.amenities import amenities
# from api.v1.views.places_amenities import place_amenities
import requests
import json
from os import getenv



@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places(city_id):
    """ Retrieves the list of all Places objects of a City"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = city.places
    list = []
    for place in places:
        list.append(place.to_dict())
    return jsonify(list)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """ Retrieves a Places object """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_place(place_id):
    """ Deletes Place objecs """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def post_place(city_id):
    """ Creates a Place """
    city = storage.get(City, city_id)
    input = request.get_json()
    if city is None:
        abort(404)
    if not input:
        abort(404, 'Not a JSON')
    if 'user_id' not in input:
        abort(404, 'Missing user_id')
    user_id = input.user_id
    if 'name' not in input:
        abort(404, 'Missing name')
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    ins = Place(**input)
    ins.city_id = city_id
    ins.save()
    return make_response(jsonify(ins.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def put_place(place_id):
    """ Updates a Place object """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if not request.get_json():
        abort(404, 'Not a JSON')
    ignore = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    input = request.get_json()
    for k, v in input.items():
        if k not in ignore:
            setattr(place, k, v)
    storage.save()
    return make_response(jsonify(place.to_dict()), 200)


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def places_search():
    """
    retrieves all Place objects depending
    of the JSON in the body of the request
    """
    req = request.get_json()
    if req is None:
        abort(400, "Not a JSON")

    req = request.get_json()
    if req is None or (
        req.get('states') is None and
        req.get('cities') is None and
        req.get('amenities') is None
    ):
        obj_places = storage.all(Place)
        return jsonify([obj.to_dict() for obj in obj_places.values()])

    places = []

    if req.get('states'):
        obj_states = []
        for ids in req.get('states'):
            obj_states.append(storage.get(State, ids))

        for obj_state in obj_states:
            for obj_city in obj_state.cities:
                for obj_place in obj_city.places:
                    places.append(obj_place)

    if req.get('cities'):
        obj_cities = []
        for ids in req.get('cities'):
            obj_cities.append(storage.get(City, ids))

        for obj_city in obj_cities:
            for obj_place in obj_city.places:
                if obj_place not in places:
                    places.append(obj_place)

    if not places:
        places = storage.all(Place)
        places = [place for place in places.values()]

    if req.get('amenities'):
        obj_am = [storage.get(Amenity, id) for id in req.get('amenities')]
        i = 0
        limit = len(places)
        HBNB_API_HOST = getenv('HBNB_API_HOST')
        HBNB_API_PORT = getenv('HBNB_API_PORT')

        port = 5000 if not HBNB_API_PORT else HBNB_API_PORT
        first_url = "http://0.0.0.0:{}/api/v1/places/".format(port)
        while i < limit:
            place = places[i]
            url = first_url + '{}/amenities'
            req = url.format(place.id)
            response = requests.get(req)
            place_am = json.loads(response.text)
            amenities = [storage.get(Amenity, obj['id']) for obj in place_am]
            for amenity in obj_am:
                if amenity not in amenities:
                    places.pop(i)
                    i -= 1
                    limit -= 1
                    break
            i += 1

    return jsonify([obj.to_dict() for obj in places])
