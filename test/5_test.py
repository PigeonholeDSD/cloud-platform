#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2022/04/30 20:31
# @Author  : Xiaoquan Xu
# @File    : 5_test.py

import uuid
import pytest
import requests
from names import *

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
    
if __name__ == "__main__":
    pytest.main(["./5_test.py"])
