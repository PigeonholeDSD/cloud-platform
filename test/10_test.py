#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2022/05/03 22:30
# @Author  : Xiaoquan Xu
# @File    : 10_test.py

# Test 10.Clear device model from the cloud
# `DELETE /device/<uuid>/model`

import os
import uuid
import json
import pytest
import tarfile
import random
import requests
import names
from names import *
from simdev import *

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def generate_url(idd=None):
    if idd == None:
        idd = uuid.uuid4()
    return API_BASE + "/device/" + str(idd) + "/model/"

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

def test_delete_straightforward():
    simd = SimDevice()
    ts = requests.get(API_BASE + "/timestamp").text
    head = {"Authorization": simd.ticket(ts)}
    url = generate_url(simd.id)[:-1]
    res = requests.delete(url, headers=head)
    assert res.status_code == 200
    
    res = requests.delete(url, headers=head)
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

def test_good_delete():
    simd = SimDevice()
    
    s = log_in_session()
    url = generate_url(simd.id)
    generate_tgz("t1.tgz")
    files = {"model": ("f1.tgz", open("t1.tgz", "rb"),\
        "application/octet-stream")}
    res = s.put(url + ALGO[0], files=files)
    h1 = hash_tar("t1.tgz")
    
    ts = requests.get(API_BASE + "/timestamp").text
    head = {"Authorization": simd.ticket(ts)}
    res = requests.get(url + ALGO[0], headers=head)
    assert res.status_code == 200
    assert hash_content(res.content) == h1
    assert "Last-Modified" in res.headers
    
    res = requests.get(url + ALGO[1], headers=head)
    assert res.status_code == 200
    assert "Last-Modified" not in res.headers
    
    res = requests.get(url + ALGO[0][1:], headers=head)
    assert res.status_code == 404
    
    res = requests.delete(url[:-1], headers=head)
    assert res.status_code == 200
    
    res = requests.get(url + ALGO[0], headers=head)
    assert res.status_code == 200
    assert "Last-Modified" not in res.headers

if __name__ == "__main__":
    pytest.main(["./10_test.py"])