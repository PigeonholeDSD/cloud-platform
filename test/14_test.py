#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2022/04/29 19:12
# @Author  : Xiaoquan Xu
# @File    : 14_test.py

# Test 14.Log in to the current session
# `POST /session`

import json
import pytest
import requests
from names import *

def test_response_status_code():
    body = {"username": USERNAME, "password": PASSWORD}
    res = requests.post(API_BASE + "/session", json=body)
    assert res.status_code == 200

def test_bad_request2():
    body = {"username": USERNAME, "password": PASSWORD}
    res = requests.post(API_BASE + "/session", data=json.dumps(body))
    assert res.status_code == 400

def test_bad_request():
    bad_body1 = {"username": USERNAME, "password": PASSWORD}
    res = requests.post(API_BASE + "/session", data=bad_body1)
    assert res.status_code == 400

    bad_body2 = {"username": "user"}
    res = requests.post(API_BASE + "/session", json=bad_body2)
    assert res.status_code == 400

def test_wrong_username_password():
    wrong_body1 = {"username": "UserName", "password": "wrong"}
    res = requests.post(API_BASE + "/session", json=wrong_body1)
    assert res.status_code == 403

    wrong_body2 = {"username": "Userser", "password": "wrongrong"}
    res = requests.post(API_BASE + "/session", json=wrong_body2)
    assert res.status_code == 403

def test_set_new_session():
    body = {"username": USERNAME, "password": PASSWORD}
    s = requests.Session()
    session1 = s.cookies.get("session")
    assert session1 == None
    res = s.post(API_BASE + "/session", json=body)
    assert res.status_code == 200
    session2 = s.cookies.get("session")
    assert session2 != None

if __name__ == "__main__":
    pytest.main(["./14_test.py"])
