#!/usr/bin/env python3
"""Module that handle all default Restful API actions for States
"""
from models.state import State
from models import storage_t
from api.views import app_views
from flask import abort, jsonify, make_response, request
from flask_login import current_user, login_required
from flasgger.utils import swag_from
from app.api.views.auth import token_auth
from app.api.views.errors import bad_request


@app_views.route('/states', methods=['GET'], strict_slashes=False)
@swag_from('documentation/state/get_state.yml', methods=['GET'])
def get_states():
    """Function that retrieves the list of all State objects    """
    all_states = storage_t.all(State).values()
    list_states = []
    for state in all_states:
        list_states.append(state.to_dict())
    return jsonify(list_states)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
@swag_from('documentation/state/get_id_state.yml', methods=['get'])
def get_state(state_id):
    """Function that retrieves a specific State"""
    state = storage_t.get(State, state_id)
    if not state:
        abort(404, description="State not found")

    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
@swag_from('documentation/state/delete_state.yml', methods=['DELETE'])
@token_auth.login_required
def delete_state(state_id):
    """Function that deletes a State Object"""
    state = storage_t.get(State, state_id)
    if not current_user.is_admin:
        abort(403, description="Access denied: Admin only!")

    if not state:
        abort(404)

    storage_t.delete(state)
    storage_t.save()

    return make_response(jsonify({}), 200)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
@swag_from('documentation/state/post_state.yml', methods=['POST'])
@token_auth.login_required
def post_state():
    """Function that creates a new State"""
    if not current_user.is_admin:
        abort(403, description="Access denied: Admin only!")
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'name' not in request.get_json():
        abort(400, description="Missing name")
    if storage_t.session.scalar(sa.select(state).where(
            name == data['name'])):
        return bad_request('State already exists')

    data = request.get_json()
    instance = State(**data)
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
@swag_from('documentation/state/put_state.yml', methods=['PUT'])
@token_auth.login_required
def put_state(state_id):
    """Function that updates a State parameters"""
    state = storage_t.get(State, state_id)
    if not state:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    ignore = ['id', 'created_at', 'updated_at']

    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(state, key, value)
    storage_t.save()
    return make_response(jsonify(state.to_dict()), 200)
