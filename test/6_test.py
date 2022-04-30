#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2022/04/30 22:24
# @Author  : Xiaoquan Xu
# @File    : 6_test.py

import uuid
import pytest
import requests
from names import *
from simdev import SimDevice

def generate_url():
    return API_BASE + "/device/" + str(uuid.uuid4()) + "/calibration"

def log_in_session() -> requests.Session:
    s = requests.Session()
    body = {"username": USERNAME, "password": PASSWORD}
    s.post(API_BASE + "/session", json=body)
    return s

def test_good_upload():
    s = log_in_session()
    url = generate_url()
    files = {"calibration": ("fake.tgz", open("fake.tgz", "rb"),\
        "application/x-tar+gzip", {"Expires": "0"})}
    res = s.put(url, files=files)
    print(res.text)
    assert res.status_code == 200

def test_good_upload2():
    s = log_in_session()
    url = generate_url()
    files = {"calibration": (".", open("fake.tgz", "rb"),\
        "application/x-tar+gzip", {"Expires": "0"})}
    res = s.put(url, files=files)
    print(res.text)
    assert res.status_code == 200

def test_bad_request():
    s = log_in_session()
    url = generate_url()
    files = {"file": ("fake.tgz", open("fake.tgz", "rb"),\
        "multipart/form-data", {"Expires": "0"})}
    res = s.put(url, files=files)
    assert res.status_code == 400

def test_bad_request2():
    s = log_in_session()
    url = generate_url()
    files = {"calibration": ("fake.csv", open("fake.csv", "rb"),\
        "application/x-tar+gzip", {"Expires": "0"})}
    res = s.put(url, files=files)
    assert res.status_code == 400

def test_bad_request3():
    s = log_in_session()
    url = generate_url()
    files = {"calibration": ("fake.tgz", open("fake.tgz", "rb"),\
        "application/x-tar+gzip", {"Expires": "0"})}
    res = s.put(url, data=files)
    assert res.status_code == 400

def test_no_file_found():
    s = log_in_session()
    url = generate_url()
    with pytest.raises(FileNotFoundError):
        files = {"calibration": ("fakee.tgz", open("fakee.tgz", "rb"),\
            "application/x-tar+gzip", {"Expires": "0"})}
        res = s.put(url, files=files)

if __name__ == "__main__":
    pytest.main(["./6_test.py"])