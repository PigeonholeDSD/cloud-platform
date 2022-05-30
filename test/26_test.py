#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2022/05/29 16:15
# @Author  : Xiaoquan Xu
# @File    : 26_test.py

# Test 26.Train the device model of a specific algorithm
# `POST /device/<uuid>/model/<algo>`

import os
import json
import uuid
import pytest
import random
import requests
import names
from names import *
from simdev import *

os.chdir(os.path.dirname(os.path.abspath(__file__)))

kALGO = -1

def generate_url(idd=None):
    if idd == None:
        idd = uuid.uuid4()
    return API_BASE + "/device/" + str(idd) + "/model/" + names.ALGO[kALGO]

def log_in_session() -> requests.Session:
    s = requests.Session()
    body = {"username": USERNAME, "password": PASSWORD}
    s.post(API_BASE + "/session", json=body)
    return s

def test_refresh_models():
    res = requests.get(API_BASE + "/models")
    assert res.status_code == 200
    names.ALGO = list(json.loads(res.text).keys())
    assert names.ALGO != []

def generate_file(name: str):
    with open(name, "w") as f:
        for _ in range(10):
            f.write(str(random.randint(1,1000000))+"\n")

def hash_content(content):
    with open("_tmp", "wb") as f:
        f.write(content)
    h = hash_file("_tmp")
    os.remove("_tmp")
    return h

def test_good_train():
    for k in range(len(names.ALGO)):
        global kALGO
        kALGO = k
        simd = SimDevice()
        ts = requests.get(API_BASE + "/timestamp").text
        
        s = log_in_session()
        url = generate_url(simd.id)
        res = s.post(url)
        assert res.status_code == 400
        
        tname = "calibration.tgz"
        files = {"calibration": ("c1", open(tname, "rb"),
            "application/x-tar+gzip", {"Expires": "0"})}
        head = {"Authorization": simd.ticket(ts),
            "Signature": simd.sign_file(tname)}
        
        res = requests.put(API_BASE + "/device/" 
            + str(simd.id) + "/calibration", files=files, headers=head)
        assert res.status_code == 200
        
        res = s.post(url)
        assert res.status_code == 200

def test_device():
    for k in range(len(names.ALGO)):
        global kALGO
        kALGO = k
        simd = SimDevice()
        ts = requests.get(API_BASE + "/timestamp").text
        
        s = log_in_session()
        url = generate_url(simd.id)
        res = s.post(url)
        assert res.status_code == 400
        
        res = requests.post(url,
            headers = {"Authorization": simd.ticket(ts)})
        assert res.status_code == 400
        
        tname = "calibration.tgz"
        files = {"calibration": ("c1", open(tname, "rb"),
            "application/x-tar+gzip", {"Expires": "0"})}
        head = {"Authorization": simd.ticket(ts),
            "Signature": simd.sign_file(tname)}
        
        res = requests.put(API_BASE + "/device/" 
            + str(simd.id) + "/calibration", files=files, headers=head)
        assert res.status_code == 200
        
        res = requests.post(url,
            headers = head)
        assert res.status_code == 200

def test_train_continuously():
    global kALGO
    kALGO = 0
    simd = SimDevice()
    ts = requests.get(API_BASE + "/timestamp").text
    
    s = log_in_session()
    url = generate_url(simd.id)
    res = s.post(url)
    assert res.status_code == 400
    
    tname = "calibration.tgz"
    files = {"calibration": ("c1", open(tname, "rb"),
        "application/x-tar+gzip", {"Expires": "0"})}
    head = {"Authorization": simd.ticket(ts),
        "Signature": simd.sign_file(tname)}
    
    res = requests.put(API_BASE + "/device/" 
        + str(simd.id) + "/calibration", files=files, headers=head)
    assert res.status_code == 200
    
    res = s.post(url)
    assert res.status_code == 200
    
    res = s.post(url)
    assert res.status_code == 200

if __name__ == "__main__":
    pytest.main(["./26_test.py"])