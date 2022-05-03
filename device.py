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


@bp.get('<uuid:devid>/email')
def get_email(devid: uuid.UUID):
    logged_in(devid)
    email = db.device.get(devid).email
    if not email:
        return '', 404
    return jsonify({
        'email': email,
    }), 200


@bp.post('<uuid:devid>/email')
def post_email(devid: uuid.UUID):
    logged_in(devid)
    data = APIRequestBody({
        'email': str,
    })
    if len(data.email) > 254 or \
            not re.match(r'^[a-zA-Z0-9_.+-]{1,64}@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)+$', data.email):
        raise error.APISyntaxError('Invalid email')
    db.device.get(devid).email = data.email
    return '', 200


@bp.delete('<uuid:devid>/email')
def delete_email(devid: uuid.UUID):
    logged_in(devid)
    db.device.get(devid).email = None
    return '', 200


@bp.get('<uuid:devid>/calibration')
def get_calibration(devid: uuid.UUID):
    logged_in(devid)
    if request.method == 'HEAD':
        return '', (200 if db.device.get(devid).calibration else 404)
    admin_only()
    path = db.device.get(devid).calibration
    if not path:
        return '', 404
    tmp_dir = mkdtemp()
    tmp_path = os.path.join(tmp_dir, 'calibration.tar.gz')
    with tarfile.open(tmp_path, "w:gz") as tar:
        for motion in os.listdir(path):
            tar.add(
                name=os.path.join(path, motion),
                arcname=motion,
            )

    @after_this_request
    def delete_file(response):
        shutil.rmtree(tmp_dir)
        return response
    return send_file(open(tmp_path, 'rb'), 'application/x-tar+gzip')


@bp.put('<uuid:devid>/calibration')
def put_calibration(devid: uuid.UUID):
    logged_in(devid)
    file = request.files.get('calibration')
    if not file:
        raise error.APISyntaxError('No file uploaded')
    if file.content_type != 'application/x-tar+gzip':
        raise error.APISyntaxError(
            'The file must be of type application/x-tar+gzip')
    path = mkdtemp()
    try:
        filename = os.path.join(path, 'cal.tar.gz')
        file.save(filename)
        if not is_admin():
            crypto.check_file(
                filename, request.headers.get('Signature', ''), devid)
        try:
            with tarfile.open(filename) as tf:
                tf.extractall(path)
            os.unlink(filename)
        except:
            raise error.APISyntaxError('Bad tarball')
        db.device.get(devid).calibration = path
        train.train(db.device.get(devid))
    finally:
        shutil.rmtree(path)
    return '', 200


@bp.delete('<uuid:devid>/calibration')
def delete_calibration(devid: uuid.UUID):
    logged_in(devid)
    db.device.get(devid).calibration = None
    return '', 200


@bp.get('<uuid:devid>/model')
def get_model(devid: uuid.UUID):
    logged_in(devid)
    model = db.device.get(devid).model
    file = model or db.model.getBase()
    response = make_response(send_file(file, 'application/octet-stream'), 200)
    response.headers['Signature'] = crypto.sign_file(file)
    if model:
        last_modified = time.gmtime(os.path.getmtime(model))
        response.headers['Last-Modified'] = time.strftime(
            '%a, %d %b %Y %H:%M:%S GMT', last_modified)
    else:
        del response.headers['Last-Modified']
    return response


@bp.put('<uuid:devid>/model')
def put_model(devid: uuid.UUID):
    admin_only()
    file = request.files.get('model')
    if not file:
        raise error.APISyntaxError('No file uploaded')
    path = os.path.join(mkdtemp(), 'model')
    file.save(path)
    db.device.get(devid).model = path
    shutil.rmtree(os.path.dirname(path))
    return '', 200


@bp.delete('<uuid:devid>/model')
def delete_model(devid: uuid.UUID):
    logged_in(devid)
    db.device.get(devid).model = None
    return '', 200


@bp.delete('<uuid:devid>')
def delete_device(devid: uuid.UUID):
    admin_only()
    data = APIRequestBody({
        'ban': bool
    })
    db.device.remove(devid)
    if data.ban:
        db.device.get(devid).banned = True
    return '', 200
