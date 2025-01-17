#!/usr/bin/env python3
"""Objects module that handle all default RestFul API actions for City - Property"""
from models.city import City
from models.property import Property_Type
from models import storage_t
from api.views import app_views
from os import environ
from flask import abort, jsonify, make_response, request
from flask_login import current_user
from flasgger.utils import swag_from
from app.api.views.authe import token_auth
from app.api.views.errors import bad_request


@app_views.route('cities/<city_id>/properties', methods=['GET'], strict_slashes=False)
@swag_from('documentation/city_property/get_cities_properties.yml', methods=['GET'])
def get_city_properties(city_id):
    """Function that retrieves the list of all Property objects of a City"""
    city = storage_t.get(City, city_id)
    if not city:
        abort(404)

    if environ.get('ECSTASY_STORAGE') == "db":
        properties = [propty.to_dict() for propty in city.properties]
    else:
        properties = [storage_t.get(Property_Type, property_id).to_dict()
                     for property_id in city.property_ids]

    return jsonify(properties)


@app_views.route('/cities/<city_id>/properties/<property_id>',
                 methods=['DELETE'], strict_slashes=False)
@swag_from('documentation/city_property/delete_city_prperties.yml',
           methods=['DELETE'])
@token_auth.login_required
def delete_city_property(city_id, property_id):
    """Function that deletes a property object of a City"""
    if not current_user.is_admin:
        abort(403, description="You do not have permission to delete property")
    city = storage_t.get(City, city_id)
    if not city:
        abort(404, description="City not found"))

    propty = storage_t.get(Property_Type, property_id)
    if not propty:
        abort(404, description="Property not found"))

    if environ.get('ECSTASY_STORAGE') == "db":
        if propty not in city.properties:
            abort(404, description="Property not found")
        city.properties.remove(propty)
    else:
        if property_id not in city.property_ids:
            abort(404, description="Property not found")
        city.property_ids.remove(property_id)

    storage_t.save()
    return make_response(jsonify({}), 200)


@app_views.route('/cities/<city_id>/properties/<property_id>', methods=['POST'],
                 strict_slashes=False)
@swag_from('documentation/city_property/post_place_properties.yml',
           methods=['POST'])
@token_auth.login_required
def post_city_property(city_id, property_id):
    """Function that link a Property object to a City
    """
    city = storage_t.get(City, city_id)
    if not city:
        abort(404, description="Property not found"))

    propty = storage_t.get(Property_Type, property_id)
    if not propty:
        abort(404, description="Property not found")

    if environ.get('ECSTASY_STORAGE') == "db":
        if propty in city.properties:
            return make_response(jsonify(propty.to_dict()), 200)
        else:
            city.properties.append(propty)
    else:
        if property_id in city.property_ids:
            return make_response(jsonify(propty.to_dict()), 200)
        else:
            city.property_ids.append(property_id)

    storage_t.save()
    return make_response(jsonify(propty.to_dict()), 201)
