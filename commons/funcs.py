#!/usr/bin/env python
# coding=utf-8

"""
@author: chen wei
@Software: PyCharm
@contact: t6i888@163.com
@file: funcs.py
@date: 2024 2024/9/22 22:46
@desc: 
"""
import base64
import logging
import time
import urllib.parse
import hashlib

from commons.databases import db

from commons.files import YamlFile
from commons import settings

logger = logging.getLogger(__name__)


def url_unquote(s: str) -> str:
    return urllib.parse.unquote(s)


def time_str() -> str:
    return str(time.time())


def add(a, b):
    return str(int(a) + int(b))


def sql(s: str) -> str:
    res = db.execute_sql(s)

    return res[0][0]


def new_id():
    #     自增，永不重复
    id_file = YamlFile(settings.id_path)
    id_file["id"] += 1
    id_file.save()

    return id_file["id"]


def last_id() -> str:
    # 不自增，只返回结果

    id_file = YamlFile(settings.id_path)
    return id_file["id"]


def md5(content: str) -> str:
    # 1，原文转为字节
    content = content.encode("utf-8")
    result = hashlib.md5(content).hexdigest()
    return result


def base64_encode(content: str) -> str:
    # 1，原文转二进制
    content = content.encode("utf-8")
    # 2，base64编码（二进制）
    encode_value = base64.b64encode(content)
    # 3，转为字符串
    encode_str = encode_value.decode("utf-8")

    return encode_str


def base64_decode(content: str) -> str:
    # 1，原文转二进制
    content = content.encode("utf-8")
    # 2，base64解码（二进制）
    decode_value = base64.b64decode(content)
    # 3，转为字符串
    decode_str = decode_value.decode("utf-8")

    return decode_str


def rsa_encode(content: str) -> str:
    ...


def rsa_decode(content: str) -> str:
    ...


if __name__ == '__main__':
    # res = url_unquote("%E6%88%90%E5%8A%9F%E3%80%82")
    # print(res)
    print(f"计数器：{new_id()}")
    print(f"当前数值：{last_id()}")
