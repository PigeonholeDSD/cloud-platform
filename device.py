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

bp = Blueprint('device', __name__, url_prefix='/api/device')


@bp.get('<uuid:devid>/email')
@check()
@validate_uuid()
def get_email(devid: uuid.UUID):
    email = db.device.get(devid).email
    if not email:
        return '', 404
    return jsonify({
        'email': email,
    }), 200


@bp.post('<uuid:devid>/email')
@check()
@validate_uuid()
def post_email(devid: uuid.UUID):
    data = APIRequestBody({
        'email': str,
    })
    if len(data.email) > 254 or \
            not re.match(r'^[a-zA-Z0-9_.+-]{1,64}@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)+$', data.email):
        raise error.APISyntaxError('Invalid email')
    db.device.get(devid).email = data.email
    return '', 200


@bp.delete('<uuid:devid>/email')
@check()
@validate_uuid()
def delete_email(devid: uuid.UUID):
    db.device.get(devid).email = None
    return '', 200


@bp.get('<uuid:devid>/calibration')
@check(admin_only=True)
@validate_uuid()
def get_calibration(devid: uuid.UUID):
    path = db.device.get(devid).calibration
    if not path:
        raise error.NotFoundError('Calibration file not found')
    if not is_admin():
        raise error.ForbiddenError('Permission denied')
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
@check()
@validate_uuid()
def put_calibration(devid: uuid.UUID):
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
        # train.train(db.device.get(devid))
    finally:
        shutil.rmtree(path)
    return '', 200


@bp.delete('<uuid:devid>/calibration')
@check()
@validate_uuid()
def delete_calibration(devid: uuid.UUID):
    db.device.get(devid).calibration = None
    return '', 200


@bp.get('<uuid:devid>/model/<string:algo>')
@check()
@validate_uuid()
@validate_algo()
def get_model(devid: uuid.UUID, algo: str):
    with open('algo/algo.json', 'r') as f:
        algo_list = json.load(f)
    model = db.device.get(devid).model[algo]
    file = (model
            or db.device.get(uuid.UUID(int=0)).model[algo] 
            or algo_list[algo]['base'].replace('$ALGO', 'algo')
        )
    response = make_response(send_file(file, 'application/octet-stream'), 200)
    response.headers['Signature'] = crypto.sign_file(file)
    if model:
        last_modified = time.gmtime(os.path.getmtime(model))
        response.headers['Last-Modified'] = time.strftime(
            '%a, %d %b %Y %H:%M:%S GMT', last_modified)
    else:
        del response.headers['Last-Modified']
    return response


@bp.put('<uuid:devid>/model/<string:algo>')
@check(admin_only=True)
@validate_uuid()
@validate_algo()
def put_model(devid: uuid.UUID, algo: str):
    file = request.files.get('model')
    if not file:
        raise error.APISyntaxError('No file uploaded')
    path = os.path.join(mkdtemp(), 'model')
    print(path)
    file.save(path)
    db.device.get(devid).model[algo] = path
    shutil.rmtree(os.path.dirname(path))
    return '', 200

@bp.post('<uuid:devid>/model/<string:algo>')
@check()
@validate_uuid()
@validate_algo()
def post_model(devid: uuid.UUID, algo: str):
    device = db.device.get(devid)
    if not device.calibration:
        raise error.CalibrationNotFoundError()
    train.train(device, algo)
    return '', 200


@bp.delete('<uuid:devid>/model')
@check()
@validate_uuid()
def delete_all_model(devid: uuid.UUID):
    with open('algo/algo.json', 'r') as f:
        algo_list = json.load(f)
    for algo in algo_list.keys():
        db.device.get(devid).model[algo] = None
    return '', 200

@bp.delete('<uuid:devid>/model/<string:algo>')
@check()
@validate_uuid()
@validate_algo()
def delete_model(devid: uuid.UUID, algo: str):
    db.device.get(devid).model[algo] = None
    return '', 200


@bp.delete('<uuid:devid>')
@check()
@validate_uuid()
def delete_device(devid: uuid.UUID):
    db.device.remove(devid)
    return '', 200
