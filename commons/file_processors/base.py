#!/usr/bin/env python
# coding=utf-8

"""
@author: CNWei
@Software: PyCharm
@contact: t6i888@163.com
@file: base
@date: 2025/3/4 17:23
@desc: 
"""
import abc


class BaseFileProcessor(abc.ABC):  # 使用 abc 模块定义抽象基类
    """
    文件处理器的抽象基类。
    定义了所有子类必须实现的方法。
    """

    @abc.abstractmethod
    def load(self):
        """加载."""
        pass

    @staticmethod
    @abc.abstractmethod
    def to_string(data: dict) -> str:
        """将文件内容转换为字符串。"""
        pass

    @staticmethod
    @abc.abstractmethod
    def to_dict(data: str) -> dict:
        """将文件内容转换为字典。"""
        pass

    @abc.abstractmethod
    def save(self, new_filepath=None):
        """将数据保存."""
        pass
