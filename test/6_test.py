#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2022/04/30 22:24
# @Author  : Xiaoquan Xu
# @File    : 6_test.py

# Test 6.Upload new calibration data to the cloud platform
# `PUT /device/<uuid>/calibration`

import os
import uuid
import tarfile
import random
import pytest
import requests
from names import *
import simdev

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def generate_url():
    return API_BASE + "/device/" + str(uuid.uuid4()) + "/calibration"

def log_in_session() -> requests.Session:
    s = requests.Session()
    body = {"username": USERNAME, "password": PASSWORD}
    s.post(API_BASE + "/session", json=body)
    return s

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
            hash_tar[fname] = simdev.hash_file(fname)
            os.remove(fname)
    os.remove(name)
    return hash_tar

def test_good_upload():
    s = log_in_session()
    url = generate_url()
    generate_tgz("t1.tgz")
    files = {"calibration": ("fake.tgz", open("t1.tgz", "rb"),\
        "application/x-tar+gzip", {"Expires": "0"})}
    res = s.put(url, files=files)
    hash_tar("t1.tgz")
    assert res.status_code == 200

def test_good_upload2():
    s = log_in_session()
    url = generate_url()
    generate_tgz("t2.tgz")
    files = {"calibration": (".", open("t2.tgz", "rb"),\
        "application/x-tar+gzip")}
    res = s.put(url, files=files)
    hash_tar("t2.tgz")
    assert res.status_code == 200

def test_bad_request():
    s = log_in_session()
    url = generate_url()
    generate_tgz("t3.tgz")
    files = {"file": ("fake.tgz", open("t3.tgz", "rb"),\
        "application/x-tar+gzip")}
    res = s.put(url, files=files)
    hash_tar("t3.tgz")
    assert res.status_code == 400

def test_bad_request2():
    s = log_in_session()
    url = generate_url()
    generate_file("fake.csv")
    files = {"calibration": ("fake.csv", open("fake.csv", "rb"),\
        "application/x-tar+gzip", {"Expires": "0"})}
    res = s.put(url, files=files)
    os.remove("fake.csv")
    assert res.status_code == 400
    
def test_good_upload3():
    s = log_in_session()
    url = generate_url()
    generate_tgz("fake.csv")
    files = {"calibration": ("fake.csv", open("fake.csv", "rb"),\
        "application/x-tar+gzip", {"Expires": "0"})}
    res = s.put(url, files=files)
    os.remove("fake.csv")
    assert res.status_code == 200

def test_bad_request3():
    s = log_in_session()
    url = generate_url()
    generate_tgz("t4.tgz")
    files = {"calibration": ("fake.tgz", open("t4.tgz", "rb"),\
        "application/x-tar+gzip", {"Expires": "0"})}
    res = s.put(url, data=files)
    hash_tar("t4.tgz")
    assert res.status_code == 400

def test_bad_request4():
    s = log_in_session()
    url = generate_url()
    generate_tgz("t5.tgz")
    files = {"calibration": ("t5.tgz", open("t5.tgz", "rb"))}
    res = s.put(url, files=files)
    hash_tar("t5.tgz")
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