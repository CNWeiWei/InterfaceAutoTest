#!/usr/bin/env python
# coding=utf-8

"""
@author: CNWei
@Software: PyCharm
@contact: t6i888@163.com
@file: file_handle
@date: 2025/3/7 09:31
@desc: 
"""
from pathlib import Path
from typing import Union

from yaml_processor import YamlProcessor
from json_processor import JsonProcessor

class FileHandle:
    def __init__(self, filepath: Union[str, Path], data: Union[dict, None] = None):
        # self.filepath: Path = Path(filepath)  # 确保 filepath 是 Path 对象
        # self.data: Union[dict, None] = data
        self.processor = get_processor(filepath, data)

    def load(self) -> None:
        self.processor.load()

    def to_string(self) -> str:
        return self.processor.to_string()

    def to_dict(self, data: str) -> None:
        self.processor.to_dict(data)

    def save(self, new_filepath: Union[str, Path, None] = None):
        self.processor.save(new_filepath)


def get_processor(filepath, data):
    ext = Path(filepath).suffix.lower()[1:]  # 获取后缀名，如 'json'
    processors = {
        'yaml': YamlProcessor,
        'yml': YamlProcessor,
        'json': JsonProcessor,

    }
    agent_model = processors.get(ext, YamlProcessor)  # 代理模式
    return agent_model(filepath, data)  # 默认回退到 Yaml
