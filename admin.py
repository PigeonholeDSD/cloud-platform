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


@bp.post('/api/session')
def create_session():
    data = APIRequestBody({
        'username': str,
        'password': str,
    })
    if db.admin.check(data.username, data.password):
        session.update({
            'user': data.username,
            'pass': data.password,
        })
        return '', 200
    else:
        raise error.ForbiddenError()


@bp.delete('/api/session')
def session_delete():
    session.pop('user', None)
    session.pop('pass', None)
    return '', 200


@bp.put('/model/base')
@check(admin_only=True)
def put_model_base():
    # admin_only()
    file = request.files.get('model')
    if not file:
        raise error.APISyntaxError('No file uploaded')
    path = os.path.join(mkdtemp(), 'model')
    file.save(path)
    db.model.setBase(path)
    shutil.rmtree(os.path.dirname(path))
    return '', 200
