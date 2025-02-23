#!/usr/bin/env python
# coding=utf-8

"""
@author: chen wei
@Software: PyCharm
@contact: t6i888@163.com
@file: api.py
@date: 2024 2024/9/12 22:52
@desc: 
"""
from commons.session import Session

# session = requests.session()
session = Session("https://jsonplaceholder.typicode.com")
session.params = {
    'Content-Type': 'application/json;charset=utf-8'
}

url = "/users"

payload = {}

# response = requests.request("POST", url, headers=headers, data=payload)
response = session.get(url, json=payload)
# print(response.text)
# print(response.url)
# print(response)
