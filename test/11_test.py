#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2022/05/01 00:37
# @Author  : Xiaoquan Xu
# @File    : 11_test.py

import os, sys
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

def test_good_download():
    s = log_in_session()
    url = generate_url()
    files = {"calibration": ("f1", open("fake.tgz", "rb"),\
        "application/x-tar+gzip", {"Expires": "0"})}
    res = s.put(url, files=files)
    assert res.status_code == 200
    
    res = s.get(url)
    assert res.status_code == 200
    assert json.loads(res.text) == files

def test_upload_twice():
    s = log_in_session()
    url = generate_url()
    files = {"calibration": ("ff1", open("fake.tgz", "rb"),\
        "application/x-tar+gzip", {"Expires": "0"})}
    res = s.put(url, files=files)
    assert res.status_code == 200
    
    s2 = log_in_session()
    files2 = {"calibration": ("ff2", open("fake.tgz", "rb"),\
        "application/x-tar+gzip", {"Expires": "0"})}
    res = s2.put(url, files=files2)
    assert res.status_code == 200
    assert files2 != files
    
    s3 = log_in_session()
    res = s3.get(url)
    assert res.status_code == 200
    assert json.loads(res.text) == files2

def test_download_twice():
    s = log_in_session()
    url = generate_url()
    files = {"calibration": ("fft1", open("fake.tgz", "rb"),\
        "application/x-tar+gzip", {"Expires": "0"})}
    res = s.put(url, files=files)
    assert res.status_code == 200
    
    s2 = log_in_session()
    res = s2.get(url)
    assert res.status_code == 200
    assert json.loads(res.text) == files
    
    s3 = log_in_session()
    res = s3.get(url)
    assert res.status_code == 200
    assert json.loads(res.text) == files
    
def test_no_data_collected():
    s = log_in_session()
    url = generate_url()
    res = s.get(url)
    assert res.status_code == 404
    
def test_reponse_upload_again():
    s = log_in_session()
    url = generate_url()
    files = {"calibration": ("fff1", open("fake.tgz", "rb"),\
        "application/x-tar+gzip", {"Expires": "0"})}
    res = s.put(url, files=files)
    assert res.status_code == 200
    
    res = s.get(url)
    assert res.status_code == 200
    res_text = res.text
    assert json.loads(res_text) == files
    
    s2 = log_in_session()
    url = generate_url()
    res = s2.put(url, files=json.loads(res_text))
    assert res.status_code == 200
    
    s3 = log_in_session()
    res = s3.get(url)
    assert res.status_code == 200
    assert res.text == res_text

def test_device_try_download():
    assert 0

if __name__ == "__main__":
    pytest.main(["./11_test.py"])