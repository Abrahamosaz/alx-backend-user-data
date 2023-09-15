#!/usr/bin/env python3
"""
module that handle all routes for session authentication
"""
from flask import jsonify, abort
from api.v1.views import app_views, request
from models.user import User


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login_user() -> str:
    """
    creating a logging functionality that uses the session object of the
    server to login the user
    """
    email = request.form.get("email")
    password = request.form.get("password")

    if not email or email  == "":
        return jsonify({"error": "email missing"}), 400
    if not password or  password == "":
        return jsonify({ "error": "password missing" }), 400
    
    users = User.search({"email": email})
    if len(users) == 0:
        return jsonify({ "error": "no user found for this email" }), 404
    for user in users:
        if user.is_valid_password(password):
            from api.v1.app import auth
            import os
            session_id = auth.create_session(user.id)
            response = jsonify(user.to_json())
            cookie_value = os.getenv("SESSION_NAME")
            response.set_cookie(cookie_value,  session_id)
            return response
        else:
            return jsonify({ "error": "wrong password" }), 401
        

@app_views.route('/auth_session/logout', methods=['DELETE'], strict_slashes=False)
def logout_user():
    """
    logout a user authenticated with session id
    """
    print("got here")
    from api.v1.app import auth
    if auth.destroy_session(request) is False:
        abort(404)
    return jsonify({}), 200

    



    
    



