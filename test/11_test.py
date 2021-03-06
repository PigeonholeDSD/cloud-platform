#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2022/05/01 00:37
# @Author  : Xiaoquan Xu
# @File    : 11_test.py

# Test 11.Download the calibration data from the cloud
# `GET /device/<uuid>/calibration`

import os
import uuid
import tarfile
import random
import pytest
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
    
def test_good_download():
    s = log_in_session()
    url = generate_url()
    tname = "t1.tgz"
    generate_tgz(tname)
    files = {"calibration": ("c1", open(tname, "rb"),\
        "application/x-tar+gzip", {"Expires": "0"})}
    
    res = s.put(url, files=files)
    assert res.status_code == 200
    
    res = s.get(url)
    assert res.status_code == 200
    assert hash_content(res.content) == hash_tar(tname)
    assert res.headers["Content-Type"] == "application/x-tar+gzip"
    
def test_upload_twice():
    s = log_in_session()
    url = generate_url()
    tname = "t21.tgz"
    generate_tgz(tname)
    files = {"calibration": ("c21", open(tname, "rb"),\
        "application/x-tar+gzip", {"Expires": "0"})}
    
    res = s.put(url, files=files)
    assert res.status_code == 200
    h1 = hash_tar(tname)
    
    s2 = log_in_session()
    tname2 = "t21.tgz"
    generate_tgz(tname2)
    files2 = {"calibration": ("c21", open(tname2, "rb"),\
        "application/x-tar+gzip", {"Expires": "0"})}
    
    res = s2.put(url, files=files2)
    assert res.status_code == 200
    
    h2 = hash_tar(tname2)
    assert h1 != h2
    
    s3 = log_in_session()
    res = s3.get(url)
    assert res.status_code == 200
    h3 = hash_content(res.content)
    
    for k in h2:
        assert k in h3
        assert h3[k] == h2[k]

def test_download_twice():
    s = log_in_session()
    url = generate_url()
    tname = "t31.tgz"
    generate_tgz(tname)
    files = {"calibration": ("c31", open(tname, "rb"),\
        "application/x-tar+gzip", {"Expires": "0"})}
    
    res = s.put(url, files=files)
    assert res.status_code == 200
    h1 = hash_tar(tname)
    
    s2 = log_in_session()
    res = s2.get(url)
    assert res.status_code == 200
    assert hash_content(res.content) == h1
    
    s3 = log_in_session()
    res = s3.get(url)
    assert res.status_code == 200
    assert hash_content(res.content) == h1
    
def test_no_data_collected():
    s = log_in_session()
    url = generate_url()
    res = s.get(url)
    assert res.status_code == 404

def test_device_try_download():
    simd = SimDevice()
    ts = requests.get(API_BASE + "/timestamp").text
    head = {"Authorization": simd.ticket(ts)}
    
    res = requests.get(generate_url(simd.id), headers=head)
    assert res.status_code == 403

if __name__ == "__main__":
    pytest.main(["./11_test.py"])