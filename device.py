import os
import re
import time
import shutil
import tarfile
from tempfile import mkdtemp
from flask import Blueprint, after_this_request, make_response, request, jsonify, send_file
import error
import train
from util import *
import db.device
import db.model

bp = Blueprint('device', __name__, url_prefix='/device')


@bp.get('<uuid:uuid>/email')
def get_email(uuid: uuid.UUID):
    logged_in(uuid)
    email = db.device.get(uuid).email
    if not email:
        return '', 404
    return jsonify({
        'email': email,
    }), 200


@bp.post('<uuid:uuid>/email')
def post_email(uuid: uuid.UUID):
    logged_in(uuid)
    data = APIRequestBody({
        'email': str,
    })
    if len(data.email) > 254 or \
            not re.match(r'^[a-zA-Z0-9_.+-]{1,64}@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)+$', data.email):
        raise error.APISyntaxError('Invalid email')
    db.device.get(uuid).email = data.email
    return '', 200


@bp.delete('<uuid:uuid>/email')
def delete_email(uuid: uuid.UUID):
    logged_in(uuid)
    db.device.get(uuid).email = None
    return '', 200


# TODO
@bp.get('<uuid:uuid>/calibration')
def get_calibration(uuid: uuid.UUID):
    logged_in(uuid)
    if request.method == 'HEAD':
        return '', (200 if db.device.get(uuid).calibration else 404)
    admin_only()
    path = db.device.get(uuid).calibration
    if not path:
        return '', 404
    tmp_dir = mkdtemp()
    tmp_path = os.path.join(tmp_dir, 'calibration.tar.gz')
    with tarfile.open(tmp_path, "w:gz") as tar:
        tar.add(path)
    file_handler = open(tmp_path, 'r')
    @after_this_request
    def delete_file(response):
        shutil.rmtree(tmp_dir)
        return response
    return send_file(file_handler)
    # file = model if model else db.model.getBase()
    # response = make_response(send_file(file), 200)
    # response.headers['Signature'] = crypto.sign(filename)
    # return response


@bp.put('<uuid:uuid>/calibration')
def put_calibration(uuid: uuid.UUID):
    logged_in(uuid)
    file = request.files.get('calibration')
    if file and file.content_type != 'application/x-tar+gzip':
        raise error.APISyntaxError(
            'The request must be of type application/json')
    path = mkdtemp()
    try:
        filename = os.path.join(path, 'cal.tar.gz')
        file.save(filename)
        crypto.check_file(filename, request.headers.get('Signature'), uuid)
        tf = tarfile.open(filename)
        tf.extractall(path)
        db.device.get(uuid).calibration = path
        train.train(db.device.get(uuid))
    finally:
        shutil.rmtree(path)
    return '', 200


@bp.delete('<uuid:uuid>/calibration')
def delete_calibration(uuid: uuid.UUID):
    logged_in(uuid)
    db.device.get(uuid).calibration = None
    return '', 200


@bp.get('<uuid:uuid>/model')
def get_model(uuid: uuid.UUID):
    logged_in(uuid)
    model = db.device.get(uuid).model
    file = model if model else db.model.getBase()
    response = make_response(send_file(file), 200)
    response.headers['Signature'] = crypto.sign_file(file)
    if model:
        last_modified = os.path.getmtime(model)
        last_modified = time.gmtime(last_modified)
        last_modified = time.strftime(
            '%a, %d %b %Y %H:%M:%S GMT', last_modified)
        response.headers['Last-Modified'] = last_modified
    return response


@bp.put('<uuid:uuid>/model')
def put_model(uuid: uuid.UUID):
    admin_only()
    file = request.files.get('model')
    if not file:
        return jsonify({
            'error': 'No file uploaded',
        }), 400
    path = os.path.join(mkdtemp(), 'model')
    file.save(path)
    db.device.get(uuid).model = path
    shutil.rmtree(os.path.dirname(path))
    return '', 200


@bp.delete('<uuid:uuid>/model')
def delete_model(uuid: uuid.UUID):
    logged_in(uuid)
    db.device.get(uuid).model = None
    return '', 200


@bp.delete('/device/<uuid:uuid>')
def delete_device(uuid):
    admin_only()
    db.device.remove(uuid)
    return '', 200
