# Author: Alex Xu
# Description: Administration and authentication APIs of cloud server.

import os
from tempfile import mkdtemp
import time
from flask import Blueprint, make_response, request, session, jsonify
import db.admin, db.model
from utils.utils import APIParser, APIParseError, get_sign

admin = Blueprint("admin", __name__)

session_parser = APIParser()
session_parser.add_prop(name="username", dtype=str)
session_parser.add_prop(name="password", dtype=str)

@admin.route("/session", methods=["POST"])
def session_post():
    try:
        data = session_parser.parse(request.data)
        username = data["username"]
        password = data["password"]
        if (db.admin.check(username=username, password=password)):
            session["user"] = username
            return make_response("", 200)
        else:
            resp_body = {
                "error": "Login failed",
            }
            resp_body = jsonify(resp_body)
            return make_response(resp_body, 401)
    except APIParseError:
        resp_body = {
            "error": "Invalid API request",
        }
        resp_body = jsonify(resp_body)
        return make_response(resp_body, 400)

@admin.route("/session", methods=["DELETE"])
def session_delete():
    if session.get("user"):
        session.pop("user")
    return make_response("", 200)

@admin.route("/model/base", methods=["PUT"])
def model_base_put():
    if not session.get("user"):
        resp_body = {
            "error": "Authentication required"
        }
        resp_body = jsonify(resp_body)
        return make_response(resp_body, 401)
    file = request.files.get("model")
    if file:
        path = mkdtemp()
        file.save(os.path.join(path, file.filename))
        print(os.path.join(path, file.filename))
        db.model.setBase(os.path.join(path, file.filename))
    else:
        data = request.data
        resp_body = {
            "error": "Invalid API request",
        }
        resp_body = jsonify(resp_body)
        return make_response(resp_body, 400)
        
    return make_response("", 200)

@admin.route("/timestamp")
def timestamp():
    data = request.data
    ts = int(time.time())
    resp_body = str(ts) + ":" + get_sign()
    return make_response(resp_body, 200)
