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

def test_good_get_email():
    body_email = {"email": "pigeonhole@ciel.dev"}
    s, url = set_email(body_email)
    
    res = s.get(url)
    assert res.status_code == 200
    print(res.text)
    print(body_email)
    assert json.loads(res.text) == body_email
    
def test_set_again():
    body_email = {"email": "pigeonholee@ciel.dev"}
    s, url = set_email(body_email)
    res = s.get(url)
    assert res.status_code == 200
    print(res.text)
    print(body_email)
    assert json.loads(res.text) == body_email
    
    body_email = {"email": "pigeonholee2@ciel.dev"}
    assert json.loads(res.text) != body_email
    
    s.post(url, json=body_email)
    res = s.get(url)
    assert res.status_code == 200
    print(res.text)
    print(body_email)
    assert json.loads(res.text) == body_email

def test_set_again_not_same_session():
    body_email = {"email": "pigeonholee@ciel.dev"}
    s, url = set_email(body_email)
    res = s.get(url)
    assert res.status_code == 200
    print(res.text)
    print(body_email)
    assert json.loads(res.text) == body_email
    
    body_email2 = {"email": "pigeonholee2@ciel.dev"}
    assert body_email != body_email2
    s2 = log_in_session()
    s2.post(url, json=body_email2)
    
    res = s.get(url)
    assert res.status_code == 200
    assert json.loads(res.text) == body_email2
    
    res2 = s2.get(url)
    assert res2.status_code == 200
    assert json.loads(res2.text) == body_email2

def test_not_same_session():
    body_email = {"email": "pigeon@ciel.dev"}
    s, url = set_email(body_email)
    res = s.get(url)
    assert res.status_code == 200
    assert json.loads(res.text) == body_email
    
    s2 = log_in_session()
    res2 = s2.get(url)
    print(res2.content)
    print(res.content)
    assert res2.content == res.content

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
