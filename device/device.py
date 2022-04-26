# Author: Alex Xu
# Description: Device management APIs of cloud server.

from flask import Blueprint, make_response, request, jsonify, send_from_directory, session
import db.device, db.model
from utils.utils import APIParser, APIParseError, check_sign
from email_validator import validate_email, EmailNotValidError
from tempfile import mkdtemp
import tarfile, os, time

device = Blueprint("device", __name__, url_prefix="/device")

email_parser = APIParser()
email_parser.add_prop(name="email", dtype=str)

@device.before_request
def auth():
    """
    Global interceptor of device APIs.

    Passed if session or header `Authorization` is invalid.

    Return 401 if both session and header `Authorization` are invalid.
    """

    if request.method in ["GET", "DELETE", "HEAD"]:
        data = request.data
    if session.get("user"):
        return None
    if ("Authorization" in request.headers.keys()) and check_sign(request.headers["Authorization"]):
        return None
    
    data = request.data
    resp_body = {
        "error": "Authentication required"
    }
    resp_body = jsonify(resp_body)
    return make_response(resp_body, 401)
    

@device.route("<uuid:uuid>/email", methods=["GET"])
def email_get(uuid: str):
    """
    Gets the contact email.

    The response is of type `application/json`. Example response:

    ```
    {
        "email": "t@t.tt"
    }
    ```

    Returns 404 if not set, 200 otherwise.
    """

    email = db.device.get(uuid).email
    # Get the request data of GET, so Flask will not return 400 automatically.
    data = request.data
    if (email):
        resp_body = {
            "email": email,
        }
        resp_body = jsonify(resp_body)
        return  make_response(resp_body, 200)
    else:
        resp_body = {
            "error": "The email is empty"
        }
        resp_body = jsonify(resp_body)
        return make_response(resp_body, 404)

@device.route("<uuid:uuid>/email", methods=["POST"])
def email_post(uuid: str):
    """
    Sets the contact email.

    The request must be of type `application/json`. Example request:

    ```
    {
        "email": "t@t.tt"
    }
    ```

    The email must be of the right form and a maximum of 254 characters.

    Returns 400 if email is invalid, 200 otherwise.
    """

    try:
        data = email_parser.parse(request.data)
        # If invalid, EmailNotValidError will be raised
        valid = validate_email(data["email"])
        # Get normalized email address
        email = valid.email
        # If length exceeds, EmailNotValidError will be raised.
        if (len(email) > 254):
            raise EmailNotValidError("The email address is too long ({} characters too many).".format(len(email) - 254))
        db.device.get(uuid).email = email
        return make_response("", 200)
    except EmailNotValidError as e:
        resp_body = {
            "error": str(e)
        }
        resp_body = jsonify(resp_body)
        return make_response(resp_body, 400)
    except APIParseError:
        resp_body = {
            "error": "Invalid API request"
        }
        resp_body = jsonify(resp_body)
        return make_response(resp_body, 400)


@device.route("<uuid:uuid>/email", methods=["DELETE"])
def email_delete(uuid: str):
    """
    Clears the contact email setting.

    Returns 200 always.
    """

    db.device.get(uuid).email = None
    return make_response("", 200)

@device.route("<uuid:uuid>/calibration", methods=["HEAD"])
def calibration_head(uuid: str):
    """
    Checks whether calibration data is available on the server.

    Returns 200 if data is found, 404 otherwise.
    """

    if (db.device.get(uuid).calibration == None):
        return make_response("", 404)
    else:
        return make_response("", 200)

@device.route("<uuid:uuid>/calibration", methods=["PUT"])
def calibration_put(uuid: str):
    """
    Upload new calibration data to the cloud platform.

    The request must have a valid `Signature` header passed from the device.

    The request should be of type `multipart/form-data` with a file field `calibration`, the file must be of type `application/x-tar+gzip`.

    Returns 200 if succeeds, or 400 if the signature is not valid.  
    """

    file = request.files.get("calibration")
    if file and file.content_type == "application/x-tar+gzip":
        path = mkdtemp()
        file.save(path)
        tf = tarfile.open(os.path.join(path, file.name))
        tf.extractall(path)
        db.device.get(uuid).calibration = path
    else:
        resp_body = {
            "error": "Invalid API request",
        }
        resp_body = jsonify(resp_body)
        return make_response(resp_body, 400)
        
    return make_response("", 200)

@device.route("<uuid:uuid>/calibration", methods=["DELETE"])
def calibration_delete(uuid: str):
    """
    Clears calibration data from the cloud.

    Returns 200 always.
    """
    db.device.get(uuid).calibration = None
    return make_response("", 200)

@device.route("<uuid:uuid>/model", methods=["HEAD"])
def model_head(uuid: str):
    """
    Checks the version of the device model on the server.

    The response contains a `Last-Modified` header of the device model. If the device model does not exist, no such header is sent, but the base version is still available to download.

    The response contains a `Content-Length` header to indicate the size of model.

    Returns 200 always.
    """
    path = db.device.get(uuid).model
    response = make_response("", 200)
    if path:
        last_modified = os.path.getmtime(path)
        last_modified = time.gmtime(last_modified)
        last_modified = time.strftime('%a, %d %b %Y %H:%M:%S GMT', last_modified)
        size = os.path.getsize(path)
        response.headers["Last-Modified"] = last_modified
        response.headers["Content-Length"] = size
    else:
        size = os.path.getsize(db.model.getBase())
        response.headers["Content-Length"] = size

    return response

@device.route("<uuid:uuid>/model", methods=["GET"])
def model_get(uuid: str):
    """
    Acquire the current version of the device model, signed with the platform key.

    If the device model does not exist, the base version is provided.

    The response is of type `application/octet-stream`.

    The response will have a `Signature` header to be passed to the device.

    Returns 200 always.
    """
    path = db.device.get(uuid).model
    if path:
        return send_from_directory(path)
    
    return send_from_directory(db.model.getBase())

@device.route("<uuid:uuid>/model", methods=["DELETE"])
def model_delete(uuid: str):
    """
    Clears device model from the cloud.

    Returns 200 always.
    """
    db.device.get(uuid).model = None
    
    return make_response("", 200)
