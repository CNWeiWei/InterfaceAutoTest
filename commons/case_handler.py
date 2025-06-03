#!/usr/bin/env python
# coding=utf-8

"""
@author: CNWei
@Software: PyCharm
@contact: t6i888@163.com
@file: case_handler
@date: 2025/5/26 22:13
@desc: 
"""
import json

import logging
from dataclasses import dataclass, asdict
from commons.models import TestCaseModel

logger = logging.getLogger(__name__)


@dataclass
class TestCaseHandle(TestCaseModel):

    @classmethod
    def new(cls, testcase: dict) -> 'TestCaseHandle':

        try:
            instance = cls(**testcase)
            return instance
        except (TypeError, ValueError) as e:
            logger.warning(f"解析错误：{e}")
            raise e

    def to_string(self) -> str:
        """
        将 字典 转换为 json 格式的字符串。

        :return:
            json 格式的字符串。
        """
        try:
            res = json.dumps(asdict(self), ensure_ascii=False)
            return res
        except TypeError as e:
            logger.error(f"将数据转换为 json 字符串时出错: {e}")
            raise e

    @staticmethod
    def to_dict(json_str: str) -> dict:
        """
        将 json 格式的字符串转换为 字典.

        :param
            json_str: json 格式的字符串。
        :return:
        """
        try:
            res = json.loads(json_str)
            return res
        except json.JSONDecodeError as e:
            logger.error(f"将 json 字符串转换为字典时出错: {e}")
            raise e


if __name__ == '__main__':
    from pathlib import Path
    from commons.file_processors import processor_factory

    test_data = Path(r"E:\PyP\InterfaceAutoTest\TestCases\test_1_user.yaml")
    yaml_data = processor_factory.get_processor_class(test_data)
    case_info = TestCaseHandle.new(yaml_data.load())
    print(case_info.to_string())
    print(type(case_info.to_string()))
    print(case_info.to_dict(case_info.to_string()))
    print(type(case_info.to_dict(case_info.to_string())))
    print(type(case_info))
    print(case_info.parametrize)

    for i in case_info.parametrize:
        print(i)
