#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2022/05/01 00:21
# @Author  : Xiaoquan Xu
# @File    : 7_test.py

# Test 7.Clear calibration data from the cloud
# `DELETE /device/<uuid>/calibration`

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

def hash_content(content):
    with open("_tmp", "wb") as f:
        f.write(content)
    return hash_tar("_tmp")

def test_good_delete():
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
    
    res = s.delete(url)
    assert res.status_code == 200
    
    res = s.get(url)
    assert res.status_code == 404

def test_no_data_before_deletion():
    s = log_in_session()
    url = generate_url()
    
    res = s.get(url)
    assert res.status_code == 404
    
    res = s.delete(url)
    assert res.status_code == 200
    
    res = s.get(url)
    assert res.status_code == 404
    
def test_delete_again():
    s = log_in_session()
    url = generate_url()
    
    res = s.get(url)
    assert res.status_code == 404
    
    res = s.delete(url)
    assert res.status_code == 200
    
    res = s.delete(url)
    assert res.status_code == 200
    
    res = s.get(url)
    assert res.status_code == 404
       
def test_delete_again_headcheck_multisession():
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
    
if __name__ == "__main__":
    pytest.main(["./7_test.py"])