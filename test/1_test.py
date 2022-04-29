#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2022/04/29 17:41
# @Author  : Xiaoquan Xu
# @File    : 1_test.py

import pytest
import requests
from names import *

def test_colon_exists():
    r = requests.Session()
    s = r.get(API_BASE+"/timestamp").text
    assert s.find(':') != -1
    
if __name__ == "__main__":
    pytest.main(["./1_test.py"])
