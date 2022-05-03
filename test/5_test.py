#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2022/04/30 20:31
# @Author  : Xiaoquan Xu
# @File    : 5_test.py

import os
import json
import uuid
import pytest
import requests
from names import *

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def generate_url():
    return API_BASE + "/device/" + str(uuid.uuid4()) + "/calibration"

def log_in_session() -> requests.Session:
    s = requests.Session()
    body = {"username": USERNAME, "password": PASSWORD}
    s.post(API_BASE + "/session", json=body)
    return s

def test_good_check():
    s = log_in_session()
    url = generate_url()
    # files = {"file": ("fake.csv", open("fake.csv", "rb"),\
    #     "multipart/form-data", {"Expires": "0"})}
    res = s.head(url)
    assert res.status_code in [200,404]

def test_updown_repeatedly():
    s = log_in_session()
    url = generate_url()
    files = {"calibration": ("dah", open("fake.tgz", "rb"),\
        "application/x-tar+gzip", {"Expires": "0"})}
    
    res = s.put(url, files=files)
    assert res.status_code == 200
    
    res = s.get(url)
    assert res.status_code == 200
    assert json.loads(res.text) == files
    
    s2 = log_in_session()
    res = s2.head(url)
    assert res.status_code == 200
    
    res = s2.delete(url)
    assert res.status_code == 200
    
    s3 = log_in_session()
    res = s3.delete(url)
    assert res.status_code == 200
    
    s4 = log_in_session()
    res = s4.head(url)
    assert res.status_code == 404

if __name__ == "__main__":
    pytest.main(["./5_test.py"])
