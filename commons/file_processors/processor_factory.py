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
from typing import Type, Union

from commons.file_processors.base_processor import BaseFileProcessor
from commons.file_processors.yaml_processor import YamlProcessor
from commons.file_processors.json_processor import JsonProcessor

# 类型别名，表示处理器类的字典
ProcessorMap = dict[str, Type[BaseFileProcessor]]
processors: ProcessorMap = {
    'yaml': YamlProcessor,
    'yml': YamlProcessor,
    'json': JsonProcessor,

}


class UnsupportedFileTypeError(Exception):
    """当文件类型不被支持时抛出此异常。"""
    pass


# def get_processor_class(file_suffix: str = "yaml") -> Type[BaseFileProcessor]:
def get_processor_class(fp: Union[Path, str]) -> 'BaseFileProcessor':
    fp = Path(fp)
    if fp.is_file():
        file_suffix = fp.suffix[1:]
        processor_class = processors.get(file_suffix.lower(), YamlProcessor)  # 代理模式

        return processor_class(fp)  # 默认回退到 Yaml
    else:
        raise UnsupportedFileTypeError(fp)


# FileHandle = get_processor("yaml")

if __name__ == '__main__':
    # 示例用法
    yaml_path = r'E:\PyP\InterfaceAutoTest\TestCases\answer\test_1_status.yaml'  # 你的 YAML 文件路径
    # yaml_file = FileHandle(yaml_path)
    # print(yaml_file.load())
    # print(type(yaml_file))
    # file_suffix = Path(yaml_path).suffix[1:]
    # print(file_suffix)
    get_processor = get_processor_class(yaml_path)
    print(get_processor.load())
