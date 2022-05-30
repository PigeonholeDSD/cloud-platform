#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2022/05/30 20:57
# @Author  : Xiaoquan Xu
# @File    : 29_test.py

# Test 29.Acquire the base model of an algorithm
# `GET /api/model/<algo>`

import os
import time
import json
import pytest
import tarfile
import random
import requests
import names
from names import *
from simdev import *

os.chdir(os.path.dirname(os.path.abspath(__file__)))

kALGO = -1

def generate_url():
    return API_BASE + "/model/" + names.ALGO[kALGO]

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
    
def test_goodget_device():
    for k in range(len(names.ALGO)):
        kALGO = k
        simd = SimDevice()
        ts = requests.get(API_BASE + "/timestamp").text
        head = {"Authorization": simd.ticket(ts)}
        res = requests.get(generate_url(), headers=head)
        assert res.status_code == 200
        # assert "Last-Modified" not in res.headers
        assert "Content-Length" in res.headers
        
        res = requests.get(API_BASE + "/device/"
            + str(simd.id) + "/model/" + names.ALGO[kALGO],
            headers=head)
        assert res.status_code == 200
        assert "Last-Modified" not in res.headers
        assert "Signature" in res.headers
        assert "Content-Length" in res.headers

def test_good_get():
    kALGO = 0
    res = requests.get(generate_url())
    assert res.status_code == 200
    assert "Content-Length" in res.headers

def test_good_get_admin():
    s = log_in_session()
    kALGO = 0
    res = s.get(generate_url())
    assert res.status_code == 200
    assert "Content-Length" in res.headers

if __name__ == "__main__":
    pytest.main(["./29_test.py"])