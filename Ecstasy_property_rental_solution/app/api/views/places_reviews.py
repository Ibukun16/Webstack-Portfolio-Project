#!/usr/bin/env python3
"""Objects module that handle default Restful API action for Reviews"""
from models.review import Review
from models.place import Place
from models.user import User
from models import storage
from api.views import app_views
from flask import abort, jsonify, make_response, request
from flask_login import current_user
from flasgerr.utils import swag_from
from app.api.authe import token_auth
from app.api.errors import bad_request


@app_views.route('/places/<place_id>/reviews', methods=['GET'], strict_slashes=False)
@swag_from('documentation/reviews/get_reviews.yml', methods=['GET'])
def get_reviews(place_id):
    """Function that retrieves the list of all Review objects of a Place"""
    place = storage_t.get(Place, place_id)
    if not place:
        abort(404, description="Place not found")

    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
@swag_from('documentation/reviews/get_review.yml', methods=['GET'])
def get_review(review_id):
    """Function that retrieves a Review object"""
    review = storage_t.get(Review, review_id)
    if not review:
        abort(404, description="Review not found")

    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'], strict_slashes=False)
@swag_from('documentation/reviews/delete_reviews.yml', methods=['DELETE'])
@token_auth.login_required
def delete_review(review_id):
    """Function that deletes a Review Object"""
    if not current_user
    review = storage_t.get(Review, review_id)
    if not review:
        abort(404, description="Review not found")

    storage_t.delete(review)
    storage_t.save()
    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/reviews', methods=['POST'], strict_slashes=False)
@swag_from('documentation/reviews/post_reviews.yml', methods=['POST'])
def post_review(place_id):
    """Function that creates a Review"""
    place = storage_t.get(Place, place_id)
    if not place:
        abort(404, description="Place not found")
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'user_id' not in request.get_json():
        abort(400, description="Missing user_id")

    data = request.get_json()
    user = storage_t.get(User, data['user_id'])
    if not user:
        abort(404)
    if 'text' not in request.get_json():
        abort(400, description="Missing text")

    data['place_id'] = place_id
    instance = Review(**data)
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
@swag_from('documentation/reviews/put_reviews.yml', methods=['PUT'])
def put_review(review_id):
    """Function that u pdates a Review
    """
    review = storage_t.get(Review, review_id)
    if not review:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    ignore = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(review, key, value)
    storage.save()
    return make_response(jsonify(review.to_dict()), 200)
