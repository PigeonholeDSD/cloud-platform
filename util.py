#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import uuid
from flask import session, request
import error
import crypto
import db.admin
from functools import wraps


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


def logged_in(devid: uuid.UUID) -> None:
    if is_admin():
        return
    crypto.check_ticket(request.headers.get('Authorization', ''), devid)


def is_admin() -> bool:
    return db.admin.check(session.get('user', ''), session.get('pass', ''))


def check(admin_only: bool=False):
    def check_decorator(f):
        @wraps(f)
        def wrapped_function(*args, **kwargs):
            if is_admin():
                return f(*args, **kwargs)
            if 'devid' not in kwargs:
                raise error.UnauthorizedError()
            crypto.check_ticket(request.headers.get('Authorization', ''), kwargs['devid'])
            if (admin_only):
                raise error.ForbiddenError('Permission denied')
            return f(*args, **kwargs)
        return wrapped_function
    return check_decorator

def validate_algo():
    def algo_decorator(f):
        @wraps(f)
        def wrapped_function(*args, **kwargs):
            with open('algo/algo.json', 'r') as f:
                algo_list = json.load(f)
            if kwargs['algo'] not in algo_list.keys():
                raise error.NotFoundError('Algorithm not found.')
            return f(*args, **kwargs)
        return wrapped_function
    return algo_decorator
