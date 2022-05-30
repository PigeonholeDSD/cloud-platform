import os
import shutil
from tempfile import mkdtemp
from flask import Blueprint, request, jsonify, send_file
import error
from util import *

bp = Blueprint('model', __name__, url_prefix='/api')

@bp.get('models')
def get_model():
    with open('algo/algo.json', 'r') as f:
        algo_list = json.load(f)
    return jsonify(algo_list), 200

@bp.get('model/<string:algo>')
@validate_algo()
def get_algo(algo: str):
    with open('algo/algo.json', 'r') as f:
        algo_list = json.load(f)
    path = (db.device.get(uuid.UUID(int=0)).model[algo]
        or algo_list[algo]['base'].replace('$ALGO', 'algo')
    )
    return send_file(path, 'application/octet-stream')

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
