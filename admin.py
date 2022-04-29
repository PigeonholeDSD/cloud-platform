import os
import shutil
from tempfile import mkdtemp
from flask import Blueprint, request, session, jsonify
import error
from util import *
import db.admin
import db.model
import db.device

bp = Blueprint('admin', __name__)


@bp.post('/session')
def create_session():
    data = APIRequestBody({
        'username': str,
        'password': str,
    })
    if db.admin.check(data.username, data.password):
        session['user'] = data.username
        session['pass'] = data.password
        return '', 200
    else:
        raise error.Forbidden('Login failed')


@bp.delete('/session')
def session_delete():
    session.pop('user', None)
    session.pop('pass', None)
    return '', 200


@bp.put('/model/base')
def model_base_put():
    admin_only()
    file = request.files.get('model')
    if not file:
        return jsonify({
            'error': 'No file uploaded',
        }), 400
    path = os.path.join(mkdtemp(), 'model')
    file.save(path)
    db.model.setBase(path)
    shutil.rmtree(os.path.dirname(path))
    return '', 200
