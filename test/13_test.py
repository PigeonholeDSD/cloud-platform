#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2022/05/03 23:11
# @Author  : Xiaoquan Xu
# @File    : 13_test.py

# Test 13.Delete everything specified from the cloud
# `DELETE /device/<uuid>`

import os
import uuid
import pytest
import json
import tarfile
import random
import requests
from names import *
from simdev import *

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def generate_url(idd=None):
    if idd == None:
        idd = uuid.uuid4()
    return API_BASE + "/device/" + str(idd)

def log_in_session() -> requests.Session:
    s = requests.Session()
    body = {"username": USERNAME, "password": PASSWORD}
    s.post(API_BASE + "/session", json=body)
    return s
    
def test_delete_straightforward():
    s = log_in_session()
    url = generate_url()
    res = s.delete(url)
    assert res.status_code == 200
    res = s.delete(url)
    assert res.status_code == 200

def test_good_delete():
    simd = SimDevice()
    
    ts = requests.get(API_BASE + "/timestamp").text
    head = {"Authorization": simd.ticket(ts)}
    body_email = {"email": "pigeonholedevice@ciel.dev"}
    url = generate_url(simd.id)
    res = requests.post(url+"/email", json=body_email, headers=head)
    assert res.status_code == 200
    
    res = requests.get(url+"/email", headers=head)
    assert res.status_code == 200
    assert json.loads(res.text) == body_email
    
    s = log_in_session()
    res = s.delete(url)
    assert res.status_code == 200
    
    res = requests.get(url+"/email", headers=head)
    assert res.status_code == 404

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

def test_good_delete2():
    simd = SimDevice()
    
    s = log_in_session()
    url = generate_url(simd.id) + "/model/"
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
    
    res = requests.delete(generate_url(simd.id), headers=head)
    assert res.status_code == 200
    
    res = requests.get(generate_url(simd.id) + "/email", headers=head)
    assert res.status_code == 404
    
    res = requests.get(url + ALGO[0], headers=head)
    assert res.status_code == 200
    assert "Last-Modified" not in res.headers

if __name__ == "__main__":
    pytest.main(["./13_test.py"])