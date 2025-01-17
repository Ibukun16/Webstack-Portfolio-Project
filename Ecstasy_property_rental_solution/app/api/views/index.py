#!/usr/bin/env python3
"""Module that handles the index to functions
"""
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.property import Property_Type
from models.review import Review
from models.state import State
from models.user import User
from models import storage
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """ Function that manage the status of API """
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def number_objects():
    """ Function that retrieves the number of each object by the type"""
    classes = [Amenity, City, Place, Property_Type, Review, State, User]
    names = ["Amenities", "Cities", "Places", "Property_Type", "Reviews", "States", "Users"]

    num_objs = {}
    for i in range(len(classes)):
        num_objs[names[i]] = storage.count(classes[i])

    return jsonify(num_objs)
