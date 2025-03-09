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

from commons.file_processors.yaml_processor import YamlProcessor
from commons.file_processors.json_processor import JsonProcessor

processors = {
    'yaml': YamlProcessor,
    'yml': YamlProcessor,
    'json': JsonProcessor,

}


def get_processor(ext):
    agent_model = processors.get(ext, YamlProcessor)  # 代理模式

    return agent_model  # 默认回退到 Yaml


FileHandle = get_processor("yaml")

if __name__ == '__main__':
    # 示例用法
    yaml_path = r'E:\PyP\InterfaceAutoTest\TestCases\answer\test_1_status.yaml'  # 你的 YAML 文件路径
    yaml_file = FileHandle(yaml_path)
    print(yaml_file)
    print(type(yaml_file))
    file_string = FileHandle.to_string(yaml_file)
    print(file_string)
    file_dict = FileHandle.to_dict(file_string)
    print(file_dict)
