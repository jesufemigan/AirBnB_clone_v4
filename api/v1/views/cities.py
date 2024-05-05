#!/usr/bin/python3
"""objects that handle RESTFUL actions for Cities"""

from models.city import City
from models.state import State
from flask import abort, jsonify, make_response, request
from api.v1.views import app_views
from models import storage


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def all_cities(state_id):
    """ Retrieves the list of all City objects of a State"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    list_cities = []
    for city in state.cities:
        list_cities.append(city.to_dict())
    return jsonify(list_cities)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """ Gets a City object """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def del_city(city_id):
    """ Deletes a City object """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def add_city(state_id):
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if not request.get_json():
        abort(404, 'Not a JSON')
    if 'name' not in request.get_json():
        abort(404, 'Missing name')
    input = request.get_json()
    ins = City(**input)
    ins.state_id = state.id
    ins.save()
    return make_response(jsonify(ins.to_dict(), 201))


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if not request.get_json():
        abort(404, 'Not a JSON')
    input = request.get_json()
    ignore = ['id', 'state_id', 'created_at', 'updated_at']
    for k, v in input.items():
        if k not in ignore:
            setattr(city, k, v)
    storage.save()
    return make_response(jsonify(city.to_dict()), 200)
