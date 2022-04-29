#!/usr/bin/env python
# -*- coding:utf8 -*-
# @TIME    : 2021/08/22 20:30
# @Author  : Xiaoquan Xu
# @File    : qubit_operator_unit_test.py

import pytest

def err(x):
    assert 0

def func(x):
    return x + 1

def test_answer():
    assert func(3) == 4

if __name__ == "__main__":
    pytest.main(["./1_test.py"])
