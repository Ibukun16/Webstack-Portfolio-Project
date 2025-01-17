#!/usr/bin/env python3
"""Object module that handles all default Restful API actions for Properties"""
from models.property import Property_Type
from models import storage
from api.views import app_views
from flask import abort, jsonify, make_response, request
from flask_login import current_user
from app.api.authe import token_auth
from app.api.errors import bad_request
from flasgger.utils import swag_from


@app_views.route('/properties', method=['GET'], strict_slashes=False)
@swag_from('documentation/property_type/all_properties.yml')
def get_properties():
    """Function that retrieves list of all types of properties available"""
    all_properties = storage.all(Property_Type).values()
    list_properties = []
    for propty in all_properties:
        list_properties.append(propty.to_dict())
    return jsonify(list_properties)


@app_views.route('/properties/<property_id>/', methods=['GET'])
@swag_from('/documentation/property_type/get_properties.yml', methods=['GET'])
def get_property(property_id):
    """Function that retrieves an details about a property"""
    propty = storage_t.get(Property_Type, property_id)
    if not propty:
        abort(404, description="Property type not found")

    return jsonify(propty.to_dict())


@app_views.route('/properties/property_id/', methods=['DELETE'],
                 strict_slashes=False)
@swag_from('documentation/property_type/delete_property.yml', methods=['DELETE'])
@token_auth.login_required
def delete_property(property_id):
    """Function that deletes a property object"""
    propty = storage_t.get(Property_Type, property_id)
    if not current_user.is_admin:
        abort(403, description="Access forbidden: Admin only!")

    if not propty:
        abort(404, description="Property not found")

    storage_t.delete(propty)
    storage_t.save()

    return make_response(jsonify({}), 200)


@app_views.route('/properties', methods=['POST'], strict_slashes=False)
@swag_from('documentation/property_type/post_property.yml', methods=['POST'])
@token_auth.login_required
def post_property():
    """Function that creates a property"""
    if not request.get_json():
        abort(400, description="Not a JSON")

    if 'name' not in request.get_json():
        abort(400, description="Missing name")

    data = request.get_json()
    instance = Property_Type(**data)
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('/properties/<property_id>', methods=['PUT'],
                 strict_slashes=False)
@swag_from('documentation/property_type/put_property.yml', methods=['PUT'])
@token_auth.login_required
def put_property(property_id):
    """Updates property"""
    if not current_user.is_admin:
        abort(403, description="Access forbidden: Admin only!")
    if not request.get_json():
        abort(400, description="Not a JSON")

    ignore = ['id', 'created_at', 'updated_at']

    propty = storage_t.get(Property_Type, property_id)

    if not propty:
        abort(404, description="Property not found")

    data = request.get_json()
    for key, val in data.items():
        if key not in ignore:
            setattr(propty, key, val)
    storage_t.save()
    return make_response(jsonify(propty.to_dict()), 200)
