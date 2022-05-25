#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2022/04/30 20:31
# @Author  : Xiaoquan Xu
# @File    : 5_test.py

# Test 5.Check whether calibration data is available
# `HEAD /device/<uuid>/calibration`

import os
import uuid
import pytest
import random
import tarfile
import requests
from names import *
from simdev import *

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def generate_url(idd=None):
    if idd == None:
        idd = uuid.uuid4()
    return API_BASE + "/device/" + str(idd) + "/calibration"

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
    """Unzip files from `name` and map their filename
    into hash value. Delete the files and the tarfile.

    Args:
        name (str): _description_

    Returns:
        _type_: _description_
    """
    hash_tar = dict()
    with tarfile.open(name, "r:gz") as ftar:
        ftar.extractall()
        for fname in ftar.getnames():
            hash_tar[fname] = hash_file(fname)
            os.remove(fname)
    os.remove(name)
    return hash_tar

def hash_content(content):
    with open("_tmp", "wb") as f:
        f.write(content)
    return hash_tar("_tmp")

def test_updown_repeatedly():
    s = log_in_session()
    url = generate_url()
    tname = "t2.tgz"
    generate_tgz(tname)
    files = {"calibration": ("c2", open(tname, "rb"),\
        "application/x-tar+gzip", {"Expires": "0"})}
    
    res = s.put(url, files=files)
    assert res.status_code == 200
    
    res = s.get(url)
    assert res.status_code == 200
    assert hash_content(res.content) == hash_tar(tname)
    
    s2 = log_in_session()
    res = s2.head(url)
    assert res.status_code == 200
    
    res = s2.delete(url)
    assert res.status_code == 200
    
    s3 = log_in_session()
    res = s3.delete(url)
    assert res.status_code == 200
    
    s4 = log_in_session()
    res = s4.head(url)
    assert res.status_code == 404


def test_updown_repeatedly_device():
    simd = SimDevice()
    url = generate_url(simd.id)
    ts = requests.get(API_BASE + "/timestamp").text
    
    tname = "t1.tgz"
    generate_tgz(tname)
    files = {"calibration": ("c1", open(tname, "rb"),\
        "application/x-tar+gzip", {"Expires": "0"})}
    head = {"Authorization": simd.ticket(ts),\
        "Signature": simd.sign_file(tname)}
    os.remove(tname)
    
    res = requests.put(url, files=files, headers=head)
    assert res.status_code == 200
    
    res = requests.head(url, headers=head)
    assert res.status_code == 403 #changed in 2.0
    
    res = requests.delete(url, headers=head)
    assert res.status_code == 200
    
    res = requests.delete(url, headers=head)
    assert res.status_code == 200
    
    res = requests.head(url, headers=head)
    assert res.status_code == 403 #changed in 2.0

if __name__ == "__main__":
    pytest.main(["./5_test.py"])
