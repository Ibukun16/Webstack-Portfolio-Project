#!/usr/bin/env python3
""" Blueprint for the app API """
from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api')

from api.views import amenities, authe, index, cities, cities_properties, \
        places, places_amenities, places_reviews, properties, users, errors, tokens
