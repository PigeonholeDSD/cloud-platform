#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2022/05/30 21:18
# @Author  : Xiaoquan Xu
# @File    : 30_test.py

# Test 30.Update the base model of an algorithm
# `PUT /api/model/<algo>`

import os
import uuid
import json
import names
import pytest
import random
import requests
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

def test_good_update():
    for k in range(len(names.ALGO)):
        kALGO = k
        s = log_in_session()
        url = generate_url()
        generate_file(f"f{k}")
        files = {"model": ("file1", open(f"f{k}", "rb"),\
            "multipart/form-data")}
        res = s.put(url, files=files)
        assert res.status_code == 200
        
    for k in range(len(names.ALGO)):
        kALGO = k
        s = log_in_session()
        url = generate_url()
        generate_file(f"f{k}")
        files = {"model": ("file1", open(f"f{k}", "rb"),\
            "multipart/form-data")}
        res = s.put(url, files=files)
        assert res.status_code == 200
        os.remove(f"f{k}")

def test_good_upload2():
    s = log_in_session()
    url = generate_url()
    generate_file("f2")
    files = {"model": ("file2", open("f2", "rb"))}
    res = s.put(url, files=files)
    os.remove("f2")
    assert res.status_code == 200

def test_bad_request():
    s = log_in_session()
    url = generate_url()
    generate_file("bf")
    files = {"files": ("bfile", open("bf", "rb"))}
    res = s.put(url, files=files)
    os.remove("bf")
    assert res.status_code == 400
    
def test_bad_request2():
    s = log_in_session()
    url = generate_url()
    generate_file("bf2")
    files = {"model": ("bfile2", open("bf2", "rb"))}
    res = s.put(url, data=files)
    os.remove("bf2")
    assert res.status_code == 400

def test_device_try_upload():
    for k in range(len(names.ALGO)):
        kALGO = k
        simd = SimDevice()
        ts = requests.get(API_BASE + "/timestamp").text
        head = {"Authorization": simd.ticket(ts)}
        generate_file("tf")
        files = {"model": ("file2", open("tf", "rb"))}
        os.remove("tf")
        res = requests.put(generate_url(simd.id), files=files, headers=head)
        assert res.status_code == 403

def test_device_try_upload_bad():
    simd = SimDevice()
    ts = requests.get(API_BASE + "/timestamp").text
    head = {"Authorization": simd.ticket(ts)}
    files = {}
    res = requests.put(generate_url(simd.id), files=files, headers=head)
    assert res.status_code == 403
    
if __name__ == "__main__":
    pytest.main(["./30_test.py"])