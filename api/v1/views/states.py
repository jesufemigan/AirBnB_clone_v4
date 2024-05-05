#!/usr/bin/python3
""" a view for State objects that handle all Restful Actions"""

from models.state import State
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """ Retrieves the list of all State objects """
    state_all = storage.all(State).values()
    list_all = []
    for state in state_all:
        list_all.append(state.to_dict())
    return(jsonify(list_all))


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """ Retrieves a State object """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_state(state_id):
    """ Deletes an object of State """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return (make_response(jsonify({}), 200))


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def new_state():
    """ Creates a State"""
    input = request.get_json
    if not input:
        abort(404, 'Not a JSON')
    if 'name' not in input:
        abort(404, 'Missing name')
    instance = State(**input)
    instance.save()
    return (make_response(jsonify(instance.to_dict()), 201))


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update(state_id):
    """Updates a State object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if not request.get_json:
        abort(404, 'Not a JSON')
    ignore = ['id', 'created_at', 'updated_at']
    updated_data = request.json
    for k, v in updated_data.items():
        if k not in ignore:
            setattr(state, k, v)
    storage.save()
    return make_response(jsonify(state.to_dict()), 200)
