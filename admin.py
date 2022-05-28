import os
import shutil
from tempfile import mkdtemp
from flask import Blueprint, request, session, jsonify
import error
from util import *
import db.admin
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
        raise error.ForbiddenError('Permission denied')


@bp.delete('/api/session')
def session_delete():
    session.pop('user', None)
    session.pop('pass', None)
    return '', 200
