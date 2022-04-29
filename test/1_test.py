#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2022/04/29 17:41
# @Author  : Xiaoquan Xu
# @File    : 1_test.py

import time
import pytest
import requests
from names import *

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

if __name__ == "__main__":
    pytest.main(["./1_test.py"])
