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

# from commons.databases import db

from commons.files import YamlFile
from commons import settings

logger = logging.getLogger(__name__)

class Funcs:

    FUNC_MAPPING = {
        "int": int,
        "float": float,
        "bool": bool
    }  # 内置函数有的，直接放入mapping；内置函数没有的，在funcs中定义，自动放入mapping


    @classmethod
    def register(cls, name: str):
        def decorator(func):
            cls.FUNC_MAPPING[name] = func
            return func

        return decorator

@Funcs.register("url_unquote")
def url_unquote(s: str) -> str:
    return urllib.parse.unquote(s)


@Funcs.register("str")
def to_string(s) -> str:
    # 将数据转换为str类型。
    return f"'{s}'"

@Funcs.register("time_str")
def time_str() -> str:
    return str(time.time())

@Funcs.register("add")
def add(a, b):
    return str(int(a) + int(b))

@Funcs.register("sql")
def sql(s: str) -> str:
    res = db.execute_sql(s)

    return res[0][0]

@Funcs.register("new_id")
def new_id():
    #     自增，永不重复
    id_file = YamlFile(settings.id_path)
    id_file["id"] += 1
    id_file.save()

    return id_file["id"]

@Funcs.register("last_id")
def last_id() -> str:
    # 不自增，只返回结果

    id_file = YamlFile(settings.id_path)
    return id_file["id"]

@Funcs.register("md5")
def md5(content: str) -> str:
    # 1，原文转为字节
    content = content.encode("utf-8")
    result = hashlib.md5(content).hexdigest()
    return result

@Funcs.register("base64_encode")
def base64_encode(content: str) -> str:
    # 1，原文转二进制
    content = content.encode("utf-8")
    # 2，base64编码（二进制）
    encode_value = base64.b64encode(content)
    # 3，转为字符串
    encode_str = encode_value.decode("utf-8")

    return encode_str

@Funcs.register("base64_decode")
def base64_decode(content: str) -> str:
    # 1，原文转二进制
    content = content.encode("utf-8")
    # 2，base64解码（二进制）
    decode_value = base64.b64decode(content)
    # 3，转为字符串
    decode_str = decode_value.decode("utf-8")

    return decode_str

@Funcs.register("rsa_encode")
def rsa_encode(content: str) -> str:
    ...

@Funcs.register("rsa_decode")
def rsa_decode(content: str) -> str:
    ...


if __name__ == '__main__':
    # res = url_unquote("%E6%88%90%E5%8A%9F%E3%80%82")
    # print(res)
    # print(f"计数器：{new_id()}")
    # print(f"当前数值：{last_id()}")
    print(Funcs().FUNC_MAPPING)