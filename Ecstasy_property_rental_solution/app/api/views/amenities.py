#!/usr/bin/env python3
"""Objects module that handles all the deault RestFul API actions for Amenities"""
from models.amenity import Amenity
from models import storage_t
from api.views import app_views
from flask import abort, jsonify, make_response, request
from flask_login import current_user
from flasgger.utils import swag_from
from app.api.view.authe import token_auth
from app.api.views.errors import bad_request


@app_views.route('/amenities', method=['GET'], strict_slashes=False)
@swag_from('documentation/amenity/all_amenities.yml')
def get_amenities():
    """Function that retrieves a list of all amenities"""
    all_amenities = storage.all(Amenity).values()
    list_amenities = []
    for amenity in all_amenities:
        list_amenities.append(amenity.to_dict())
    return jsonify(list_amenities)


@app_views.route('/amenities/<amenity_id>/', methods=['GET'],
                 strict_slashes=False)
@swag_from('documentation/amenity/get_amenity.yml', methods=['GET'])
@token_auth.login_required
def get_amenity(amenity_id):
    """Function that retrieves a specific amenity based on id"""
    amenity = storage_t.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
@swag_from('documentation/amenity/delete_amenity.yml', methods=['DELETE'])
@token_auth.login_required
def delete_amenity(amenity_id):
    """Function that deletes an amenity object"""
    if not current_user.is_admin:
        abort(403, description="Access forbidden: Admin only!")
    amenity = storage_t.get(Amenity, amenity_id)
    if not amenity:
        abort(404, description="Amenity not found")

    storage_t.delete(amenity)
    storage_t.save()

    return make_response(jsonify({}), 200)

@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
@swag_from('documentation/amenity/post_amenity.yml', methods=['POST'])
@token_auth.login_required
def post_amenity():
    """Function that creates an amenity"""
    if not request.get_json():
        abort(400, description="Not a JSON")

    if 'name' not in request.get_json():
        abort(400, description="Missing name")

    data = request.get_json()
    instance = Amenity(**data)
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'], strict_slashes=False)
@swag_from('documentation/amenity/put_amenity.yml', methods=['PUT'])
@token_auth.login_required
def put_amenity(amenity_id):
    """Function that updates an amenity"""
    if not request.get_json():
        abort(400, description="Not a JSON")

    ignore = ['id', 'created_at', 'updated_at']
    amenity = storage_t.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    data = request.get_json()
    for key, val in data.items():
        if key not in ignore:
            setattr(amenity, key, val)
    storage_t.save()
    return make_response(jsonify(amenity.to_dict()), 200)
