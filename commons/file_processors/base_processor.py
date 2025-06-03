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
from pathlib import Path
from typing import Union


class BaseFileProcessor(abc.ABC):  # 使用 abc 模块定义抽象基类
    """
    文件处理器的抽象基类。
    定义了所有子类必须实现的方法。
    """
    def __init__(self, filepath: Union[str, Path], **kwargs):

        self.filepath: Path = Path(filepath)  # 确保 filepath 是 Path 对象

    @abc.abstractmethod
    def load(self) -> dict:
        """加载."""
        raise NotImplementedError

    @abc.abstractmethod
    def save(self, data: dict, new_filepath: Union[str, Path, None] = None) -> None:
        """将数据保存."""
        raise NotImplementedError
