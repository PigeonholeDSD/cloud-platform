#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2022/05/01 00:21
# @Author  : Xiaoquan Xu
# @File    : 7_test.py

import os
import json
import uuid
import pytest
import requests
from names import *
from simdev import SimDevice

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def generate_url():
    return API_BASE + "/device/" + str(uuid.uuid4()) + "/calibration"

def log_in_session() -> requests.Session:
    s = requests.Session()
    body = {"username": USERNAME, "password": PASSWORD}
    
    s.post(API_BASE + "/session", json=body)
    return s

def test_good_delete():
    s = log_in_session()
    url = generate_url()
    files = {"calibration": ("df1", open("fake.tgz", "rb"),\
        "application/x-tar+gzip", {"Expires": "0"})}
    
    res = s.put(url, files=files)
    assert res.status_code == 200
    
    res = s.get(url)
    assert res.status_code == 200
    assert json.loads(res.text) == files
    
    res = s.delete(url)
    assert res.status_code == 200
    
    res = s.get(url)
    assert res.status_code == 404

def test_no_data_before_deletion():
    s = log_in_session()
    url = generate_url()
    
    res = s.get(url)
    assert res.status_code == 404
    
    res = s.delete(url)
    assert res.status_code == 200
    
    res = s.get(url)
    assert res.status_code == 404
    
def test_delete_again():
    s = log_in_session()
    url = generate_url()
    
    res = s.get(url)
    assert res.status_code == 404
    
    res = s.delete(url)
    assert res.status_code == 200
    
    res = s.delete(url)
    assert res.status_code == 200
    
    res = s.get(url)
    assert res.status_code == 404
       
def test_delete_again_headcheck_multisession():
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
    pytest.main(["./7_test.py"])