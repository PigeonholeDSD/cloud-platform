#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2022/04/29 17:41
# @Author  : Xiaoquan Xu
# @File    : 1_test.py

# Test 1.Request a cloud-signed time stamp
# `GET /timestamp`

import time
import pytest
import tarfile
import random
import requests
from names import *
from simdev import *
    
def test_colon_exists():
    r = requests.Session()
    s = r.get(API_BASE + "/timestamp")
    assert s.text.find(':') != -1
    assert s.status_code == 200

def test_same_second_return_same_valve():
    get1 = requests.get(API_BASE + "/timestamp")
    get2 = requests.get(API_BASE + "/timestamp")
    assert get1.text.split(":")[0] == get2.text.split(":")[0]
    assert get1.text.split(":")[1] == get2.text.split(":")[1]
    assert get1.text == get2.text
    assert get1.status_code == 200
    assert get2.status_code == 200

def test_different_second_return_different_valve():
    get1 = requests.get(API_BASE + "/timestamp")
    time.sleep(1.5)
    get2 = requests.get(API_BASE + "/timestamp")
    print(get1.text.split(":"))
    print(get2.text.split(":"))
    assert get1.text.split(":")[0] != get2.text.split(":")[0]
    assert get1.text.split(":")[1] != get2.text.split(":")[1]
    assert get1.status_code == 200
    assert get2.status_code == 200

def test_response_status_code():
    res = requests.get(API_BASE + "/timestamp")
    assert res.status_code == 200

def generate_url(idd=None):
    if idd == None:
        idd = uuid.uuid4()
    return API_BASE + "/device/" + str(idd) + "/calibration"

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

def test_timestamp_timeout():
    simd = SimDevice()
    url = generate_url(simd.id)
    ts = "1651599134:6699d446784646870e46830bf5ea1ad3b9f06d2b"
    print(ts)
    
    tname = "t1.tgz"
    generate_tgz(tname)
    files = {"calibration": ("c1", open(tname, "rb"),\
        "application/x-tar+gzip", {"Expires": "0"})}
    head = {"Authorization": simd.ticket(ts),\
        "Signature": simd.sign_file(tname)}
    os.remove(tname)
    
    res = requests.put(url, files=files, headers=head)
    assert res.status_code == 400
    
    res = requests.head(url, headers=head)
    assert res.status_code == 404

if __name__ == "__main__":
    pytest.main(["./1_test.py"])
