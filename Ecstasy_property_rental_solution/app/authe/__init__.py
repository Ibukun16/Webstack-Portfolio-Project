#!/usr/bin/env python3
"""Module that initializes the authentication package
"""
from flask import Blueprint

app_views = Blueprint('auth', __name__)

from app.authe import access, forms
