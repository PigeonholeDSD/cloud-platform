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

def set_email(body_email):
    s = log_in_session()
    url = generate_url()
    s.post(url, json=body_email)
    return s, url

def test_response_status_code():
    body_email = {"email": "pigeonhole@ciel.dev"}
    s, url = set_email(body_email)
    res = s.get(url)
    assert res.status_code == 200
    print(res.text)
    print(body_email)
    assert json.loads(res.text) == body_email
    
def test_set_again():
    body_email = {"email": "pigeonhole@ciel.dev"}
    s, url = set_email(body_email)
    res = s.get(url)
    assert res.status_code == 200
    print(res.text)
    print(body_email)
    assert json.loads(res.text) == body_email
    
    body_email = {"email": "pigeonhole2@ciel.dev"}
    assert json.loads(res.text) != body_email
    s.post(url, json=body_email)
    res = s.get(url)
    assert res.status_code == 200
    print(res.text)
    print(body_email)
    assert json.loads(res.text) == body_email

def test_no_email_set_before():
    s = log_in_session()
    url = generate_url()
    res = s.get(url)
    assert res.status_code == 404

def test_bad_email():
    body_email = {"email": "pigeonhole@cieldev"}
    s, url = set_email(body_email)
    res = s.get(url)
    assert res.status_code == 404
    assert res.text == ""

def test_bad_email2():
    body_email = {"email": "pigeonhole@ciel..dev"}
    s, url = set_email(body_email)
    res = s.get(url)
    assert res.status_code == 404
    assert res.text == ""

def test_bad_email3():
    body_email = {"email": "pigeonhole@@ciel.dev"}
    s, url = set_email(body_email)
    res = s.get(url)
    assert res.status_code == 404
    assert res.text == ""

def test_bad_email4():
    body_email = {"email": "pigeonholllllllllllllllllllllllll"
        "llllllllllllllllllllllllllllllllllllllllllllllllllllle"
            "@ciellllllllllllllllllllllllllllllllllllllllllllllll"
                "lllllllllllllllllllllllllllllllllllllllllllllllll."
                    "deeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee"
                        "eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeev"}
    s, url = set_email(body_email)
    res = s.get(url)
    assert res.status_code == 404
    assert res.text == ""

def test_bad_email5():
    body_email = {"email": "pigeonhole @ciel.dev"}
    s, url = set_email(body_email)
    res = s.get(url)
    assert res.status_code == 404
    assert res.text == ""

def test_nearly_bad_email():
    body_email = {"email": "pigeonhollllllll"
        "llllllllllllllllllllllllllllllllllllle"
            "@ciellllllllllllllllllllllllllllllll"
                "lllllllllllllllllllllllllllllllll."
                    "deeeeeeeeeeeeeeeeeeeeeeeeeeeeeee"
                        "eeeeeeeeeeeeeeeeeeeeeeeeeeeev"}
    print(body_email)
    s, url = set_email(body_email)
    res = s.get(url)
    assert res.status_code == 200
    assert json.loads(res.text) == body_email

if __name__ == "__main__":
    pytest.main(["./3_test.py"])
