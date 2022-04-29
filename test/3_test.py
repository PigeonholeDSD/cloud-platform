#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2022/04/29 22:23
# @Author  : Xiaoquan Xu
# @File    : 3_test.py

import uuid
import json
import pytest
import requests
from names import *

def generate_url():
    return API_BASE + "/device/" + str(uuid.uuid4()) + "/email"

def log_in_session() -> requests.Session:
    s = requests.Session()
    body = {"username": USERNAME, "password": PASSWORD}
    s.post(API_BASE + "/session", json=body)
    return s

def set_email():
    s = log_in_session()
    body_email = {"email": "pigeonhole@ciel.dev"}
    url = generate_url()
    s.post(url, json=body_email)
    return s, url, body_email

def test_response_status_code():
    s, url, body_email= set_email()
    res = s.get(url)
    assert res.status_code == 200
    print(res.text)
    print(body_email)
    assert json.loads(res.text) == body_email
    
if __name__ == "__main__":
    pytest.main(["./3_test.py"])
