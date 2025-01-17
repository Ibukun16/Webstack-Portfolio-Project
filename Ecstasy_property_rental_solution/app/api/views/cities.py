#!/usr/bin/env python3
"""Objects Module that handles all the default Restful API for cities"""
from models.city import City
from models.state import State
from models import storage_t
from api.views import app_views
from flask import abort, jsonify, make_response, request
from flask_login import current_user
from flasgger.utils import swag_from
from app.api.views.authe import token_auth
from app.api.views.errors import bad_request


@app_views.route('/states/<state_id>/cities', methods=['GET'], strict_slashes=False)
@swag_from('documentation/city/cities_by_state.yml', methods=['GET'])
def get_cities(state_id):
    """Function that retrieves the list of all cities object
    of a specific state, or a specific city
    """
    list_cities = []
    state = storage_t.get(State, state_id)
    if not state:
        abort(404, description="State not found")
    for city in state.cities:
        list_cities.append(city.to_dict())

    return jsonify(list_cities)


@app_views.route('/cities/<city_id>/', methods=['GET'], strict_slashes=False)
@swag_from('documentation/city/get_city.yml', methods=['GET'])
def get_city(city_id):
    """Function that retrieves a specific city based on id"""
    city = storage_t.get(City, city_id)
    if not city:
        abort(404, description="City not found"))
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
@swag_from('documentation/city/delete_city.yml', methods=['DELETE'])
@token_auth.login_required
def delete_city(city_id):
    """Functioin that delete city based on the provided id"""
    if not current_user.is_admin:
        abort(403, description="Access forbidden: Admin only!")
    city = storage_t.get(City, city_id)
    if not city:
        abort(404, description="City not found")

    storage.delete(city)
    storage.save()


    return make_response(jsonify({}), 200)


@app_views.route('/states/<state_id>/cities', methods=['POST'], strict_slashes=False)
@swag_from('documentation/city/post_city.yml', methods=['POST'])
@token_auth.login_required
def post_city(state_id):
    """Function that creates a City instance"""
    if not current_user.is_admin:
        abort(403, description="Access forbidden: Admin only!")
    state = storage_t.get(State, state_id)
    if not state:
        abort(404, description="City not found")
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'name' not in request.get_json():
        abort(400, description="Missing name")

    data = request.get_json()
    instance = City(**data)
    instance.state_id = state.id
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
@swag_from('documentation/city/put_city.yml', methods=['PUT'])
@token_auth.login_required
def put_city(city_id):
    """Function that updates City instance"""
     if not current_user.is_admin:
        abort(403, description="Access forbidden: Admin only!")
    city = storage_t.get(City, city_id)
    if not city:
         abort(404, description="City not found")
    if not request.get_json():
        abort(400, description="Not a JSON")

    ignore = ['id', 'state_id', 'created_at', 'updated_at']
    data = request.get_json()
    for key, val in data.items():
        if key not in ignore:
            setattr(city, key, val)
    storage_t.save()
    return make_response(jsonify(city.to_dict()), 200)
