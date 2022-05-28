#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2022/04/29 19:29
# @Author  : Xiaoquan Xu
# @File    : 2_test.py

# Test 2.Set the contact email
# `POST /device/<uuid>/email`

import uuid
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

def test_device():
    simd = SimDevice()
    ts = requests.get(API_BASE + "/timestamp").text
    head = {"Authorization": simd.ticket(ts)}
    body_email = {"email": "pigeonholedevice@ciel.dev"}
    url = generate_url(simd.id)
    res = requests.post(url, json=body_email, headers=head)
    assert res.status_code == 200

def test_response_status_code():
    s = log_in_session()
    body_email = {"email": "t@t.tt"}
    url = generate_url()
    res = s.post(url, json=body_email)
    print(url)
    assert res.status_code == 200
    
def test_response_status_code2():
    s = log_in_session()
    body_email = {"email": "pigeonhole@ciel.dev"}
    url = generate_url()
    res = s.post(url, json=body_email)
    assert res.status_code == 200

def test_set_again():
    s = log_in_session()
    body_email = {"email": "t@t.tt"}
    url = generate_url()
    res = s.post(url, json=body_email)
    assert res.status_code == 200
    
    body_email["email"] = "tt@t.tt"
    res = s.post(url, json=body_email)
    assert res.status_code == 200
    
def test_bad_uuid():
    s = log_in_session()
    body_email = {"email": "t@t.tt"}
    url = generate_url()
    res = s.post(url, json=body_email)
    assert res.status_code == 200
    
    url2 = url[:-19] + '-' +url[-18:]
    assert url2 == url
    
    url = url[:-8] + '-' +url[-7:]
    res = s.post(url, json=body_email)
    assert res.status_code == 404
    
def test_nil_uuid():
    s = log_in_session()
    body_email = {"email": "t@t.tt"}
    url = generate_url("00000000-0000-0000-0000-000000000000")
    res = s.post(url, json=body_email)
    assert res.status_code == 404

def test_no_email():
    s = log_in_session()
    body_no_email = {"username": USERNAME, "password": PASSWORD}
    url = generate_url()
    res = s.post(url, json=body_no_email)
    assert res.status_code == 400

def test_bad_email_domain_also_200():
    s = log_in_session()
    body_bad_email = {"email": "pigeonhoe@c.dev"}
    url = generate_url()
    res = s.post(url, json=body_bad_email)
    assert res.status_code == 200
    
def test_bad_email_too_long():
    s = log_in_session()
    body_bad_email = {"email": "hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhole11111111111111@ciel.dev"}
    url = generate_url()
    res = s.post(url, json=body_bad_email)
    assert res.status_code == 400
    
if __name__ == "__main__":
    pytest.main(["./2_test.py"])
