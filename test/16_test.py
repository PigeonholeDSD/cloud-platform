#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2022/05/04 00:51
# @Author  : Xiaoquan Xu
# @File    : 16_test.py

# Test 16.Set a default model to the cloud
# `PUT /model/base`

import os
import pytest
import random
import requests
from names import *
from simdev import *

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def generate_url():
    return API_BASE + "/model/base"

def log_in_session() -> requests.Session:
    s = requests.Session()
    body = {"username": USERNAME, "password": PASSWORD}
    s.post(API_BASE + "/session", json=body)
    return s
    
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

def test_good_set():
    s = log_in_session()
    url = generate_url()
    fname = "f1.233"
    generate_file(fname)
    files = {"model": ("file1", open(fname, "rb"))}
    res = s.put(url, files=files)
    h1 = hash_file(fname)
    os.remove(fname)
    assert res.status_code == 404
    
    # simd = SimDevice()
    # ts = requests.get(API_BASE + "/timestamp").text
    # head = {"Authorization": simd.ticket(ts)}
    # res = requests.get(API_BASE + "/device/" + str(simd.id) + "/model", headers=head)
    # assert "Last-Modified" not in res.headers
    # assert hash_content(res.content) == h1
    # assert res.status_code == 200

def test_interesting_request():
    s = log_in_session()
    url = generate_url()
    files = {"model": ("file1", "file2")}
    res = s.put(url, files=files)
    assert res.status_code == 404

def test_interesting_request2():
    s = log_in_session()
    url = generate_url()
    files = {"model": "file1"}
    res = s.put(url, files=files)
    assert res.status_code == 404

def test_bad_request():
    s = log_in_session()
    url = generate_url()
    files = {"model": ("balala",)}
    with pytest.raises(ValueError):
        res = s.put(url, files=files)

def test_bad_request2():
    s = log_in_session()
    url = generate_url()
    files = {"modell": ("file1", "file2")}
    res = s.put(url, files=files)
    assert res.status_code == 404

if __name__ == "__main__":
    pytest.main(["./16_test.py"])