import os
import shutil
from tempfile import mkdtemp
from flask import Blueprint, request, jsonify, send_file
import error
from util import *

bp = Blueprint('model', __name__, url_prefix='/api')

@bp.get('models')
@check()
def get_model():
    with open('algo/algo.json', 'r') as f:
        algo_list = json.load(f)
    return jsonify(algo_list), 200

@bp.get('model/<string:algo>')
@check()
@validate_algo()
def get_algo(algo: str):
    algo_list = json.load('algo/algo.json')
    if algo not in algo_list.keys():
        raise error.NotFoundError('Algorithm not found.')
    return send_file(open(algo_list[algo]['base']), 'application/octet-stream')

@bp.put('model/<string:algo>')
@check(admin_only=True)
@validate_algo()
def put_algo(algo: str):
    file = request.files.get('model')
    if not file:
        raise error.APISyntaxError('No file uploaded')
    path = os.path.join(mkdtemp(), 'model')
    file.save(path)
    db.device.get(uuid.UUID(int=0)).model[algo] = path
    shutil.rmtree(os.path.dirname(path))
    return '', 200