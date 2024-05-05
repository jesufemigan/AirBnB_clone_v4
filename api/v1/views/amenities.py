#!/usr/bin/python3
""" Creates view for Amenity objects that handle all RESTFUL API functions"""
from models.amenity import Amenity
from models import storage
from flask import jsonify, abort, make_response, request
from api.v1.views import app_views


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenites():
    """ Retrieves all amenity objects """
    amenities = storage.all(Amenity).values()
    list = []
    for amenity in amenities:
        list.append(amenity.to_dict())
    return jsonify(list)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """ Retrieves an A menity object"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_amenity(amenity_id):
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/amenities', methods=['POST'],
                 strict_slashes=False)
def post_amenity():
    """ Creates a Amenity  """
    if not request.get_json():
        abort(404, 'Not a JSON')
    if 'name' not in request.get_json():
        abort(404, 'Missing name')
    input = request.get_json()
    ins = Amenity(**input)
    ins.save()
    return make_response(jsonify(ins.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def put_amenity(amenity_id):
    """ Updates Amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if not request.get_json():
        abort(404, 'Not a JSON')
    if 'name' not in request.get_json():
        abort(404, 'Missing name')
    ignore = ['id', 'created_at', 'update_at']
    input = request.get_json()
    for k, v in input.items():
        if k not in ignore:
            setattr(amenity, k, v)
    storage.save()
    return make_response(jsonify(amenity.to_dict()), 200)
