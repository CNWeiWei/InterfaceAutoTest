#!/usr/bin/env python
# coding=utf-8

"""
@author: CNWei
@Software: PyCharm
@contact: t6i888@163.com
@file: case_parser
@date: 2025/2/27 17:25
@desc: 
"""

import logging
from dataclasses import dataclass, asdict, field

import yaml

from commons.models import CaseInfo


class CaseParser:
    @staticmethod
    def to_yaml(case_data: dict) -> str:
        return yaml.safe_dump(case_data, allow_unicode=True, sort_keys=False)

    @staticmethod
    def from_yaml(yaml_str: str) -> CaseInfo:
        return CaseInfo(**yaml.safe_load(yaml_str))


if __name__ == '__main__':
    with open(r'D:\CNWei\CNW\InterfaceAutoTest\TestCases\answer\test_1_status.yaml', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    print(data)
    print(type(data))
    # print(CaseInfo(**data))
    case_parser = CaseParser()
    case_data_ = case_parser.to_yaml(data)
    # print(case_data_)
    case_parser.from_yaml(case_data_)
    # print(type(case_data_))
