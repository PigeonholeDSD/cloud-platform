#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2022/05/03 23:11
# @Author  : Xiaoquan Xu
# @File    : 13_test.py

# Test 13.Delete everything specified from the cloud
# `DELETE /device/<uuid>`

import os
import uuid
import pytest
import json
import requests
from names import *
from simdev import *

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def generate_url(idd=None):
    if idd == None:
        idd = uuid.uuid4()
    return API_BASE + "/device/" + str(idd)

def log_in_session() -> requests.Session:
    s = requests.Session()
    body = {"username": USERNAME, "password": PASSWORD}
    s.post(API_BASE + "/session", json=body)
    return s
    
def test_delete_straightforward():
    s = log_in_session()
    url = generate_url()
    req = {"ban": True}
    res = s.delete(url, json=req)
    assert res.status_code == 200

def test_good_delete():
    simd = SimDevice()
    
    ts = requests.get(API_BASE + "/timestamp").text
    head = {"Authorization": simd.ticket(ts)}
    body_email = {"email": "pigeonholedevice@ciel.dev"}
    url = generate_url(simd.id)
    res = requests.post(url+"/email", json=body_email, headers=head)
    assert res.status_code == 200
    
    res = requests.get(url+"/email", headers=head)
    assert res.status_code == 200
    assert json.loads(res.text) == body_email
    
    s = log_in_session()
    req = {"ban": True}
    res = s.delete(url, json=req)
    assert res.status_code == 200
    
    res = requests.get(url+"/email", headers=head)
    assert res.status_code == 404

def test_bad_delete():
    simd = SimDevice()
    
    ts = requests.get(API_BASE + "/timestamp").text
    head = {"Authorization": simd.ticket(ts)}
    body_email = {"email": "pigeonholedevice@ciel.dev"}
    url = generate_url(simd.id)
    res = requests.post(url+"/email", json=body_email, headers=head)
    assert res.status_code == 200
    
    res = requests.get(url+"/email", headers=head)
    assert res.status_code == 200
    assert json.loads(res.text) == body_email
    
    s = log_in_session()
    req = {"ban": 123}
    res = s.delete(url, json=req)
    assert res.status_code == 400
    
    res = requests.get(url+"/email", headers=head)
    assert res.status_code == 200

if __name__ == "__main__":
    pytest.main(["./13_test.py"])