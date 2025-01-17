#!/usr/bin/env python3
"""Module that handles all API authentications
"""
import sqlalchemy as sa
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from models import storage_t
from models.users import User
from app.api.views.errors import error_response

basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth()


@basic_auth.verify_password
def verify_password(username, password):
    user = storage_t.session.scalar(sa.select(User).where(User.username == username))
    if user and user.check_password(password):
        return user


@basic_auth.error_handler
def basic_auth_error(status):
    return error_response(status)


@token_auth.verify_token
def verify_token(token):
    return User.check_token(token) if token else None


@token_auth.error_handler
def token_auth_error(status):
    return error_response(status)
