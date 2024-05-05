#!/usr/bin/python3
""" Create a new view for User object that handles
all default RESTFul API actions
"""
from models.user import User
from models import storage
from flask import abort, jsonify, make_response, request
from api.v1.views import app_views


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """ Retrieves the list of all User objects"""
    users = storage.all(User).values()
    list = []
    for u in users:
        list.append(u.to_dict())
    return jsonify(list)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """ Retrieves a User object """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def del_user(user_id):
    """ Deletes a User objecs """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def post_user():
    """ Creates a User """
    if not request.get_json():
        abort(404, 'Not a JSON')
    if 'email' not in request.get_json():
        abort(404, 'Missing email')
    if 'password' not in request.get_json():
        abort(404, 'Missing password')
    input = request.get_json()
    ins = User(**input)
    ins.save()
    return make_response(jsonify(ins.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def put_user(user_id):
    """ Updates a User object """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    if not request.get_json():
        abort(404, 'Not a JSON')
    ignore = ['id', 'email', 'created_at', 'updated_at']
    input = request.get_json()
    for k, v in input.items():
        if k not in ignore:
            setattr(user, k, v)
    storage.save()
    return make_response(jsonify(user.to_dict()), 200)
