#!/usr/bin/python3
"""
route for handling User objects and operations
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models.user import User
from models import storage


@app_views.route("/users", strict_slashes=False)
def user_get_all():
    """
    retrieves all User objects
    """
    users = storage.all(User)
    return jsonify(user.to_dict() for user in users)


@app_views.route("/users/<user_id>", strict_slashes=False)
def user_by_id(user_id):
    """
    gets a specific User object by ID
    """

    user = storage.get(User,user_id)

    if user:
        return jsonify(user.to_dict())
    else:
        return abort(404)


@app_views.route("/users/<user_id>",
                 methods=["DELETE"],
                 strict_slashes=False)
def user_delete_by_id(user_id):
    """
    deletes User by id
    """

    user = storage.get(User, user_id)

    if user:
        storage.delete(user)
        storage.save()
    else:
        return abort(404)


@app_views.route("/users",
                 methods=["POST"],
                 strict_slashes=False)
def user_create():
    """
    create user route
    """
    if request.content_type != 'application/json':
        return abort(400, 'Not a JSON')
    if not request.get_json():
        return abort(400, 'Not a JSON')
    data = request.get_json()

    if "email" not in data:
        return abort(400, 'Missing email')
    if "password" not in data:
        return abort(400, 'Missing password')

    user = User(**data)
    user.save()

    return jsonify(user.to_dict()), 201


@app_views.route("/users/<user_id>",
                 methods=["PUT"],
                 strict_slashes=False)
def user_put(user_id):
    """
    updates specific User object by ID
    """
    user = storage.get(User, user_id)
    if user:
        if request.content_type != 'application/json':
            return abort(400, 'Not a JSON')
        if not request.get_json():
            return abort(400, 'Not a JSON')
        data = request.get_json()
        ignore_keys = ["id", "created_at", "updated_at", "email"]

        for key, val in data.items():
            if key not in ignore_keys:
                setattr(user, key, val)

        user.save()
        return jsonify(user.to_dict()), 200
    else:
        return abort(404)

