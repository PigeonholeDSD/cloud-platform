#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import os.path
import atexit
import secrets
from datetime import timedelta
from signal import SIGTERM
from flask import Flask
import error
import admin
import crypto
import device
import model
from util import *

os.chdir(os.path.dirname(os.path.abspath(__file__)))
os.setpgrp()
@atexit.register
def goodbye():
    os.killpg(0, SIGTERM)

app = Flask(__name__)
app.config.update({
    'SECRET_KEY': secrets.token_hex(32),
    'PERMANENT_SESSION_LIFETIME': timedelta(hours=2),
    'TICKET_LIFETIME': 60*60,
    'CLOUD_KEY': crypto.cloud_key(),
    'SESSION_COOKIE_SAMESITE': 'None',
    'SESSION_COOKIE_SECURE': False,
})

app.register_blueprint(admin.bp)
app.register_blueprint(device.bp)
app.register_blueprint(model.bp)
app.register_error_handler(error.APISyntaxError, error.APISyntaxError.handler)
app.register_error_handler(error.UnauthorizedError, error.UnauthorizedError.handler)
app.register_error_handler(error.ForbiddenError, error.ForbiddenError.handler)
app.register_error_handler(error.BadSignatureError, error.BadSignatureError.handler)
app.register_error_handler(error.NotFoundError, error.NotFoundError.handler)
app.register_error_handler(error.CalibrationNotFoundError, error.CalibrationNotFoundError.handler)
app.add_url_rule('/api/timestamp', view_func=crypto.timestamp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
