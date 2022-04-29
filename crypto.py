import time
import hmac
import uuid
import hashlib
from flask import current_app
import error


def timestamp(_time: int=0) -> str:
    t = str(int(_time if _time else time.time()))
    sign = hmac.new(current_app.config['SECRET_KEY'].encode(
    ), t.encode(), hashlib.sha1).hexdigest()
    return t+':'+sign


def check_timestamp(ts: str) -> None:
    try:
        t = int(ts.split(':', 1)[0])
        if t+current_app.config['TICKET_LIFETIME'] < time.time():
            raise Exception()
        if timestamp(t) == ts:
            return
        raise Exception()
    except Exception:
        raise error.NotLoggedIn('Invalid device ticket')


def check_ticket(ticket: uuid.UUID) -> None:
    return check_timestamp(ticket)

def sign(file: str) -> str:
    return ''

def verify(file: str, sign: str) -> bool:
    return True