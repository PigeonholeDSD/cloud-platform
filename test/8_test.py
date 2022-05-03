#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2022/05/03 22:14
# @Author  : Xiaoquan Xu
# @File    : 8_test.py

# Test 8.Check the version of the device model on the server
# `HEAD /device/<uuid>/model`

import os
import uuid
import time
import pytest
import tarfile
import random
import requests
from names import *
from simdev import *

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def generate_url(idd=None):
    if idd == None:
        idd = uuid.uuid4()
    return API_BASE + "/device/" + str(idd) + "/model"

def log_in_session() -> requests.Session:
    s = requests.Session()
    body = {"username": USERNAME, "password": PASSWORD}
    s.post(API_BASE + "/session", json=body)
    return s
    
def test_good_check_base_model():
    simd = SimDevice()
    ts = requests.get(API_BASE + "/timestamp").text
    head = {"Authorization": simd.ticket(ts)}
    res = requests.head(generate_url(simd.id), headers=head)
    assert "Last-Modified" not in res.headers
    assert res.headers["Content-Length"][0] != '-'
    assert res.status_code == 200

def generate_file(name: str):
    with open(name, "w") as f:
        for _ in range(10):
            f.write(str(random.randint(1,1000000))+"\n")

def generate_tgz(name: str):
    n_file = random.randint(1,5)
    with tarfile.open(name, "w:gz") as ftar:
        for i in range(n_file):
            fname = name[:-4] + str(i) + ".csv"
            generate_file(fname)
            ftar.add(fname)
            os.remove(fname)

def hash_tar(name: str):
    hash_tar = hash_file(name)
    os.remove(name)
    return hash_tar

def hash_content(content):
    with open("_tmp", "wb") as f:
        f.write(content)
    return hash_tar("_tmp")

def test_good_check_model():
    simd = SimDevice()
    s = log_in_session()
    url = generate_url(simd.id)
    generate_tgz("t1.tgz")
    files = {"model": ("f1.tgz", open("t1.tgz", "rb"),\
        "application/octet-stream")}
    res = s.put(url, files=files)
    hash_tar("t1.tgz")
    
    ts = requests.get(API_BASE + "/timestamp").text
    head = {"Authorization": simd.ticket(ts)}
    res = requests.head(generate_url(simd.id), headers=head)
    print(res.headers["Last-Modified"])
    print(time.strftime('%a, %d %b %Y %H', time.gmtime(time.time())))
    assert res.headers["Last-Modified"].find(time.strftime(\
        '%a, %d %b %Y %H', time.gmtime(time.time()))) == 0
    assert res.content == b""
    assert res.status_code == 200
    assert res.headers["Content-Length"][0] != '-'

if __name__ == "__main__":
    pytest.main(["./8_test.py"])