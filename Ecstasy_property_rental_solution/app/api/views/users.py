#!/usr/bin/env python3
"""Module that handles all default RestFul API actions for Users
"""
import sqlalchemy as sa
from models.user import User
from models import storage_t
from api.views import app_views
from api.views.authe import token_auth
from api.views.errors import bad_request
from flask import abort, jsonify, make_response, request, url_for
from flask_login import current_user
from flask_login import login_required
from flasgger.utils import swag_from


@app_views.route('/users', methods=['GET'], strict_slashes=False)
@swag_from('documentation/user/all_users.yml')
@token_auth.login_required
def get_users():
    """Function that retrieves the list of all user objects or a specific user"""
    all_users = storage_t.all(User).values()
    list_users = []
    for user in all_users:
        list_users.append(user.to_dict())
    return jsonify(list_users)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
@swag_from('documentation/user/get_user.yml', methods=['GET'])
@token_auth.login_required
def get_user(user_id):
    """Function that retrieves a user"""
    user = storage_t.get(User, user_id)
    if not user:
        abort(404, description="User not found")
    return jsonify(user.to_dict())

@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
@swag_from('documentation/user/delete_user.yml', methods=['DELETE'])
@token_auth.login_required
def delete_user(user_id):
    """Function that permanently remove a user from the app"""
    current_user = token_auth.current_user()
    if current_user().id != user_id and not current_user.is_admin:
        abort(403, description="You do not have permission to delete this user")
    user = storage_t.get(User, user_id)
    if not user:
        abort(404, description="User not found")

    storage.delete(user)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
@swag_from('documenttation/user/post_user.yml', methods=['POST'])
def post_user():
    """Function that creates a user"""
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")

    required = ['username', 'email', 'password']
    missing = [field for field in required if field not in data]
    if missing:
        abort(400, description=f"Please provide required field: {', '.join(missing)}")
    if storage_t.session.scalar(sa.select(User).where(
            User.username == data['username'])):
        return bad_request('Username already used, please choose a different username')
    if storage_t.session.scalar(sa.select(User).where(
            User.email == data['email'])):
        return bad_request('Email already used, please provide
                           a different email address')

    instance = User(**data)
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
@swag_from('documenttation/user/put_user.yml', methods=['PUT'])
@token_auth.login_required
def update_user(user_id):
    """Function that updates a user"""
    if token_auth.current_user().id != user_id:
        abort(403, description='You do not have permission to update user')
    user = storage_t.get(User, user_id)
    if not user:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    ignore = ['id', 'email', 'created_at', 'updated_at']

    data = request.get_json()
    for key, val in data.items():
        if key not in ignore:
            settattr(user, key, val)
        storage_t.save()
        return make_response(jsonify(user.to_dict()), 200)
