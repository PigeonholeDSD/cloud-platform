#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2022/05/27 13:59
# @Author  : Xiaoquan Xu
# @File    : 28_test.py

# Test 28.Get metadata of available algorithms
# `GET /models`

import os
import uuid
import pytest
import json
import requests
from names import *
from simdev import *

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def generate_url():
    return API_BASE + "/models"

def log_in_session() -> requests.Session:
    s = requests.Session()
    body = {"username": USERNAME, "password": PASSWORD}
    s.post(API_BASE + "/session", json=body)
    return s
    
def test_good_get():
    s = log_in_session()
    url = generate_url()
    res = s.get(url)
    assert res.status_code == 200
    assert list(json.loads(res.text).keys()) != []

if __name__ == "__main__":
    pytest.main(["./28_test.py"])