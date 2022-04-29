#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2022/04/29 20:41
# @Author  : Xiaoquan Xu
# @File    : 15_test.py

import pytest
import requests
from names import *

URL = API_BASE + "/session"

def log_in_return_sessioncode():
    body = {"username": USERNAME, "password": PASSWORD}
    res = requests.post(URL, json=body)
    print(res.cookies)
    return res.cookies.get("session")

def test_response_status_code():
    session = log_in_return_sessioncode()
    res = requests.delete(URL, cookies={"session": session})
    assert res.status_code == 200
    assert res.cookies.get("session") == None

def test_logout_without_login():
    res = requests.delete(URL)
    assert res.status_code == 200
    assert res.cookies.get("session") == None

if __name__ == "__main__":
    pytest.main(["./15_test.py"])
