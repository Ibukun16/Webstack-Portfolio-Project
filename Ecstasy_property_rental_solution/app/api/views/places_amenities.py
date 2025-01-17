#!/usr/bin/env python3
"""objects that handle all default RestFul API actions for Place - Amenity """
from models.place import Place
from models.amenity import Amenity
from models import storage
from api.views import app_views
from os import environ
from flask import abort, jsonify, make_response, request
from flask_login import current_user
from flasgger.utils import swag_from
from app.api.views.authe import token_auth
from app.api.views.errors import bad_request


@app_views.route('places/<place_id>/amenities', methods=['GET'], strict_slashes=False)
@swag_from('documentation/place_amenity/get_places_amenities.yml', methods=['GET'])
def get_place_amenities(place_id):
    """Function that retrieves the list of all Amenity objects of a Place
    """
    place = storage_t.get(Place, place_id)
    if not place:
        abort(404, description="Place not found")

    if environ.get('ECSTASY_STORAGE') == "db":
        amenities = [amenity.to_dict() for amenity in place.amenities]
    else:
        amenities = [storage.get(Amenity, amenity_id).to_dict()
                     for amenity_id in place.amenity_ids]

    return jsonify(amenities)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
@swag_from('documentation/place_amenity/delete_place_amenities.yml',
           methods=['DELETE'])
@token_auth.login_required
def delete_place_amenity(place_id, amenity_id):
    """Function that deletes an Amenity object of a Place"""
    if not current_user.is_admin:
        abort(403, description="Access forbidden: Admin only")

    place = storage_t.get(Place, place_id)
    if not place:
        abort(404, description="Place not found")

    amenity = storage_t.get(Amenity, amenity_id)
    if not amenity:
        abort(404, description="Place not found"))

    if environ.get('ECSTASY_STORAGE') == "db":
        if amenity not in place.amenities:
            abort(404, description="Amenities not found")
        place.amenities.remove(amenity)
    else:
        if amenity_id not in place.amenity_ids:
            abort(404)
        place.amenity_ids.remove(amenity_id)

    storage_t.save()
    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['POST'],
                 strict_slashes=False)
@swag_from('documentation/place_amenity/post_place_amenities.yml',
           methods=['POST'])
@token_auth.login_required
def post_place_amenity(place_id, amenity_id):
    """Function that link an Amenity object to a Place"""
    place = storage_t.get(Place, place_id)
    if not place:
        abort(404, description="Place not found")

    amenity = storage_t.get(Amenity, amenity_id)
    if not amenity:
        abort(404, description="Amenity not found")

    if environ.get('ECSTASY_STORAGE') == "db":
        if amenity in place.amenities:
            return make_response(jsonify(amenity.to_dict()), 200)
        else:
            place.amenities.append(amenity)
    else:
        if amenity_id in place.amenity_ids:
            return make_response(jsonify(amenity.to_dict()), 200)
        else:
            place.amenity_ids.append(amenity_id)

    storage_t.save()
    return make_response(jsonify(amenity.to_dict()), 201)
