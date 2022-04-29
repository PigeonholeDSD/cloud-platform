#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2022/04/29 19:29
# @Author  : Xiaoquan Xu
# @File    : 2_test.py

import time
import pytest
import requests
from names import *

def err(x):
    assert 0

def func(x):
    return x + 1

def test_answer():
    assert func(3) == 4

if __name__ == "__main__":
    pytest.main(["./2_test.py"])
