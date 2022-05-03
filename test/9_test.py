#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2022/05/02 23:27
# @Author  : Xiaoquan Xu
# @File    : 9_test.py

import os
import uuid
import pytest
import requests
from names import *
import simdev
from simdev import SimDevice 

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def generate_url(id):
    if id == None:
        id = uuid.uuid4()
    return API_BASE + "/device/" + str(id) + "/model"

def log_in_session() -> requests.Session:
    s = requests.Session()
    body = {"username": USERNAME, "password": PASSWORD}
    s.post(API_BASE + "/session", json=body)
    return s
    
def test_good_getmodel():
    simd = SimDevice()
    ts = requests.get(API_BASE + "/timestamp").text
    head = {"Authorization": simd.ticket(ts)}
    res = requests.get(generate_url(simd.id), headers=head)
    assert "Last-Modified" not in res.headers

if __name__ == "__main__":
    pytest.main(["./9_test.py"])