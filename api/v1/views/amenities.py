#!/usr/bin/python3
"""
route for handling Amenity objects and operations
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models.amenity import Amenity
from models import storage


@app_views.route("/amenities", strict_slashes=False)
def amenity_get_all():
    """
    retrieves all Amenity objects
    """
    amenity_list = []
    for key, value in storage.all(Amenity).items():
        amenity_list.append(value.to_dict())
    return jsonify(amenity_list)


@app_views.route("/amenities/<amenity_id>", strict_slashes=False)
def amenity_by_id(amenity_id):
    """
    gets a specific Amenity
    """

    amenity = storage.get(Amenity, amenity_id)

    if amenity:
        return jsonify(amenity.to_dict())
    else:
        abort(404)


@app_views.route("/amenities/<amenity_id>",
                 methods=["DELETE"],
                 strict_slashes=False)
def amenity_delete_by_id(amenity_id):
    """
    deletes Amenity by id
    """

    amenity = storage.get(Amenity, amenity_id)

    if amenity:
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route("/amenities",
                 methods=["POST"],
                 strict_slashes=False)
def amenity_create():
    """
    create amenity route
    """

    if request.content_type() != 'application/json':
        return abort(400, 'Not a JSON')
    if not request.get_json():
        return abort(400, 'Not a JSON')
    data = request.get_json()

    if "name" not in data:
        return abort(400, 'Missing name')

    amenity = Amenity(**data)
    amenity.save()

    return jsonify(amenity.to_dict()), 201


@app_views.route("/amenities/<amenity_id>",  methods=["PUT"],
                 strict_slashes=False)
def amenity_put(amenity_id):
    """
    updates specific Amenity object by ID
    """
    if request.content_type() != 'application/json':
        return abort(400, 'Not a JSON')
    if not request.get_json():
        return abort(400, 'Not a JSON')
    data = request.get_json()

    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        ignore_keys = ["id", "created_at", "updated_at"]
        for key, val in data.items():
            if key not in ignore_keys:
                setattr(amenity, key, val)
            amenity.save()
            return jsonify(amenity.to_dict()), 200
    else:
        return abort(404)
