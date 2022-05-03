#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2022/04/30 18:45
# @Author  : Xiaoquan Xu
# @File    : 4_test.py

# Test 4.Clear the contact email setting
# `DELETE /device/<uuid>/email`

import uuid
import json
import pytest
import requests
from names import *
from simdev import *

def generate_url(idd=None):
    if idd == None:
        idd = uuid.uuid4()
    return API_BASE + "/device/" + str(idd) + "/email"

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

def test_device():
    simd = SimDevice()
    
    ts = requests.get(API_BASE + "/timestamp").text
    head = {"Authorization": simd.ticket(ts)}
    body_email = {"email": "pigeonholedevice@ciel.dev"}
    url = generate_url(simd.id)
    res = requests.post(url, json=body_email, headers=head)
    assert res.status_code == 200
    
    res = requests.get(url, headers=head)
    assert res.status_code == 200
    assert json.loads(res.text) == body_email
    
    res = requests.delete(url, headers=head)
    assert res.status_code == 200
    
    res = requests.get(url, headers=head)
    assert res.status_code == 404

def test_good_clear_email():
    body_email = {"email": "pigeonhole@ciel.dev"}
    s, url = set_email(body_email)
    
    res = s.get(url)
    assert json.loads(res.text) == body_email
    
    res = s.delete(url)
    assert res.status_code == 200
    assert res.text == ""
    
    res = s.get(url)
    assert res.status_code == 404
    assert res.text == ""
    
def test_no_email_before_clear():
    s = log_in_session()
    url = generate_url()
    
    res = s.get(url)
    assert res.status_code == 404
    assert res.text == ""
    
    res = s.delete(url)
    assert res.status_code == 200
    assert res.text == ""
    
def test_delete_again():
    body_email = {"email": "pigeonholeno@ciel.dev"}
    s, url = set_email(body_email)
    
    res = s.get(url)
    assert json.loads(res.text) == body_email
    
    res = s.delete(url)
    res = s.delete(url)
    assert res.status_code == 200
    assert res.text == ""
    
    res = s.get(url)
    assert res.status_code == 404
    assert res.text == ""

if __name__ == "__main__":
    pytest.main(["./4_test.py"])
