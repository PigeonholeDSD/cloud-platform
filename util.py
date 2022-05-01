#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import uuid
from flask import session, request
import error
import crypto
import db.admin


class APIRequestBody(object):
    def __init__(self, schema: dict):
        if not request.is_json:
            raise error.APISyntaxError('The request must be of type application/json')
        try:
            self.data = json.loads(request.data)
        except json.JSONDecodeError:
            raise error.APISyntaxError('Invalid JSON')
        if not isinstance(self.data, dict):
            raise error.APISyntaxError('Invalid request object')
        for key, dtype in schema.items():
            if not isinstance(self.data.get(key), dtype):
                raise error.APISyntaxError(
                    f'Argument \'{key}\' must be of type {dtype}')

    def __getattr__(self, key):
        return self.data.get(key)

    def __getitem__(self, key):
        return self.data.get(key)


def logged_in(uuid: uuid.UUID):
    if is_admin():
        return
    crypto.check_ticket(request.headers.get('Authorization', ''), uuid)


def is_admin() -> bool:
    return db.admin.check(session.get('user', ''), session.get('pass', ''))


def admin_only():
    if not is_admin():
        raise error.Forbidden()
