#!/usr/bin/env python
# coding=utf-8

"""
@author: chen wei
@Software: PyCharm
@contact: t6i888@163.com
@file: templates.py
@date: 2024 2024/9/22 22:20
@desc: 
"""
import copy
import logging
import re
import string
from commons.funcs import Funcs


logger = logging.getLogger(__name__)


class Template(string.Template):
    """
    1，支持函数调用
    2，参数也可以是变量
    """

    call_pattern = re.compile(r"\${(?P<func_name>.*?)\((?P<func_args>.*?)\)}")

    def render(self, mapping: dict) -> str:
        s = self.safe_substitute(mapping)  # 原有方法替换变量
        s = self.safe_substitute_funcs(s, mapping)

        return s

    def safe_substitute_funcs(self, template, mapping) -> str:
        """
        解析字符串中的函数名和参数，并将函数调用结果进行替换
        :param template: 字符串
        :param mapping: 上下文，提供要使用的函数和变量
        :return: 替换后的结果
        """
        mapping = copy.deepcopy(mapping)
        logger.info(f"mapping更新前: {mapping}")
        # mapping.update(self.FUNC_MAPPING)  # 合并两个mapping
        mapping.update(Funcs.FUNC_MAPPING)  # 合并两个mapping
        logger.info(f"mapping更新后: {mapping}")
        def convert(mo):
            func_name = mo.group("func_name")
            func_args = mo.group("func_args").split(",")
            func = mapping.get(func_name)  # 读取指定函数
            func_args_value = [mapping.get(arg, arg) for arg in func_args]

            if func_args_value == [""]:  # 处理没有参数的func
                func_args_value = []

            if not callable(func):
                return mo.group()  # 如果是不可调用的假函数，不进行替换
            else:
                return str(func(*func_args_value))  # 否则用函数结果进行替换

        return self.call_pattern.sub(convert, template)

