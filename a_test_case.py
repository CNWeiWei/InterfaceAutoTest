#!/usr/bin/env python
# coding=utf-8

"""
@author: chen wei
@Software: PyCharm
@contact: t6i888@163.com
@file: a_test_case.py
@date: 2024 2024/9/15 19:15
@desc: 
"""
from requests import Session
import requests

session = Session()


def test_1():
    base_url = "https://jsonplaceholder.typicode.com"
    session.params = {
        'Content-Type': 'application/json;charset=utf-8'
    }

    url = f"{base_url}/users"

    payload = {}

    # response = requests.request("POST", url, headers=headers, data=payload)
    response = session.get(url, json=payload)
    print(response.json()[0]["username"])
    assert response.status_code == 200


def test_2():
    base_url = r'https://api.kuleu.com/api/action'
    params = {"text": "爱情"}
    header = {
        "user-agent": 'Mozilla / 5.0(Windows NT 10.0;Win64;x64) AppleWebKit / 537.36(KHTML, like Gecko) '
                      'Chrome / 128.0.0.0Safari / 537.36'
    }
    response = requests.get(base_url, headers=header, params=params)
    # print(response.text)
    print(response.json())
    print(response.request.url)
    assert response.status_code == 200
