#!/usr/bin/env python
# coding=utf-8

"""
@author: chen wei
@Software: PyCharm
@contact: t6i888@163.com
@file: models.py
@date: 2024 2024/9/15 21:14
@desc: 声明yaml用例格式
"""
import logging
from dataclasses import dataclass, asdict, field

import allure
import yaml

from commons.templates import Template
from commons import settings
from utils import case_validator

logger = logging.getLogger(__name__)


@dataclass
class CaseInfo:
    title: str
    request: dict
    extract: dict
    validate: dict
    parametrize: list = field(default_factory=list)
    epic: str = settings.allure_epic
    feature: str = settings.allure_feature
    story: str = settings.allure_story

    def to_yaml(self) -> str:
        # 序列化成yaml字符串
        yaml_str = yaml.safe_dump(
            asdict(self),
            allow_unicode=True,  # allow_unicode：使用unicode编码正常显示中文
            sort_keys=False)
        return yaml_str

    @classmethod
    def by_yaml(cls, yaml_str):
        # 反序列化
        obj = cls(**yaml.safe_load(yaml_str))
        return obj

    @allure.step("断言")
    def assert_all(self):
        _validator = case_validator.CaseValidator()
        # print(case_validator.VALIDATORS)

        if not self.validate:
            return

        _validator.assert_all(self.validate)
        # for assert_type, assert_value in self.validate.items():
        #     for msg, data in assert_value.items():
        #         a, b = data[0], data[1]
        #         # print(assert_type, a, b, msg)
        #         match assert_type:
        #             case 'equals':
        #                 logger.info(f"assert {a} == {b}, {msg}")
        #                 assert a == b, msg
        #             case 'not_equals':
        #                 logger.info(f"assert {a} != {b}, {msg}")
        #                 assert a != b, msg
        #             case 'contains':
        #                 logger.info(f"assert {a} in {b}, {msg}")
        #                 assert a in b, msg
        #             case 'not_contains':
        #                 logger.info(f"assert {a} not in {b}, {msg}")
        #                 assert a not in b, msg
        # case "xxxxx

    def ddt(self) -> list:  # 返回一个列表，列表中应该包含N个注入了变量的caseInfo
        case_list = []
        if not self.parametrize:  # 没有使用数据驱动测试
            logger.info("1，执行这一步")
            # case_info_str = self.to_yaml()  # 转字符串
            # case_info_str = Template(case_info_str).render(d)  # 输入变量
            # case_info = self.by_yaml(case_info_str)  # 转成类
            # case_list.append(case_info)
            case_list.append(self)
        else:  # 使用数据驱动测试
            args_name = self.parametrize[0]
            args_value_list = self.parametrize[1:]
            for args_value in args_value_list:
                d = dict(zip(args_name, args_value))
                print(f"D的值：{d}")
                # d 就是数据驱动测试的变量，应输入到用例中
                case_info_str = self.to_yaml()  # 转字符串
                case_info_str = Template(case_info_str).render(d)  # 输入变量
                case_info = self.by_yaml(case_info_str)  # 转成类

                case_list.append(case_info)  # 加入到返回值
        return case_list


if __name__ == '__main__':
    with open(r'E:\PyP\InterfaceAutoTest\TestCases\answer\test_1_status.yaml', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    # print(data)
    case_info = CaseInfo(**data)
    s = case_info.to_yaml()
    # print(s)
    new_case_info = case_info.by_yaml(s)
    # print(new_case_info)
    ddt_ddt = case_info.ddt()
    print(ddt_ddt)
